xquery version "1.0";

import module namespace request="http://exist-db.org/xquery/request";
import module namespace transform="http://exist-db.org/xquery/transform";
import module namespace ft="http://exist-db.org/xquery/lucene";

declare namespace exist="http://exist.sourceforge.net/NS/exist";
declare option exist:serialize "method=xhtml media-type=text/html";
let $document_id	:= request:get-parameter('id','')

return 
	let $opslag := doc(concat("/db/apps/brandes/xml", $document_id))
	return transform:transform($opslag, doc("/db/apps/brandes/xslt/smn.xsl"),<parameters><param name="query" value="test"/></parameters>)
	