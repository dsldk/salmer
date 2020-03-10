xquery version "1.0";
declare namespace tei = "http://www.tei-c.org/ns/1.0";
declare option exist:serialize "method=json media-type=text/javascript";


let $document_id	:= request:get-parameter('id','')

return 
	let $xmldoc := doc(concat("/db/apps/brandes/xml/", $document_id))
	let $source := $xmldoc/tei:TEI/tei:teiHeader/tei:fileDesc/tei:sourceDesc/tei:listWit/tei:witness/tei:msDesc/tei:msIdentifier
	let $manuscript_id := $source/tei:idno
	let $library := $source/tei:repository
	let $city := $source/tei:settlement
	let $metadata := $xmldoc/tei:TEI/tei:teiHeader/tei:fileDesc/tei:titleStmt
	let $title := $metadata/tei:title 
	let $author := $metadata/tei:author
    let $application := $xmldoc/tei:TEI/tei:teiHeader/tei:encodingDesc/tei:appInfo/tei:application
	return 
	<results>
	{$author}{$title}{$manuscript_id}{$library}{$city}{$application}           
	 </results>