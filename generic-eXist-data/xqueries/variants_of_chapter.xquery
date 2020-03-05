xquery version "1.0";
declare namespace tei = "http://www.tei-c.org/ns/1.0";
declare option exist:serialize "method=json media-type=text/javascript";
let $query	:= request:get-parameter('id','')
let $chapter := xs:integer(request:get-parameter('chapter','0'))
let $section := xs:integer(request:get-parameter('section','0'))
let $xmldoc := doc(concat("/db/apps/brandes/xml/", $query))

let $notes := if ($chapter !=0 and $section != 0) then            
                  $xmldoc//tei:body/tei:div[$chapter]/tei:div[$section]//tei:ref[@type='variant']
              else if ($chapter !=0) then
                  $xmldoc//tei:body/tei:div[$chapter]//tei:ref[@type='variant']
              else $xmldoc//tei:body//tei:ref[@type='variant']
return
    <results>
	   {$notes}
	</results>
