xquery version "1.0" encoding "UTF-8";
declare namespace tei = "http://www.tei-c.org/ns/1.0";
declare option exist:serialize "method=json media-type=text/javascript";

let $authors := distinct-values(collection("/db/apps/salmer/xml")/tei:TEI//tei:author/text()) 

return

<results> {
for $author in $authors
    let $titles := collection("/db/apps/salmer/xml")//tei:titleStmt[tei:author=$author]/tei:title
    order by $author
    return               
        <authors><author>{$author}</author>{
            for $title in $titles order by $title
                return <titles><title>{$title/text()}</title> <id>{util:document-name($title)}</id></titles>
              }</authors>    
    }</results>