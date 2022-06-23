$(document).ready(function() {
    var lookupUrl = '//wstest.dsl.dk/lex/query?app=sal&version=1.0&q='
    //wstest.dsl.dk/lex/query?app=brandes&version=1.0&q='
    $('.chapter-box').on('click', '.theActualDocument #region-content', function(event) {
        if ($('#click-lookup-note-checkbox').prop('checked')) {
            // only do lookup if setting is activated
            // Gets clicked on word (or selected text if text is selected)
            var sel = window.getSelection();
            let parentNode = sel.anchorNode.parentNode;
            let queryWord = sel.toString();
            let allowedNodes = ['H1', 'H2', 'H3', 'H4', 'H5', 'H6', 'P', 'DIV'];
            let allowMixedNodes = ['EM'];
            
            if (sel.anchorNode != sel.focusNode) {
                let anchorParent = sel.anchorNode.parentNode;
                let focusParent = sel.focusNode.parentNode;
                if ((!allowedNodes.includes(anchorParent.nodeName)) && (!allowMixedNodes.includes(anchorParent.nodeName))) {
                    parentNode = focusParent;
                    if (sel.focusNode.nodeType === 3) {
                        queryWord = sel.focusNode.nodeValue.substr(0, sel.focusOffset);
                    } else {
                        queryWord = focusParent.childNodes[0].nodeValue.substr(0, sel.focusOffset);                    
                    }
                }
            }
            queryWord = queryWord.replace(/[()!;.,]/gi, '')
            queryWord = queryWord.replace(/^ +/gi, '')
            queryWord = queryWord.replace(/ +$/gi, '')
            
            // only allow lookups of words that are not people, works of art, characters etc.
            if (queryWord) {
                // && !parentNode.hasClass('persName') && !parentNode.hasClass('fictionalpersName') && !parentNode.hasClass('bibl') && !parentNode.hasClass('placeName') && !parentNode.hasClass('facsimile-link') && !parentNode.hasClass('legacy-page-break') && !parentNode.hasClass('lang')) {
                if (queryWord.length > 0) {
                    if (lookupUrl) {
                        $.ajax({
                            url: lookupUrl + queryWord,
                            method: 'GET',
                            dataType: 'html'
                        }).done(function(response) {
                            $('#dictionary-lookup-tab').html(response);
                            var tabIndex = $('#tabs > div > div').index($('#dictionary'));
                            $('#tabs').tabs('option', 'active', tabIndex);
                        })
                    } else {
                        console.warn('lookupUrl is not defined')
                    }
                }
            }
        }
    });
});
