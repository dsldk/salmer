# Copyright (C) 2017-19 Dansk Sprog- og Litteraturselskab.
#
# This file is part of the Georg Brandes website.
#
# The Georg Brandes website is free software: you can redistribute it
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
from django.contrib import admin
from .models import (
    Location,
    Person,
    Character,
    Note,
    Publication,
    Nationality,
    Genre,
    Country,
    LocationType,
    LiteratureSource,
    LiteratureSourceAuthor,
    City,
    Variant,
)
from django.contrib.admin.views import main as admin_views_main


types = [
    Person,
    Character,
    Genre,
    Country,
    LocationType,
    LiteratureSource,
    LiteratureSourceAuthor,
    City,
    Nationality,
    Variant,
]


class BrandesAdmin(admin.ModelAdmin):
    exclude = ("profession", "profession_order", "variants", "city")
    list_per_page = 2000


for type in types:
    admin.site.register(type, BrandesAdmin)


class LocationAdmin(admin.ModelAdmin):
    exclude = ("profession", "profession_order", "city")
    list_per_page = 2000


admin.site.register(Location, LocationAdmin)


class NoteAdmin(admin.ModelAdmin):
    readonly_fields = ("id",)
    exclude = ("profession", "note_id")
    list_per_page = 2000


admin.site.register(Note, NoteAdmin)


class PublicationAdmin(admin.ModelAdmin):
    list_per_page = 500
    list_max_show_all = 10000


admin.site.register(Publication, PublicationAdmin)


admin_views_main.MAX_SHOW_ALL_ALLOWED = 10000
