xquery version "1.0";
declare namespace tei = "http://www.tei-c.org/ns/1.0";
declare option exist:serialize "method=json media-type=text/javascript";


let $document_id	:= request:get-parameter('id','')

return 
	let $xmldoc := doc(concat("/db/apps/salmer/xml/", $document_id))
	return 
	<results> {
        for $section at $sCount in $xmldoc/tei:TEI/tei:text/tei:body/tei:div
            return <sections><no>{$sCount}</no><name>{$section/tei:head[@type="add"]//normalize-space()}</name></sections>
            
	 }</results>