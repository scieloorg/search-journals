$(function(){
    
    $('.fancybox_iframe').fancybox({
        'width': 650,
        'height': 490,
        'autoScale': 'true',
        'centerOnScroll': true,
        'type' : 'iframe',
        'titlePosition' : 'inside',
    });

    $('.fancybox_iframe75').fancybox({
        'width': '75%',
        'height': '75%',
        'autoScale': 'false',
        'centerOnScroll': true,
        'type' : 'iframe',
    });

    $('.fancybox').fancybox();
    
    $('#affix').affix({
      offset: {
        top:  200,
        bottom: 270
      }
    })

    $('.defaultValue').each(function(){
        var defaultVal = $(this).attr('title');
        $(this).focus(function(){
            if ($(this).val() == defaultVal){
                $(this).removeClass('active').val('');
            }
        })
        .blur(function(){
            if ($(this).val() == ''){
                $(this).addClass('active').val(defaultVal);
            }
        })
        .blur().addClass('active');
    });

    $('form').submit(function(){
        $('.defaultValue').each(function(){
            var defaultVal = $(this).attr('title');
            if ($(this).val() == defaultVal){
                $(this).val('');
            }
        });
    });

    $('.nav-toggle').click(function(){
            //get collapse content selector
            var collapse_content_selector = $(this).attr('href');                   
 
            //make the collapse content to be shown or hide
            var toggle_switch = $(this);
            $(collapse_content_selector).toggle(function(){
                //animation complete
            });
            return false;
    });

    $('#flash').delay(500).fadeIn('normal', function() {
        $(this).delay(3500).fadeOut();
    });

    // prevent submit of default placeholder text
    $("#searchForm").submit( function( event ) {      
      $("#q").focus();
    });

})