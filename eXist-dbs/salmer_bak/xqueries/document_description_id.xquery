declare option exist:serialize "method=json media-type=text/javascript";
let $document_id	:= request:get-parameter('id','')
let $xmldoc := doc("/db/apps/salmer/tables/document-descriptions.xml")

for $x in $xmldoc/ids/document_id
where id_with_manuscript=$document_id
return $x/id_without_manuscript
