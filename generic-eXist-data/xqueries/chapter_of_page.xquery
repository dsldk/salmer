xquery version "1.0";
declare namespace tei = "http://www.tei-c.org/ns/1.0";
declare namespace fn="http://www.w3.org/2005/xpath-functions";
declare option exist:serialize "method=json media-type=text/javascript";



let $document_id	:= request:get-parameter('id','')
let $page	:= request:get-parameter('page','')

return 
	let $xmldoc := doc(concat("/db/apps/brandes/xml/", $document_id))
    let $introduction := for $chapter at $sCount in $xmldoc/tei:TEI/tei:text/tei:front/tei:div
                     return <chapters><no>0</no><name>{$chapter/tei:head[@type="add"]//normalize-space()}</name></chapters>	
	let $hits := for $chapter at $cCount in $xmldoc/tei:TEI/tei:text/tei:body/tei:div
	                 let $sections := $chapter/tei:div[child::tei:head[@type="add"]]
                            for $section at $sCount in (if($sections) then $sections else $chapter)
                             let $page_breaks := $section//tei:pb
                             for $page_break in $page_breaks
                                 return if ($page_break/string(@n) = $page) then
                                     <results><chapter>{$cCount}</chapter>
                                     {(if($sections) then <section>{$sCount}</section> else "")}
                                     <page>{$page_break/string(@n)}</page></results>
                                 else ""
                                                                                    
	return 
	<results>
	   {$hits}
	</results>
