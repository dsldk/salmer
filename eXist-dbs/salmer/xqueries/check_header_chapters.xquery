xquery version "1.0";

declare namespace tei = "http://www.tei-c.org/ns/1.0";
declare option exist:serialize "method=xhtml media-type=text/html";
declare option exist:serialize "method=json media-type=text/javascript";

let $document_id	:= request:get-parameter('id','')

return 
	let $document := doc(concat("/db/apps/salmer/xml/", $document_id))
	return 
	<intro_texts> 
    	<title_page>
    	   <exists>{fn:exists($document//tei:front/tei:titlePage)}</exists>
    	   <no>{$document//tei:front/tei:titlePage/@n/string()}</no>
    	</title_page>
    	<preface>
    	   <exists>{fn:exists($document//tei:front//tei:div[@xml:id="preface"])}</exists>
    	   <no>{$document//tei:front//tei:div[@xml:id="preface"]/@n/string()}</no>
    	</preface>
    	<epigraph>
    	   <exists>{fn:exists($document//tei:front/tei:epigraph)}</exists>
    	   <no>{$document//tei:front/tei:epigraph/@n/string()}</no>
    	</epigraph>
    	<dedication>
    	   <exists>{fn:exists($document//tei:front/tei:div[@type="dedication"])}</exists>
    	   <no>{$document//tei:front/tei:div[@type="dedication"]/@n/string()}</no>
    	</dedication>
    	<calendar>
    	   <exists>{fn:exists($document//tei:front/tei:div[@xml:id="calendar"])}</exists>
    	   <no>{$document//tei:front/tei:div[@xml:id="calendar"]/@n/string()}</no>
    	</calendar>
    	<introduction>
    	   <exists>{fn:exists($document//tei:front/tei:div[@xml:id="introduction"])}</exists>
    	   <no>{$document//tei:front/tei:div[@xml:id="introduction"]/@n/string()}</no>
    	</introduction>
    	<toc-section>
    	   <exists>{fn:exists($document//tei:front/tei:div[@xml:id="toc-section"])}</exists>
    	   <no>{$document//tei:front/tei:div[@xml:id="toc-section"]/@n/string()}</no>
    	</toc-section>
	</intro_texts>
	
