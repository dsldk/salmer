xquery version "1.0";
declare namespace tei="http://www.tei-c.org/ns/1.0";
declare namespace exist="http://exist.sourceforge.net/NS/exist";
declare namespace request="http://exist-db.org/xquery/request";
declare namespace ft="http://exist-db.org/xquery/lucene";
declare namespace functx = "http://www.functx.com";
import module namespace kwic="http://exist-db.org/xquery/kwic";
declare base-uri "http://localhost:8080/exist/rest/db/apps/salmer/";

declare function functx:contains-case-insensitive
  ( $arg as xs:string? ,
    $substring as xs:string )  as xs:boolean? {
   contains(upper-case($arg), upper-case($substring))
 } ;
 
declare option exist:serialize "method=json media-type=text/javascript";

let $data-collection := "/db/apps/salmer/xml/"
let $q := request:get-parameter('q', '')
let $categories := request:get-parameter('category', '')
let $languages := request:get-parameter('language', '')
let $from  := request:get-parameter('from', '0000-00-00')
let $to  := request:get-parameter('to', '9999-00-00')
let $projects := request:get-parameter('project', '')
let $documents := collection($data-collection)/tei:TEI
let $search_options := <options><default-operator>and</default-operator></options>


let $query-results := for $document in $documents   
                      let $text_matches := if ($q='') then $document
                         else $document//tei:div[ft:query(., $q, $search_options)]
                      let $summary_matches := $document//tei:summary[functx:contains-case-insensitive(.,$q)]                      
                      let $place_matches := $document//tei:placeName[functx:contains-case-insensitive(.,$q)]
                      where ($text_matches or $summary_matches or $place_matches)
                      return $document                                          

let $query-results-possibly-all := if ($q='') then $documents else $query-results

let $category-results := if ($categories) then
                         for $document in $query-results-possibly-all
                             for $category in $categories
                                 where   $category = $document/tei:teiHeader/tei:profileDesc/tei:textClass/tei:keywords/tei:term/text()
                          return $document
                         else $query-results

let $language-results := if ($languages) then
                              for $document in $category-results
                                  for $language in $languages
                                      where $language = $document/tei:teiHeader/tei:profileDesc/tei:langUsage/tei:language/@ident
                                  return $document
                         else $category-results

let $project-results := if ($projects) then
                              for $document in $language-results
                                  for $project in $projects
                                    where $project = $document/tei:teiHeader//tei:encodingDesc/tei:projectDesc/tei:ab/text()
                                  return $document
                         else $language-results

let $search-results := if (empty($project-results))
                       then collection($data-collection)/tei:TEI[functx:contains-case-insensitive(.,$q)]
                       else $project-results
   
let $count := count($search-results)

let $matching_sections :=  if ($q='') then "" else
                           for $document in $search-results
                             let $chapters := $document//tei:body/tei:div[tei:head]
                             let $matching_chapters :=
                             for  $chapter at $chapter_no in $chapters
                                 let $text_matches := $chapter[ft:query(., $q, $search_options)]
                                 let $sections := $chapter/tei:div[tei:head]
                                 return 
                                     if (count($text_matches)) then 
                                         for $section at $section_no in $sections
                                            let $section_text_matches := $section[ft:query(., $q, $search_options)]
                                            where $section_text_matches 
                                            return <r><id>{util:document-name($document)}</id><chapter>{$chapter_no}</chapter><section>{$section_no}</section></r>                                                                   
                                     else ""                             
                             return $matching_chapters

return    
            <results>
            <no_of_results>{$count}</no_of_results>
            <matching-sections>{$matching_sections}</matching-sections>                               
            {
                    for $doc in $search-results
                        let $id := util:document-name($doc)
                        let $date_for_web_page := $doc//tei:teiHeader/tei:profileDesc/tei:creation/tei:date/text()
                        let $date := string($doc//tei:teiHeader/tei:profileDesc/tei:creation/tei:date/@when)
                        let $date_not_before := string($doc//tei:teiHeader/tei:profileDesc/tei:creation/tei:date/@notBefore)
                        let $date_not_after := string($doc//tei:teiHeader/tei:profileDesc/tei:creation/tei:date/@notAfter)
                        let $date_when := string($doc//tei:teiHeader/tei:profileDesc/tei:creation/tei:date/@when)                        
                        let $place := $doc//tei:teiHeader/tei:profileDesc//tei:placeName/text()                       
                        let $summary := $doc/tei:teiHeader/tei:profileDesc//tei:abstract/tei:ab/text()
                        let $category := $doc/tei:teiHeader/tei:profileDesc/tei:textClass/tei:keywords/tei:term
                        let $language := $doc/tei:teiHeader/tei:profileDesc//tei:language
                        let $title := $doc//tei:titleStmt/tei:title/text()
                        let $author := $doc//tei:titleStmt/tei:author/text()
                        let $project := $doc/tei:teiHeader//tei:encodingDesc/tei:projectDesc/tei:ab/text()
                        order by $title
                     return if (contains($id,'.xml')) then
                        <result_list>
                            <id>{$id}</id>
                            <title>{$title}</title>
                            <author>{$author}</author>
                            <chapter></chapter>
                            <section></section>
                            <summary>{$summary}</summary>
                            <date_for_web_page>{$date_for_web_page}</date_for_web_page>
                            <date>{$date_when}</date>
                            <date_when>{$date_when}</date_when>
                            <date_not_before>{$date_not_before}</date_not_before>
                            <date_not_after>{$date_not_after}</date_not_after>
                            <category>{$category}</category>
                            <language>{$language}</language>
                            <project>{$project}</project>
                            <kwic>{kwic:summarize($doc, <config width="140"/>)}</kwic>
                        </result_list> 
                        else <result_list>Not xml file</result_list>
                        
            }</results>
