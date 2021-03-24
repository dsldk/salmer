var loc = document.cookie.replace(/(?:(?:^|.*;\s*)_LOCALE_\s*\=\s*([^;]*).*$)|^.*$/, "$1") || 'da';
var __ = {
  en: i18n.create({
    values: {
      'Note': 'Note',
      'Kommentar': 'Notes',
      'Tekstkritik': 'Textual criticism',
      'Person': 'Person',
      'Litterær figur': 'Literary figure',
      'Værk': 'Work',
      'Sted': 'Place',
      'Forfatterens note': 'Author\'s note',
      'Faksimile': 'Facsimile',
      'Faksimile af side': 'Facsimile for page',
      'Se en stor udgave af': 'See a large version of',
      'Faksimilen': 'Facsimile',
      'kunne ikke findes': 'was not found',
			'Vælg sprog': 'Choose language',
			'Vælg supplerende tekst': 'Choose supplementary text',
			'Tekstredegørelse': 'Text account',
			'Indledning': 'Introduction',
			'Kolofon': 'Colophon',
			'Tekstvidner': 'Sources',
      'Der skete en fejl. Teksten kunne ikke indlæses.': 'An error occured. The text could not be loaded',
      'Der skete en fejl. Kommentarer kunne ikke indlæses.': 'An error occured. Notes could not be loaded',
      'Bladr til forrige faksimile': 'Show previous facsimile',
      'Bladr til næste faksimile': 'Show next facsimile'
    }
  }),
  da: i18n.create({
    values: {
      'Note': 'Note',
      'Kommentar': 'Kommentar',
      'Tekstkritik': 'Tekstkritik',
      'Person': 'Person',
      'Litterær figur': 'Litterær figur',
      'Værk': 'Værk',
      'Sted': 'Sted',
      'Forfatterens note': 'Forfatterens note',
      'Faksimile': 'Faksimile',
      'Faksimile af side': 'Faksimile af side',
      'Se en stor udgave af': 'Se en stor udgave af',
      'Faksimilen': 'Faksimilen',
      'kunne ikke findes': 'kunne ikke findes',
			'Vælg sprog': 'Vælg sprog',
			'Vælg supplerende tekst': 'Vælg supplerende tekst',
			'Tekstredegørelse': 'Tekstredegørelse',
			'Indledning': 'Indledning',
			'Kolofon': 'Kolofon',
			'Tekstvidner': 'Tekstvidner',
      'Der skete en fejl. Teksten kunne ikke indlæses.': 'Der skete en fejl. Teksten kunne ikke indlæses',
      'Der skete en fejl. Kommentarer kunne ikke indlæses.': 'Der skete en fejl. Kommentarer kunne ikke indlæses.',
      'Bladr til forrige faksimile': 'Bladr til forrige faksimile',
      'Bladr til næste faksimile': 'Bladr til næste faksimile'
    }
  })
}
