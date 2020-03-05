# Copyright (C) 2017-20 Dansk Sprog- og Litteraturselskab and Magenta ApS.
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
from django.db import models


def make_list_danish(list_of_strings):
    danish_text = u""
    if len(list_of_strings) > 1:
        first_items = list_of_strings[:-1]
        first_items_as_string = u", ".join(first_items)
        last_item = list_of_strings[-1]
        danish_text = u"%s og %s" % (first_items_as_string, last_item)
    else:
        danish_text = u", ".join(list_of_strings)
    return danish_text


class Profession(models.Model):
    name = models.CharField(
        max_length=255, db_index=True, unique=True, verbose_name="Profession"
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]
        verbose_name = "profession"
        verbose_name_plural = "professioner"


class Nationality(models.Model):
    name = models.CharField(
        max_length=255, db_index=True, unique=True, verbose_name="Nationalitet"
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]
        verbose_name = "nationalitet"
        verbose_name_plural = "nationaliteter"


class Person(models.Model):
    first_name = models.CharField(
        max_length=255,
        blank=True,
        db_index=True,
        verbose_name="Fornavn og evt. mellemnavne",
    )
    last_name = models.CharField(
        max_length=255,
        db_index=True,
        verbose_name="Efternavn (eller fyrstenavn (dvs. f.eks."
        " Alexander den Store))",
    )
    uid = models.CharField(
        max_length=255,
        db_index=True,
        unique=True,
        verbose_name="Unik xml-venlig id. Skriv f.eks. soeren-oegaard, hvis"
        " navnet er Søren Øgård.",
    )
    year_born = models.IntegerField(
        db_index=True, blank=True, null=True, verbose_name="Fødselsår"
    )
    year_born_is_approx = models.BooleanField(
        blank=True, verbose_name="Fødselsåret er omtrentligt"
    )
    year_dead = models.IntegerField(
        db_index=True, blank=True, null=True, verbose_name="Evt. dødsår"
    )
    year_dead_is_approx = models.BooleanField(
        blank=True, verbose_name="Dødsåret er omtrentligt"
    )
    notes_about_life_span = models.CharField(
        max_length=255,
        db_index=True,
        blank=True,
        null=True,
        verbose_name="Alternativ angivelse af leve- el. virketid",
    )
    nationality = models.ForeignKey(
        Nationality, blank=True, null=True, verbose_name="Nationalitet",
        on_delete=models.PROTECT
    )
    secondary_nationality = models.ForeignKey(
        Nationality,
        blank=True,
        null=True,
        related_name="nationality_relation",
        verbose_name='Sekundær Nationalitet. Hvis personen er'
        ' amerikansk-engelsk vælges engelsk i dette felt'
        ' (og amerikansk i feltet "Nationalitet")',
        on_delete=models.PROTECT
    )
    variants = models.TextField(
        blank=True,
        verbose_name="Pseudonymer, tidligere navne eller øgenavne.  Skriv"
        " et pr. linje",
    )
    description_of_profession = models.CharField(
        max_length=255,
        db_index=True,
        blank=True,
        null=True,
        verbose_name='Oplysninger om profession og/eller stand. F.eks.'
        ' "kejserinde af Rusland fra 1730"',
    )
    profession = models.ManyToManyField(
        Profession,
        blank=True,
        verbose_name="Profession og/eller stand. Forfatter",
    )
    profession_order = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Rækkefølge hvis professionerne ikke skal"
        " vises alfabetisk",
    )
    notes = models.TextField(
        blank=True,
        verbose_name="Andre informationer om personen (vises overalt)",
    )
    editorial_notes = models.TextField(
        blank=True,
        verbose_name="Redaktionelle bemærkninger (bliver ikke vist)",
    )

    def __str__(self):
        full_name = self.last_name + ", " + self.first_name
        if full_name.endswith(", ") or full_name.startswith(", "):
            full_name = full_name.replace(", ", "")

        year_born = self.year_born
        if year_born is not None and str(year_born).startswith("-"):
            year_born = str(year_born)[1:] + " f.Kr."

        year_dead = self.year_dead
        if year_dead is not None and str(year_dead).startswith("-"):
            year_dead = str(year_dead)[1:] + " f.Kr."

        if self.year_born_is_approx:
            year_born = "ca. %s" % year_born
        if self.year_dead_is_approx:
            year_dead = "ca. %s" % year_dead

        if not (year_born and year_dead):
            lifespan = " ({})".format(self.notes_about_life_span)
        else:
            lifespan = " ({}-{})".format(year_born, year_dead)
        if year_born and not year_dead:
            lifespan = " (født {})".format(year_born)
        if not year_born and year_dead:
            lifespan = " (død {})".format(year_dead)
        if self.notes_about_life_span:
            lifespan = " (%s)" % self.notes_about_life_span
        if self.year_born is not None and self.year_dead is not None:
            if self.year_born < 0 and self.year_dead > 0:
                lifespan = lifespan[:-1] + " e.Kr)"

        lifespan = lifespan.replace(" (None)", "").replace("()", "")
        full_name += lifespan

        profession = self.description_of_profession
        if self.nationality is not None:
            full_name += ", %s" % self.nationality.name
        elif profession:
            full_name += ", "
        if self.secondary_nationality is not None:
            full_name += "-%s" % self.secondary_nationality.name

        full_name += " %s" % profession
        if self.notes:
            full_name += " (%s)" % self.notes
        full_name += "."
        return full_name

    class Meta:
        ordering = ["last_name", "first_name", "year_born"]
        verbose_name = "person"
        verbose_name_plural = "personer"
        unique_together = (
            ("first_name", "last_name", "year_born", "year_dead"),
        )


class LocationType(models.Model):
    name = models.CharField(
        max_length=255,
        db_index=True,
        unique=True,
        verbose_name="Geografisk kategori",
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]
        verbose_name = "Geografisk kategori"
        verbose_name_plural = "Geografiske kategorier"


class Country(models.Model):
    name = models.CharField(
        max_length=255, db_index=True, verbose_name="Land", unique=True
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]
        verbose_name = "land"
        verbose_name_plural = "lande"


class City(models.Model):
    name = models.CharField(
        max_length=255, db_index=True, verbose_name="navn", unique=True
    )
    country = models.ForeignKey(
        Country, blank=True, null=True, verbose_name="Land", on_delete=models.PROTECT
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]
        verbose_name = "by"
        verbose_name_plural = "byer"


class Location(models.Model):
    name = models.CharField(
        max_length=255, db_index=True, verbose_name="Officielt navn for stedet"
    )
    uid = models.CharField(
        max_length=255,
        db_index=True,
        unique=True,
        null=True,
        verbose_name='Unik xml-venlig id. Skriv f.eks.  koebenhavns-raadhus,'
        ' hvis navnet er "Københavns Rådhus"',
    )
    variants = models.TextField(
        blank=True,
        verbose_name="Evt. alternative stavemåder eller uofficielle navne"
        " for stedet. Skriv et pr. linje",
    )
    location_type = models.ManyToManyField(
        LocationType, blank=True, verbose_name="Kategori",
    )
    city = models.ForeignKey(City, blank=True, null=True, verbose_name="By",
        on_delete=models.PROTECT
    )
    country = models.ManyToManyField(Country, blank=True, verbose_name="Land",)
    notes = models.TextField(blank=True, verbose_name="Noter (vises overalt)")
    editorial_notes = models.TextField(
        blank=True,
        verbose_name="Redaktionelle bemærkninger (bliver ikke vist)",
    )

    def __str__(self):
        country_list = self.country.all()
        location_list = self.location_type.all()
        countries = make_list_danish([c.name for c in country_list])
        categories = make_list_danish([c.name for c in location_list])
        full_title = ""
        if country_list and location_list:
            full_title = "%s, %s i %s" % (self.name, categories, countries)
        elif location_list:
            full_title = "%s, %s" % (self.name, categories)
        elif country_list:
            full_title = "%s, %s" % (self.name, countries)
        else:
            full_title = self.name

        notes = self.notes
        if notes:
            notes = " (%s)" % notes
        full_title += notes
        full_title += "."
        return full_title

    class Meta:
        ordering = ["name"]
        verbose_name = "sted"
        verbose_name_plural = "steder"


class Genre(models.Model):
    name = models.CharField(
        max_length=255, db_index=True, unique=True, verbose_name="Genre"
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]
        verbose_name = "genre"
        verbose_name_plural = "genrer"


class Publication(models.Model):
    author = models.ManyToManyField(
        Person,
        blank=True,
        # limit_choices_to = {'profession__name': 'forfatter'},
        verbose_name="Forfatter(e)",
    )
    title = models.CharField(
        max_length=255,
        db_index=True,
        blank=True,
        verbose_name="Titel (på originalsproget)",
    )
    danish_title = models.CharField(
        max_length=255, db_index=True, blank=True, verbose_name="Dansk titel"
    )
    uid = models.CharField(
        max_length=255,
        db_index=True,
        unique=True,
        null=True,
        verbose_name="Unik xml-venlig id. Skriv f.eks. "
        "heiberg-en-sjael-efter-doeden",
    )
    part_of = models.CharField(
        max_length=255,
        db_index=True,
        blank=True,
        verbose_name="Trykt/indgår i",
    )
    year_first_published = models.IntegerField(
        db_index=True,
        blank=True,
        null=True,
        verbose_name="Originalens udgivelsesår",
    )
    notes_about_publishing_years = models.CharField(
        max_length=255,
        db_index=True,
        blank=True,
        verbose_name="Noter om udgivelsesår (Hvis værket er udgivet over en"
        " årrække eller hvis der er andre udgivelser)",
    )
    variants = models.TextField(
        blank=True, verbose_name="Alternative titler. Skriv en pr. linje"
    )
    genre = models.ManyToManyField(Genre, blank=True, verbose_name="genre(r)")
    notes = models.TextField(
        blank=True, verbose_name="Andre informationer om værket (vises altid)"
    )
    editorial_notes = models.TextField(
        blank=True,
        verbose_name="Redaktionelle bemærkninger (bliver ikke vist)",
    )

    class Meta:
        ordering = [
            "author__last_name",
            "author__first_name",
            "title",
            "year_first_published",
        ]
        verbose_name = "værk"
        verbose_name_plural = "værker"
        # unique_together = (
        #  ("author__lastname", "title","year_first_published"),
        # )

    def __str__(self, first_name_of_author_first=False):
        authors = self.author.values()
        genre = make_list_danish([genre.name for genre in self.genre.all()])
        if genre:
            genre = ", %s" % genre
        part_of = self.part_of
        if part_of:
            part_of = ", %s" % part_of
        publication_year = self.year_first_published
        if publication_year:
            if publication_year is not None and str(
                publication_year
            ).startswith("-"):
                publication_year = str(publication_year)[1:] + " f.Kr."
            publication_year = ", %s" % (publication_year)
        elif self.notes_about_publishing_years:
            publication_year = ", %s" % (self.notes_about_publishing_years)
        else:
            publication_year = ""

        full_author_names = []

        for author in authors:
            if first_name_of_author_first:
                full_name = author["first_name"] + " " + author["last_name"]
            else:
                full_name = author["last_name"] + ", " + author["first_name"]
            if full_name.endswith(", "):
                full_name = full_name[:-2]
            full_author_names.append(full_name)

        full_author_names = ", ".join(full_author_names).strip()
        if full_author_names == "":
            full_author_names = "(ingen forfatter)"
        title = self.title
        if not title:
            title = self.danish_title

        called_from_character_view = first_name_of_author_first
        notes = ""
        if not called_from_character_view:
            notes = self.notes
            if notes and not called_from_character_view:
                notes = " (%s)" % notes

        full_title = "%s: %s%s%s%s%s" % (
            full_author_names,
            title,
            part_of,
            genre,
            publication_year,
            notes,
        )
        if not called_from_character_view:
            full_title += "."
        if len(full_title) > 250:
            full_title = full_title[:250] + "..."

        return full_title


class Character(models.Model):
    name = models.CharField(
        max_length=255,
        db_index=True,
        verbose_name="fornavn og evt. mellemnavne",
    )
    uid = models.CharField(
        max_length=255,
        db_index=True,
        unique=True,
        verbose_name="Unik xml-venlig id. Skriv f.eks.  soeren-oegaard,"
        " hvis navnet er Søren Øgård",
    )
    variants = models.TextField(
        blank=True,
        verbose_name="Pseudonymer, tidligere navne eller"
        " øgenavne. Skriv et pr. linje",
    )
    publication = models.ForeignKey(
        Publication, blank=True, null=True, verbose_name="Værk",
        on_delete=models.PROTECT,
    )
    notes = models.TextField(
        blank=True, verbose_name="Noter om personen (vises overalt)"
    )
    editorial_notes = models.TextField(
        blank=True,
        verbose_name="Redaktionelle bemærkninger (bliver ikke vist)",
    )

    class Meta:
        ordering = ["name"]
        verbose_name = "litterær figur"
        verbose_name_plural = "litterære figurer"
        # unique_together = (("name","publication.title"),)

    def __str__(self):
        publication = ""
        name_of_character = "%s" % (self.name)
        if self.publication is not None:
            publication = " (%s)" % (
                self.publication.__str__(first_name_of_author_first=True)
            )
        full_title = name_of_character + publication
        full_title += "."
        return full_title


class LiteratureSourceAuthor(models.Model):
    first_name = models.CharField(
        max_length=255,
        blank=True,
        db_index=True,
        verbose_name="Fornavn og evt. mellemnavne",
    )
    last_name = models.CharField(
        max_length=255, blank=True, db_index=True, verbose_name="Efternavn"
    )

    def __str__(self):
        full_name = self.last_name + ", " + self.first_name
        if full_name.endswith(", ") or full_name.startswith(", "):
            full_name = full_name.replace(", ", "")
        return full_name

    class Meta:
        ordering = ["last_name"]
        verbose_name = "forfattere af sekundærlitteratur"
        verbose_name_plural = "forfatter af sekundærlitteratur"
        # unique_together = (("first_name", "last_name"),)


class LiteratureSource(models.Model):
    author = models.ManyToManyField(
        LiteratureSourceAuthor, blank=True, verbose_name="Hovedforfatter"
    )
    other_authors = models.CharField(
        max_length=255,
        db_index=True,
        blank=True,
        verbose_name="Evt. andre forfattere",
    )
    title = models.CharField(
        max_length=255, db_index=True, blank=True, verbose_name="Titel"
    )
    publication_id = models.CharField(
        max_length=255,
        db_index=True,
        unique=True,
        null=True,
        verbose_name="Unik xml-venlig id. Skriv"
        " f.eks. heiberg-en-sjael-efter-doeden",
    )
    editors = models.CharField(
        max_length=255, db_index=True, blank=True, verbose_name="Redaktører"
    )
    anthology = models.CharField(
        max_length=255,
        db_index=True,
        blank=True,
        verbose_name="Del af antologien:",
    )
    journal = models.CharField(
        max_length=255,
        db_index=True,
        blank=True,
        verbose_name="Indgår i denne avis, tidsskrift eller bogserie",
    )
    location_of_publication = models.ManyToManyField(
        City, db_index=True, blank=True, verbose_name="Udgivelsessted (by)"
    )
    publication_year = models.IntegerField(
        db_index=True, blank=True, null=True, verbose_name="Udgivelsesår"
    )
    publication_end_year = models.IntegerField(
        db_index=True,
        blank=True,
        null=True,
        verbose_name="Sidste udgivelsesår, i tilfælde af at publikationen"
        " er udgivet over en årrække",
    )
    publication_is_still_being_published = models.BooleanField(
        blank=True, verbose_name="Værket er fortsat under udgivelse"
    )
    pages = models.CharField(
        max_length=255,
        db_index=True,
        blank=True,
        verbose_name="Sideinterval f.eks. 155-161",
    )
    notes = models.TextField(
        blank=True,
        verbose_name="Andre informationer om værket (vises overalt)",
    )
    editorial_notes = models.TextField(
        blank=True,
        verbose_name="Redaktionelle bemærkninger (bliver ikke vist)",
    )

    class Meta:
        ordering = ["author__last_name"]
        verbose_name = "litteratur"
        verbose_name_plural = "litteratur"
        # unique_together = (("title", "year_first_published"),)

    def __str__(self):
        authors = self.author.values()
        full_author_names = [
            author["first_name"] + " " + author["last_name"]
            for author in authors
        ]
        full_author_names = ", ".join(full_author_names).strip()
        if full_author_names == "":
            full_author_names = "(uden forfatter)"
        title = self.title
        if not title:
            title = self.danish_title
        publication_year_end = ""
        if self.publication_end_year:
            publication_year_end = "-%s" % self.publication_end_year
        if self.publication_is_still_being_published:
            publication_year_end = "-"
        publication_year_text = ", %s%s" % (
            self.publication_year,
            publication_year_end,
        )
        editors = self.editors
        if self.editors:
            editors = ", %s (red.)" % editors
        anthology = self.anthology
        if self.anthology:
            anthology = ", %s" % anthology
        journal = self.journal
        if self.journal:
            journal = ", %s" % journal
        pages = self.pages
        if self.pages:
            pages = ", %s" % pages
        notes = self.notes
        if notes:
            notes = " (%s)" % notes
        return "%s: %s%s%s%s%s%s%s." % (
            full_author_names,
            title,
            editors,
            anthology,
            journal,
            publication_year_text,
            pages,
            notes,
        )


class Note(models.Model):
    volume = models.PositiveIntegerField(
        db_index=True, blank=True, null=True, verbose_name="Bind"
    )
    page = models.PositiveIntegerField(
        db_index=True, blank=True, null=True, verbose_name="Side"
    )
    line = models.PositiveIntegerField(
        db_index=True, blank=True, null=True, verbose_name="Linje"
    )
    note_letter = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Hvis der er flere noter på en linje, indtastes"
        " her et bogstav, typisk 'b' eller 'c' eller 'd' osv.",
    )
    note_id = models.CharField(
        max_length=255,
        db_index=True,
        null=True,
        verbose_name="Unik xml-venlig id. Indtast f.eks."
        " h-bind-1-side-4-linje-12-b hvis det er anden note i "
        "Hovedstrømninger bind 1, side 4, linje 12.",
    )
    lemma = models.CharField(max_length=1023, blank=True, verbose_name="Lemma")
    text = models.TextField(
        blank=True, verbose_name="Notetekst (vises overalt)"
    )
    literature_reference = models.ForeignKey(
        LiteratureSource,
        blank=True,
        null=True,
        verbose_name="Litteraturhenvisning",
        on_delete=models.PROTECT
    )
    link_text = models.CharField(
        max_length=1023,
        blank=True,
        verbose_name='Linktekst, f.eks. "Heinse 1787:5-6"',
    )
    editorial_notes = models.TextField(
        blank=True,
        verbose_name="Redaktionelle bemærkninger om noten (bliver ikke vist)",
    )

    class Meta:
        ordering = ["volume", "page", "line"]
        verbose_name = "note"
        verbose_name_plural = "noter"

    def __str__(self):
        volume_text = "bind %s" % self.volume
        if self.volume is None:
            volume_text = "(bind ikke angivet)"
        page_text = ""
        line_text = ""
        link_text = ""
        note_letter = ""
        if self.page is not None:
            page_text = ", side %s" % self.page
        if self.line is not None:
            line_text = ", linje %s" % self.line
        if self.link_text:
            link_text = "(%s)" % self.link_text
        if self.note_letter:
            note_letter = ", %s" % self.note_letter

        title = "%s%s%s%s (id=%s): %s] %s %s" % (
            volume_text,
            page_text,
            line_text,
            note_letter,
            self.id,
            self.lemma,
            self.text,
            link_text,
        )
        title = title.strip()
        if not title.endswith("."):
            title = title + "."
        return title


REVISION = "REVISION"
ADDITION = "ADDITION"
OMISSION = "OMISSION"
variant_type_choices = (
    (REVISION, "omarbejdelse"),
    (ADDITION, "tilføjelse"),
    (OMISSION, "udeladelse"),
)


class Variant(models.Model):

    variant_id = models.CharField(  # From the "<div id=.../>".
        max_length=255,
        db_index=True,
        null=True,
        verbose_name="Unik xml-venlig id. Gerne kombination"
        " af værk og tal, f.eks. 'hs1_001'",
    )

    variant_type = models.CharField(  # From the "<h1>...</h1>".
        max_length=128,
        verbose_name="type",
        choices=variant_type_choices,
        default=REVISION
    )
    variant_description = models.CharField(  # From the <h2.../> part.
        max_length=1024,
        db_index=True,
        null=True,
        verbose_name="Beskrivelse"
    )

    variant_text = models.TextField(  # Remainder of "<div>".
        blank=True, verbose_name="Variant-tekst"
    )
    
    class Meta:
        ordering = ["variant_id",]
        verbose_name = "variant"
        verbose_name_plural = "varianter"

    def __str__(self):
        return "{} - {} - {}".format(
            self.variant_id, self.variant_type, self.variant_description
        )
