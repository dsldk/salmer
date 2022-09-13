xquery version "1.0" encoding "UTF-8";
declare namespace tei = "http://www.tei-c.org/ns/1.0";
declare option exist:serialize "method=json media-type=text/javascript";

let $authors := collection("/db/apps/salmer/xml")/tei:TEI//tei:author

return

<results> {
for $author in distinct-values($authors)
    order by $author
    return               
        <authors 
            id="{distinct-values(collection("/db/apps/salmer/xml")/tei:TEI//tei:author[text()=$author]/@xml:id)}"
            name="{$author}" />
        
    }</results>