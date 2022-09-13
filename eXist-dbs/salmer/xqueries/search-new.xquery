xquery version "1.0";
declare namespace tei="http://www.tei-c.org/ns/1.0";
declare namespace exist="http://exist.sourceforge.net/NS/exist";
declare namespace request="http://exist-db.org/xquery/request";
declare namespace ft="http://exist-db.org/xquery/lucene";

import module namespace kwic="http://exist-db.org/xquery/kwic";
declare boundary-space strip;
declare option exist:serialize "indent=no";
declare option exist:serialize "method=json media-type=text/javascript";
(:declare option exist:serialize "method=html media-type=text/html";:)
(:declare option exist:serialize "method=xml media-type=text/xml";:)


let $q := request:get-parameter('q', '')
let $coll := collection("/db/apps/salmer/xml")/tei:TEI/tei:text

(: Here, generate results for front and back matter :)
let $front_hits := $coll/tei:front/tei:div[ft:query(., $q)]
let $back_hits := $coll/tei:back/tei:div[ft:query(., $q)]

let $front_results := for $hit in $front_hits
    let $page_no := util:expand($hit, "expand-xincludes=no highlight-matches=both")//exist:match/preceding::tei:pb[1]/string(@n)
    order by ft:score($hit) descending
        return
    <result_list>
        <page_no>{$page_no}</page_no>
        <chapter_no>front</chapter_no>
        <section_no>{count($hit/tei:div[ft:query(., $q)]/preceding-sibling::tei:div) +1}</section_no>
        <id>{util:document-name($hit)}</id>
        <title>{$hit/ancestor::*//tei:titleStmt/tei:title/text()}</title>
        <q>{$q}</q>
        <kwic>{kwic:summarize($hit, <config width="40"/>)}</kwic>
    </result_list>

let $back_results := for $hit in $back_hits
    let $page_no := util:expand($hit, "expand-xincludes=no highlight-matches=both")//exist:match/preceding::tei:pb[1]/string(@n)
    order by ft:score($hit) descending
        return
    <result_list>
        <page_no>{$page_no}</page_no>
        <chapter_no>back</chapter_no>
        <section_no>{count($hit/tei:div[ft:query(., $q)]/preceding-sibling::tei:div) +1}</section_no>
        <id>{util:document-name($hit)}</id>
        <title>{$hit/ancestor::*//tei:titleStmt/tei:title/text()}</title>
        <q>{$q}</q>
        <kwic>{kwic:summarize($hit, <config width="40"/>)}</kwic>
    </result_list>


(: This works:)
(: Please note that this path selects the div which is most specific to the query :)
let $body_hits := $coll/tei:body/tei:div/tei:div[ft:query(., $q)]
let $body_results := for $hit in $body_hits
    let $page_no := util:expand($hit, "expand-xincludes=no highlight-matches=both")//exist:match/preceding::tei:pb[1]/string(@n)
    order by ft:score($hit) descending
    return 
    <result_list>
        <page_no>{$page_no}</page_no>
        <chapter_no>{count($hit/preceding-sibling::tei:div) + 1}</chapter_no>
        <section_no>{count($hit/ancestor::tei:div[ft:query(., $q)]/preceding-sibling::tei:div) +1}</section_no>
        <id>{util:document-name($hit)}</id>
        <title>{$hit/ancestor::*//tei:titleStmt/tei:title/text()}</title>
        <q>{$q}</q>
        <kwic>{kwic:summarize($hit, <config width="40"/>)}</kwic>
    </result_list>
    (:let $page_no := util:expand($hit, "expand-xincludes=no highlight-matches=both")//exist:match/preceding::tei:pb[1]/string(@n)
    order by ft:score($hit) descending
        return
    <result_list>
        <page_no>{$page_no}</page_no>
        <pn>{$hit//tei:pb/string(@n)}</pn>
        <chapter_no>{count($hit/preceding-sibling::tei:div) + 1}</chapter_no>
        <section_no>{count($hit/tei:div[ft:query(., $q)]/preceding-sibling::tei:div) +1}</section_no>
        <id>{util:document-name($hit)}</id>
        <title>{$hit/ancestor::*//tei:titleStmt/tei:title/text()}</title>
        <q>{$q}</q>
        <kwic>{kwic:summarize($hit, <config width="40"/>)}</kwic>
    </result_list>:)
    
let $count := count($body_results) + count($front_results) + count($back_results)
return    
   <results>
       <no_of_results>{$count}</no_of_results>
       <!--{$front_results}-->
       {$body_results}
       <!--{$back_results}-->
   </results>