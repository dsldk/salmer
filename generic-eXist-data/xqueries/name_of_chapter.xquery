xquery version "1.0";

import module namespace request="http://exist-db.org/xquery/request";
import module namespace transform="http://exist-db.org/xquery/transform";
import module namespace ft="http://exist-db.org/xquery/lucene";
declare namespace tei = "http://www.tei-c.org/ns/1.0";

declare namespace exist="http://exist.sourceforge.net/NS/exist";
declare option exist:serialize "method=json media-type=text/javascript";

let $query	:= "test"
let $query	:= request:get-parameter('id','')
let $chapter := xs:integer(request:get-parameter('chapter',''))	

return
	let $xmldoc := doc(concat("/db/apps/brandes/xml/", $query))
	let $chapter := $xmldoc/tei:TEI/tei:text/tei:body/tei:div[$chapter]/tei:head[1]
	return 
	<results> {
	   $chapter/text()
	   }</results>