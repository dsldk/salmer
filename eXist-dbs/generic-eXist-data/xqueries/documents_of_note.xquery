xquery version "1.0";
declare namespace tei="http://www.tei-c.org/ns/1.0";
declare option exist:serialize "method=json media-type=text/javascript"; 

let $note_id    := request:get-parameter('note_id','')
let $note_type  := request:get-parameter('note_type','')
let $xmldocs := collection("/db/apps/brandes/xml/")

let $r := for $document in $xmldocs
    let $notes := if ($note_type = "personer") then ($document//tei:persName[@key=$note_id]) else (if ($note_type = 'vaerker') then ($document//tei:bibl[@n=$note_id]) else (if ($note_type = "steder") then ($document//tei:placeName[@key=$note_id]) else ($document//tei:persName[@key=$note_id  and @type="fictional"])))

    for $note in $notes
        let $line_nos :=  $note/preceding::tei:pb[1]/string(@n)                 
        return <results>
   {$document//tei:teiHeader//tei:title/text()}#s. {$line_nos}#{util:document-name($document)}            
            </results>
        return <r>
        {$r}
        </r>
