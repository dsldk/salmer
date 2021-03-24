$(function(){


	/* checkCookie(); // Uncomment to enable cookie popup */

	// attach click functionality to annotation controls
  $('#text-critical-note-checkbox').click(function(event) {colorAllTextCriticalNotes(this,'.mei svg .dir.comment, .textcriticalnote','.textcriticalnote','blue');});
  // determine whether notes should be shown in MeiAjax.js
  comments = $('#text-critical-note-checkbox').prop('checked')
	$('#click-lookup-note-checkbox').click(function(event) {enableDictLookup(this);});
  $('#tabs').tabs();

	// on page load, replace the "vanilla" browser state with one we define ourselves,
	// so that we can be sure that all navigational states have a state object.
	// this is needed so we can distinguish anchor links -- which also push a state to
	// the history stack -- from navigation actions.
	pushToHistory(window.location.href, 1)

	// save selected tab in browser storage, so we can activate this tab on page load
	$('#tabs').on('tabsactivate', function (event, ui) {
		sessionStorage.setItem('active-tab', ui.newTab.attr('aria-controls'));
	});

  // if we are on the text view, handle the tabs at page load
  if ($('#tabs').length) {
    var tabId = getFirstVisibleTab().attr('id');
  	if (sessionStorage.getItem('active-tab')) {
  		// if the prev tab is not currently hidden, select it instead of the first visible tab
  		if (!$('#' + tabId).hasClass('hidden')) {
        tabId = sessionStorage.getItem('active-tab');
  		}
  	}
    activateTab(tabId);
  }

	// when expanding/collapsing search field, calculate the proper height
	$('#search-field-toggle').change(function (event, settings) {
		var checked = $(this).prop('checked');
		var searchBox = $('#search-field');
		var height = checked ? searchBox.get(0).scrollHeight + 'px' : '';

		requestAnimationFrame(function () {
			if (settings && settings.instant) {
				searchBox.css('transition-duration', '0s');
			}
			else {
				searchBox.css('transition-duration', '');
			}
			searchBox.css('height', height);
			searchBox.find('input[name="q"]').focus();
		});
	})

	var isSearch = /http.*?\/search/.test(window.location.href);
	if (isSearch) {
		$('#search-field-toggle').trigger('change', { instant: true }); // calculate height and animate

    $('#search-mobile').submit(function(){
      // copy the checkbox values from the search form so that this
      // form can respect those settings.
      var documentIds = $('#search-form [name="document_id"]:checked').map(function(){
        return $('<input>', {
          name: 'document_id',
          value: $(this).val(),
          type: 'hidden'
        }).get(); // "expand" with .get() because otherwise we get nested objects
      });

      $(this).append(documentIds);
    });
	}

	// when submitting the search form on the results page, we should
	// copy the input value from the text field to the hidden field,
	// in case the text field was changed.
	$('form[name="manuscripts"]').submit(function () {
		$(this).find('input[name="q"]').val($('#search-mobile input[name="q"]').val());
	});

  // select/deselect search options
  $('#search-form .select-all').click(function(){
    $('input[name=document_id]').prop('checked', true);
  });
  $('#search-form .deselect-all').click(function(){
    $('input[name=document_id]').prop('checked', false);
  });

	// when expanding/collapsing nav, calculate the proper height
	$('#header__menu-toggle').change(function () {
		var checked = $(this).prop('checked');
		var headerMenu = $('.header__menu');
		var height = checked ? headerMenu.get(0).scrollHeight + 'px' : '';

		requestAnimationFrame(function () {
			headerMenu.css('height', height);
		});
	})

	// Get new page from backend when paginating a text in primary language (left side of screen)
	$('.chapter-box').on('change', '.chapter-dropdown', paginateText);
	// We need to perform the same operation for clicks on pagination links
	$('.chapter-box').on('click', '.chapter-selector-wrapper a, .nextPreviousbox a', paginateText);

	// when clicking a comment link in the text column, focus the comment tab
	$('.chapter-box').on('click', '.comment-link', function () {
		activateTab('#comments');
	});

	// Get new page from backend when paginating a text on a secondary language
	$('#translations').on('change', '.chapter-dropdown', function() {
		$('#lang-chapter-wrapper').addClass('loading');
		getManuscript($(this), '/text')
		.done(function(result) {
			updateTextWrapper('#lang-chapter-wrapper', result);
			$('#lang-chapter-wrapper').removeClass('loading');
		});
	});

	// // When paginating a primary language, just submit the form as usual
	// $('.chapter-box').on('change', '.chapter-dropdown', function() {
	// 	var form = $(this).closest('form').get(0); // .get(0) to convert to DOMElement
	// 	form.submit();
	// });

	// When paginating via prev/next buttons or links (i.e. not changing select)
	// in secondary langauge, prevent default (= follow link), and instead get text
	// via AJAX.
	$('#translations').on('click', '.chapter-selector .arrow-r, .chapter-selector .arrow-l, .nextPreviousbox a', function(e) {
		e.preventDefault();
		var href = $(this).attr('href');
		if (href) {
			$('#lang-chapter-wrapper').addClass('loading');
			requestText('/text' + href)
			.done(function(result) {
				updateTextWrapper('#lang-chapter-wrapper', result);
				$('#lang-chapter-wrapper').removeClass('loading');
			});
		}
	})

	// map of translations that exist for each text
	var translations = [
		{
			'Dansk': 'christian-3-bibel',
		},
		{
			'Dansk': 'claus-mortensen-messe-1529',
		},
		{
			'Dansk': 'dietz-salmebog-1529',
		},
		{
			'Dansk': 'dietz-salmebog-1536',
		},
		{
			'Dansk': 'jespersen_1573',
		},
		{
			'Dansk': 'malmoe-salmebog',
		},
		{
			'Dansk': 'oluf-ulriksen-messe-1535',
		},
		{
			'Dansk': 'oluf-ulriksen-messehaandbog-1539',
		},
		{
			'Dansk': 'thomissoen_1569',
		},
	]

	// ugly way to transform array of translations to array of text ids
	var textIds = [].concat.apply([], translations.map(function (lang) {
		return Object.entries(lang).map(function (entry) {
			return entry[1] // item 1 is text id, item 0 is language label
		})
	}))

	var rightLanguageSelector = $('<select/>', {
		'class': 'language-dropdown select-css',
		name: 'language'
	}).append($('<option/>', { // append the placeholder option
		value: null,
		text: __[loc]('Vælg sprog'),
		disabled: 'disabled',
		selected: 'selected'
	}));

	// get the specified text when changing the language selector, and then show the chapter wrapper
	rightLanguageSelector.change(function(){
		var langId = $(this).val()
		$('#lang-chapter-wrapper').addClass('loading');
		requestText('/' + langId + '?text_only=1')
		.done(function(result) {
			updateTextWrapper('#lang-chapter-wrapper', result);
			$('#lang-chapter-wrapper').show();
			$('#lang-chapter-wrapper').removeClass('loading');
		})
	});

	var currentPath = window.location.pathname;
	// find the translation object that contains a substring of the current path as one of its IDs
	var availableLanguages = translations.find(function(translation) {
		return Object.entries(translation).some(function(lang) {
			var hasCurrentPath = currentPath.indexOf(lang[1]) !== -1;
			if (hasCurrentPath) {
				delete translation[lang[0]]; // delete the language we came from, as we don't want to display the same language on both sides
			}
			return hasCurrentPath;
		})
	});
	// see if we are actually left with any languages
	var showLanguageSelector = function () {
		for (var prop in availableLanguages) {
			if (availableLanguages.hasOwnProperty(prop)) {
				return true;
			}
			return false;
		}
		return false;
	}
	if(showLanguageSelector()) {
		// add the langauges as options to the select element
		Object.entries(availableLanguages).forEach(function(lang) {
			rightLanguageSelector.append($('<option/>', {
				value: lang[1],
				text: lang[0]
			}))
		});
		// add the select element to the DOM
		rightLanguageSelector.appendTo('.language-selector');
	} else {
		// hide the tab and the content pane from view
		$('#translations').hide();
		$('[href="#translations"]').closest('li').hide();
	}

	var docId = currentPath.replace(/^\//,'').split('/')[0]; // replace any leading slash, then split on slash, then take the 0th item

	// only if we are on a text page: get the meta texts
	if (textIds.indexOf(docId) > -1) {
		// create and populate a meta text selector, and listen to change events in
		// order to load meta texts
		var metaTypes = [
			{
				type: 'introductions',
				label: __[loc]('Indledning')
			},
			{
				type: 'colophons',
				label: __[loc]('Kolofon')
			},
			{
				type:	'accounts',
				label: __[loc]('Tekstredegørelse')
			},
			{
				type: 'sources',
				label: __[loc]('Tekstvidner')
			}
		];

		var metaSelector = $('<select/>', {
			'class': 'meta-dropdown select-css',
			name: 'meta'
		}).append($('<option/>', { // append the placeholder option
			value: null,
			text: __[loc]('Vælg supplerende tekst'),
			disabled: 'disabled',
			selected: 'selected'
		}));

		metaSelector.change(function(e, replaceStrategy){
      // replaceStrategy determines how we are to update the history stack
      // 0: Push new state
      // 1: Replace state
      // 2: Don't modify history
			var metaType = $(this).val()
			requestText('/meta/' + docId + '/' + metaType)
			.done(function(result) {
				$('#meta-wrapper').html(result).show();
        // determine the location and query portion of the URL we want to push
        // to the history stack
        var newLocation;
        if (window.location.search) {
          // construct a new 2 dimensional array of search options
          var params = parseSearchString(window.location.search);
          // now params is of shape [['foo', 'bar'], ['baz', 'boo']]
          // for a search string ?foo=bar&baz=boo
          // now filter out the meta param if it is already there
          params = params.filter(function (param) {
            return param[0] !== 'meta'
          });
          // and add it again
          params.push(['meta', metaType]);
          // now join everything together
          params = buildSearchString(params);
          newLocation = window.location.href.replace(
            window.location.search,
            params
          );
        } else {
          newLocation = window.location.href + '?meta=' + metaType;
        }
        if (replaceStrategy !== 2) {
          pushToHistory(newLocation, replaceStrategy);
        }
			})
		})

		// make a HEAD request for each meta type, in order to see if we should add it
		// to the selector. We can't just make an array of deferreds with $.when.apply,
    // 'cause if one of them were to fail, the "master" deferred would fail with
    // the failure of this single deferred, and discard the other deferreds
    // irregardless of their success, failure or even completion

    // we need to possibly pre-select the item that corresponds to the
    // ?meta=xyz part of the URL, so prepare a variable for that before we
    // enter the loop
    var selectedMeta;
    if (window.location.search) {
      var searchParams = parseSearchString(window.location.search);
      var metaParam = searchParams.filter(function (param) {
        return param[0] === 'meta';
      })[0]; // take item 0 because the return of .filter() is an array
      selectedMeta = metaParam ? metaParam[1] : null;
    }
		var metaTexts = metaTypes.forEach(function (metaType) {
			$.ajax({
				url: '/meta/' + docId + '/' + metaType.type,
				method: 'HEAD',
        complete: function (jqXHR, status) {
          var status = jqXHR.status
          if (status === 200) {
            // check if the meta selector is already appended to page,
            // and if not, add the option to the metaSelector variable,
            // and then reassign that variable so that the next options
            // are added to the DOM element rather than the variable
            var newOption = $('<option/>', {
              value: metaType.type,
              text: metaType.label,
            });
            if (selectedMeta == metaType.type) {
              newOption.prop('selected', true);
            }
            metaSelector.append(newOption);
            // if the new option is to be selected, trigger the 'change' event for it
            // so that we can load its meta text
            if (newOption.prop('selected')) {
              // activate meta text tab
              activateTab('#meta');
              metaSelector.trigger('change', [1]); // replace state instead of pushing a new state to the stack, as we are simply setting up the page
            }
            if (!$('.meta-selector .meta-dropdown').length) {
              metaSelector.appendTo('.meta-selector');
              metaSelector = $('.meta-selector .meta-dropdown');
            }
            // order the options according to 'metaTypes', so that they always
            // appear in the same order regardless of the order in which
            // the HEAD requests completed
            metaTypes.forEach(function (metaType) {
              metaSelector.find('option[value="' + metaType.type + '"]').detach().appendTo(metaSelector);
            });
            // show the meta tab, as we have at least one option to show
    				$('#meta').removeClass('displaynone');
    				$('[href="#meta"]').closest('li').removeClass('displaynone');
          }
          else if(!metaSelector.find('option').length) {
            // remove the tab and the content pane from view
            $('#meta').hide();
            $('[href="#meta"]').closest('li').hide();
          }
        }
			})
		});

    // toggling reader width
    $('#reader-width').change(function() {
      var isOn = $(this).prop('checked');
      if (isOn) {
        $('.page-wrapper .documentFrame.container').addClass('full-width');
        $('label[for="reader-width"] .checkbox-label-text img').attr('src', '/static/collapse.svg');
      } else {
        $('.page-wrapper .documentFrame.container').removeClass('full-width');
        $('label[for="reader-width"] .checkbox-label-text img').attr('src', '/static/expand.svg');
      }
    });

    // clicking a link in a text or in the meta text view should not trigger
    // a full reload if the destination is within the same manuscript we're
    // currently in
    $('.chapter-box, .tabs-box').on('click', 'a', function(e) {
      var targetHref = $(this).attr('href');
      var isSameManuscript;
      var searchParams;
      // check if the target href begins with the current doc ID
      if (targetHref.indexOf('/' + docId) === 0) {
        isSameManuscript = true;
        // check if the new href has search parameters
        var newSearchParams = targetHref.split('?')[1];
        if (newSearchParams) {
          newSearchParams = '?' + newSearchParams;
          newSearchParams = parseSearchString(newSearchParams);
        } else {
          newSearchParams = [];
        }
        // also take the current search params
        var currentSearchParams = parseSearchString(window.location.search);
        // ... and replace them with their new counterparts
        searchParams = mergeSearchParams(currentSearchParams, newSearchParams);
        // now put it back in the targetHref
        targetHref = targetHref.split('?')[0] + buildSearchString(searchParams);
      }
      else if (targetHref.match(/^\?/)) {
        isSameManuscript = true;
        var currentSearchParams = parseSearchString(window.location.search);
        var newSearchParams = parseSearchString(targetHref);
        searchParams = mergeSearchParams(currentSearchParams, newSearchParams);
        // now put it back in the targetHref
        targetHref = window.location.pathname + buildSearchString(searchParams) + window.location.hash;
        console.log('targetHref', targetHref)
      }
      if (isSameManuscript === true) {
        // stop default action of the link, and do an AJAX pagination instead
        e.preventDefault();
        // only paginate if we are not targeting the exact same text we're already on
        if (targetHref.indexOf(window.location.pathname) === -1) {
          paginateText.call(this, e);
        }

        // also set the meta text if applicable
        var metaOption = searchParams.filter(function (param) {
          return param[0] === 'meta'
        })[0];
        if (metaOption) {
          $('select[name="meta"]').val(metaOption[1]);
          $('select[name="meta"]').trigger('change', [2])
        }
      }
    });
	}

	// when popping to another state, get the text corresponding to the state title
	$(window).on('popstate', function (event) {
		var stateObj = event.originalEvent.state

		// only actually refetch content if we're popping to a state that has a state object
		if (stateObj) {
			// select the chapter option corresponding to the state we just popped,
      // if it differs from what is currently selected.
      // We can't use String.endsWith because IE11 :( So we make our own comparison
      var chapter = $('.chapter-box .chapter-dropdown').val();
      var path = window.location.pathname;
      var sameChapter = path.substring(path.length - chapter.length) === chapter; // take the substring of the path that corresponds to the chapter and see if they are equal
      if (!sameChapter) {
  			$('.chapter-box .chapter-dropdown option[data-ajax-url="/text' + window.location.pathname + '"]').prop('selected', true);

  			// load the chapter corresponding to the state we just popped
  			$('.chapter-box').addClass('loading');
  			requestText('/text' + window.location.pathname)
  			.done(function(result) {
  				updateTextWrapper('.chapter-box', result)
  				$('.chapter-box').removeClass('loading');
  			})
  			.fail(function() {
  				showStatusPopup(__[loc]('Der skete en fejl. Teksten kunne ikke indlæses.'));
  			});

  			// also get any notes for the notes tab
  			// with the requestText as AJAX request
  			updateCommentBox(requestText('/notes' + window.location.pathname));
      }

			// set up other dropdowns according to state
			Object.entries(stateObj).forEach(function (item) {
				var dropdown = item[0]
				var value = item[1] // Object.entries() returns pairs of key, value
				if ($(dropdown).val() != value) { // if the dropdown is not already set to the value stored in the state...
					$(dropdown).val(value); // ... set it
          // we have to handle the meta selector separately, as simply triggering
          // its change event will actually push a new state. We don't want that,
          // as we are in the middle of popping an old state. So we use the
          // replaceStrategy parameter of the change callback for the meta
          // selector.
          if (dropdown === 'select[name="meta"]') {
            $(dropdown).trigger('change', [2]);
          } else {
            $(dropdown).trigger('change');
          }
				}
			})
		}
	});

  // convenience function to convert a query string to an array of arrays
  // input: ?foo=bar&baz=boo, output: [['foo', 'bar'], ['baz', 'boo']]
  function parseSearchString(params) {
    params = params.replace(/^\?/, ''); // strip leading ?
    params = params.split('&');
    params = params.map(function (param) {
      return param.split('=')
    });
    return params;
  }

  // convenience function to build an array of [['foo', 'bar'], ['baz', 'boo']]
  // back to a search string, i.e. the reverse of the above.
  function buildSearchString(params) {
    params = params.map(function (param) {
      return param.join('=')
    });
    params = params.join('&');
    params = '?' + params;
    return params;
  }

  // convenience function to merge search params given two arrays of
  // [['foo', 'bar'], ['baz', 'boo']]. The latter will take precedence over
  // the former
  function mergeSearchParams(params1, params2) {
    // if any of the new search params exist in the old search params,
    // remove the old params
    params1 = params1.filter(function (oldParam) {
      return !params2.some(function (newParam) {
        return newParam[0] === oldParam[0]
      });
    });
    // ... and replace them with their new counterparts
    return params1.concat(params2);
  }

	// convenience function for making AJAX requests
	function requestText(url) {
		return $.ajax({
			url: url,
			method: 'GET',
			dataType: 'html'
		})
	}

	// convenience function for getting text via AJAX based on the paginator form in the template
	function getManuscript(elem, urlPrefix) {
		var baseUrl = '';
		if (elem.is('select')) {
			baseUrl = elem.children(':selected').attr('data-ajax-url');
		} else if (elem.is('a')) {
			baseUrl = elem.attr('href');
		}
		if (baseUrl) {
			return requestText(urlPrefix + baseUrl);
		}
		var form = elem.closest('form');
		var elements = form.get(0).elements; // .get(0) to convert to DOMElement
		var qstring = $.map(elements, function(element, idx) {
			return element.name + '=' + element.value;
		});
		qstring = '/?' + qstring.join('&') + '&text_only=1';

		return requestText(qstring)
	}

	// convenience function to update text wrapper with result of ajax request
	function updateTextWrapper(wrapperSelector, result) {
		$(wrapperSelector).html(result)
		activateNotesInLeftColumn(); // generate new popups as these new ones weren't ready when we initialized the page
		activateNotesInRightColumn();

    if (wrapperSelector === '.chapter-box') {
      try {
        initMusic(loc); // call initMusic from MeiAjax.js
      } catch (e) {
        console.warn('there was an error calling initMusic in MeiAjax.js', e);
      }
    }
	}

	// event handler for pagination in left-hand text
	function paginateText (e) {
		e.preventDefault(); // prevent links from being followed (arrow buttons)
		e.stopPropagation(); // prevent the form from submitting

		$('.chapter-box').addClass('loading');
		getManuscript($(this), '/text')
		.done(function(result) {
			updateTextWrapper('.chapter-box', result);
			$('.chapter-box').removeClass('loading');
		})
		.done(function(){
			var textPath = this.url.replace(/^\/text/, ''); // strip leading '/text' as we don't want it to show in the URL. this.url refers to the url property of the ajax method
      textPath = textPath.indexOf('?') === -1 ? textPath + window.location.search : textPath;
      textPath = textPath.indexOf('#') === -1 ? textPath + window.location.hash : textPath;
			pushToHistory(textPath);
			// window.scrollTo(window.pageXOffset, 0); // scroll to top, but keep x scroll position
		})
		.fail(function() {
			showStatusPopup(__[loc]('Der skete en fejl. Teksten kunne ikke indlæses.'));
		})

		// also get any notes for the notes tab
		// with the getManuscript as AJAX request
		updateCommentBox(getManuscript($(this), '/notes'));
	}

	// show status popup
	function showStatusPopup(statusText) {
		var popup = $('body').append($('<div/>', {
			'class': 'ajax-status',
			'text': statusText
		}));
		setTimeout(function () {
			var statusBox = $('.ajax-status')
			statusBox.addClass('move-left'); // move the notice to the left
			setTimeout(function () {
				statusBox.remove();
			}, 300); // delete the element from the DOM after 300ms, corresponding to CSS transition duration
		}, 3000); // hide notice after 3s
	}

	// handle comment box
	function updateCommentBox(jqXHR) {
		var commentBox = $('#comments');
		var commentTab = $('[href="#comments"]').closest('li');
		commentBox.scrollTop(0);
		commentBox.addClass('loading');
		jqXHR.done(function(result) {
			commentBox.removeClass('loading');
			if (result.length > 1) { // only show the comment tab if there are comments to show
				commentBox.removeClass('hidden');
				commentTab.removeClass('hidden');
				// activateTab('#comments');
				updateTextWrapper('#comments', result);
			} else {
				commentBox.addClass('hidden');
				commentTab.addClass('hidden');
				// if the comment tab was active, simply activate the first visible tab instead
				if ($('#tabs > div > div').index($('#comments')) == $('#tabs').tabs('option', 'active')) {
					var firstVisibleTab = getFirstVisibleTab();
					activateTab(firstVisibleTab.attr('id'));
				}
			}
		})
		.fail(function() {
			showStatusPopup(__[loc]('Der skete en fejl. Kommentarer kunne ikke indlæses.'));
		});
	}

	// activate tab by id
	function activateTab(tabId) {
		tabId = tabId.replace(/^#/, ''); // strip any leading hashmark
		var tabIndex = $('#tabs > div > div').index($('#' + tabId));
		if (tabIndex >= 0) {
			$('#tabs').tabs('option', 'active', tabIndex);
		} else {
			$('#tabs').tabs('option', 'active', 0);
		}
	}

  // get first visible tab
  function getFirstVisibleTab() {
    return $('#tabs > div > div:not(.hidden)').eq(0)
  }

	// push a state to the history stack
	function pushToHistory(url, replace) {
		var dropdowns = ['#translations select[name="chapter"]', 'select[name="meta"]', 'select[name="language"]']; // CSS selectors for the dropdowns whose state we want to (re)load on popstate
		var stateObj = {}

		dropdowns.forEach(function (dropdown) { // add the current value of all the relevant dropdowns to the state obj
			stateObj[dropdown] = $(dropdown).val()
		});
		if (replace) {
			return history.replaceState(stateObj, '', url);
		}
		return history.pushState(stateObj, '', url);
	}

  // clicking a facsimile link should show it in the right-hand pane.
  $('.chapter-box, #meta-wrapper, #facsimile-tab').on('click', '.facsimile-link, .facsimile-pagination', function(e) {
    e.preventDefault();
    var pg = $(this).text();
    var href = $(this).attr('href');
    var filenameRegex = /[^\/]+$/;
    // check if the image exists
    $.ajax({
      url: href,
      method: 'HEAD',
      complete: function (jqXHR, status) {
        var injectedHtml = '';
        var status = jqXHR.status;

        var facsimileList = [
          {
            name: 'E1',
            file: '001.jpg'
          },
          {
            name: 'E57',
            file: '057.jpg'
          },
          {
            name: 'E58',
            file: '058.jpg'
          }
        ]

        // can't use Array.prototype.findIndex in IE11, so use .map.indexOf
        var currentFacsimileIndex = facsimileList.map(function (facsimile) {
          return facsimile.file
        }).indexOf(href.match(filenameRegex)[0])

        var prevFacsimile = null
        var nextFacsimile = null
        if (currentFacsimileIndex > 0) {
          prevFacsimile = facsimileList[currentFacsimileIndex - 1]
        }
        if (currentFacsimileIndex < facsimileList.length - 1) {
          nextFacsimile = facsimileList[currentFacsimileIndex + 1]
        }

        var buttonPrev = prevFacsimile ? '<a class="btn btn-primary arrow-l facsimile-pagination" href="' +
          href.replace(filenameRegex, prevFacsimile.file) + // replace the last path segment of our original URL with our new image
          '" aria-label="' + __[loc]('Bladr til forrige faksimile') + '">' +
          '<span class="sr-only">' + prevFacsimile.name + '</span>' +
          '</a>' : '';

        var buttonNext = nextFacsimile ? '<a class="btn btn-primary arrow-r facsimile-pagination" href="' +
          href.replace(filenameRegex, nextFacsimile.file) + // replace the last path segment of our original URL with our new image
          '" aria-label="' + __[loc]('Bladr til næste faksimile') + '">' +
          '<span class="sr-only">' + nextFacsimile.name + '</span>' +
          '</a>' : '';

        if (status === 200) {
          injectedHtml = '<div class="facsimile-thumb">' + '<span class="facsimile-title">' +
            __[loc]('Faksimile af side') + ' ' +
            pg + '</span>' +
            '<div class="facsimile-wrapper">' +
            buttonPrev +
            '<a href="' + href + '" target="_blank">' +
            '<img src="' + href + '" alt="">' +
            '<span>' + __[loc]('Se en stor udgave af') + ' ' + pg + '</span>' +
            '</a>' +
            buttonNext +
            '</div></div>';
        }
        else {
          injectedHtml = '<div class="facsimile-thumb">' + '<span class="facsimile-title">' +
            __[loc]('Faksimilen') + ' ' + pg + ' ' + __[loc]('kunne ikke findes') +
            '</span><div class="facsimile-wrapper">' +
            buttonPrev +
            buttonNext +
            '</div></div>';
        }

        $('#facsimile-tab').html(injectedHtml);
        activateTab('#facsimile');
      }
    });
  });
});

function checkCookie()
{
	var cookies = document.cookie;
	var cookie_start = cookies.indexOf('cookieAccept');

	if (cookie_start === -1) {
		var html = '<div class="cookies"><div class="container"><div class="row"><div class="col-md-12"><div class="left"><h1>Acceptér cookies fra siden her</h1><button>Acceptér</button><a href="#" class="">Læs mere om cookies</a></div><div class="right"><p>Danicum Diplomatarium bruger cookies til at indsamle oplysninger om brugen af webstedet. Du kan altid slette cookies fra Danicum Diplomatariumt igen, hvis du ønsker. Når du accepterer cookies bliver denne bjælke ikke længere vist.</p></div></div></div></div></div>';
		$('body').prepend(html);

		$('.cookies button').on('click', function(){
			var date = new Date();
			var days = 365;

			date.setTime(date.getTime() + (days*24*60*60*1000));
			var expires = '; expires=' + date.toGMTString();

			document.cookie = 'cookieAccept=yes; ' + expires;
			$('.cookies').hide();
		});
	}
}

function setCookie(name,value,days) {
    var expires = "";
    if (days) {
        var date = new Date();
        date.setTime(date.getTime() + (days*24*60*60*1000));
        expires = "; expires=" + date.toUTCString();
    }
    document.cookie = name + "=" + (value || "")  + expires + "; path=/";
}

function colorAllNotes(checkbox, note_class, background_color) {
  if (checkbox.checked) {
    $(note_class).each(function() {
      $(this).css({
        'backgroundColor': background_color,
        cursor: 'pointer'
      });
    });
    setCookie(note_class, 'checked', 365);
  } else {
    $(note_class).each(function() {
      $(this).css({
        'backgroundColor': 'transparent',
        cursor: 'default'
      });
    });
    setCookie(note_class, '', 365);
  }
}

function enableDictLookup (checkbox) {
	if(checkbox.checked) {
		setCookie('.clickLookup', 'checked', 365);
	}
	else {
		setCookie('.clickLookup', '', 365);
	}
}

function colorAllNotesByCookie(checkbox, note_class, background_color) {
/* if (getCookie(note_class) != 'checked') { } */
}



function colorAllTextCriticalNotes(checkbox, note_class, cookie_name, background_color) {
  if (checkbox.checked) {
    $(note_class).each(function() {
      $(this).css({
        color: background_color,
        display: 'inline',
        cursor: 'pointer',
        visibility: 'visible'
      });
      $(this).removeClass('hidden');
    });
    setCookie(cookie_name, 'checked', 365);
  } else {
    $(note_class).each(function() {
      $(this).css({
        display: 'none',
        cursor: 'default',
        visibility: 'hidden'
      });
    });
    setCookie(cookie_name, '', 365);
  }
  // determine whether notes should be shown in MeiAjax.js
  // note the variable name! It should not be "enableComments" here,
  // as this variable name is only used upon initialization. Instead,
  // we should change "comments" directly as this is the variable eventually
  // evaluated during initMusic()
  comments = checkbox.checked
}
