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

let $document_id := request:get-parameter('document_id', '')
let $xmldoc := doc(concat("/db/apps/brandes/xml", $document_id))
let $chapter_id := request:get-parameter('chapter', '')
let $chapters := $xmldoc/tei:TEI/tei:text/tei:body/tei:div
let $chapter := $chapters[xs:integer($chapter_id)]
let $q := request:get-parameter('q', '')
let $chapterdiv := $chapter
let $match := for $section at $sCount in $chapterdiv/tei:div
              let $text_matches := if ($q='') then $chapter//tei:l 
                  else $section[functx:contains-case-insensitive(.,$q)]               
              where $text_matches
              return <sections><no>{$sCount}</no><name>{$section/tei:head[@type="add"]//normalize-space()}</name></sections>
return <results>{$match}</results>
