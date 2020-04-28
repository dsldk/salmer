xquery version "1.0" encoding "UTF-8";
declare namespace tei = "http://www.tei-c.org/ns/1.0";
declare option exist:serialize "method=json media-type=text/javascript";

let $id	:= request:get-parameter('id','')
let $author := doc(concat("/db/apps/salmer/xml/", $id))/tei:TEI/tei:teiHeader/tei:fileDesc//tei:author/text()
return 
    if ($author = 'empty' or empty($author)) then
       <div></div>
    else
       <div>af {$author}</div>