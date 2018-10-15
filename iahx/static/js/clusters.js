function remove_filter(id) {
    if ( $("#"+id).is(":visible") ) {
        $("#"+id).attr("checked", false);
    }else{
        // remove hidden file
        $("#"+id).remove();    
    }
    $("#form_clusters").submit();
}

function add_filter(id) {
    
    filter = $("#"+id);

    // check or uncheck
    if(filter.is(':checked')) {
        filter.attr('checked', false);
    } else {
        filter.attr('checked', true);
    }

    $("#form_clusters").submit();
}


function show_all_clusters() {
    $(".bContent ul").slideDown(200);
}

function hide_all_clusters() {
    $(".bContent ul").slideUp(200);
}

function toggle_cluster(name) {
    $("#ul_" + name).slideToggle(100);
}

function show_more_clusters (cluster, limit) {

    var form = document.getElementById("form_clusters");
    // add anchor name for go to cluster position after reload page
    form.action = form.action + "#" + cluster;
    form.fb.value = cluster + ":" + limit;

    $("#form_clusters").submit();

    form.fb.value == "";
    return false;
}

function reset_filters(){

    $('<input>').attr({
        type: 'hidden',
        id: 'reset_filters',
        name: 'reset_filters',
        value: 'ALL'
    }).appendTo('#form_clusters');

    $("#form_clusters").submit();

}