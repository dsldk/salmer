xquery version "1.0" encoding "UTF-8";
declare namespace tei = "http://www.tei-c.org/ns/1.0";
declare option exist:serialize "method=json media-type=text/javascript";

let $id	:= request:get-parameter('id','')
let $author := doc(concat("/db/apps/salmer/xml/", $id))/tei:TEI/tei:teiHeader/tei:fileDesc/tei:titleStmt/tei:author/text()
let $comma_space_author := concat(", ", $author)
let $title := doc(concat("/db/apps/salmer/xml/", $id))/tei:TEI/tei:teiHeader/tei:fileDesc/tei:titleStmt/tei:title/text()
return 
    if ($author = 'empty' or empty($author)) then
       <div>{$title}</div>
    else
       (:<div>{$title, $comma_space_author}</div>:)
       <div>{$title}</div>