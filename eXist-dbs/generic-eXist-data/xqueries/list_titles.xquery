xquery version "1.0" encoding "UTF-8";
declare namespace tei = "http://www.tei-c.org/ns/1.0";
declare option exist:serialize "method=json media-type=text/javascript";



<results> {
for $opslag in collection("/db/apps/brandes/xml")/tei:TEI          
    let $path := util:document-name($opslag)
    order by $opslag//tei:title
    return    
    <result> 
        <path>{$path}</path>
        <id>{$opslag//tei:title/text()} <!--({$opslag//tei:sourceDesc//tei:idno/text()})--></id>
    </result>
    }</results>