$(function(){

    // getting the count to add in cluster menu
    manipulate_bookmark('count');

    var checkbox = $(".my_selection");

    checkbox.change(function(){
        var value = $(this).val();

        if($(this).is(':checked'))
            manipulate_bookmark('a', value);
        else
            manipulate_bookmark('d', value);
    });

})

function manipulate_bookmark(func, id) {
    var href = "bookmark/"+ func;

    if(id != "")
        href = href + "/" + id;


    $.get(href+"?_=" + new Date().getTime(), function(data) {
        var total = parseInt(data);
        var t = $(".my_selection_count");
        t.html(data);
        if(total > 0) {
            t.addClass("highlighted");
        } else{
            t.removeClass("highlighted");
        }
        searchFormBuilder.ShowCloseSelectedItemsBarMobile(total);
    })
}

// if confirms message, clean the list and go to the main page
function clean_bookmark(phrase) {
    if(confirm(phrase)) {
        manipulate_bookmark('c');
        $(".my_selection").attr('checked', false);
        var form = document.searchForm;

        if (form.q.value.substring(0,4) == '+id:'){
            form.q.value = "";
        }
        form.from.value = 0;
        form.submit();
    }

}

// list the bookmark, beggining from first result
function list_bookmark() {
    $.get('bookmark/list?_='+ new Date().getTime(), function(q) {
        var form = document.searchForm;
        form.q.value = q;
        form.from.value = 0;
        form.page.value = "1";
        $("input[name^='filter']").remove();
        form.submit();
    })
}
