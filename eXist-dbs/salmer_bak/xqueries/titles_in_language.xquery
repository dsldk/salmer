xquery version "1.0" encoding "UTF-8";
declare namespace tei = "http://www.tei-c.org/ns/1.0";
declare option exist:serialize "method=json media-type=text/javascript";

let $language-id := request:get-parameter('language-id', '')

let $titles := (collection("/db/apps/salmer/xml")/tei:TEI//tei:teiHeader[tei:profileDesc//tei:language/@ident=$language-id]//tei:title)

(:return <titles>{$titles}</titles>:)
return
<results> {
for $title in $titles
    order by $title
    return  
    <titles 
            id="{util:document-name($title)}"
            name="{$title}" />      
    }</results>
(:<!--<titles 
            id="{util:document-name(collection("/db/apps/salmer/xml")//tei:titleStmt[tei:title/@xml:id=$title/@xml:id])}"
            name="{$title}" />-->:)
        (:id="{util:document-name(collection("/db/apps/salmer/xml")/tei:TEI//tei:titleStmt[tei:title=$title])}":)
        (:id="{util:document-name(collection("/db/apps/salmer/xml")/tei:TEI//tei:titleStmt[tei:title=$title])}":)