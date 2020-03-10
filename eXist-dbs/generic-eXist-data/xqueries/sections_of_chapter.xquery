xquery version "1.0";
declare namespace tei = "http://www.tei-c.org/ns/1.0";
declare option exist:serialize "method=json media-type=text/javascript"; 


let $document_id	:= request:get-parameter('id','')
let $chapter_id	    := request:get-parameter('chapter','')

return 
	let $xmldoc := doc(concat("/db/apps/brandes/xml/", $document_id))	                 
	let $chapters := $xmldoc/tei:TEI/tei:text/tei:body/tei:div
	let $chapter := $chapters[xs:integer($chapter_id)]
	return (:<s>{$chapter//tei:head[@type="add"]}</s>:)
	   <sections> {
       for $section at $count in $chapter/tei:div/tei:head
           return <sections><no>{$count}</no><section>{$section//normalize-space()}</section></sections>
           } </sections>