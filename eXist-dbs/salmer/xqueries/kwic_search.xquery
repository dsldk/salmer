xquery version "1.0";
declare namespace tei="http://www.tei-c.org/ns/1.0";
declare namespace exist="http://exist.sourceforge.net/NS/exist";
declare namespace request="http://exist-db.org/xquery/request";
declare namespace ft="http://exist-db.org/xquery/lucene";
import module namespace kwic="http://exist-db.org/xquery/kwic";
declare base-uri "http://localhost:8080/exist/rest/db/apps/salmer/";
declare boundary-space strip;
declare option exist:serialize "indent=no";
declare option exist:serialize "method=json media-type=text/javascript"; 

let $data-collection := "/db/apps/salmer/xml"
let $q := request:get-parameter('q', 'intetsaadantordisamlingen')
let $parent_of_documents := collection($data-collection)
let $search_options := <options><default-operator>and</default-operator></options>

let $search-results := $parent_of_documents//tei:TEI[ft:query(., $q)]

let $results :=  for $doc in $search-results
                        let $id := util:document-name($doc)
                        let $title := $doc//tei:teiHeader//tei:title/text()
                     return if (contains($id,'.xml')) then
                        for $chapter at $chapter_no in $doc//tei:text/tei:body/tei:div                        
                             for $section at $section_no in $chapter/tei:div
                                let $text_with_matches := $section[ft:query(., $q,$search_options)] 
                                let $page_no := util:expand($text_with_matches, "expand-xincludes=no highlight-matches=both")//exist:match/preceding::tei:pb[1]/string(@n)
                                where $text_with_matches                                
                                return                                
                                <result_list>
                                    <page_no>{$page_no}</page_no>
                                    <chapter_no>{$chapter_no}</chapter_no>
                                    <section_no>{$section_no}</section_no>
                                    <id>{$id}</id>
                                    <title>{$title}</title>
                                    <q>{$q}</q>
                                    <kwic>{kwic:summarize($text_with_matches, <config width="50"/>)}</kwic>                                    
                                </result_list> 
                        else <result_list>Not xml file</result_list>

let $count := count($results)

return    
            <results>
                <no_of_results>{$count}</no_of_results>
                {$results}
            </results>
