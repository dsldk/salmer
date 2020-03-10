xquery version "1.0";
declare namespace tei="http://www.tei-c.org/ns/1.0";
declare namespace exist="http://exist.sourceforge.net/NS/exist";
declare namespace request="http://exist-db.org/xquery/request";
declare namespace ft="http://exist-db.org/xquery/lucene";
import module namespace kwic="http://exist-db.org/xquery/kwic";
let $q := request:get-parameter('q', '')
let $documents := collection("/db/apps/salmer/xml")/tei:TEI


let $results :=  
    for $doc in $documents return
        for $chapter at $chapter_no in $doc//tei:text/tei:body/tei:div
            for $section at $section_no in $chapter/tei:div
                let $text_with_matches := if ($q='') then $chapter
                    else $section[ft:query(., $q)]
                where $text_with_matches             
                return                                
                <result_list>
                    <chapter_no>{$chapter_no}</chapter_no>
                    <section_no>{$section_no}</section_no>                                    
                    <kwic>{kwic:summarize($text_with_matches, <config width="55"/>)}</kwic>                                   
                </result_list> 

return  
    <results>
        {$results}
    </results>
