xquery version "1.0" encoding "UTF-8";
declare namespace tei = "http://www.tei-c.org/ns/1.0";
declare option exist:serialize "method=json media-type=text/javascript";

let $categories := distinct-values(collection("/db/apps/salmer/xml")/tei:TEI//tei:term/text()) 

return

<results> {
for $category in $categories
    order by $category
    return               
        <categories>{$category}</categories>
    }</results>