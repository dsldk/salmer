function getContentArea(){
	// to end all doubt on where the content sits. It also felt a bit silly doing this over and over in every
	// function, even if it is a tiny operation. Just guarding against someone changing the names again, in the name
	// of semantics or something.... ;)
	node =  document.getElementById('region-content')
	if (! node){
		node = document.getElementById('content')
		}
	return node
	}


function highlight_terms(regexps, contents) {
  var exact_regexp = regexps.exact;
  var inexact_regexp = regexps.inexact;
  var tag_exp = /<[^>]+>/;

  var res = [];
  while (contents) {
    var me = exact_regexp && contents.match(exact_regexp);
    var mi = inexact_regexp && contents.match(inexact_regexp);


    var m, cls;


    if (!mi && !me) {
      break;
    }
    if (mi && (!me || mi.index < me.index)) {
      cls = "highlightedSearchTermInexact";
      m = mi;
    } else {
      cls = "highlightedSearchTerm";
      m = me;
    }

    var index = m.index + m[1].length;
    var len = m[2].length;
    if (!len) break;
    // Make sure we are not inside of html
    var precontents = contents.substr(0, index);
    if (precontents.match(/<[^>]*$/)) {
      var postcontents = contents.substr(index);
      var pm = postcontents.match(/>/);
      if (!pm) break;
      var new_ind = index + pm.index + 1;
      res.push(contents.substr(0, new_ind));
      contents = contents.substr(new_ind);
      continue;
    }
    res.push(contents.substr(0, index));
    var to_mark = contents.substr(index, len);

    // Do not break the html tree-structure.
    while (true) {
      var m2 = to_mark.match(/<[^>]+>/);
      if (!m2) break;
      var ind = m2.index;
      if (ind) {
        res.push("<span class=\"" + cls + "\">");
        res.push(to_mark.substr(0, ind));
        res.push("</span>");
      }
      res.push(m2[0]);
      to_mark = to_mark.substr(ind + m2[0].length);
    }
    res.push("<span class=\"" + cls + "\">");
    res.push(to_mark);
    res.push("</span>");

    contents = contents.substr(index + len);
  }

  res.push(contents);
  return res.join('');
}

function mark_terms(regexps, contentarea) {
  if (contentarea != null) {
      contentarea.innerHTML = highlight_terms(regexps, contentarea.innerHTML);
  }
}

function get_terms (terms) {
  if (!terms) return null;
  terms = decodeURI(terms).split(',');
  var res = [];
  var regexp = new RegExp("[^\\][\\w\\dæøåÆØÅ*?]+", "g");
  for (var i = 0, len = terms.length; i < len; i++) {
    if (!terms[i]) continue;
    var match = terms[i].match(/^[^\w\dæøåÆØÅ*?]*(.*?)[^\w\dæøåÆØÅ*?]*$/);
    if (match) {
      terms[i] = match[1];
    }
    terms[i] = terms[i].replace(/[æÆ]/g, "[æÆ]");
    terms[i] = terms[i].replace(/[åÅ]/g, "[åÅ]");
    terms[i] = terms[i].replace(/[øØ]/g, "[øØ]");
    terms[i] = terms[i].replace(regexp, "(<[^>]+>|[^\\w\\dæøåÆØÅ<>])+");
    terms[i] = terms[i].replace(/\*+/g, "[æøåÆØÅÆ\\w\\d]*");
    terms[i] = terms[i].replace(/\?/g, "[øæåÆÅØ\\w\\d]");
    res.push(terms[i]);
  }

  if (!res.length) return null;

  return new RegExp("([^\\w\\dæøåÆØÅ]|^)(" + res.join('|') + ")([^\\w\\dæøåÆØÅ]|$)", "i");
}

function myHighlight() {
  var contentarea = getContentArea();
  var exact_terms = window.location.search.match(new RegExp("q=([^&]*)", "i"));
  if (exact_terms) {
    exact_terms = get_terms(exact_terms[1]);
  }
  var inexact_terms = window.location.search.match(new RegExp("inexact_terms=([^&]*)", "i"));
  if (inexact_terms) {
    inexact_terms = get_terms(inexact_terms[1]);
  }

  var regexps = {
    exact: exact_terms,
    inexact: inexact_terms
  };

  mark_terms(regexps,contentarea);
}

$(function() {
    myHighlight();
});