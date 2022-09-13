xquery version "1.0" encoding "UTF-8";
declare namespace tei = "http://www.tei-c.org/ns/1.0";
declare option exist:serialize "method=json media-type=text/javascript";

let $languages := collection("/db/apps/salmer/xml")/tei:TEI//tei:language/@ident 

return

<results> {
for $language in distinct-values($languages)
    order by $language
    return
        <languages>{$language}</languages>
    }</results>