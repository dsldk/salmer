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
from copy import deepcopy
from .exist_api.exist_api import listify, execute_xquery
from operator import itemgetter


def chapter_names(xquery_folder, document_id):
    if document_id == "favicon.ico.xml":
        return {"chapters_of_document": [], "page_is_available": False}
    chapters_of_document_url = (
        xquery_folder + "chapters_of_document.xquery?id=%s" % document_id
    )
    document = get(chapters_of_document_url)
    page_is_available = True

    if document.status_code != 200:
        page_is_available = False
        chapters_of_document = []
    else:
        document_structure = loads(document.text)
        if document_structure is not None:
            chapters_of_document = document_structure.get("sections")
        else:
            chapters_of_document = []
        if isinstance(chapters_of_document, dict):
            chapters_of_document = [chapters_of_document]
        if chapters_of_document == [{"name": None, "no": "1"}]:
            chapters_of_document = []

    return {
        "chapters_of_document": chapters_of_document,
        "page_is_available": page_is_available,
    }


def flatten_chapter_and_sections(chapters_of_document):
    flattened_list = []
    for chapter in chapters_of_document:
        chapter_dict = {"name": chapter["name"], "no": chapter["no"]}
        flattened_list.append(chapter_dict)
        for section in listify(chapter.get("sections")):
            section_dict = {
                "name": str(section["name"]),
                "no": chapter["no"] + "/" + section["no"],
            }
            if section["name"] is not None:
                flattened_list.append(section_dict)
    return flattened_list


def add_to_header(header_chapters, header_chapter_list, tag_name, title_name):
    if header_chapters[tag_name]["exists"] == "true":
        no_in_sequence = header_chapters[tag_name]["no"]
        if no_in_sequence is None:
            no_in_sequence = 0
        else:
            no_in_sequence = int(no_in_sequence)
        header_chapter_list.append(
            {
                "name": title_name,
                "header_no": no_in_sequence,
                "no": title_name.lower(),
            }
        )
    return header_chapter_list


def add_header_chapters(xquery_folder, document_id, chapters_of_document):
    url = xquery_folder + "check_header_chapters.xquery?id=%s" % document_id
    # import pdb; pdb.set_trace()
    result = get(url)
    header_chapters = result.json()
    header_chapter_list = []

    header_chapter_list = add_to_header(
        header_chapters, header_chapter_list, "title_page", "Titelblad"
    )
    header_chapter_list = add_to_header(
        header_chapters, header_chapter_list, "dedication", "Dedikation"
    )
    header_chapter_list = add_to_header(
        header_chapters, header_chapter_list, "preface", "Forord"
    )
    header_chapter_list = add_to_header(
        header_chapters, header_chapter_list, "epigraph", "Motto"
    )

    sorted_header = sorted(header_chapter_list, key=itemgetter("header_no"))
    chapters_of_document = sorted_header + chapters_of_document
    return chapters_of_document


def chapter_and_section_names(xquery_folder, document_id):
    chapters_of_document_url = (
        xquery_folder
        + "chapters_and_sections_of_document.xquery?id=%s" % document_id
    )

    document = get(chapters_of_document_url)
    page_is_available = True

    if document.status_code != 200:
        page_is_available = False
        chapters_of_document = []
    else:
        document_structure = loads(document.text)
        if document_structure is not None:
            chapters_of_document = document_structure.get("chapters")
        else:
            chapters_of_document = []
        if isinstance(chapters_of_document, dict):
            chapters_of_document = [chapters_of_document]
        if chapters_of_document == [{"name": None, "no": "1"}]:
            chapters_of_document = []

    chapters_of_document = flatten_chapter_and_sections(chapters_of_document)
    chapters_of_document = add_header_chapters(
        xquery_folder, document_id, chapters_of_document
    )

    return {
        "chapters_of_document": chapters_of_document,
        "page_is_available": page_is_available,
    }


def get_sections(xquery_folder, document_id, chapter):
    try:
        if chapter < 1:
            return []
        sections_url = (
            xquery_folder
            + "sections_of_chapter.xquery?id=%s&chapter=%s"
            % (document_id, chapter)
        )

        document = get(sections_url).content
        document = document.decode("utf-8")
        if document and document != "null":
            sections = loads(document).get("sections")

        else:
            sections = []
        sections = listify(sections)
    except Exception:
        sections = []
    return sections


def chapter_name(xquery_folder, document_id, chapter):
    if not chapter:
        chapter = 1
    chapter = int(chapter)
    url = xquery_folder + "name_of_chapter.xquery?id=%s&chapter=%s" % (
        document_id,
        chapter,
    )
    the_chapter_name = (
        get(url).text.replace("\\n", "").replace("\\t", "").replace('"', "")
    )
    if the_chapter_name == "null":
        the_chapter_name = "(uden titel)"
    return the_chapter_name


def section_name(xquery_folder, document_id, chapter, section):
    if not section:
        section = 1
    section = int(section)
    url = (
        xquery_folder
        + "name_of_section.xquery?id=%s&chapter=%s&section=%s"
        % (document_id, chapter, section)
    )
    the_section_name = (
        get(url).text.replace("\\n", "").replace("\\t", "").replace('"', "")
    )
    if the_section_name == "null":
        the_section_name = "(uden titel)"
    return the_section_name


def get_chapter(xquery_folder, document_id, chapter, section):
    url = (
        xquery_folder
        + "get_chapter_or_section.xquery?id=%s&chapter=%s&section=%s"
        % (document_id, chapter, section)
    )
    if chapter == 0:
        url = (
            xquery_folder
            + "get_chapter_or_section.xquery?id=%"
            + "s&chapter=%s&frontpage_section=%s"
            % (document_id, chapter, section)
        )
    if isinstance(chapter, str):
        url = url.replace("chapter=", "chapter_name=")
    pages = get(url).text
    return pages


def get_section_info(
    xquery_folder,
    document_id,
    chapter,
    current_section,
    sections,
    sections_of_previous_chapter,
):
    previous_section_name = 0
    next_section_name = 0
    if sections:
        if current_section > 0:
            previous_section_name = section_name(
                xquery_folder, document_id, chapter, current_section - 1
            )
        next_section_name = section_name(
            xquery_folder, document_id, chapter, current_section + 1
        )
    last_section = 0
    last_section_in_previous_chapter = 0
    last_section_in_previous_chapter_name = ""
    if len(sections) > 0:
        last_section = int(sections[-1].get("no"))
    if len(sections_of_previous_chapter) > 0:
        section = sections_of_previous_chapter[-1]
        last_section_in_previous_chapter = int(section.get("no"))
        last_section_in_previous_chapter_name = section.get("section")
    is_last_section = False
    if last_section == current_section:
        is_last_section = True
    section_info = {
        "previous_section_name": previous_section_name,
        "next_section_name": next_section_name,
        "last_section_in_previous_chapter": last_section_in_previous_chapter,
        "last_section_in_previous_chapter_name": last_section_in_previous_chapter_name,  # noqa
        "is_last_section": is_last_section,
    }
    return section_info


def get_chapter_of_string(request, xquery_folder, results, query):
    results_with_chapters = []
    # if not query:
    #    return results_with_chapters
    for result in results:
        document_id = result.get("id")
        xquery = "get_chapter_of_string.xquery?document_id=%s.xml&q=%s" % (
            document_id,
            query,
        )
        chapters_struct = execute_xquery(request, xquery)
        chapters_list = []
        if chapters_struct is not None:
            chapters_list = listify(chapters_struct.get("sections"))
        chapters = [chapter.get("no") for chapter in chapters_list]
        for chapter in chapters:
            result_from_chapter = deepcopy(result)
            result_from_chapter["chapter"] = chapter
            result_from_chapter["id"] = "%s/%s" % (result.get("id"), chapter)
            sections = get_sections(
                xquery_folder, "%s.xml" % document_id, int(chapter)
            )
            sections = [section.get("no") for section in sections]
            if sections:
                xquery = (
                    "get_sections_of_string.xquery?document_id="
                    + "%s.xml&chapter=%s&q=%s"
                    % (document_id, int(chapter), query)
                )
                section_struct = execute_xquery(request, xquery)
                section_list = []
                if section_struct:
                    section_list = listify(section_struct.get("sections"))
                section_list = [
                    int(section.get("no")) for section in section_list
                ]
                for section_no in section_list:
                    result_from_section = deepcopy(result)
                    result_from_section["chapter"] = chapter
                    result_from_section["section"] = section_no
                    result_from_section["id"] = "%s/%s/%s" % (
                        result.get("id"),
                        chapter,
                        section_no,
                    )
                    results_with_chapters.append(result_from_section)
            else:
                results_with_chapters.append(result_from_chapter)
    return results_with_chapters
