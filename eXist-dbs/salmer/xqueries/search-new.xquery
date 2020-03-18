xquery version "1.0";
declare namespace tei = "http://www.tei-c.org/ns/1.0";
declare namespace exist = "http://exist.sourceforge.net/NS/exist";
declare namespace request = "http://exist-db.org/xquery/request";
declare namespace ft = "http://exist-db.org/xquery/lucene";
declare namespace functx = "http://www.functx.com";
import module namespace kwic = "http://exist-db.org/xquery/kwic";
(:declare base-uri "http://localhost:8080/exist/rest/db/apps/salmer/";:)



declare function functx:contains-case-insensitive
($arg as xs:string?,
$substring as xs:string) as xs:boolean? {
    contains(upper-case($arg), upper-case($substring))
};

(:~
    Helper function: create a lucene query from the user input
:)

(:declare function shakes:do-query($queryStr as xs:string?, $mode as xs:string?) {
    let $query := shakes:create-query($queryStr, $mode)
    for $hit in collection($config:app-root)//SCENE[ft:query(., $query)]
    order by ft:score($hit) descending
    return $hit
};
:)

(:
declare function shakes:create-query($queryStr as xs:string?, $mode as xs:string?) {
        <query>
        {
            if ($mode eq 'any') then
                for $term in tokenize($queryStr, '\s')
                return
                    <term occur="should">{$term}</term>
            else if ($mode eq 'all') then
                for $term in tokenize($queryStr, '\s')
                return
                    <term occur="must">{$term}</term>
            else if ($mode eq 'phrase') then
                <phrase>{$queryStr}</phrase>
            else
                <near>{$queryStr}</near>
        }
        </query>
};
:)

(:declare option exist:serialize "method=json media-type=text/javascript";:)
declare option exist:serialize "method=xhtml media-type=text/html";
declare variable $q := request:get-parameter('q', '');
declare variable $languages := request:get-parameter('language', '');
declare variable $categories := request:get-parameter('category', '');

<results>{
        (:let $data-collection := ("/db/apps/salmer/xml/"):)
        (:let $q := request:get-parameter('q', ''):)
        (:let $documents := collection($data-collection)/tei:TEI:)
        (:let $search_options := <options><default-operator>and</default-operator></options>:)
        
        let $context := collection("/db/apps/salmer/xml")//tei:text
        let $hits := ($context//tei:p[ft:query(., $q)], $context//tei:lg[ft:query(., $q)])
        let $number-of-hits := count($hits)
        (:for $hit in collection("/db/apps/salmer/xml")//tei:text//tei:p[ft:query(., $q)]:)
        
        for $hit at $count in $hits
        order by ft:score($hit) descending
        return
            
            <div><hit><!--<number-of-hits>{$number-of-hits}</number-of-hits>-->
                <p>{$count}</p>
                <p>{base-uri($hit)}</p>
                <!--<p>{$q}</p>-->
                <!--<title>{string(root($hit)//tei:teiHeader//tei:title)},
                    {
                        for $headline in $hit/ancestor::tei:div/tei:head[@type = "add"]
                        return
                            if ($headline is $hit/ancestor::tei:div/tei:head[@type = "add"][last()])
                            then                         
                                <part nr="{index-of($headline/ancestor::tei:div//tei:head[@type = "add"], $headline)}">{concat($headline, ' ')}</part> (:and index-of($headline/ancestor::tei:div//tei:head[@type = "add"], $headline):)
                            else
                                <part nr="{index-of($headline/ancestor::tei:div//tei:head[@type = "add"], $headline)}">{concat($headline, ', ')}</part> 
                                (:this is too slow -> and index-of(root($headline)//tei:text/tei:body/tei:div/tei:head[@type = "add"], $headline):)
                    }</title>-->
                
                
                <!--<author>{string(root($hit)//tei:teiHeader//tei:author)}</author>-->
                <!--<summary>{string(root($hit)//tei:teiHeader//tei:abstract)}</summary>-->
                <!--<categories>{
                        let $categories := root($hit)//tei:term/text()
                        for $category in $categories
                        return
                            <category>{$category}</category>
                    }</categories>-->
                <p>{
                        let $languages := root($hit)//tei:language/text()
                        for $language in $languages
                        return
                            <language>{$language}</language>
                    }</p>
                <p>{
                        kwic:summarize($hit, <config
                            width="100" link="{root($hit)}"/>)
                    }</p>
                <!--<full-result>{string($hit)}</full-result>-->
            </hit></div>
    
    }</results>
