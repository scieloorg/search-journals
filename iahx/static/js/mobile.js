$(document).ready(function(){
    nav();
    filters();
    orderby();
    submit_form();
});

function nav(){
    var speed = 300;
    var navHeight = $(".h-nav").height();

    $(".i-nav-show").on("click", function(){
        $(this).hide();
        $(".i-nav-hide").show();

        $(".h-nav").css({"height":"0px", "display":"block"}).stop().animate({"height":navHeight},speed);
        $('.resultSet').hide();
    });

    $(".i-nav-hide").on("click", function(){
        $(this).hide();
        $(".i-nav-show").show();

        $(".h-nav").stop().animate({"height":"0px"}, speed, function(){
            $(this).hide();
        });
        $('.resultSet').show();
    });
};

function filters(){
    var speed = 300;
    var iShow = "<span class='i-show'></span>";
    var iHide = "<span class='i-hide'></span>";

    $(".show-filters").on("click", function(){
        var element = $(this);
        $('.filters').toggle();
    });

    $(".c-filters-lia").on("click", function(){
        var element = $(this);
        var filtersHeight = element.siblings(".c-filters-sub").height();
        var click = element.find("span").attr("class");

        if(click == "i-show"){
            element.find(".i-show").addClass("i-hide").removeClass("i-show");
            element.siblings(".c-filters-sub").css({"height":"0px", "display":"block"}).stop().animate({"height":filtersHeight},speed);
        }else{
            element.find(".i-hide").addClass("i-show").removeClass("i-hide");
            element.siblings(".c-filters-sub").stop().animate({"height":"0px"}, speed, function(){
                $(this).hide();
                $(this).css({"height":"auto"});
            });
        }
    });

};


function orderby(){
    var speed = 300;
    var iShow = "<span class='i-show'></span>";
    var iHide = "<span class='i-hide'></span>";

    $(".show-orderby").on("click", function(){
        var element = $(this);
        $('.orderby').toggle();
    });

    $(".c-orderby-li").on("click", function(){
        var element = $(this);
        var form = document.searchForm;
        
        var new_sort = $('input[name=sortBy]:checked').val();

        form.sort.value = new_sort;

        document.searchForm.submit();

    });        

};

function submit_form(){
    $('.c-results-a, .c-filters-lbl, .c-filter-remove').click(function() {
       $('#loading').show();
       return true;            
    });

    $('#searchForm').submit(function() {
       $('#loading').show();
       return true;
    });
}