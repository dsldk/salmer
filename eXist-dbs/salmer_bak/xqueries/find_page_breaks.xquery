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
let $section := xs:integer(request:get-parameter('section','0'))

return
	let $xmldoc := doc(concat("/db/apps/salmer/xml/", $query))
	return if ($section = 0) then		
	   let $pbs := $xmldoc/tei:TEI/tei:text/tei:body/tei:div[$chapter]//tei:pb
	   return <pbs> {for $pb in $pbs return <page_no>{$pb/@n}{$pb/@ana}</page_no>   } </pbs>
	 
	 else
	 let $pbs := $xmldoc/tei:TEI/tei:text/tei:body/tei:div[$chapter]/tei:div[$section]//tei:pb
	   return <pbs> {for $pb in $pbs return <page_no>{$pb/@n}{$pb/@ana}</page_no> } </pbs>
	 
	 