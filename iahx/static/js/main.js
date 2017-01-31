var isOldIE = $("html").is(".lt-ie9");
var Portal = {
	Init: function() {
		$(".showTooltip").tooltip();

		$(".mainNav .menu").on("click",function(e) {
			e.preventDefault();

			var t = $(this),
				d = t.data("rel");

			d = $(d,".mainNav");

			if(d.is(":visible")) {
				t.removeClass("opened");
				d.slideUp("fast");
			} else {
				t.Class("opened");
				d.slideDown("fast");
			}
		});

		$(".shareFacebook,.shareTwitter,.shareDelicious,.shareGooglePlus,.shareLinkedIn,.shareReddit,.shareStambleUpon,.shareCiteULike,.shareMendeley").on("click",function(e) {
			e.preventDefault();

			var url = escape(this.href),
				links = {
					"facebook": "https://www.facebook.com/sharer/sharer.php?u=",
					"twitter": "https://twitter.com/intent/tweet?text=",
					"delicious": "https://delicious.com/save?url=",
					"googleplus": "https://plus.google.com/share?url=",
					"linkedin": "http://www.linkedin.com/shareArticle?mini=true&url=",
					"reddit": "http://www.reddit.com/submit?url=",
					"stambleupon": "http://www.stumbleupon.com/submit?url=",
					"citeulike": "http://www.citeulike.org/posturl?url=",
					"mendeley": "http://www.mendeley.com/import/?url="
				},
				go2 = "";
			if($(this).is(".shareFacebook"))
				go2 = links.facebook + url;
			else if($(this).is(".shareTwitter"))
				go2 = links.twitter + url;
			else if($(this).is(".shareDelicious"))
				go2 = links.delicious + url;
			else if($(this).is(".shareGooglePlus"))
				go2 = links.googleplus + url;
			else if($(this).is(".shareLinkedIn"))
				go2 = links.linkedin + url;
			else if($(this).is(".shareReddit"))
				go2 = links.reddit + url;
			else if($(this).is(".shareStambleUpon"))
				go2 = links.stambleupon + url;
			else if($(this).is(".shareCiteULike"))
				go2 = links.citeulike + url;
			else if($(this).is(".shareMendeley"))
				go2 = links.mendeley + url;

			window.open(go2,'share');
		});

		$(".sendViaMail").on("click",function(e) {
			e.preventDefault();
			$("#SendViaEmail").modal("show");
		});

		$(".showBlock").on("click",function() {
			var t = $(this),
				rel = t.data("rel"),
				hide = t.data("hide");

			$(rel).find("input:text,textarea").val("");
			$(rel).slideDown("fast");
			$(hide).hide();
		});

		$(".showFloatInfo").on("click",function() {
			var cmd = $(this).data("rel");
			cmd = cmd.split(";");

			$("a",cmd[0]).removeClass("selected");
			$(cmd[2]).hide();

			if(cmd[1] != "null") {
				$(this).addClass("selected");
				$(cmd[1]).fadeIn("fast");
			}
		});

		$(".slider").each(function() {
			var container = $(this);
				itens = container.find(".slide-item"),
				wrapper = container.find(".slide-wrapper"),
				prev = container.find(".slide-back"),
				next = container.find(".slide-next"),
				itemProps = {
					w: itens.eq(0).outerWidth(),
					h: itens.eq(0).outerHeight()
				},
				wrapperWidth = (itens.length*itemProps.w)+100,
				containerWidth = container.find(".slide-container").outerWidth();

			wrapper.width(wrapperWidth);
			container.find(".slide-container").height(itemProps.h);

			prev.css("top",(itemProps.h/2)+"px");
			next.css("top",(itemProps.h/2)+"px");

			prev.hide();
			if(wrapper.width() <= container.width()) {
				next.hide();
			}

			prev.on("click",function(e) {
				e.preventDefault();
				var left = wrapper.css("left") == "auto" ? 0 : parseInt(wrapper.css("left"));

				wrapper.animate({
					left: "+="+itemProps.w
				},300,function() {
					var nLeft = wrapper.css("left") == "auto" ? 0 : parseInt(wrapper.css("left"));
					if(nLeft == 0)
						prev.hide();
				});
				next.show();

			});

			next.on("click",function(e) {
				e.preventDefault();
				var left = wrapper.css("left") == "auto" ? 0 : parseInt(wrapper.css("left"));

				wrapper.animate({
					left: "-="+itemProps.w
				},300,function() {
					var nLeft = wrapper.css("left") == "auto" ? 0 : parseInt(wrapper.css("left"));
					if(nLeft <= -(wrapperWidth-containerWidth-100))
						next.hide();
				});
				prev.show();
			});
		});

		$(".alternativeHeader").each(function() {
			var menu = $(".mainMenu nav ul").html();
			$(this).find("nav ul").html(menu);
		});

		var headerHeight = $("header").outerHeight();
		$(window).on("scroll",function() {
			var y = window.scrollY > 0 ? window.scrollY : (window.pageYOffset > 0 ? window.pageYOffset : document.documentElement.scrollTop);

			if(y > headerHeight) {
				$(".alternativeHeader").stop(true,false).animate({
					top: "0"
				},200);
			} else {
				$(".alternativeHeader").stop(true,false).animate({
					top: "-60px"
				},200);
			}
		});

		$(".expandCollapseContent").on("click",function(e) {
			e.preventDefault();

			var idx = $("#issueIndex"),
				info = $("#issueData"),
				t = this;

			idx.css("float","right");

			if(info.is(":visible")) {
				info.fadeOut("fast",function() {
					idx.animate({
						width: "100%"
					},300);
					$(t).find(".glyphBtn").removeClass("opened").addClass("closed");
				});
			} else {
				idx.animate({
					width: "75%"
				},300,function() {
					info.fadeIn("fast");
					$(t).find(".glyphBtn").removeClass("closed").addClass("opened");
				});
			}

			$(t).tooltip("hide");

		});

		$(".collapse-title").on("click",function() {
			var t = $(this),
				ctt = t.next(".collapse-content");

			if(ctt.is(":visible")) {
				ctt.slideUp("fast");
				t.addClass("closed");
			} else {
				ctt.slideDown("fast");
				t.removeClass("closed");
			}
		});

		$(".goto").on("click",function(e) {
			e.preventDefault();

			var d = $(this).attr("href");
			d = d.replace("#","");

			var p = $("a[name="+d+"]").offset();

			$("html,body").animate({
				scrollTop: (p.top-60)
			},500);
		});


		$(".trigger").on("click",function(e) {
			e.preventDefault();
			var obj = $(this).data("rel");

			$(obj).click();
		});

		$("input[name='link-share']").focus(function() {
			$(this).select();
			if (window.clipboardData && clipboardData.setData) {
				clipboardData.setData('text', $(this).text());
			}
		}).mouseup(function(e) {
			e.preventDefault();
		});
	}
},
searchFormBuilder = {
	SearchHistory: "",
	Init: function() {
		var p = "form.searchFormBuilder";
		var lang = document.language.lang.value;

		searchFormBuilder.SearchHistory = Cookie.Get("searchHistory");

		$(p).on("submit",function(e) {

			var historyQuery = $.trim($("#iptQuery").text());

			var expr = $("*[name='q[]']",p),
				connector = $("select[name='bool[]']",p),
				idx = $("select[name='index[]']",p),
				searchQuery = "";

			for(var i=0,l=expr.length;i<l;i++) {
				if ( $(expr[i]).attr('id') == 'iptQuery' ){
					var v = $(expr[i]).text();
				}else{
					var v = $(expr[i]).val();
				}
				if(v != "") {
					var ci = $("option:selected",idx[i]).val();

					if(i >= 1) {
						var b = $("option:selected",connector[i-1]).val();
						searchQuery += " "+b+" ";
					}
					if(ci != "") {
						searchQuery += "("+ci+":("+v+"))";
					} else {
						searchQuery += (l == 2 ? v : "("+v+")");
					}
				}
			}
			var where = $("input[name='collection']:checked",p).val();

			if (where !== undefined && where != ''){
				// check if filter by collection is not defined
				if ( $("input[name='filter[in][]']").length == 0){
					initial_filter_in = $('<input>').attr({type: 'hidden', name: 'filter[in][]', value:'scl'}).appendTo('#searchForm');
				}
			}

			var search_by_year = $("input[name='publicationYear']:checked",p).val();
			if (search_by_year == "1"){
				var pub_year_start =  $("select[name='y1Start'] option:selected",p).val();
				if (pub_year_start != ''){
					searchQuery += ' AND publication_year:[' + pub_year_start + ' TO *]';
				}
			}else if(search_by_year == "2"){
				var pub_year_start =  $("select[name='y2Start'] option:selected",p).val();
				var pub_year_end =  $("select[name='y2End'] option:selected",p).val();
				if (pub_year_start != '' && pub_year_end != ''){
					searchQuery += ' AND publication_year:[' + pub_year_start + ' TO ' + pub_year_end + ']';
				}
			}

			// remove boolean operators from begining or end of query
			searchQuery = searchQuery.replace(/^AND|AND$|^OR|OR$/g, "");

			if (searchQuery == ''){
				searchQuery = '*';
			}
			searchQuery = $.trim(searchQuery);

			var total = 0;
			var form = document.searchForm;
			var form_action = form.action;
			var form_params = 'q=' + searchQuery;

			get_result_total(form_action, form_params, function(total){
				if (total == 0){
					$("#ResultArea").hide();
					$("#NoResults").removeClass('hide');
					$("#TotalHits").html('0');
					// send query again to register in history
					send_query_to_history(form_action, form_params);
					// update same page with no result message
					if (historyQuery != ''){
						var form = document.updateHistoryPage;
						$("#updateHistoryPage #clear").val("");
						$("#updateHistoryPage #noresult").val("true");
    					$("#updateHistoryPage").submit();
					}else{
						// increment history data on page
						var history_number = parseInt($(".searchHistoryItem").data("history"));
						$(".searchHistoryItem").data("history", history_number + 1);
						$(".searchHistoryItem").html("#" + (history_number + 1));
						$("#searchHistoryQuery").html(searchQuery);
					}
				}else{
					// delete filters and other form parameters
					$("input[type='hidden']").remove();
					var searchForm = document.searchForm;
					// clear my_selection list
					manipulate_bookmark('c');
					// execute search
					$('<input>').attr({type: 'hidden', name: 'q', value:searchQuery}).appendTo('#searchForm');
					$('<input>').attr({type: 'hidden', name: 'lang', value:lang}).appendTo('#searchForm');
					$('<input>').attr({type: 'hidden', name: 'page', value:'1'}).appendTo('#searchForm');
					searchForm.submit();
				}
			});

			return false;
		});

		$("textarea.form-control:visible",p).on("keyup",searchFormBuilder.TextareaAutoHeight).trigger("keyup");
		$("a.clearIptText",p).on("click",searchFormBuilder.ClearPrevInput);

		$(p).on("keypress",function(e) {
			if(e.keyCode == 13)
				$(p).submit();
		});


		if($(".searchActions").length)
			window.searchActionsStart = $(".searchActions").offset().top;

		$(".newSearchField",p).on("click",function(e) {
			e.preventDefault();
			searchFormBuilder.InsertNewFieldRow(this,"#searchRow-matriz .searchRow",".searchFormBuilder .searchRow-container");
		});

		$("select.setMinValue").on("change",function() {
			var v = $(this).val(),
				d = $(this).data("rel");

			var dv = $(d).val();
			v = parseInt(v);
			dv = parseInt(dv);

			if(dv < v)
				$(d).val("0");

			$("option",d).each(function() {
				var iv = parseInt($(this).text());
				if(iv <= v)
					$(this).prop("disabled",true);
				else
					$(this).prop("disabled",false);
			});
		});

		$(".collapseBlock .title a.action").on("click",function() {
			var t = $(this),
				ctt = t.parent().next(".content");

			if(ctt.is(":visible")) {
				ctt.slideUp("fast");
				t.addClass("closed").removeClass("opened");
				t.parent().addClass("closed");
			} else {
				ctt.slideDown("fast");
				t.addClass("opened").removeClass("closed");
				t.parent().removeClass("closed");
			}
		});

		$(".collapseBlock .filterCollapsedList",p).each(function() {
			var t = $(this),
				chd = t.find(".filterItem"),
				showAll = $(".showAll",t);

			if(chd.length > 5) {
				showAll.show();
			}
		});

		$(".collapseBlock .showAll",p).on("click",function() {
			var t = $(this),
				pt = t.parent(),
				txtToggle = t.data("texttoggle"),
				txt = t.text();

			if(pt.outerHeight() > 200) {
				pt.removeClass("opened");
			} else {
				pt.addClass("opened");
			}
			t.text(txtToggle).data("texttoggle",txt);
		});

		$(".collapseBlock .filterCollapsedList input:checkbox").on("click",function() {
			$("#apply_filters_button").removeProp("disabled");
		});

		$(".articleAction, .searchHistoryItem, .colActions .searchHistoryIcon",p).tooltip();

		$(".selectAll").on("click",function() {

			var t = $(this),
				itens = $(".results .item input.checkbox",p),
				selCount = $("#selectedCount",p),
				selCountInt = parseInt(selCount.text());

			if(t.is(":checked")) {
				itens.each(function() {
					$(this).prop("checked",true);
				});
				t.data("all","1");
			} else {
				itens.each(function() {
					$(this).prop("checked",false);
				});
				t.data("all","0");
			}
			searchFormBuilder.CountCheckedResults("#selectedCount",".results .item input.checkbox:checked");
		});

		$(".clusterSelectAll").on("click",function() {
			var t = $(this),
				itens = $("#selectClusterItens .filterBody input.checkbox"),
				checked = t.is(":checked");

			itens.each(function() {
				$(this).prop("checked",checked);
				$(this).trigger("change");
			});
			
			if(checked) {
				t.data("all","1");
			} else {
				t.data("all","0");
			}
		});

		$(".results .item input.checkbox").on("change",function() {
			var t = $(this),
				selAll = $(".selectAll",p),
				selCount = $("#selectedCount",p),
				selCountInt = parseInt(selCount.text());

			if(!t.is(":checked")) {
				var all = selAll.data("all");
				if(all == "1") {
					selAll.prop("checked",false).data("all","0");
				}
			}

			// Executar aqui ações para adicionar item à "sua lista"

			searchFormBuilder.CountCheckedResults("#selectedCount",".results .item input.checkbox:checked");
		});

		$("#form_clusters input.checkbox").on("change",function() {
			var t = $(this);
			var tvalue = t.val();
			var tid = t.attr('id');
			var cluster_id = tid.substr(0, tid.lastIndexOf('_'));
			var tall_option = $("#" + cluster_id + "_ALL");
			var itens = $("#form_clusters #ul_" + cluster_id + " input.checkbox");

			if (tvalue != '*' && tall_option.is(":checked")){
				tall_option.prop("checked", false);
			} else if (tvalue == '*') {
				itens.each(function() {
					if ( $(this).val() != '*' ){
						$(this).prop("checked",false);
					}
				});
			}

		});

		$("a.orderBy").on("click",function() {
			var t = $(this),
				field = t.data("field"),
				container = $(t.data("rel")),
				sort_items = [],
				group = t.data("group");

			if(typeof group !== "undefined") {
				var groupItens = $("a.orderBy[data-group='"+group+"']");
				groupItens.removeClass("orderBy_selected");
			}

			t.addClass("orderBy_selected");

			$(".filterItem",container).each(function() {
				var ti = $(this),
					val = ti.data(field),
					arr = [];

				if(!isNaN(parseInt(val))) {
					val = parseInt(val);
				}
				arr.push(val);
				arr.push(ti);
				sort_items.push(arr);
				ti.remove();
			});

			if(typeof sort_items[0][0] === "number")
				sort_items.sort(function(a, b){return b[0]-a[0]});
			else
				sort_items.sort(function (a, b) {
    				return a.toString().localeCompare(b);
				});

			for(var i=0;i<sort_items.length;i++) {
				container.append(sort_items[i][1]);
			}
		});


		$(".openNewWindow").on("click",function(e) {
			e.preventDefault();

			window.open(this.href,'print','width=760,height=550');
		});

		$(".openSelectItens").on("click",function(e) {
			e.preventDefault();

			var t = $(this),
				rel = t.data("rel"),
				filter_id = t.data("filter"),
				filter_label = t.data("label"),
				mod = $("#selectClusterItens"),
				modContainer = $(".filterBody",mod),
				modTitle = $(".modal-title",mod);

			var lang = document.language.lang.value;
			// get itens from modal window
			var modal_filter_id = "#filter_" + filter_id

			$("#orderby_results").data("rel", modal_filter_id).addClass("orderBy_selected");
			$("#orderby_alpha").data("rel", modal_filter_id).removeClass("orderBy_selected").html(filter_label);
			$("#statistics").data("cluster", filter_label);
			$("#statistics").data("chartsource", modal_filter_id);
			$("#exportcsv").data("cluster", filter_label);
			$("#exportcsv").data("chartsource", modal_filter_id);
			var selAll = $("#selectClusterItens_all");
			var filter_all = $("#" + filter_id + "_ALL");

			selAll.attr("name", "filter[" + filter_id + "][]");
			if ( filter_all.is(":checked") ) {
				selAll.prop("checked",true);
				selAll.data("all", "1");
			}else{
				selAll.prop("checked",false);
				selAll.data("all", "0");
			}

			modTitle.html(filter_label);
			modContainer.empty();

			var select_form = $("#selectClusterItensForm");
		    $.ajax({ // create an AJAX call...
		        data: select_form.serialize(), // get the form data
		        type: 'GET', 				   // GET or POST
		        url: 'list-filter/' + filter_id + '?lang=' + lang, // the file to call
				beforeSend: function() {
					$('.filterBody').html('<img src="' + STATIC_URL + 'image/loading.gif" style="margin-left:190px"/>');
				},
		        success: function(response) { // on success..
					$('.filterBody').html(response); // update the DIV

					$('.filterBody input.checkbox').off("change.enableBtn").on("change.enableBtn",function() {
						var counter = $(".filterBody input.checkbox:checked").length,
							btn = $(".cluster-actions-menu a.singleBtn");

						if(counter > 0) {
							btn.removeClass("singleBtn_disabled").tooltip("disable");
						} else {
							btn.addClass("singleBtn_disabled").tooltip("enable");
						}
					});
		        }
		    });
			mod.modal("show");

		});

		$("#selectClusterItens").on("click", ".filterBody input.checkbox", function() {
			var t = $(this);
			var selAll = $(".clusterSelectAll");

			$("#no_cluster_selected").slideUp("fast");
			if(t.is(":checked")) {
				var all = selAll.data("all");
				if(all == "1") {
					selAll.prop("checked",false);
					selAll.data("all","0");
				}
			}
		});


		$("#SendViaEmail,#Export").on("shown.bs.modal",function() {
			var t = $(this),
				selection = parseInt($("#selectedCount").text());

			t.find("input:eq(0)").focus();

			if(selection > 0) {
				t.find(".selection").show();
				t.find(".selection strong").text(selection);
			} else {
				t.find(".selection").hide();
			}
		});

		$("form.validate").on("submit",function() {
			var rtn = true;

			$("input.valid",this).each(function() {
				var ti = $(this);

				if(ti.is(".multipleMail")) {
					if(Validator.MultipleEmails(ti.val(),";") === false) {
						ti.parent().addClass("has-error");
						rtn = false;
					} else
						ti.parent().removeClass("has-error");
				} else {
					if(ti.val() === "") {
						ti.parent().addClass("has-error");
						rtn = false;
					} else
						ti.parent().removeClass("has-error");
				}
			});

			return rtn;
		});

		$(".searchHistoryIcon.add",p).on("click",function() {
			$("html, body").animate({ scrollTop: 0 }, "fast");
			searchFormBuilder.InsertSearchHistoryItem(this);
		});
		$(".searchHistoryIcon.search",p).on("click",function() {
			$("#iptQuery").empty();
			searchFormBuilder.InsertSearchHistoryItem(this);
			$("#searchHistoryForm").submit();
		});
		$(".searchHistoryIcon.erase",p).on("click",function(e) {
			e.preventDefault();
			var $item = $(this).data("item");
			$("#confirmEraseItem span.item").text($item);
			$("#confirmEraseItem input.item").val($item);

			$("#confirmEraseItem").modal("show");
		});
		$(".searchHistoryIcon.eraseAll",p).on("click",function(e) {
			e.preventDefault();

			$("#confirmEraseAll").modal("show");
		});

		$("#iptQuery").on("keypress",function(e) {
			if(e.keyCode == 13)
				$("#searchHistoryForm").submit();
		});

		$(".showTooltip").tooltip();

		$("input[data-show!=''],input[data-hide!='']").on("click",function() {
			var s = $(this).data("show"),
				h = $(this).data("hide");

			if(typeof s != "undefined")
				$(s).slideDown("fast").find("input[type='radio']:eq(0)").trigger("click");

			if(typeof h != "undefined")
				$(h).slideUp("fast");

		});

		$(".searchModal").on("click",function() {
			var d = $(this).data("modal"),
				expr = $(this).data("expr");

			$(".searchExpression",d).text(expr);
			$("#clipboardSearchExpression").val(expr);

			$(d).modal("show");
		});

		$(".editQuery").on("click",function() {
			var d = $(this).data("modal"),
				expr = $(this).data("expr"),
				q = $("#iptQuery");

			q.append(expr).focus();
			$(this).effect("transfer", { to: q }, 1000);
			searchFormBuilder.PlaceCaretToEnd(document.getElementById("iptQuery"));
		});

		$(".openCitationModal").on("click",function() {
			var modal = $("#CitationModal"),
				title = $(this).data("title");
				citationContainer = $("#CitationModal-Citations"),
				downloadContainer = $("#CitationModal-Downloads"),
				citation = $(this).data("citation"),
				citationCtt = "",
				download = $(this).data("download"),
				downloadCtt = "";

			if(typeof citation != "undefined" && typeof download != "undefined") {
				citation = citation.split(";;");
				for(var i=0,l=citation.length;i<l;i++) {
					citation[i] = citation[i].split("::");
					citation[i][1] = citation[i][1].replace(/</g,"&lt;").replace(/>/g,"&gt;").replace(/\[b\]/g,"<strong>").replace(/\[\/b\]/g,"</strong>");

					citationCtt += '<div class="modal-body searchExpression">';
					citationCtt += '	<label>'+citation[i][0]+'</label>';
					citationCtt += '	<div>'+citation[i][1]+'</div>';
					citationCtt += '</div>';
				}

				download = download.split(";;");
				for(var i=0,l=download.length;i<l;i++) {
					download[i] = download[i].split("::");

					downloadCtt += '<a href="'+download[i][1]+'" target="_blank" class="download">'+download[i][0]+'</a> ';
				}

				citationContainer.html(citationCtt);
				downloadContainer.html(downloadCtt);

				modal.find(".modal-title strong").html(title);
				modal.modal("show");
			}
		});

		$("#apply_filters_button").on("click",function(e) {
			var form = $("#form_clusters");
			var form_action = form.attr('action');
			var form_params = form.serialize();

			var total = 0;
			get_result_total(form_action, form_params, function(total){
				if (total == 0){
					$("#ResultArea").hide();
					$("#NoResults").removeClass('hide');
					$("#TotalHits").html('0');
					$('html,body').animate({
					    scrollTop: 0
					}, 700);
					// send query again to register in history
					send_query_to_history(form_action, form_params);
					// increment history data on page
					var history_number = parseInt($(".searchHistoryItem").data("history"));
					$(".searchHistoryItem").data("history", history_number + 1);
					$(".searchHistoryItem").html("#" + (history_number + 1));
				}else{
					// clear my_selection list
					manipulate_bookmark('c');
					form.submit();
				}
			});
			return false;
		});

		$("input.onlyNumbers").on("keydown",function(e) {
			if($.inArray(e.keyCode, [46, 8, 9, 27, 13, 110]) !== -1 ||
				// Ctrl+A
				(e.keyCode == 65 && e.ctrlKey === true) ||
				// Ctrl+V
				(e.keyCode == 86 && e.ctrlKey === true) ||
				// Ctrl+R
				(e.keyCode == 82 && e.ctrlKey === true) ||
				// home, end, left, right
				(e.keyCode >= 35 && e.keyCode <= 39) ||
				// macosX keycodes
				(!e.shiftKey && (e.keyCode >= 48 && e.keyCode <= 57))
				) {
					return;
			} else {
				e.preventDefault();
			}
		}).on("blur",function() {
			var v = $(this).val();
			v = v.replace(/[A-Za-z$-.\/\\\[\]=_@!#^<>;"]/g, "");

			$(this).val(v);
		});

		$(".showContextHelper").on("focus.showContextHelper blur.showContextHelper",function(e) {
			var t = $(this),
				contextHelper = $(t.data("helper")),
				cl = "contextHelper_focus";

			if(contextHelper.length > 0) {
				if(e.type == "focus")
					contextHelper.addClass(cl);
				else {
					setTimeout(function() {
						contextHelper.removeClass(cl);
					},500)
				}
			}
		});

		$("#BuscaAjuda").on("hidden.bs.modal",function() {
			$(".showContextHelper:eq(0)").focus();
		});

		$(window).scroll(function() {
			if($(window).scrollTop() > window.searchActionsStart)
				$(".searchActions").addClass("fixed");
			else
				$(".searchActions").removeClass("fixed");
		});
	},
	InsertSearchHistoryItem: function(obj) {
		var $item = $(obj).data("item"),
			$ctt = $(obj).parent().parent().find(".colSearch").text(),
			q = $("#iptQuery"),
			shItem = '&#160;<div class="searchHistoryItem" contenteditable="false"  data-toggle="tooltip" data-placement="top" title="'+$ctt+'">#'+$item+'</div> AND&#160;';

		q.append(shItem).focus();
		q.find(".searchHistoryItem").tooltip();
		$(obj).effect("transfer", { to: q.find(".searchHistoryItem:last-child") }, 1000);
		searchFormBuilder.PlaceCaretToEnd(document.getElementById("iptQuery"));
	},
	InsertNewFieldRow: function(t,matrix,container) {
		t = $(t);
		matrix = $(matrix).clone();
		container = $(container);

		var c = t.data("count");

		matrix.attr("id","searchRow-"+c);
		matrix.find(".eraseSearchField").data("rel",c);

		matrix.find(".eraseSearchField").on("click",function(e) {
			e.preventDefault();
			searchFormBuilder.EraseFieldRow(this);
		});

		if(searchFormBuilder.SearchHistory != "") {
			matrix.find("input[name='q[]']").on("focus",function() {
				searchFormBuilder.SearchHistoryFocusIn(this);
			}).on("blur",function() {
				searchFormBuilder.SearchHistoryFocusOut(this);
			});
		}

		matrix.appendTo(container).slideDown("fast");

		matrix.find("textarea.form-control:visible").on("keyup",searchFormBuilder.TextareaAutoHeight).trigger("keyup");
		matrix.find("a.clearIptText").on("click",searchFormBuilder.ClearPrevInput);
		matrix.find(".showTooltip").tooltip();

		c = parseInt(c);
		c++;
		t.data("count",c);
	},
	TextareaAutoHeight: function() {
		$(this).css("height","auto");
		$(this).height(this.scrollHeight);
		if(this.value != "")
			$(this).next("a").fadeIn("fast");
		else
			$(this).next("a").fadeOut("fast");
	},
	ClearPrevInput: function() {
		$(this).prev("input,textarea").val("").trigger("keyup");
	},
	EraseFieldRow: function(t) {
		t = $(t);

		var i = t.data("rel");

		$("#searchRow-"+i).slideUp("fast",function() {
			$(this).remove();
		});
	},
	CountCheckedResults: function(t,r) {
		t = $(t);
		var	preSelected = parseInt(t.data("preselected")),
			selResults = parseInt($(r+":checked").length),
			c = preSelected + selResults;

		t.text(c);
		if(c > 0) {
			t.addClass("highlighted");
		} else
			t.removeClass("highlighted");
	},
	SearchHistoryFocusIn: function(t) {
		if(searchFormBuilder.SearchHistory != "") {
			var pos = $(t).offset();

			$("#searchHistory").data("rel",t).css({
				"top": (pos.top+50)+"px",
				"left": (pos.left)+"px"
			}).slideDown("fast");
		}
	},
	SearchHistoryFocusOut: function(t) {
		if(searchFormBuilder.SearchHistory != "") {
			setTimeout(function() {
				$("#searchHistory").slideUp("fast");
			},100);
		}
	},
	SearchHistoryClick: function(txt,t) {
		var txt = $(txt).text();
			txt = txt.substr((txt.indexOf(": ")+2),txt.length);

		$(t).val(txt).focus();
	},
	PlaceCaretToEnd: function(el) {
		el.focus();
	    if (typeof window.getSelection != "undefined" && typeof document.createRange != "undefined") {
			var range = document.createRange();
			range.selectNodeContents(el);
			range.collapse(false);

			var sel = window.getSelection();
			sel.removeAllRanges();
			sel.addRange(range);
		} else if (typeof document.body.createTextRange != "undefined") {
			var textRange = document.body.createTextRange();
			textRange.moveToElementText(el);
			textRange.collapse(false);
			textRange.select();
	    }
	}
},
Article = {
	TopBinder: [],
	Init: function() {
		var articleText = $("#articleText"),
			articleTextP = articleText.offset(),
			articleMenuW = $(".articleMenu").width(),
			p = $(".paragraph",articleText);

		for(var i = 0, l = p.length; i<l; i++) {
			var c = $("p",p[i]).outerHeight(), r = $(".refList",p[i]), rh = r.outerHeight();
			if(rh > c) {
				r.addClass("outer").css("height",c);
			}
		}

		$("sup",p).on("mouseenter mouseleave",function(e) {
			var c = this.className;
			c = c.replace("xref ","");
			var b = $("li."+c), p = b.parent("ul");

			if(c.indexOf(" ") >= 0) {
				c = c.split(" ");
				c = "li." + c.join(",li.");
				b = $(c);
				p = b.parent("ul");
			}
			if(e.type === "mouseenter") {
				p.addClass("full");
				b.addClass("highlight").find(".opened").fadeIn("fast");
			} else {
				p.removeClass("full");
				b.removeClass("highlight").find(".opened").hide();
			}
		});
		$(".refList li",p).on("mouseenter mouseleave",function(e) {
			var p = $(this).parent("ul");
			if(e.type === "mouseenter") {
				p.addClass("full");
				$(this).addClass("highlight").find(".opened").fadeIn("fast");
			} else {
				p.removeClass("full");
				$(this).removeClass("highlight").find(".opened").hide();
			}
		});

		$(".thumb").on("mouseenter mouseleave click",function(e) {
			var p = $(this).parent().parent().find(".preview");
			if(e.type == "mouseenter") {
				p.fadeIn("fast");
			} else if(e.type == "mouseleave") {
				p.fadeOut("fast");
			} else if(e.type == "click") {
				window.open(p.find("img").attr("src"));
			}
		});

		$(".collapseTitle").on("click",function() {
			var ctt = $(this).next(),
				ico = $(this).find(".collapseIcon");

			if(ctt.is(":visible")) {
				ctt.slideUp("fast");
				ico.removeClass("opened");
			} else {
				ctt.slideDown("fast");
				ico.addClass("opened");
			}
		});

		$(".expandReduceText").on("click",function(e) {
			e.preventDefault();
			var ref = $("#articleText .ref"),
				txt = $("#articleText .text"),
				s = $(this).data("expandreducetext"),
				tw = $(this).data("defaultwidth");

			if(typeof tw == "undefined")
				$(this).data("defaultwidth",txt.outerWidth());

			if(s == true) {
				ref.hide();
				txt.outerWidth("100%");

				$(this).data("expandreducetext",false);
			} else {
				txt.width(tw);
				ref.hide();

				$(this).data("expandreducetext",true);
			}

			var t = $(window).scrollTop();
			setTimeout(function() {
				Article.ArticleStructureBuilder();
				Article.ArticleStructureSelect(t);
			},100);


		});

		$(".articleTxt sup.xref:not(.big)").on("click",function() {
			var c = $(this).text(),
				d = $(".ref-list");

			if(c.indexOf(",") == -1) {
				parseInt(c);
				c--;
			} else {
				c = c.split(",");
				c = c[0];

				parseInt(c);
				c--;
			}

			var p = $("li:eq("+c+")",d).offset();
			$("html,body").animate({
				scrollTop: (p.top-60)
			},500);
		});

		articleTextP.top = articleTextP.top - 25;
		$(window).scroll(function() {
			var t = $(window).scrollTop();
			if(t > articleTextP.top)
				$(".articleMenu").addClass("fixed").width(articleMenuW);
			else
				$(".articleMenu").removeClass("fixed");

			Article.ArticleStructureSelect(t);
		});

		var downloadOpt = $(".downloadOptions li.group"),
			downloadOptW = 100/downloadOpt.length;

		downloadOpt.css("width",downloadOptW+"%");


		Article.ArticleStructureBuilder();
	},
	ArticleStructureBuilder: function() {
		var structure = $(".articleMenu"),
			content = $("#articleText .articleSection"),
			idx = 0,
			ctt = '';

		Article.TopBinder = [];

		content.each(function() {
			var t = $(this).data("anchor"),
				h = $(this).find("h1"),
				offset = $(this).offset();

			if(idx == 0)
				Article.TopBinder.push(0);
			else
				Article.TopBinder.push(offset.top);

			if(typeof t == "undefined") return true;

			ctt += '<li '+(idx == 0 ? 'class="selected"' : '')+'>';
			ctt += '	<a href="#articleSection'+idx+'">'+t+'</a>';

			if(h.length > 1) {
				var iidx = 0;
				ctt += '<ul>';
				h.each(function() {
					var ooffset = $(this).offset();
					Article.TopBinder.push(ooffset.top);

					ctt += '<li>';
					ctt += '	<a href="#as'+idx+'-heading'+iidx+'">'+$(this).text()+'</a>';
					ctt += '</li>';

					iidx++;
				});
				ctt += '</ul>';
			}
			ctt += '</li>';

			idx++;
		});

		structure.html(ctt);

		$("a",structure).on("click",function(e) {
			e.preventDefault();

			var d = $(this).attr("href");
			d = d.replace("#","");

			var p = $("a[name="+d+"]").offset();

			$("html,body").animate({
				scrollTop: (p.top-60)
			},500);
		});
	},
	ArticleStructureSelect: function(pos) {
		var structure = $(".articleMenu"),
			idx = 0;

		for(var i=0,l=Article.TopBinder.length;i<l;i++) {
			if(pos <= (Article.TopBinder[i]-100)) {
				structure.find("li").removeClass("selected");
				structure.find("li:eq("+(i-1)+")").addClass("selected");
				break;
			}
		}

	}
};

var Validator = {
MultipleEmails: function(val,delimiter) {
	var delimiter = delimiter || ';';
	var filter  = /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
	var error = true;

	var aEmails = val.split(delimiter);

	for(var i = 0; i < aEmails.length; i++) {
		aEmails[i] = aEmails[i].trim();
		if(aEmails[i] == '' || filter.test(aEmails[i]) == false)
			error = false;
	}

	return error;
}
};

var Cookie = {
	Get: function(cookieName,path) {
		if(typeof path === "undefined") path = "";
		else path = path+"/";
		cookieName = path+cookieName;
		if (document.cookie.length > 0) {
	        c_start = document.cookie.indexOf(cookieName + "=");
	        if (c_start != -1) {
	            c_start = c_start + cookieName.length + 1;
	            c_end = document.cookie.indexOf(";", c_start);
	            if (c_end == -1) {
	                c_end = document.cookie.length;
	            }
	            return unescape(document.cookie.substring(c_start, c_end));
	        }
	    }
	    return "";
	},
	Set: function(cookieName, value, days, path) {
		var expires;
		if(typeof days !== "undefined") {
	        var date = new Date();
	        date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
	        expires = "; expires=" + date.toGMTString();
	    } else
	    	expires = "";
	    if(typeof path === "undefined") path = "";
	    else path = path + "/";

	    if(Cookie.Get(cookieName) != "") {
	    	document.cookie = path+cookieName + "=" + value + "expires=Thu, 01 Jan 1970 00:00:01 GMT" + "; path=/";
	    }
	    document.cookie = path+cookieName + "=" + value + expires + "; path=/";
	}
};

$(function() {
	Portal.Init();

	if($("form.searchFormBuilder").length)
		searchFormBuilder.Init();

	if($("#articleText").length)
		Article.Init();

	$(".goto_page").keyup(function(event){
	    if(event.keyCode == 13){
	    	new_page = $(this).val();
	        go_to_page(new_page);
	    }
	});

	$(".exportCSV").on("click",function(e) {
		e.preventDefault();

		var t = $(this),
			title = t.data("cluster"),
			chartSource = t.data("chartsource");

		var grupo = $(chartSource);
	    var lista = grupo.find('li');
		var regex = /<span>\d+<\/span>/i;
		var params= "";

	    for (i = 0; i < lista.length; i++){
			clusterSelection = lista[i].getElementsByTagName('input')[0];
			if (!clusterSelection.checked){
				continue;
			}
	        cluster = lista[i].innerHTML;
	        clusterLabel = lista[i].getElementsByTagName('label')[0].innerHTML;
			clusterLabel = clusterLabel.replace(/^\s+|\s+$/g, '');

	        ma = regex.exec(cluster);
	        if (ma != null) {
	            clusterTotal = ma[0].replace(/(<([^>]+)>)/g,'');
	            params += "&l[]=" + clusterLabel + "&d[]=" + clusterTotal;
	        }
	    }
		if (params == ""){
			$("#no_cluster_selected").slideDown("fast");
			return;
		}

	    var csvLink  = SEARCH_URL + "chartjs/?type=export-csv&title=" + title + params;
		if(isOldIE) {
			csvLink = encodeURI(csvLink);
		}
		export_win = window.open(csvLink);
	});

	$(".openStatistics").on("click",function(e) {
		e.preventDefault();

		var t = $(this),
			title = t.data("cluster"),
			chartType = t.data("type"),
			chartSource = t.data("chartsource");

		// check if has any item selected
		var grupo = $(chartSource);
		var lista = grupo.find('li');
		var any_selected = false;
		for (i = 0; i < lista.length; i++){
			clusterSelection = lista[i].getElementsByTagName('input')[0];
			if (clusterSelection.checked){
				any_selected = true;
				break;
			}
		}
		if (any_selected == false){
			$("#no_cluster_selected").slideDown("fast");
			return;
		}

		$("#Statistics").data({
			"title": title,
			"charttype": chartType,
			"chartsource": chartSource
		}).modal({
			"show": true
		});
	});

	$("#Statistics").on("shown.bs.modal",function() {
		var regex = /<span>\d+<\/span>/i;
	    var params= "";

		var t = $(this),
			chartBlock = $(".chartBlock",this),
			title = t.data("title"),
			chartType = t.data("charttype"),
			chartSource = t.data("chartsource");

		var grupo = $(chartSource);
	    var lista = grupo.find('li');

	    for (i = 0; i < lista.length; i++){
			clusterSelection = lista[i].getElementsByTagName('input')[0];
			if (!clusterSelection.checked){
				continue;
			}
	        cluster = lista[i].innerHTML;
	        clusterLabel = lista[i].getElementsByTagName('label')[0].innerHTML;
			clusterLabel = clusterLabel.replace(/^\s+|\s+$/g, '');

	        ma = regex.exec(cluster);
	        if (ma != null) {
	            clusterTotal = ma[0].replace(/(<([^>]+)>)/g,'');
	            params += "&l[]=" + clusterLabel + "&d[]=" + clusterTotal;
	        }
	    }
	    var chartDataUrl = "chartjs/?type=" + chartType + "&title=" + title + params;
	    var csvLink  = "chartjs/?type=export-csv&title=" + title + params;

		chartDataUrl = encodeURI(chartDataUrl);
		if(isOldIE) {
			csvLink = encodeURI(csvLink);
		}

		t.find(".modal-title .cluster").text(title);
		t.find(".link a").attr("href",csvLink);

		chartBlock.html('<canvas id="chart" width="950" height="400"></canvas>');

		var canvas = $("#chart").get(0);

		if(isOldIE) {
			canvas = G_vmlCanvasManager.initElement(canvas);
		}

		var ctx = canvas.getContext("2d");
		ctx.clearRect(0,0,550,400);

		$.ajax({
			url: chartDataUrl,
			type: "POST",
			dataType: "json",
			beforeSend: function() {
				chartBlock.addClass("loading");
			}
		}).done(function(data) {
			chartBlock.removeClass("loading");
			switch(chartType) {
				case "doughnut":
					window.graph = new Chart(ctx).Doughnut(data,{
						scaleGridLineWidth : 1
					});
					break;
				case "bar":
					window.graph = new Chart(ctx).Bar(data,{
						scaleGridLineWidth : 1
					});
					break;
				case "line":
					window.graph = new Chart(ctx).Line(data,{
						scaleGridLineWidth : 1
					});
					break;
				case "pie":
					window.graph = new Chart(ctx).Pie(data,{
						scaleGridLineWidth : 1
					});
					break;
				default:
					window.graph = new Chart(ctx).Pie(data,{
						scaleGridLineWidth : 1
					});
					break;
			}
		});
	}).on("hidden.bs.modal",function() {
		window.graph.clear().destroy();
		$(".chartBlock canvas",this).remove();
	});

	$(".openCitedBy").on("click",function(e) {
		e.preventDefault();
		var t = $(this),
			pid = t.data("pid");

		var article_title = $("#title-" + pid).html();
		$("#CitedBy").modal("show");
		$("#CitedBy #article_cited").html(article_title);
		// make request to citedby service
		$.ajax({
			type: "get",
			url: 'http://citedby.scielo.org/api/v1/pid/',
			data: '&q=' + pid,
			dataType: 'jsonp',
			beforeSend: function() {
				$('#CitedBy .modal-body').html('<img src="' + STATIC_URL + 'image/loading_dots.gif" style="margin-left:190px"/>');
			},
			success: function(response) { // on success..
				articles = response.cited_by;
				modal_body = $('#CitedBy .modal-body');
				label_cited = modal_body.data("label-cited");
				label_nocited = modal_body.data("label-nocited");
				if (articles.length == 0){
					modal_body.html('<h3>' + label_nocited + '</h3>');
				}else{
					modal_body.html('<strong>' + label_cited + '</strong>:');
					modal_body.append('<ul>');
					for (i = 0; i < articles.length; i++){
						article = articles[i];
						var author_list = '';
						var author_total = article.authors.length;
						for (var a = 0; a < author_total; a++){
							var author  = article.authors[a];
							author_list += author.surname + ', ' + author.given_names;
							if (a < (author_total-1)) author_list += '; ';
						}
						modal_body.append('<li><a href="' + article.url + '" target="_blank">' +
						article.titles[0] + '</a> ' + author_list + '<br/><i>' + article.source + '</i></li><br/>');
					}
					modal_body.append('</ul>');
				}
			}
		});
	});

	$(".openExport, .sendViaMail").on("click",function(e) {
		selection_count = $(".my_selection_count").html();
		total = parseInt(selection_count);
	    if(total > 0) {
			$("#export_selection_user_selection").prop('checked', true);
			$("#sendViaEmail_selection_my_selection").prop('checked', true);
		}else{
			$("#export_selection_current_page").prop('checked', true);
			$("#sendViaEmail_selection_page").prop('checked', true);
		}
	});

	$(".openJournalInfo").on("click",function(e) {
		e.preventDefault();
		var t = $(this),
			issn = t.data("issn"),
			publisher = t.data("publisher"),
			collection = t.data("collection");

		var journal_title = t.html();
		$("#JournalInfo").modal("show");
		modal_body = $('#JournalInfo .modal-body');
		modal_footer = $('#JournalInfo .modal-footer');
		modal_body.html('<h2>' + journal_title + '</h2>');

		modal_body.append('<p>' + publisher + '</p>');
		if (issn != ''){
			modal_body.append('<strong>ISSN:</strong> ' + issn + '<br/>');
		}

		// make request to citedby service
		$.ajax({
			type: "get",
			url: 'http://analytics.scielo.org/ajx/bibliometrics/journal/google_h5m5_chart?',
			data: 'journal=' + issn,
			dataType: 'jsonp',
			success: function(response) { // on success..
				console.log("sucess");
				h5_serie = response.options.series[0].data;
				h5_last = h5_serie[h5_serie.length-1];
				m5_serie = response.options.series[1].data;
				m5_last = m5_serie[h5_serie.length-1];
				year_list = response.options.xAxis.categories;
				last_year = year_list[year_list.length-1];
				modal_body.append('<strong>Google Scholar</strong><br/>');
				modal_body.append('<strong>' + last_year + '</strong><br/>');
				modal_body.append('<strong>índice h5:</strong> <a href="' +  h5_last.ownURL + '" target="_blank">' + h5_last.y + '</a><br/>');
				modal_body.append('<strong>mediana h5:</strong> <a href="' +  m5_last.ownURL + '" target="_blank">' + m5_last.y + '</a><br/>');
			}
		});
		$("#journal_info_more_link").attr("href", "http://analytics.scielo.org/?journal=" + issn + "&collection=" + collection);
	});	
});


function get_result_total(form_action, form_params, callback){
	// query iAHx and return total
	$.ajax({
		type: 'GET',
		data: form_params + '&output=metasearch',
		url: form_action,
		success: function(response) { // on success..
			total = $(response).find('total').text();
			total = parseInt(total);
			callback(total);
		}
	});
}

// make a request that only include a query in history
function send_query_to_history(form_action, form_params){
	$.ajax({
		type: 'GET',
		data: form_params,
		url: form_action,
	});
}