xquery version "1.0" encoding "UTF-8";
declare namespace tei = "http://www.tei-c.org/ns/1.0";
declare namespace xs="http://www.w3.org/2001/XMLSchema";
declare option exist:serialize "method=json media-type=text/javascript"; 

declare function local:idAndTitle($document_identifiers, $idno) 
{
<manuscript>
    <idno>{$idno} ({distinct-values($document_identifiers[tei:idno=$idno]/ancestor::tei:teiHeader/tei:profileDesc//tei:date/string())})</idno>
          {
            for $title in distinct-values($document_identifiers[tei:idno=$idno]/../../../../..//tei:title)
               let $id  := util:document-name($title)
               order by $title
               return <title>{$title}</title>
          }
     
</manuscript>
};

declare function local:manuscripts($document_identifiers, $place, $library)
{
<manuscripts_for_place> 
            <location>{$place}, {$library}</location>
            <manuscripts>{for $idno in distinct-values($document_identifiers[tei:repository=$library]/tei:idno)
                return local:idAndTitle($document_identifiers,$idno)
                }
            </manuscripts>
            </manuscripts_for_place>
};


let $document_identifiers := collection("/db/apps/brandes/xml")/tei:TEI//tei:msIdentifier
return 
<results> {
for $place in  distinct-values($document_identifiers/tei:settlement)
    order by $place
    return               
        for $library in distinct-values($document_identifiers[tei:settlement=$place]/tei:repository)        
          order by $library
          return local:manuscripts($document_identifiers,$place,$library)
                                    
    }</results>