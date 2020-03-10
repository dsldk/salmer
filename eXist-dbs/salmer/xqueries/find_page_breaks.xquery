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
let $chapter_name := request:get-parameter('chapter_name','')

return
	let $xmldoc := doc(concat("/db/apps/salmer/xml/", $query))
	let $pbs := 
	   if ($chapter_name = 'titelblad')
       then $xmldoc//tei:front/tei:titlePage//tei:pb
       else if ($chapter_name = 'forord')                
       then $xmldoc//tei:front/tei:div[@type="preface"]//tei:pb
       else if ($chapter_name = 'dedikation')
       then $xmldoc//tei:front/tei:div[@type="dedication"]//tei:pb
       else if ($chapter_name = 'motto')
       then $xmldoc//tei:front/tei:epigraph//tei:pb
	   else if ($section = 0) then		
	      $xmldoc/tei:TEI/tei:text/tei:body/tei:div[$chapter]//tei:pb	 
	   else
	      $xmldoc/tei:TEI/tei:text/tei:body/tei:div[$chapter]//tei:div[$section]//tei:pb
	      
	return <pbs>{for $pb in $pbs return <page_no>{$pb/@n}</page_no>}</pbs>
	 
	 
