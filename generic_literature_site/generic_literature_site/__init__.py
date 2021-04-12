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
from pyramid.config import Configurator
import django


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)
    facsimile_dir = settings["facsimiles"]
    config.include("pyramid_chameleon")
    config.add_static_view(
        name="static/facsimiles", path=facsimile_dir, cache_max_age=3600
    )
    config.add_static_view("static", "static", cache_max_age=3600)
    config.add_route("index_view", "/")
    config.add_route("textlist_view", "/texts")
    config.add_route("search_results", "/search")
    # config.add_route("advanced_search_view", "/advanced-search")
    config.add_route("about_site_view", "/about")
    config.add_route("instructions_view", "/instructions")
    config.add_route("meta_view", "/meta/{document}/{type}")
    config.add_route("register_view", "/register/{type}/{first_letter}")
    config.add_route("guidelines_view", "/guidelines")
    config.add_route(
        "research_page_view",
        "/research/{page:.*?}.{extension:(?i)(html|pdf|jpg|jpeg|"
        + "gif|png|webp)$}",
    )
    config.add_route("research_view", "/research")
    config.add_route("english_view", "/english")
    config.add_route("danish_view", "/danish")
    config.add_route("data_view", "/data")
    config.add_route("go_popup", "/go_popup")
    config.add_route("about_view", "/{document}/about")
    config.add_route("front_page_view", "/front-page")
    config.add_route(
        "section_view_notes", "/notes/{document}/{chapter}/{section}"
    )
    config.add_route("chapter_view_notes", "/notes/{document}/{chapter}")
    config.add_route("document_view_notes", "/notes/{document}")
    config.add_route(
        "section_view_text", "/text/{document}/{chapter}/{section}"
    )
    config.add_route("facsimiles", "/{document}/facsimile_info")
    config.add_route("chapter_view_text", "/text/{document}/{chapter}")
    config.add_route("document_view_text", "/text/{document}")
    config.add_route("section_view", "/{document}/{chapter}/{section}")
    config.add_route("chapter_view", "/{document}/{chapter}")
    config.add_route("document_view", "/{document}")
    config.add_translation_dirs("generic_literature_site:locale")

    config.scan()
    while True:
        try:
            django.setup()
            break
        except Exception:
            pass

    return config.make_wsgi_app()
