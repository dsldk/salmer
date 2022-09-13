xquery version "1.0";
declare namespace tei="http://www.tei-c.org/ns/1.0";
declare namespace exist="http://exist.sourceforge.net/NS/exist";
declare namespace request="http://exist-db.org/xquery/request";
declare namespace ft="http://exist-db.org/xquery/lucene";
declare namespace functx = "http://www.functx.com";
import module namespace kwic="http://exist-db.org/xquery/kwic";


declare function functx:contains-case-insensitive
  ( $arg as xs:string? ,
    $substring as xs:string )  as xs:boolean? {
   contains(upper-case($arg), upper-case($substring))
 } ;

declare option exist:serialize "method=json media-type=text/javascript";
let $search_options := <options><default-operator>and</default-operator></options>
let $document_id := request:get-parameter('document_id', '')
let $q := request:get-parameter('q', '')
let $xmldoc := doc(concat("/db/apps/salmer/xml/", $document_id))
let $divs := $xmldoc/tei:TEI/tei:text/tei:body/tei:div
let $match := for $chapter at $sCount in $xmldoc/tei:TEI/tei:text/tei:body/tei:div
              let $text_matches := if ($q='') then $chapter
                  else $chapter[ft:query(., $q,$search_options)]
              where $text_matches             
              return <sections><no>{$sCount}</no><name>{$chapter/tei:head[@type="add"]//normalize-space()}</name></sections>
let $match_for_lemmatized_texts := for $chapter at $sCount in $divs
              let $text_matches := if ($q='') then $chapter
                  else $chapter//tei:w[ft:query(., $q,$search_options)]
              where $text_matches             
              return <sections><no>{$sCount}</no><name>{$chapter/tei:head[@type="add"]//normalize-space()}</name></sections>
return <results>{$match}{$match_for_lemmatized_texts}</results>
