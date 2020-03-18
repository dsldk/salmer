xquery version "1.0" encoding "UTF-8";
declare namespace tei = "http://www.tei-c.org/ns/1.0";
declare option exist:serialize "method=xhtml media-type=text/html";
<html>
    <body>
        <div>
            <ul>{
                    for $file in collection("/db/apps/salmer/xml")/tei:TEI
                    order by $file//tei:titleStmt/tei:title[1]
                    return 
                    <li>{util:document-name($file)}
                    <ul>{
                    for $part in $file/tei:text/(tei:front|tei:body|tei:back)
                    return <li>{$part//tei:head}</li>
                    }</ul>
                    </li>
                }</ul>
        </div>
    </body>
</html>