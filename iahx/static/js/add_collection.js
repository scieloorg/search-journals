$(document).ready(
    function(){
        $('div.record div.data').each(
           function(){

              var author = $(this).find('div.author').html();
              author = author.replace(/[^ ]+/i,'');
              var title  = $(this).find('h3 > a').html();
              if (title == null){
                title = $(this).find('h3').html();
              }

              var id     = $(this).parent().attr('id');
              var loc = location.href;

              if ( loc.indexOf('?') > 0 ){
                loc = loc.substring(0,loc.indexOf('?'));
              }

              var url = loc.replace(/#?$/i,'');

              // monta url para pagina de detalhes do recurso caso o usuario não esteja nela
              if ( loc.indexOf('resources/') == -1) {
                  url = loc.replace(/([a-z]+\.php)?#?$/i,'resources/'+id);
              }
              var source = window.location.hostname;

              var x = $(this).parent().find('div.user-actions div.scielo a');

              var obj = new Object();
              obj.url = $.trim(url);
              obj.source = $.trim(source);
              obj.author = $.trim(author);
              obj.title = $.trim(title);
              obj.id = $.trim(id);

              x.click( function(){
                $.post('/regional/add_servplat.php',obj,
            function(data){
                if(data == true){
                    alert('Documento adicionado à coleção.');
                }else{
                    alert('O documento não foi adicionado corretamente à coleção.');
                }
            });

              });
           }
        )
   }
);
