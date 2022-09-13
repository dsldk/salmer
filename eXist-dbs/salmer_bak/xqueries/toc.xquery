xquery version "1.0" encoding "UTF-8";
declare namespace tei = "http://www.tei-c.org/ns/1.0";
declare option exist:serialize "method=xhtml media-type=text/html";
<html>
    <body>
        <div>
            <ul>{
                    for $opslag in collection("/db/apps/salmer/xml")/tei:TEI
                    let $path := util:document-name($opslag)
                    let $title := $opslag//tei:titleStmt/tei:title[1]
                        
                        order by $opslag//tei:titleStmt/tei:title[1]
                    
                    return
                        
                        <li>{$path},
                            {$title}
                            <ul>{
                                    let $divs := $opslag//tei:div
                                    for $div in $divs
                                    return
                                        <li>{$div/tei:head[1]}
                                        <ul>{
                                        let $chapters := $div/tei:div
                                        for $chapter in $chapters
                                        return <li>{$chapter/tei:head[1]}</li>
                                        
                                        }</ul>
                                        
                                        
                                        </li>
                                
                                }</ul>
                        </li>
                
                }</ul>
        </div>
    </body>
</html>