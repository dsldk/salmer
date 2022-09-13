xquery version "1.0";

import module namespace request="http://exist-db.org/xquery/request";
import module namespace transform="http://exist-db.org/xquery/transform";
import module namespace ft="http://exist-db.org/xquery/lucene";
declare namespace tei="http://www.tei-c.org/ns/1.0";
declare namespace exist="http://exist.sourceforge.net/NS/exist";
declare option exist:serialize "method=xhtml media-type=text/html";

let $query	:= request:get-parameter('id','')
let $chapter_name := request:get-parameter('chapter_name','')
let $chapter := xs:integer(request:get-parameter('chapter','0'))
let $stylesheet := doc("/db/apps/salmer/xslt/section.xsl")
let $section := xs:integer(request:get-parameter('section','0'))
let $frontpage_section := xs:integer(request:get-parameter('frontpage_section','0'))
let $xmldoc := doc(concat("/db/apps/salmer/xml/", $query))
let $selection := if ($chapter_name = 'metadata')
                  then $xmldoc//tei:teiHeader
                  else if ($chapter_name = 'titelblad')
                  then $xmldoc//tei:front/tei:titlePage
                  else if ($chapter_name = 'front')
                  then $xmldoc/tei:TEI//tei:front
                  else if ($chapter_name = 'back')
                  then $xmldoc/tei:TEI//tei:back
                  else $xmldoc//tei:body/tei:div[$chapter]

let $latest-pb := if ($section = 0)
    then $selection/preceding::tei:pb[1]
    else $selection/tei:div[$section]/preceding::tei:pb[1]
let $latest-pb-param := (<param name="facs" value="{$latest-pb/@facs}"/>,<param name="n" value="{$latest-pb/@n}"/>)

return if ($section = 0 and $selection[tei:lg])
       
       (: if verse :)
	   then let $line-index := index-of(($xmldoc//tei:l), $selection/tei:lg[1]/tei:l[1])
	        let $line-index-param := <param name="line-index" value="{$line-index}"/>
	        return <results>{transform:transform($selection, $stylesheet, <parameters>{$line-index-param}{$latest-pb-param}</parameters>)}</results> 
	   else if ($section = 0 and $selection[tei:p])	   
	        (: if prose :)
	        then <results>{transform:transform($selection, $stylesheet, <parameters>{$latest-pb-param}</parameters>)}</results> 	        
	        else if ($section != 0)	        
	          (: if (sub)section :)
	          (: let chapter_head be the first head(line) element above the selected subsection :)
	          (: for the time being this headline is transformed and subsequently wrapped in an h1 element :)
	          then let $chapter_head := $selection/tei:head[not(@type="add")][1]
	               let $selection := $selection/tei:div[$section] 
	               return 
    	               if ($selection[tei:lg])
    	               (: if poetry :)
    	               then let $line-index := index-of(($xmldoc//tei:l), $selection/tei:lg[1]/tei:l[1])
    	                    let $line-index-param := <param name="line-index" value="{$line-index}"/>
    	                    return <results>{transform:transform($selection, $stylesheet, <parameters>{$line-index-param}{$latest-pb-param}</parameters>)}</results> 
    	               else if ($section = 1) then   	                    
    	                    <results><h1>{transform:transform($chapter_head, $stylesheet, <parameters></parameters>)}</h1>{transform:transform($selection, $stylesheet, <parameters>{$latest-pb-param}</parameters>)}</results>
    	                    else
    	                    <results>{transform:transform($selection, $stylesheet, <parameters>{$latest-pb-param}</parameters>)}</results>
                       else <results>{transform:transform($selection, $stylesheet, <parameters>{$latest-pb-param}</parameters>)}</results>
                       

