xquery version "1.0";
declare namespace tei = "http://www.tei-c.org/ns/1.0";
declare option exist:serialize "method=json media-type=text/javascript";


let $document_id	:= request:get-parameter('id','')

return 
	let $xmldoc := doc(concat("/db/apps/salmer/xml/", $document_id))
 let $frontmatter := if ($xmldoc/tei:TEI//tei:front/tei:div)
                      then <chapters><name>Redaktionelt</name><no>front</no> {for $section at $sCount in $xmldoc/tei:TEI//tei:front/tei:div
         return <sections><no>{$sCount}</no><name>{$section/tei:head[@type="add"]//normalize-space()}</name></sections>}</chapters>
         else ""
	let $chapters := for $chapter at $sCount in $xmldoc/tei:TEI/tei:text/tei:body/tei:div
                      return <chapters><no>{$sCount}</no><name>{$chapter/tei:head[@type="add"]//normalize-space()}</name>
                                
                                    {for $section at $sCount in $chapter/tei:div//tei:head[@type="add"]//normalize-space() 
                                     return <sections><no>{$sCount}</no><name>{$section}</name></sections>}
                                
                            </chapters>                     
 let $backmatter := if ($xmldoc/tei:TEI//tei:back/tei:div)
                      then <chapters><name>Appendiks</name><no>back</no> {for $section at $sCount in $xmldoc/tei:TEI//tei:back/tei:div
         return <sections><no>{$sCount}</no><name>{$section/tei:head[@type="add"]//normalize-space()}</name></sections>}</chapters>
         else ""
    return 
    <results>
       {$frontmatter}
       {$chapters}
       {$backmatter}

    </results>
