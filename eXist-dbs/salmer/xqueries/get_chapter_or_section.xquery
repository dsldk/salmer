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
let $selection := if ($chapter_name = 'titelblad')
                  then <p xmlns="http://www.tei-c.org/ns/1.0">{$xmldoc//tei:front/tei:titlePage}</p>
                  else if ($chapter_name = 'forord')                
                  then $xmldoc//tei:front/tei:div[@type="preface"]/(tei:p|tei:head[not(@type='add')])              
                  else if ($chapter_name = 'dedikation')
                  then $xmldoc//tei:front/tei:div[@type="dedication"]
                  else if ($chapter_name = 'motto')
                  then $xmldoc//tei:front/tei:epigraph
                  (:Denne regel synes at løse problemet med udtræk af hele Emigrantlitteraturen
                  else if ($section = 0)
                  then $xmldoc//tei:body/tei:div[$chapter]/(tei:p|tei:head[not(@type='add')]):)
                  else if ($section = 0)
                  then $xmldoc//tei:body/tei:div[$chapter]/(tei:p|
                                                            tei:head[not(@type='add')]|
                                                            tei:div/tei:head[@type="sub"]|
                                                            tei:div[tei:head[@type="sub"]]/*
                                                            )
                  else $xmldoc//tei:body/tei:div[$chapter]

return if ($section = 0 and $selection[tei:lg])
	   then let $line-index := index-of(($xmldoc//tei:l), $selection/tei:lg[1]/tei:l[1])
	        let $line-index-param := <param name="line-index" value="{$line-index}"/>
	        return <results>{transform:transform($selection, $stylesheet, <parameters>{$line-index-param}</parameters>)}</results> 
	   else if ($section = 0 and $selection[tei:p])
	        then <results>{transform:transform($selection, $stylesheet, <parameters></parameters>)}</results> 	        
	        else if ($section != 0)
	          then let $selection := $selection/tei:div[$section]
	               return if ($selection[tei:lg])
	               then let $line-index := index-of(($xmldoc//tei:l), $selection/tei:lg[1]/tei:l[1])
	                    let $line-index-param := <param name="line-index" value="{$line-index}"/>
	                    return <results>{transform:transform($selection, $stylesheet, <parameters>{$line-index-param}</parameters>)}</results> 
	          else <results>{transform:transform($selection, $stylesheet, <parameters></parameters>)}</results>	    
    else <results>{transform:transform($selection, $stylesheet, <parameters></parameters>)}</results>	
