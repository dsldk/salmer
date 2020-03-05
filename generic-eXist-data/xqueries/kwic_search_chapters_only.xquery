xquery version "1.0";
declare namespace tei="http://www.tei-c.org/ns/1.0";
declare namespace exist="http://exist.sourceforge.net/NS/exist";
declare namespace request="http://exist-db.org/xquery/request";
declare namespace ft="http://exist-db.org/xquery/lucene";
declare namespace functx = "http://www.functx.com";
import module namespace kwic="http://exist-db.org/xquery/kwic";
declare base-uri "http://localhost:8080/exist/rest/db/apps/brandes/";
declare boundary-space strip;
declare option exist:serialize "indent=no";
declare option exist:serialize "method=json media-type=text/javascript"; 

let $data-collection := "/db/apps/brandes/xml"
let $q := request:get-parameter('q', '')
let $categories := request:get-parameter('category', '')
let $languages := request:get-parameter('language', '')
let $from  := request:get-parameter('from', '0000-00-00')
let $to  := request:get-parameter('to', '9999-00-00')
let $documents := collection($data-collection)/tei:TEI
let $parent_of_documents := collection($data-collection)
let $search_options := <options><default-operator>and</default-operator></options>
let $with_metadata := request:get-parameter('with_metadata', '')

let $query-results := if ($q='') then $documents else
                      $parent_of_documents//tei:TEI[ft:query(., $q)]


                       
let $category-results := if ($categories[1]) then
                         for $document in $query-results
                             for $category in $categories                         
                                 where  $document/tei:teiHeader/tei:profileDesc/tei:textClass/tei:keywords/tei:term/text() = $categories                                                   
                          return $document
                         else $query-results

let $language-results := if ($languages[1]) then
                              for $document in $category-results
                                  for $language in $languages                            
                                      where  $document/tei:teiHeader/tei:profileDesc/tei:langUsage/tei:language/@ident = $languages                        
                                  return $document
                         else $category-results

let $search-results := $language-results


let $results :=  for $doc in $search-results
                        let $id := util:document-name($doc)
                        let $date_for_web_page := $doc//tei:teiHeader/tei:profileDesc/tei:creation/tei:date/text()
                        let $date := string($doc//tei:teiHeader/tei:profileDesc/tei:creation/tei:date/@when)
                        let $date_not_before := string($doc//tei:teiHeader/tei:profileDesc/tei:creation/tei:date/@notBefore)
                        let $date_not_after := string($doc//tei:teiHeader/tei:profileDesc/tei:creation/tei:date/@notAfter)
                        let $date_when := string($doc//tei:teiHeader/tei:profileDesc/tei:creation/tei:date/@when)                        
                        let $title := $doc//tei:teiHeader//tei:title/text()
                        let $summary := $doc/tei:teiHeader//tei:abstract/tei:ab/text()
                        let $category := $doc/tei:teiHeader/tei:profileDesc/tei:textClass/tei:keywords/tei:term
                        let $language := $doc/tei:teiHeader/tei:profileDesc//tei:language
                        let $parent-head := $doc//tei:head/text()
                        order by $id                      
                     return if (contains($id,'.xml')) then
                        for $chapter at $chapter_no in $doc//tei:text/tei:body/tei:div                        
                            let $chapter_matches := $chapter[ft:query(., $q,$search_options)]                                                            
                            let $page_no := util:expand($chapter_matches, "expand-xincludes=no highlight-matches=both")//exist:match/preceding::tei:pb[1]/string(@n)
                                where $chapter_matches                               
                                return                                
                                <result_list>
                                    <page_no>{$page_no}</page_no>
                                    <chapter_no>{$chapter_no}</chapter_no>
                                    <section_no>{0}</section_no>
                                    <name>{$chapter/tei:head//normalize-space()}</name>
                                    <id>{$id}</id>
                                    <title>{$title}</title>
                                    <summary>{$summary}</summary>
                                    <date_for_web_page>{$date_for_web_page}</date_for_web_page>
                                    <date>{$date_when}</date>
                                    <date_when>{$date_when}</date_when>
                                    <date_not_before>{$date_not_before}</date_not_before>
                                    <date_not_after>{$date_not_after}</date_not_after>
                                    <category>{$category}</category>
                                    <language>{$language}</language>
                                    <parent-head>{$parent-head}</parent-head>
                                    <q>{$q}</q>
                                    <kwic>{kwic:summarize($chapter_matches, <config width="50"/>)}</kwic>                                    
                                </result_list> 
                        else <result_list>Not xml file</result_list>

let $count := count($results)

return    
            <results>
                <no_of_results>{$count}</no_of_results>
                {$results}
            </results>