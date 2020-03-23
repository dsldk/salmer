# Copyright (C) 2017-20 Dansk Sprog- og Litteraturselskab and Magenta ApS.
#
# This file is part of DSL's generic literature site template.
#
# This template website is free software: you can redistribute it
# and/or modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranties of
# MERCHANTABILITY, SATISFACTORY QUALITY, or FITNESS FOR A PARTICULAR
# PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
from requests import get
from json import loads
from pyramid.httpexceptions import HTTPFound
from .exist_api.exist_api import listify, remove_dot_xml


def set_menu_by_cookie(request):
    one_year_in_seconds = 31536000
    menu_by = request.GET.get("menu_by")
    if menu_by:
        request.response.set_cookie(
            "menu_by", value=menu_by, max_age=one_year_in_seconds
        )


def make_listings_for_menu(xquery_folder, document_id):
    titles_url = xquery_folder + "list_titles.xquery"
    titles = get(titles_url)
    titles_text = get(titles_url).text
    url = xquery_folder + "list_authors.xquery"
    titles_for_authors = (
        []
    )  # loads(get(url).text.replace('empty', 'Ukendt')).get("authors")
    url = xquery_folder + "list_manuscripts.xquery"
    titles_response = get(url)
    ok = titles_response.ok
    if ok:
        titles_response = titles_response.text
    titles_if_any = {}
    if ok:
        titles_if_any = loads(titles_response)
    titles_by_manuscripts_with_nil = []
    if ok and titles_if_any:
        titles_by_manuscripts_with_nil = titles_if_any.get(
            "manuscripts_for_place"
        )
    titles_by_manuscripts = []
    # import pdb; pdb.set_trace()
    for manuscript in listify(titles_by_manuscripts_with_nil):
        if not isinstance(
            manuscript.get("manuscripts").get("manuscript"), list
        ):
            manuscript["manuscripts"]["manuscript"] = [
                manuscript["manuscripts"]["manuscript"]
            ]
        if manuscript.get("location") != "nil, nil":
            titles_by_manuscripts.append(manuscript)

    try:
        titles_json = loads(titles_text)
    except Exception:
        titles_json = {"result": []}
    url_and_titles = titles_json.get("result")
    id_of_title = {}
    for aut in url_and_titles:
        id_of_title[aut["id"]] = "/?id=" + aut["path"]

    title_list = titles_json.get("result")
    title_of_current_document = "".join(
        [i["path"] == document_id and i["id"] or "" for i in title_list]
    )

    length_of_extension = len(".xml")

    for url_and_title in url_and_titles:
        url_and_title["path"] = url_and_title.get("path")[
            :-length_of_extension
        ]

    for title_for_author in titles_for_authors:
        for title in title_for_author.get("titles"):
            if isinstance(title, str):
                title = {"id": title_for_author.get("titles")}
                if isinstance(title["id"], list):
                    title_for_author["titles"] = [title["id"]]
            else:
                title["id"] = title.get("id")[:-length_of_extension]
    return {
        "url_and_titles": url_and_titles,
        "titles_for_authors": titles_for_authors,
        "titles_by_manuscripts": titles_by_manuscripts,
        "id_of_title": id_of_title,
        "titles": titles,
        "title_of_current_document": title_of_current_document,
    }


def redirect_from_select_menu(
    request, menu_by, document_id, chapter, current_section, sections
):
    redirect = False
    html = getattr(request, "html", None)
    if not request.GET.get("is_rest_url"):
        document_id = request.GET.get("id")
        chapter = request.GET.get("chapter")
        if not chapter:
            if chapter != 0:
                chapter = "titelblad"
        document_id = remove_dot_xml(document_id)
        menu_by_argument = ""
        url_prefix = "/text" if request.GET.get("text_only") else ""
        if menu_by:
            menu_by_argument = "?menu_by=%s" % menu_by
        if not document_id and not html:
            # print ("redirecting to front page")
            redirect = HTTPFound(location="/front-page%s" % menu_by_argument)
        elif (
            document_id
            and chapter
            and current_section
            and sections
            and not html
        ):
            # print ("redirecting to section")
            redirect = HTTPFound(
                location=url_prefix
                + (
                    "/%s/%s/%s%s"
                    % (document_id, chapter, current_section, menu_by_argument)
                )
            )
        elif document_id and chapter and not html:
            # print ("redirecting to chapter")
            redirect = HTTPFound(
                location=url_prefix
                + ("/%s/%s%s" % (document_id, chapter, menu_by_argument))
            )
    return redirect


def get_breadcrumb(request, title_of_current_document):
    breadcrumb = ["ikke xml"]
    title_from_request = getattr(request, "title", None)

    if title_of_current_document:
        breadcrumb[0] = title_of_current_document
    elif title_from_request:
        breadcrumb[0] = title_from_request
    elif request.path_info == "/front-page":
        breadcrumb[0] = ""
    else:
        breadcrumb[0] = "Håndskriftsbeskrivelse"
    if request.path_info.endswith(
        "/about"
    ) and not request.path_info.startswith("/about"):
        breadcrumb.append("tekstbeskrivelse")
        breadcrumb[0] = (
            request.path_info.partition("/about")[0][1:]
            .title()
            .replace("-", " ")
        )
    return breadcrumb
