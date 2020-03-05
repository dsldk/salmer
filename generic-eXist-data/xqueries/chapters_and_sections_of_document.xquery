xquery version "1.0";
declare namespace tei = "http://www.tei-c.org/ns/1.0";
declare option exist:serialize "method=json media-type=text/javascript";


let $document_id	:= request:get-parameter('id','')

return 
	let $xmldoc := doc(concat("/db/apps/brandes/xml/", $document_id))
    let $introduction := for $chapter at $sCount in $xmldoc/tei:TEI/tei:text/tei:front/tei:div
                     return <chapters><no>0</no><name>{$chapter/tei:head[@type="add"]//normalize-space()}</name></chapters>	
	let $chapters := for $chapter at $sCount in $xmldoc/tei:TEI/tei:text/tei:body/tei:div
                      return <chapters><no>{$sCount}</no><name>{$chapter/tei:head[@type="add"]//normalize-space()}</name>
                                
                                    {for $section at $sCount in $chapter/tei:div//tei:head[@type="add"]//normalize-space() 
                                     return <sections><no>{$sCount}</no><name>{$section}</name></sections>}
                                
                            </chapters>                     
	return 
	<results>
	   {$chapters}
	</results>