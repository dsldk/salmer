xquery version "1.0";
declare namespace tei="http://www.tei-c.org/ns/1.0";
declare option exist:serialize "method=json media-type=text/javascript";

let $q := request:get-parameter('id', '')
let $book_id := request:get-parameter('book_id', '')
let $data-collection := collection("/db/apps/salmer/xml/")

let $xmldoc := doc("/db/apps/salmer/xml/christian-3-bibel.xml")

let $match := for $chapter at $chapter_no in $xmldoc/tei:TEI/tei:text/tei:body/tei:div            
              where $chapter//tei:div/@xml:id = $book_id
              return 
                for $section at $section_no in $chapter/tei:div
                where $section//tei:div/@xml:id = $book_id              
                return 
                    <chapter_and_section>
                        <chapter_no>{$chapter_no}</chapter_no>
                        <section_no>{(:if ($chapter_no = 3) then number($section_no)-1 else:)$section_no}</section_no>
                        <chapter_name>{$chapter/tei:head[@type="add"]//normalize-space()}</chapter_name>
                        <section_name>{$section/tei:head[@type="add"]//normalize-space()}</section_name>
                    </chapter_and_section>

let $book_match := for $chapter at $chapter_no in $xmldoc/tei:TEI/tei:text/tei:body/tei:div            
              where $chapter//tei:div/@xml:id = $book_id
              return 
                    <chapter_and_section>
                        <chapter_no>{$chapter_no}</chapter_no>
                        <section_no>1</section_no>
                        <chapter_name>{$chapter/tei:head[@type="add"]//normalize-space()}</chapter_name>
                        <section_name>ukendt</section_name>
                    </chapter_and_section>
                                      
return <results>{$match}</results>