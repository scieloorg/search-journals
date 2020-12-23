var next_line = 3;

// show/refresh index list
function show_index(line, update){

    element_id = $(line).attr("id");
    block_id = element_id.substring(element_id.lastIndexOf('-') + 1);
    if (!update){
        $('#list-' + block_id).toggle();
    }

    init = $('#input-' + block_id).val();
    index = $('#index-' + block_id).find(':selected').val();
    options = $('#select-' + block_id);

    options.find('option').remove().end();

    $.getJSON(SEARCH_URL + "browse-index/" + index +"/?init=" + init, function(result) {
        $.each(result.terms, function() {
            options.append($("<option />").val(this).text(this));
        });

    });
}

// previous keys
function  show_prev(line) {
    element_id = $(line).attr("id");
    block_id = element_id.substring(element_id.lastIndexOf('-') + 1);

    options = $('#select-' + block_id);
    init = options.find('option:first-child').val();
    index = $('#index-' + block_id).find(':selected').val();

    options.find('option').remove().end();

    $.getJSON(SEARCH_URL + "browse-index/" + index + "/?dir=previous&init=" + init, function(result) {
        $.each(result.terms, function() {
            options.append($("<option />").val(this).text(this));
        });
    });
}

function show_next(line) {
    element_id = $(line).attr("id");
    block_id = element_id.substring(element_id.lastIndexOf('-') + 1);

    options = $('#select-' + block_id);                
    init = options.find('option:last-child').val();
    index = $('#index-' + block_id).find(':selected').val();
    options.find('option').remove().end();

    $.getJSON(SEARCH_URL + "browse-index/" + index + "/?dir=next&init=" + init, function(result) {
        $.each(result.terms, function() {
            options.append($("<option />").val(this).text(this));
        });
    });
}

// select one term from index
function select_term(line){
    element_id = $(line).attr("id");
    block_id = element_id.substring(element_id.lastIndexOf('-') + 1);

    query_input = $('#input-' + block_id);
    selected_key= $('#select-' + block_id).find(':selected').val();                
    query_input.val('"' + selected_key + '"');

}


function add_new_line(obj) {
    var previous_line = next_line-1;

    var block = $(".block-q").clone();
    //alert(block.html());
    // update id's
    block.find('#input-2').attr('id', 'input-' + next_line);
    block.find('#list-2').attr('id', 'list-' + next_line);    
    block.find('#index-2').attr('id', 'index-' + next_line);
    block.find('#select-2').attr('id', 'select-' + next_line);
    block.find('#show-2').attr('id', 'show-' + next_line);
    block.find('#next-2').attr('id', 'next-' + next_line);
    block.find('#prev-2').attr('id', 'prev-' + next_line);
    block.find('#refresh-2').attr('id', 'refresh-' + next_line);

    $('#select-' + next_line).find('option').remove().end();
    $('#list-' + next_line).css('display', 'none');

    var html = block.html();
    var more = $(".more");

    // update counter
    next_line++;

    more.append(html);
}

function new_line(obj) {
    if(obj.value.length < 1) {
        add_new_line();        
    }
}

function add_query(current, q, bool, index) {
    
    current = current + " " + bool + " (";

    if(index === "") {
        current = current + q;
    } else {
        current = current + index + ':(' + q + ')';
    }

    current = current + ")";
    return current;
}

function search() {
    var search_form = document.searchForm;
    var form = document.advanced;
    var q = form["q[]"];
    var index = form['index[]'];
    var bool = form['bool[]'];
    var query = "";

    if(q[0].value != "") {
        query = add_query("", q[0].value, "", index[0].value);
        for(i=0; i<=bool.length; i++) {
            if(q[i+1] && q[i+1].value != "") {
                query = add_query(query, q[i+1].value, bool[i].value, index[i+1].value);
            }
        }
    }

    search_form.q.value = $.trim(query);
    
    if (query.length >= 2048) {
        search_form.method = "POST";
    } else {
        search_form.method = "GET";
    }
    search_form.submit();

    return false;
}