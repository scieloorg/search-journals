$(document).ready(
    function(){
        var view = $('#view').val();

        $('div.record div.data').each(
            function(){
                if ( 'mobile' == view ) {
                  var x = $(this).parent().find('nav.c-share div.platserv a.add-collection');

                  //var author = $(this).find('div.author').html();
                  var author = $(this).find('div.author').text();
                  author = author.replace(/[^ ]+/i,'');

                  var title = $(this).find('h1.c-results-tit').html();
                } else {
                  var x = $(this).parent().find('div.user-actions div.platserv a.add-collection');

                  //var author = $(this).find('div.author').html();
                  var author = $(this).find('div.author').text();
                  author = author.replace(/[^ ]+/i,'');

                  var title = $(this).find('h3 > a').html();
                  if (title == null){
                      title = $(this).find('h3').html();
                  }
                }

                var id = $(this).parent().attr('id');

                var loc = location.href;
                if ( loc.indexOf('?') > 0 ){
                    loc = loc.substring(0,loc.indexOf('?'));
                }
                var url = loc.replace(/#?$/i,'');

                // monta url para pagina de detalhes do recurso caso o usuario não esteja nela
                if ( loc.indexOf('resource/') == -1) {
                    //url = loc.replace(/([a-z]+\.php)?#?$/i,'resource/'+id);
                    var url = $(this).find('h3 > a').attr('href');
                }

                var source = window.location.hostname+'/'+SITE;

                var obj = new Object();
                obj.url = $.trim(url);
                obj.source = $.trim(source);
                obj.author = $.trim(author).replace(/\s+/g, " ");
                obj.title = $.trim(title);
                obj.id = $.trim(id);

                //alert(JSON.stringify(obj, null, 4));

                x.on('click', function(){
                    obj.userTK = unescape(getCookie('userTK'));

                    if ( obj.userTK == 'undefined' ){
                        var data = encodeURIComponent(JSON.stringify(obj));
                        var win = window.open(SERVICES_PLATFORM_DOMAIN + '/client/controller/authentication/?lang=' + LANG + '&data=' + data, '_blank');
                        win.focus();
                    }else{
                        if (obj.id.match("^lis-")) {
                            var task = 'addLink';
                        } else {
                            var task = 'addDoc';
                        }

                        $.post(SERVICES_PLATFORM_DOMAIN + '/client/controller/servicesplatform/control/business/task/' + task, obj, function(data){
                            if (isJSON(data)){
                                response = $.parseJSON(data);
                            }else{
                                response = data;
                            }

                            if (obj.id.match("^lis-")) {
                                if(data == true){
                                    alert(ADD_LINK_SUCCESS);
                                }else if(data == 'exists'){
                                    alert(LINK_EXISTS);
                                }else{
                                    alert(ADD_LINK_ERROR);
                                }
                            } else {
                                if(data == true){
                                    alert(ADD_TO_COLLECTION_SUCCESS);
                                }else if(typeof response == 'object'){
                                    alert(COLLECTION_EXISTS);
                                }else{
                                    alert(ADD_TO_COLLECTION_ERROR);
                                }
                            }
                        });
                    }
                });
            }
        );

        $('div#rss a.add-rss').on('click', function(){
            var name = $('div.identification h1').text();
            var url = $(location).attr('href');
            var sep = ' | ';

            if (QUERY.trim()) {
                name += sep + QUERY;
                sep = ' AND ';
            }

            if (FILTER.trim()) {
                name += sep + FILTER;
            }

            if ( name.length > 150 ) {
                name = name.substr(0, 144) + ' [...]';
            }

            if (~url.indexOf("output=site")) {
                url = url.replace('output=site', 'output=rss');
            } else {
                if (QUERY.trim()) {
                    url += '&output=rss';
                } else {
                    url = SEARCH_URL + '?output=rss';
                }
            }

            var obj = new Object();
            obj.userTK = unescape(getCookie('userTK'));
            obj.name = $.trim(name);
            obj.url = $.trim(url);

            $.post(SERVICES_PLATFORM_DOMAIN + '/client/controller/servicesplatform/control/business/task/addRSS', obj, function(data){
                if(data){
                    if(data == 'exists'){
                        alert(RSS_EXISTS);
                    }else{
                        alert(ADD_RSS_SUCCESS);
                    }
                }else{
                    alert(ADD_RSS_ERROR);
                }
            });
        });

        function getCookie(name) {
          var value = "; " + document.cookie;
          var parts = value.split("; " + name + "=");
          if (parts.length == 2) return parts.pop().split(";").shift();
        }

        function isJSON(str) {
            try {
                JSON.parse(str);
            } catch (e) {
                return false;
            }

            return true;
        }
    }
);
