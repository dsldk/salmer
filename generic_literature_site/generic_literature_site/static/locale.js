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
      'Georg Brandes\' note': 'Georg Brandes\' note',
      'Faksimile': 'Facsimile',
			'Vælg sprog': 'Choose language',
			'Vælg supplerende tekst': 'Choose supplementary text',
			'Tekstredegørelse': 'Text account',
			'Indledning': 'Introduction',
			'Kolofon': 'Colophon',
			'Tekstvidner': 'Sources',
      'Der skete en fejl. Teksten kunne ikke indlæses.': 'An error occured. The text could not be loaded',
      'Der skete en fejl. Kommentarer kunne ikke indlæses.': 'An error occured. Notes could not be loaded'
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
      'Georg Brandes\' note': 'Georg Brandes\' note',
      'Faksimile': 'Faksimile',
			'Vælg sprog': 'Vælg sprog',
			'Vælg supplerende tekst': 'Vælg supplerende tekst',
			'Tekstredegørelse': 'Tekstredegørelse',
			'Indledning': 'Indledning',
			'Kolofon': 'Kolofon',
			'Tekstvidner': 'Tekstvidner',
      'Der skete en fejl. Teksten kunne ikke indlæses.': 'Der skete en fejl. Teksten kunne ikke indlæses',
      'Der skete en fejl. Kommentarer kunne ikke indlæses.': 'Der skete en fejl. Kommentarer kunne ikke indlæses.'
    }
  })
}
