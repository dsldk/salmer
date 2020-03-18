xquery version "1.0" encoding "UTF-8";
declare namespace tei = "http://www.tei-c.org/ns/1.0";
declare option exist:serialize "method=json media-type=text/javascript";

let $author-id := request:get-parameter('author-id', '')

let $titles := collection("/db/apps/salmer/xml")//tei:titleStmt[tei:author/@xml:id=$author-id]/tei:title

(:return <titles>{$titles}</titles>:)
return
<results> {
for $title in distinct-values($titles)
    order by $title
    return               
        <titles 
            id="{util:document-name(collection("/db/apps/salmer/xml")//tei:titleStmt[tei:title/text()=$title])}"
            name="{$title}" />
        
    }</results>
