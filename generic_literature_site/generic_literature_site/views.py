# Copyright (C) 2017-20 Dansk Sprog- og Litteraturselskab og Magenta ApS.
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
import os
import functools
import re
import logging
import collections
import zlib

from json import loads, dumps

from urllib3 import HTTPConnectionPool


from pyramid.response import Response
from pyramid.renderers import get_renderer
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPNotFound
from requests import get
from pagecalc import Paginator

from .exist_api.parse_arguments import (
    parse_arguments,
    parse_category_arguments,
    parse_language_arguments,
    convert_to_danish_characters,
    get_language_to_code,
)
from .exist_api.exist_api import (
    check_availability_of_server,
    execute_xquery,
    listify,
    remove_dot_xml,
    add_dot_xml,
    view_html,
)
from .chapters_and_sections import (
    get_sections,
    get_chapter,
    chapter_name,
    chapter_names,
    get_section_info,
    chapter_and_section_names,
)
from .menu import (
    make_listings_for_menu,
    redirect_from_select_menu,
    set_menu_by_cookie,
    get_breadcrumb,
)
import django

from bs4 import BeautifulSoup

import memcache

from django.core.exceptions import ObjectDoesNotExist

from pyramid.i18n import TranslationStringFactory

_ = TranslationStringFactory("generic_literature_site")


django.setup()

from literature_data.models import (  # noqa
    Note,
    Person,
    Character,
    Location,
    Publication,
)


class Stopwords:
    _stopwords = None

    @classmethod
    def stopwords(cls):
        if not cls._stopwords:
            current_dir = os.path.dirname(__file__)
            stopwords_file = os.path.join(current_dir, "locale/stopwords.txt")
            with open(stopwords_file, "r") as f:
                stopwords = [w.strip() for w in f.readlines()]
                cls._stopwords = set(stopwords)
        return cls._stopwords


def access_django(func):
    """Decorator to avoid stale DB connections."""

    @functools.wraps(func)
    def django_enabled(*args, **kwargs):
        django.db.close_old_connections()
        result = func(*args, **kwargs)
        return result

    return django_enabled


@view_config(route_name="document_view", renderer="templates/document.pt")
def document_view(request):
    request.GET["id"] = request.matchdict.get("document")
    return smn_view(request)


@view_config(route_name="document_view_text", renderer="templates/text.pt")
def document_view_text(request):
    request.GET["id"] = request.matchdict.get("document")
    return smn_view(request)


suffix_by_meta_type = {
    "accounts": "acc",
    "colophons": "col",
    "introductions": "int",
    "sources": "sources",
}


@view_config(route_name="meta_view", renderer="templates/raw_text.pt")
def meta_view(request):
    request.title = _("Om teksten")
    document_id = request.matchdict.get("document")
    meta_type = request.matchdict.get("type")
    suffix = suffix_by_meta_type.get(meta_type, None)
    locale_name = request.locale_name
    file_path = "html/{}/{}_{}_{}.html".format(
        meta_type, document_id, suffix, locale_name
    )
    request = view_html(request, file_path)
    if request.response.status_code > 400:
        return {"pages": request.response.status}
    else:
        # OK.
        return {"pages": request.html}


@view_config(route_name="section_view", renderer="templates/document.pt")
def section_view(request):
    request.GET["section"] = request.matchdict.get("section")
    return chapter_view(request)


@view_config(route_name="section_view_text", renderer="templates/text.pt")
def section_view_text(request):
    request.GET["section"] = request.matchdict.get("section")
    return chapter_view(request)


@view_config(route_name="chapter_view", renderer="templates/document.pt")
def chapter_view(request):
    request.GET["id"] = request.matchdict.get("document")
    request.GET["chapter"] = request.matchdict.get("chapter")
    request.GET["is_rest_url"] = "True"
    return smn_view(request)


@view_config(route_name="chapter_view_text", renderer="templates/text.pt")
def chapter_view_text(request):
    request.GET["id"] = request.matchdict.get("document")
    request.GET["chapter"] = request.matchdict.get("chapter")
    request.GET["is_rest_url"] = "True"
    return smn_view(request)


@view_config(route_name="section_view_notes", renderer="templates/note_tab.pt")
def section_view_notes(request):
    request.GET["id"] = request.matchdict.get("document", "")
    request.GET["section"] = request.matchdict.get("section", "")
    request.GET["chapter"] = request.matchdict.get("chapter", "")
    request.GET["is_rest_url"] = "True"

    notes_dict = setup_note_dict(request)

    notes_for_chapter = []
    notes_not_in_database = 0
    try:
        notes_for_chapter = notes_dict["notes"]
        notes_not_in_database = notes_dict["notes_not_found"]
    except Exception as e:
        logging.warning("Problems with notes tab." + str(e))

    return {
        "note_list": notes_for_chapter,
        "notes_not_found": notes_not_in_database,
    }


@view_config(route_name="chapter_view_notes", renderer="templates/note_tab.pt")
def chapter_view_notes(request):
    return section_view_notes(request)


@view_config(
    route_name="document_view_notes", renderer="templates/note_tab.pt"
)
def document_view_notes(request):
    return section_view_notes(request)


# @view_config(route_name='text_view', renderer="templates/text.pt")
# def text_view(request):
#     request.GET['id'] = request.matchdict.get('document')
#     request.GET['section'] = request.matchdict.get('section') or None
#     request.GET['chapter'] = request.matchdict.get('chapter') or None
#     return smn_view(request)


def format_person_for_site(person):
    full_name = person.first_name + " " + person.last_name
    if full_name.endswith(", ") or full_name.startswith(", "):
        full_name = full_name.replace(", ", "")

    year_born = person.year_born
    if year_born is not None and str(year_born).startswith("-"):
        year_born = str(year_born)[1:] + " " + _("f.Kr.")

    year_dead = person.year_dead
    if year_dead is not None and str(year_dead).startswith("-"):
        year_dead = str(year_dead)[1:] + " " + _("f.Kr.")

    if person.year_born_is_approx:
        year_born = _("ca.") + " %s" % year_born
    if person.year_dead_is_approx:
        year_dead = _("ca.") + " %s" % year_dead

    if not (year_born and year_dead):
        lifespan = " ({})".format(person.notes_about_life_span)
    else:
        lifespan = " ({}-{})".format(year_born, year_dead)
    if year_born and not year_dead:
        lifespan = " (" + _("født") + " {})".format(year_born)
    if not year_born and year_dead:
        lifespan = " (død {})".format(year_dead)
    if person.notes_about_life_span:
        lifespan = " (%s)" % person.notes_about_life_span
    if person.year_born is not None and person.year_dead is not None:
        if person.year_born < 0 and person.year_dead > 0:
            lifespan = lifespan[:-1] + " e.Kr)"

    lifespan = lifespan.replace(" (None)", "").replace("()", "")
    full_name += lifespan
    notes = person.notes.strip()
    if notes:
        if len(notes) > 1:
            capitalized_notes = notes[0].upper() + notes[1:]
            notes = ": %s" % capitalized_notes
        if not notes.endswith("."):
            notes = "%s." % notes
    else:
        notes = ""

    full_text = full_name + notes
    return full_text


def make_list_danish(list_of_strings):
    danish_text = ""
    if len(list_of_strings) > 1:
        first_items = list_of_strings[:-1]
        first_items_as_string = ", ".join(first_items)
        last_item = list_of_strings[-1]
        danish_text = "%s og %s" % (first_items_as_string, last_item)
    else:
        danish_text = ", ".join(list_of_strings)
    return danish_text


def colorByCookie(request, pages, class_name, color):
    if request.cookies.get("." + class_name) == "checked":
        pages = pages.replace(
            'class="%s"' % class_name,
            'class="%s" style="cursor:pointer;background-color:%s"'
            % (class_name, color),
        )
    elif class_name == "realnote":
        pages = pages.replace(
            'class="%s"' % class_name,
            'class="%s hidden" style="cursor:pointer;background-color:%s"'
            % (class_name, color),
        )
    elif class_name == "textcriticalnote":
        pages = pages.replace(
            'class="%s annotation-marker"' % class_name,
            'class="%s annotation-marker hidden" style="cursor:pointer;background-color:%s"'
            % (class_name, color),
        )
    return pages


def isEnglish(s):
    try:
        s.encode(encoding="utf-8").decode("ascii")
    except UnicodeDecodeError:
        return False
    else:
        return True


def replace_note_tag_contents(pages, note_id, note_type):
    tag = 'style="display: none;">%s</span>'

    tag_with_id = tag % note_id
    tag_with_real_name = tag % note_type
    if not isEnglish(note_id):
        tag_with_real_name = _("Fejl: id indeholder ikke-engelske tegn")
    pages = pages.replace(tag_with_id, tag_with_real_name)
    pages = pages.replace(
        '</span><span class="notelink"', '</span> <span class="notelink"'
    )
    pages = pages.replace(
        '</span><span class="realnote"', '</span> <span class="realnote"'
    )
    pages = pages.replace(
        '</span><span class="textcriticalnote"',
        '</span> <span class="textcriticalnote"',
    )
    return pages


def prepare_publication_note(request, pages, note_id):
    publication_object = Publication.objects.get(uid=note_id)
    publication = (
        publication_object.__str__(first_name_of_author_first=True) + "."
    )
    pages = colorByCookie(request, pages, "bibl", "#EAE18A")
    pages = replace_note_tag_contents(pages, note_id, publication)
    return pages


def prepare_character_note(request, pages, note_id):
    character = Character.objects.get(uid=note_id)
    notes = character.notes
    if not notes.strip():
        notes = ""
    else:
        notes = ": %s" % character.notes
    person = "%s%s" % (str(character).strip(), notes)
    pages = colorByCookie(request, pages, "fictionalpersName", "#F6CDF6")
    pages = replace_note_tag_contents(pages, note_id, person)
    return pages


def prepare_person_note(request, pages, note_id):
    note = Person.objects.get(uid=note_id)
    person = format_person_for_site(note)
    nationality = note.nationality
    if nationality is not None:
        nationality = str(note.nationality) + " "
    else:
        nationality = ""
    profession_and_nationality = (
        ": " + nationality + note.description_of_profession + ". "
    )
    if ": " in person:
        person = person.replace(": ", profession_and_nationality)
    else:
        person = "%s%s" % (person, profession_and_nationality)
    pages = colorByCookie(request, pages, "persName", "#EDD19F;")
    pages = replace_note_tag_contents(pages, note_id, person)
    return pages


def prepare_place_note(request, pages, note_id):
    pages = colorByCookie(request, pages, "placeName", "#D1DFB6")
    if note_id:
        note = Location.objects.get(uid=note_id)
        place = str(note)
        pages = replace_note_tag_contents(pages, note_id, place)
    return pages


def prepare_comment_note(request, pages, note_id):
    pages = colorByCookie(request, pages, "realnote", "transparent")
    return pages


def prepare_criticism_note(request, pages, note_id):
    pages = colorByCookie(request, pages, "textcriticalnote", "transparent")
    return pages


@access_django
def insert_note_type(request, soup, pages, css_class, type_for_log):
    notes = soup.findAll("span", {"class": css_class})
    for note_tag in notes:
        note_id = note_tag.text.strip()
        # if note_id:
        #    logging.info("Gets %s %s from database" % (type_for_log, note_id))
        try:
            if css_class == "biblcontents":
                pages = prepare_publication_note(request, pages, note_id)
            if css_class == "persNamecontents" and type_for_log == "persName":
                pages = prepare_person_note(request, pages, note_id)
            if (
                css_class == "fictionalpersNamecontents"
                and type_for_log == "fictional persName"
            ):
                pages = prepare_character_note(request, pages, note_id)
            if (
                css_class == "placeNamecontents"
                and type_for_log == "placeName"
            ):
                pages = prepare_place_note(request, pages, note_id)
            if css_class == "notecontents" and type_for_log == "realnote":
                pages = prepare_comment_note(request, pages, note_id)
            if (
                css_class == "appnotecontents"
                and type_for_log == "textcriticalnote"
            ):
                pages = prepare_criticism_note(request, pages, note_id)
        except ObjectDoesNotExist:
            if note_id:
                logging.warning(
                    "%s %s could not be found" % (type_for_log, note_id)
                )
    return pages


@access_django
def insert_note_texts(request, pages):
    soup = BeautifulSoup(pages, "html.parser")
    notes = soup.findAll("span", {"class": "notecontents"})

    for note_tag in notes:
        note_id = note_tag.text.strip()
        try:
            note_id = int(note_id[1:])
            note = Note.objects.get(id=note_id)
            literature_reference = note.literature_reference
            if literature_reference is None:
                literature_reference = ""
            else:
                literature_reference = " (%s)" % note.link_text
            note_text = ">%s] %s%s.<" % (
                note.lemma,
                note.text,
                literature_reference,
            )
            note_text = note_text.replace("..", ".")
            pages = pages.replace(">n%s<" % str(note_id), note_text)
            pages = pages.replace(
                '<a href="notelinkn', '<a class="comment-link" href="#n'
            )

        except ObjectDoesNotExist:
            if note_id:
                logging.warning("Id %s could not be found" % note_id)
        except ValueError:
            if note_id == "n":
                logging.warning(
                    "Wrong note format. Please append number after the letter"
                )
            else:
                logging.warning(
                    "Note id %s must be the letter n followed by an integer"
                    % note_id
                )

    pages = insert_note_type(
        request, soup, pages, "persNamecontents", "persName"
    )
    pages = insert_note_type(
        request, soup, pages, "fictionalpersNamecontents", "fictional persName"
    )
    pages = insert_note_type(
        request, soup, pages, "placeNamecontents", "placeName"
    )
    pages = insert_note_type(request, soup, pages, "biblcontents", "bibl")
    pages = insert_note_type(request, soup, pages, "notecontents", "realnote")
    pages = insert_note_type(
        request, soup, pages, "appnotecontents", "textcriticalnote"
    )
    return pages


@access_django
def notes_for_document(
    xquery_folder, document_id, chapter, section, section_and_chapter
):
    if section_and_chapter in [
        "titelblad",
        "dedikation",
        "preface",
        "forord",
        "motto",
        "introduktion",
        "kalender",
        "indholdsfortegnelse",
    ]:
        return []
    url = (
        xquery_folder
        + "notes_of_chapter.xquery?id=%s&chapter=%s&section=%s"
        % (document_id, chapter, section)
    )
    document = get(url).content
    document = document.decode("utf-8")
    refs = []
    note_numbers = []
    if document and document != "null":
        refs = loads(document)["ref"]
        try:
            note_numbers = [ref["target"] for ref in refs]
        except Exception:
            print('error in <ref target=""')
    notes = []
    notes_not_found = 0
    for note_id in note_numbers:
        try:
            note_number = int(note_id.replace("n", ""))
            note = Note.objects.get(id=note_number)
            literature_reference = note.literature_reference
            link_text = ""
            if literature_reference is None:
                literature_reference = ""
                note_text = "<strong>%s</strong><br/>%s" % (
                    note.lemma,
                    note.text,
                )
            else:
                literature_reference = "  %s" % note.literature_reference
                link_text = note.link_text
                note_text = """<script type="text/javascript">
                          jQuery( document ).ready( function() {
                            jQuery( '#dialog%s' ).dialog( { 'autoOpen': false,
                            'title':'Litteratur', 'padding':0, minHeight: 80,
                            position:['middle',20], resizable: false,
                            draggable: false, } );
                          });
                        </script><strong>%s</strong><br/>%s
                        <span id="publicationReferenceInNote%s"
                        class="publicationReferenceInNote">%s</span>.
                        <div id="dialog%s">
                          <div style="margin:0;padding-top:5px;">%s<div>
                        </div>""" % (
                    note_id,
                    note.lemma,
                    note.text,
                    note_id,
                    link_text,
                    note_id,
                    literature_reference,
                )
            if not note_text.endswith(".") and "</a>." not in note_text:
                note_text = note_text.strip() + "."
            note = {"note_id": note_id, "note": note_text}

            notes.append(note)
        except Exception:
            notes_not_found += 1

    return {"notes": notes, "notes_not_found": notes_not_found}


def setup_note_dict(request):
    database_address = request.registry.settings["exist_server"]
    xquery_folder = database_address + "xqueries/"
    arguments = parse_arguments(request, available_categories)
    document_id = add_dot_xml(arguments.get("id"))
    chapter = arguments["chapter"]
    current_section = arguments["section"]
    section_and_chapter = chapter
    if current_section:
        section_and_chapter = "%s/%s" % (chapter, current_section)

    notes_dict = notes_for_document(
        xquery_folder,
        document_id,
        chapter,
        current_section,
        section_and_chapter,
    )

    return notes_dict


def get_introduction_text(request, arguments):
    introduction_folder = (
        request.registry.settings["exist_server"] + "html/introductions"
    )
    document_id_without_xml = arguments.get("id")
    introduction_text = get(
        introduction_folder + "/" + document_id_without_xml + "_int_da.html"
    ).text

    # Her skal laves en funktion, der hiver litteraturnotenumrene ud af
    # introduction_text og putter dem i note_numbers. Derefter skal den
    # nederste del af notes_for_document.

    return introduction_text


def add_named_chapters(
    request,
    xquery_folder,
    document_id,
    chapters,
    sections,
    chapter,
    current_section,
):
    if isinstance(chapter, str):
        named_chapter = chapter
        chapter = 1
    else:
        named_chapter = chapter
    try:
        sections_of_previous_chapter = get_sections(
            xquery_folder, document_id, chapter - 1
        )
    except Exception:
        sections_of_previous_chapter = []
    if not current_section and sections:
        current_section = 0
    chapter_arg = chapter
    if named_chapter:
        chapter_arg = named_chapter
    chapters_of_document = chapters["chapters_of_document"]
    additional_chapters = [
        {"name": "Titelblad", "no": "titelblad"},
        {"name": "Dedikation", "no": "dedikation"},
        {"name": "Motto", "no": "motto"},
        {"name": "Forord", "no": "preface"},
        {"name": "Indholdsfortegnelse", "no": "toc-section"},
        {"name": "Kalender", "no": "calendar"},
        {"name": "Introduktion", "no": "introduction"},
    ]
    chapters_of_document = additional_chapters + chapters_of_document
    for additional_chapter in additional_chapters:
        additional_chapter_name = additional_chapter.get("no")
        chapter_content = get_chapter(
            xquery_folder,
            document_id,
            additional_chapter_name,
            current_section,
        )
        if chapter_content == "<results></results>":
            chapters_of_document.remove(additional_chapter)
    return {
        "chapters_of_document": chapters_of_document,
        "chapter_arg": chapter_arg,
        "sections_of_previous_chapter": sections_of_previous_chapter,
        "named_chapter": named_chapter,
        "chapter": chapter,
    }


@view_config(route_name="index_view", renderer="templates/document.pt")
def smn_view(request):
    database_address = request.registry.settings["exist_server"]
    xquery_folder = database_address + "xqueries/"
    arguments = parse_arguments(request, available_categories)
    search_string = request.GET.get("q")
    if not search_string:
        search_string = ""
    document_id = add_dot_xml(arguments.get("id"))
    ok = check_availability_of_server(request)
    if not ok or document_id in ["resources.xml", "favicon.ico.xml"]:
        return empty_dictionary()
    chapter = arguments["chapter"]
    current_section = arguments["section"]
    section_and_chapter = chapter
    if current_section:
        section_and_chapter = "%s/%s" % (chapter, current_section)
    results = arguments["results"]
    menu_by = arguments["menu_by"]
    sections = get_sections(xquery_folder, document_id, chapter)
    chapters = chapter_names(xquery_folder, document_id)
    page_is_available = chapters["page_is_available"]
    chapters_and_sections = chapter_and_section_names(
        xquery_folder, document_id
    )
    chapter_dict = add_named_chapters(
        request,
        xquery_folder,
        document_id,
        chapters,
        sections,
        chapter,
        current_section,
    )
    chapters_of_document = chapter_dict["chapters_of_document"]
    author_of_document = execute_xquery(
        request, f"author_of_document.xquery?id={document_id}"
    )
    chapter_arg = chapter_dict["chapter_arg"]
    sections_of_previous_chapter = chapter_dict["sections_of_previous_chapter"]
    named_chapter = chapter_dict["named_chapter"]
    chapter = chapter_dict["chapter"]
    redirect = redirect_from_select_menu(
        request, menu_by, document_id, chapter, current_section, sections
    )
    if redirect and chapter != 0:
        return redirect
    pages = get_chapter(
        xquery_folder, document_id, chapter_arg, current_section
    )
    document_id_without_xml = remove_dot_xml(document_id)
    pages = pages.replace("document_id_placeholder", document_id_without_xml)
    try:
        previous_chapter_name = chapter_name(
            xquery_folder, document_id, chapter - 1
        )
    except Exception:
        pass
    last_chapter = 0
    if chapters_of_document:
        try:
            last_chapter = int(chapters_of_document[-1].get("no"))
        except Exception:
            last_chapter = 0
    next_chapter_name = ""
    if chapter < last_chapter:
        next_chapter_name = chapter_name(
            xquery_folder, document_id, chapter + 1
        )

    section_info = get_section_info(
        xquery_folder,
        document_id,
        chapter,
        current_section,
        sections,
        sections_of_previous_chapter,
    )
    previous_section_name = section_info["previous_section_name"]

    last_section_in_previous_chapter = section_info[
        "last_section_in_previous_chapter"
    ]
    last_section_in_previous_chapter_name = section_info[
        "last_section_in_previous_chapter_name"
    ]
    is_last_section = section_info["is_last_section"]
    next_section_name = section_info["next_section_name"]
    is_last_chapter = False
    if chapter == len(chapters_of_document):
        is_last_chapter = True
    set_menu_by_cookie(request)
    listings_for_menu = make_listings_for_menu(xquery_folder, document_id)
    titles_for_authors = listings_for_menu["titles_for_authors"]
    id_of_title = listings_for_menu["id_of_title"]
    titles = listings_for_menu["titles"]
    title_url = xquery_folder + "/title_of_document.xquery?id=" + document_id
    title_of_current_document = (
        get(title_url).text.replace('"', "").replace("null", "")
    )
    breadcrumb = get_breadcrumb(request, title_of_current_document)
    pages = pages.replace("</span>]   ", "]   ")
    if hasattr(request, "title"):
        title_of_current_document = request.title
    pages = insert_note_texts(request, pages)
    chapters_of_document = chapters_and_sections["chapters_of_document"]

    notes_dict = setup_note_dict(request)

    notes_for_chapter = []
    notes_not_in_database = 0
    try:
        notes_for_chapter = notes_dict["notes"]
        notes_not_in_database = notes_dict["notes_not_found"]
    except Exception as e:
        logging.warning("Problems with notes tab." + str(e))

    variants_lists_folder = (
        request.registry.settings["exist_server"] + "html/text-variant-lists"
    )
    document_id_without_xml = arguments.get("id")
    variants_list = get(
        variants_lists_folder + "/" + document_id_without_xml + "_var_da.html"
    )
    if variants_list.status_code > 400:
        variants_list_text = None
    else:
        # OK.
        variants_list_text = variants_list.text

    def get_location(chapter_no):
        return "/%s/%s" % (arguments.get("id"), chapter_no)

    def get_prefix(chapter):
        prefix = ""
        # chapter.no is x/y for chapter/section, i.e. sections
        # will contain a slash. Use this to distinguish from chapters,
        # and indent the section
        if "/" in str(chapter["no"]):
            prefix += "&nbsp;&nbsp;&nbsp;"
        # chapters such as "titelblad" will have a property "header_no"
        # with a value of 0
        if "header_no" not in chapter or not chapter["header_no"] == 0:
            prefix += str(chapter["no"]).replace("/", ".") + ": "
        return prefix

    return {
        "layout": site_layout(),
        "page_title": "Home",
        "smn": results,
        "pages": pages,
        "title_of_current_document": title_of_current_document,
        "author_of_document": author_of_document,
        "breadcrumb": breadcrumb,
        "titles": titles.text,
        "document_id": document_id,
        "document_id_without_xml": document_id_without_xml,
        "chapters_of_document": chapters_of_document,
        "chapters_and_sections_of_document": chapters_and_sections,
        "sections_of_chapter": sections,
        "sections_of_previous_chapter": sections_of_previous_chapter,
        "is_last_section": is_last_section,
        "is_last_chapter": is_last_chapter,
        "no_of_chapters": len(chapters_of_document),
        "current_chapter": chapter,
        "current_named_chapter": named_chapter,
        "current_section": current_section,
        "current_section_and_chapter": section_and_chapter,
        "previous_chapter_name": previous_chapter_name,
        "next_chapter_name": next_chapter_name,
        "previous_section_name": previous_section_name,
        "next_section_name": next_section_name,
        "last_section_in_previous_chapter": last_section_in_previous_chapter,
        "last_section_in_previous_chapter_name": last_section_in_previous_chapter_name,  # noqa
        "titles_for_authors": titles_for_authors,
        "page_is_available": page_is_available,
        "id_of_title": id_of_title,
        "menu_by_not_cookie": menu_by,
        "html": getattr(request, "html", None),
        "title": title_of_current_document,
        "note_list": notes_for_chapter,
        "notes_not_found": notes_not_in_database,
        "variants_list_text": variants_list_text,
        "locale_name": request.locale_name,
        "search_string": search_string,
        "next_chapter": _("Næste kapitel"),
        "previous_chapter": _("Forrige kapitel"),
        "next_section": _("Næste afsnit"),
        "previous_section": _("Forrige afsnit"),
        "no_title": _("(uden titel)"),
        "get_location": get_location,
        "get_prefix": get_prefix,
    }


def site_layout():
    renderer = get_renderer("generic_literature_site:templates/layout.pt")
    layout = renderer.implementation().macros["layout"]
    return layout


def front_page_layout():
    renderer = get_renderer(
        "generic_literature_site:templates/layout_of_front_page.pt"
    )
    layout = renderer.implementation().macros["layout"]
    return layout


@view_config(route_name="about_view", renderer="templates/about.pt")
def about_view(request):
    exist_server = request.registry.settings["exist_server"]
    folder = exist_server + "html"
    id_without_extension = request.matchdict.get("document")
    document_id = id_without_extension + ".html"
    about_url = folder + "/" + document_id
    about = get(about_url)
    about_text = about.text
    xml_header = '<?xml version="1.0" encoding="UTF-8"?>\n'
    about_text = about_text.replace(xml_header, "")
    request.html = about_text
    folder = exist_server + ""
    title_url = (
        folder
        + "/xqueries/title_of_document.xquery?id="
        + id_without_extension
        + ".xml"
    )
    json = get(title_url).text
    title = ""
    if json:
        title = loads(json)
    request.title = title
    return smn_view(request)


@view_config(route_name="about_site_view", renderer="templates/about.pt")
def about_site_view(request):
    request.title = _("Om projektet")
    locale_name = request.locale_name
    request = view_html(request, "about_{}.html".format(locale_name))
    return smn_view(request)


@view_config(route_name="data_view", renderer="templates/about.pt")
def data_view(request):
    request.title = _("Data")
    locale_name = request.locale_name
    request = view_html(request, "data_{}.html".format(locale_name))
    return smn_view(request)


@view_config(route_name="english_view", renderer="templates/about.pt")
def english_view(request):
    request.locale_name = "en"
    response = smn_view(request)

    response.set_cookie("_LOCALE_", "en")
    return response


@view_config(route_name="danish_view", renderer="templates/about.pt")
def danish_view(request):
    request.locale_name = "da"
    response = smn_view(request)

    response.set_cookie("_LOCALE_", "da")
    return response


@view_config(route_name="front_page_view", renderer="templates/front_page.pt")
def front_page_view(request):
    return {"layout": front_page_layout()}


@view_config(route_name="instructions_view", renderer="templates/about.pt")
def instructions_view(request):
    request.title = _("Vejledning")
    locale_name = request.locale_name
    request = view_html(request, "instructions_{}.html".format(locale_name))
    return smn_view(request)


@access_django
def get_notes(register_type, first_letter):
    if register_type == "personer":
        notes = Person.objects.filter(last_name__startswith=first_letter)
    if register_type == "vaerker":
        notes = Publication.objects.filter(title__startswith=first_letter)
    if register_type == "steder":
        notes = Location.objects.filter(name__startswith=first_letter)
    if register_type == "litteraere_figurer":
        notes = Character.objects.filter(name__startswith=first_letter)
    return notes


@view_config(route_name="register_view", renderer="templates/index.pt")
def register_view(request):
    request.title = _("Register")
    register_type = request.matchdict.get("type")
    first_letter = request.matchdict.get("first_letter")
    search_string = request.GET.get("q")
    if not search_string:
        search_string = ""

    notes = get_notes(register_type, first_letter)
    register_items = []
    mem_cache = memcache.Client(
        ["127.0.0.1:11211"], debug=0, server_max_value_length=1024 * 1024 * 16
    )
    for register_item in notes:
        # Maybe we got references for this item in the cache.
        mc_key = (register_type + register_item.uid).replace(" ", "")
        references = mem_cache.get(mc_key)
        if references is None:

            # See if there's any references for this item.
            references = []
            xquery = "documents_of_note.xquery?note_id={}&note_type={}".format(
                register_item.uid, register_type
            )
            refs = execute_xquery(request, xquery)
            # Format with or without references as the case may be.
            results = refs["results"] if refs else []
            if isinstance(results, str):
                results = [results]
            for r in results:
                title, page, document_id = r.split("#")
                document_name, _unused = os.path.splitext(document_id)
                # TODO: Find a better way to do this.
                # But don't included lemmatised versions.
                if "lemmatised" in document_name:
                    continue
                page_no = page.split(" ")[-1]
                # Get chapter for page number
                xquery = "chapter_of_page.xquery?id={}&page={}".format(
                    document_id, page_no
                )
                chapter_and_section = execute_xquery(request, xquery)
                try:
                    chapter = chapter_and_section["results"]["chapter"]
                    section = (
                        chapter_and_section["results"]["section"]
                        if "section" in chapter_and_section["results"]
                        else None
                    )
                except TypeError:
                    if (
                        chapter_and_section
                        and type(chapter_and_section["results"]) is list
                    ):
                        chapter = chapter_and_section["results"][0]["chapter"]
                        section = (
                            chapter_and_section["results"][0]["section"]
                            if "section" in chapter_and_section["results"][0]
                            else None
                        )
                    else:
                        print(
                            "FAILED: {}, note={}, document={}, page={}".format(
                                chapter_and_section,
                                register_item.uid,
                                document_id,
                                page_no,
                            )
                        )
                        continue
                link = (
                    '<a href="/{}/{}/{}#{}">{}, {}</a>'.format(
                        document_name, chapter, section, page_no, title, page
                    )
                    if section
                    else '<a href="/{}/{}#{}">{}, {}</a>'.format(
                        document_name, chapter, page_no, title, page
                    )
                )
                if link not in references:
                    references.append(link)
            mem_cache.set(mc_key, references, time=86400)
        new_item = {"text": str(register_item), "refs": list(references)}
        register_items.append(new_item)

    danish_letters = [chr(c) for c in range(ord("A"), ord("Z") + 1)] + [
        "Æ",
        "Ø",
        "Å",
    ]

    return {
        "layout": site_layout(),
        "faksimile": None,
        "title": "Søgeresultat",
        "danish_letters": danish_letters,
        "register_type": register_type,
        "first_letter": first_letter,
        "register_items": register_items,
        "search_string": search_string,
    }


@view_config(route_name="textlist_view", renderer="templates/about.pt")
def textlist_view(request):
    request.title = _("Tekster")
    locale_name = request.locale_name
    request = view_html(request, "texts_{}.html".format(locale_name))
    return smn_view(request)


@view_config(route_name="guidelines_view", renderer="templates/about.pt")
def guidelines_view(request):
    request.title = _("Vejledning")
    locale_name = request.locale_name
    request = view_html(request, "guidelines_{}.html".format(locale_name))
    return smn_view(request)


@view_config(route_name="research_page_view", renderer="templates/about.pt")
def research_page_view(request):
    request.title = _("Forskning")
    page = request.matchdict["page"]
    extension = request.matchdict["extension"]
    path = "html/research/" + page + "." + extension
    if extension == "html":
        request = view_html(request, path)
        return smn_view(request)
    file = get(request.registry.settings["exist_server"] + path)
    if file:
        return Response(
            content_type=file.headers["content-type"], body=file.content
        )
    return HTTPNotFound()


@view_config(route_name="research_view", renderer="templates/about.pt")
def research_view(request):
    request.title = _("Forskning")
    locale_name = request.locale_name
    request = view_html(request, "research_{}.html".format(locale_name))
    return smn_view(request)


available_categories = [
    "historie",
    "skoenlitteratur",
    "jura",
    "kogebog",
    "medicin",
    "naturkundskab",
    "historie",
    "ordsprog",
    "religion",
]


def get_available_documents(request):
    documents_xquery = "list_titles.xquery"
    documents = execute_xquery(request, documents_xquery)
    available_documents = {}

    for d in documents["result"]:
        xml_name = d["path"]
        author_xquery = f"author_of_document.xquery?id={xml_name}"
        author = execute_xquery(request, author_xquery)
        if author:
            title = author + ": " + d["id"]
        else:
            title = d["id"]
        available_documents[xml_name] = title

    return available_documents


@view_config(route_name="search_results", renderer="templates/search.pt")
def search_results_view(request):
    ok = check_availability_of_server(request)
    if not ok:
        return empty_dictionary()
    arguments = parse_arguments(request, available_categories)
    language_arguments = parse_language_arguments(arguments)
    category_arguments = parse_category_arguments(arguments)
    search_string = arguments["search_string"]
    results_per_page = int(arguments["results_per_page"])
    language_argument = language_arguments.get("language_argument")
    languages = language_arguments.get("languages")
    category_argument = category_arguments.get("category_argument")
    categories_as_text = category_arguments.get("categories_as_text")
    word = search_string

    document_ids = request.GET.getall("document_id")

    xquery = "kwic_search.xquery?q=%s&%s%s" % (
        word,
        category_argument,
        language_argument,
    )

    mem_cache = memcache.Client(["127.0.0.1:11211"], debug=0)
    mc_key = xquery.replace(" ", "")
    cached_document = mem_cache.get(mc_key)
    if cached_document:
        document = zlib.decompress(cached_document).decode()
        document = loads(document)
    elif word and word.lower() not in Stopwords.stopwords():
        document = execute_xquery(request, xquery)
        zipped_document = zlib.compress(dumps(document).encode())
        mem_cache.set(mc_key, zipped_document, time=86400)
    else:
        document = {"no_of_results": 0, "result_list": []}

    if isinstance(document, bytes):
        raise RuntimeError("This should never ever happen!!!")
    search_result = listify(document.get("result_list") or [])

    results = process_search_results(search_result, document_ids)
    no_of_results = len(results)
    page = 1
    paginator = Paginator(total=len(results), by=results_per_page)
    pages = paginator.paginate(page)

    url_without_page_argument = "&".join(
        filter(lambda x: not x.startswith("page"), request.url.split("&"))
    )
    url_without_results_per_page_argument = "&".join(
        filter(
            lambda x: not x.startswith("results_per_page"),
            url_without_page_argument.split("&"),
        )
    )

    languages_as_text = languages

    request.title = _("Søgeresultat")

    no_of_results = len(results)

    result_dict = {
        "layout": site_layout(),
        "title": "Søgeresultat",
        "title_of_current_document": "Søgeresultat",
        "faksimile": None,
        "menu_by_not_cookie": None,
        "breadcrumb": ["Søgeresultat"],
        "titles_for_authors": [],
        "results": results,
        "no_of_results": no_of_results,
        "search_string": search_string,
        "categorys": [],
        "categories_as_text": categories_as_text,
        "languages_as_text": languages_as_text,
        "languages": languages,
        "paginator": pages,
        "results_per_page": results_per_page,
        "page": page,
        "url_without_page_argument": url_without_page_argument,
        "url_without_results_per_page_argument": url_without_results_per_page_argument,  # noqa
        "words_for_link": search_string,
        "available_documents": get_available_documents(request),
    }

    return result_dict


def format_kwic_lines(i):
    kwic_lines = []
    if "kwic" in i and "p" in i["kwic"]:
        hits = i["kwic"]["p"]
    else:
        print("Result {} has no kwic lines", i)
        hits = []
    page_nos = i["page_no"].split() if i["page_no"] else []
    page_nos = collections.deque(page_nos)

    for sentence in listify(hits):
        try:
            sentence = sentence.get("span")
        except Exception:
            print("%s is not dict" % sentence)
            continue
        page_no = page_nos.popleft() if page_nos else None
        page_no_str = "#{}".format(page_no) if page_no else ""
        html = "<span>"
        skip = False
        for part in sentence:
            text = part.get("#text", "")
            if part.get("class") == "hi":
                link = '<a href="/%s/%s/%s?q=%s%s">%s</a>' % (
                    i["id"],
                    i["chapter_no"],
                    i["section_no"],
                    i["q"],
                    page_no_str,
                    text,
                )
                text = "<strong>%s</strong>" % link
                highlighted_text = text
            else:
                text = re.sub("<[^<]+?>", "", text)

                if text.lower().strip().endswith(
                    i["q"]
                ) or text.lower().strip().startswith(i["q"]):
                    skip = True
            html = html + text
        if skip:
            continue
        if highlighted_text == html.replace("<p>", "").replace("</p>", ""):
            html = None
        if page_no is not None:
            html = "%s (side %s)" % (html, page_no)
        if html is not None:
            kwic_lines.append(html)

    kwic_lines = list(set(kwic_lines))
    return kwic_lines


def order_by_id(results):

    document_id_dict = {}
    for result in results:
        document_id = result["id"]
        list_of_results = document_id_dict.get(document_id)
        if list_of_results is None:
            list_of_results = []
        if result not in list_of_results:
            list_of_results.append(result)
        document_id_dict[document_id] = list_of_results
    ordered_dict = collections.OrderedDict(
        sorted(document_id_dict.items(), key=lambda t: t[0])
    )

    return ordered_dict


def process_search_results(search_result, document_ids):
    results = []
    if search_result:
        for i in listify(search_result):
            if not i:
                continue
            chapter_title = i.get("title")
            if chapter_title is None:
                chapter_title = _("(ingen titel)")
            summary = i.get("summary")
            summary = listify(summary) if summary else []
            summary = "".join(summary)
            id_with_xml = i.get("id")
            document_id = id_with_xml.replace(".xml", "")
            if document_ids and id_with_xml not in document_ids:
                continue

            document_languages_json = []
            if i.get("language") is not None:
                document_languages_json = i.get("language").get("language")
            document_languages = listify(document_languages_json)

            language_to_code = get_language_to_code()
            code_to_language = {v: k for k, v in language_to_code.items()}
            idents = []
            language_code = ""
            for language in document_languages:
                language_code = language.get("ident")
                idents.append(code_to_language.get(language_code))
            if idents != [None]:
                document_languages = ", ".join(idents)
                document_languages = convert_to_danish_characters(
                    document_languages
                )
                language_as_word = {
                    "da": "dansk",
                    "en": "engelsk",
                    "fr": "fransk",
                    "de": "tysk",
                }
                if document_languages in language_as_word.keys():
                    document_languages = language_as_word[document_languages]
            if language_code not in code_to_language:
                document_languages = []
            category = i.get("category")
            if category is not None:
                category = category.get("term")
            if type(category) is list:
                category = ", ".join(category)
            if category is not None:
                category = convert_to_danish_characters(
                    category.replace("empty", "")
                )
            kwic_lines = format_kwic_lines(i)
            results.append(
                {
                    "page_no": i["page_no"],
                    "chapter_no": i["chapter_no"],
                    "section_no": i["section_no"],
                    "id": document_id,
                    "title": chapter_title,
                    "summary": summary,
                    "languages": document_languages,
                    "category": category,
                    "kwic": kwic_lines,
                }
            )
        results = order_by_id(results)
    return results


GO_PROXY = HTTPConnectionPool("ordnet-ws1.dsl.lan", port="9196", maxsize=10)


@view_config(route_name="go_popup", renderer="templates/go_popup.pt")
def go_popup(request):
    """Return query - word must be unicode"""
    entry_id = request.GET.get("entry_id")
    fields = {"entry_id": entry_id, "format": "html", "app": "smn"}
    try:
        resp = GO_PROXY.request("GET", "/query", fields=fields)
        result = resp.data
    except Exception:
        result = ""
    return {"result": result}


def empty_dictionary():
    return {
        "layout": site_layout(),
        "page_title": "Error",
        "smn": {},
        "pages": [],
        "title_of_current_document": "Error: eXist is probably down",
        "titles": "",
        "document_id": "Error",
        "chapters_of_document": "",
        "no_of_chapters": "",
        "current_chapter": 0,
        "previous_chapter_name": "",
        "next_chapter_name": "",
        "titles_for_authors": [],
        "page_is_available": False,
        "id_of_title": "",
        "faksimile": "",
        "breadcrumb": "",
        "title": "Error: eXist is probably down",
        "search_string": "Error: eXist is probably down",
        "old_danish_search_strings": [],
        "from_date": "",
        "to_date": "",
        "languages": [],
        "languages_as_text": "",
        "categories_as_text": "",
        "no_of_results": 0,
        "menu_by_not_cookie": None,
    }
