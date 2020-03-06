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

from SPARQLWrapper import SPARQLWrapper, JSON
import wikipedia


def wikipedia_text_from_person(birth, death):
    sparql = SPARQLWrapper(
        "https://query.wikidata.org/bigdata/namespace/wdq/sparql"
    )
    sparql.setQuery(
        """
    PREFIX wikibase: <http://wikiba.se/ontology#>
    PREFIX wd: <http://www.wikidata.org/entity/>
    PREFIX wdt: <http://www.wikidata.org/prop/direct/>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX bd: <http://www.bigdata.com/rdf#>
    select ?person ?personLabel ?personDescription ?birth ?death
    WHERE
    {
      ?person wdt:P31 wd:Q5. # instance of human
      ?person wdt:P569 ?birth . # birth date
      ?person wdt:P570 ?death . # death date
      filter (?birth = "1842-02-04"^^xsd:dateTime
       && ?death = "1842-02-04"^^xsd:dateTime) # And between these two dates
    OPTIONAL {
            ?pid rdfs:label ?person filter (lang(?person) = "da") .
    }
    }
    """
    )

    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    for result in results["results"]["bindings"]:
        print(result["person"]["value"])

    sparql.setQuery(
        """PREFIX wd: <http://www.wikidata.org/entity/>
    PREFIX schema: <http://schema.org/>

    SELECT ?url ?p ?o
    WHERE
    {
      ?url schema:about wd:Q316045 .
      FILTER (SUBSTR(str(?url), 1, 25) = "https://da.wikipedia.org/")
    }"""
    )

    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    url = results["results"]["bindings"][0]["url"]["value"]

    wikipedia.set_lang("da")
    page = wikipedia.page(url[30:])

    print("Logo: %s" % page.images[-4])
    print("Beskrivelse: %s" % page.summary)
    import ipdb

    ipdb.set_trace()


wikipedia_text_from_person("1842-02-04", "1842-02-04")
