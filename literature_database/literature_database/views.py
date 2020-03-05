# Copyright (C) 2017-19 Dansk Sprog- og Litteraturselskab.
# 
# This file is part of DSL's website template.
#
# This website template is free software: you can redistribute it
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
from django.shortcuts import render
from django.http import HttpResponse
from literature_data.models import (Person, Publication, Nationality,
        Profession, Note, Genre, Character, Location, LocationType,
        Country, LiteratureSourceAuthor, LiteratureSource, City)
import csv, re
from slugify import slugify

def update_professions(request):
    file_name = "person-database_hovedstrømninger - Ark1.csv"
    file_path = "spreadsheets/" + file_name
    file_to_be_imported = csv.reader(open(file_path), delimiter=',', quotechar='"')
    first_line_text = 'Fornavn/titel'
    profession_dictionary = dict()
    duplicate_names = []
    for line in file_to_be_imported:
        if line[0]:
            name = (line[0], line[1])
            if profession_dictionary.get(name):
                print ("Duplicate name %s" % str(name))
                duplicate_names.append(name)
            else:
                profession_dictionary[name] = line[4]
        #{('Abélard', 'Pierre', '1079-1142'): 'skolastisk teolog'}

    for person in Person.objects.all():
        if not person.description_of_profession:
            if (person.last_name,person.first_name) in duplicate_names:
                #print("Duplicate: " + person.first_name + ' ' + person.last_name + ' maybe ' + profession_dictionary.get((person.last_name,person.first_name)))
                pass
            else:
                profession_from_spreadsheat = profession_dictionary.get((person.last_name, person.first_name))
                if profession_from_spreadsheat:
                    print(person.first_name + ' ' + person.last_name + ': ' + profession_from_spreadsheat)
                    person.description_of_profession = profession_from_spreadsheat
                    person.save()

    person = Person.objects.get(person_id='john-byron-1756-1791')
    person.description_of_profession = "kaptajn, garderofficer"
    person.save()
    person = Person.objects.get(person_id='john-byron')
    person.description_of_profession = "admiral"
    person.save()
    person = Person.objects.get(person_id='elisabeth')
    person.description_of_profession = "kejserinde"
    person.save()
    person = Person.objects.get(person_id='robert-emmet-1720-1802')
    person.description_of_profession = "læge"
    person.save()
    person = Person.objects.get(person_id='robert-emmet')
    person.description_of_profession = "frihedskæmper"
    person.save()
    person = Person.objects.get(person_id='anselm-feuerbach-1775-1833')
    person.description_of_profession = "kriminalist"
    person.save()
    person = Person.objects.get(person_id='anselm-feuerbach')
    person.description_of_profession = "arkæolog"
    person.save()
    person = Person.objects.get(person_id='john-moore')
    person.description_of_profession = "læge og forfatter"
    person.save()
    person = Person.objects.get(person_id='robert-southey')
    person.description_of_profession = "lyriker og forfatter"
    person.save()
    person = Person.objects.get(person_id='wilhelm-1-1781-1864')
    person.description_of_profession = "konge af Württemberg fra 1816"
    person.save()
    person = Person.objects.get(person_id='wilhelm-1')
    person.description_of_profession = "konge af Preussen 1861, kejser af Tyskland fra 1871"
    person.save()
    return HttpResponse("Professions updated")
