function send_email() {
    var form = document.emailForm;

    var dest_emails = '';
    $("input[name='email[]']").each(function() {
        var value = $(this).val();
        if (value != '') {
            dest_emails += value;
        }
    });

    if( dest_emails === "") {
        alert("Informe o email para envio.");
        return false;
    }

    if( dest_emails.search("@") < 0) {
        alert("Informe um email válido.");
        return false;   
    }
    
    return true;
}

function add_more_email() {

    var dest = $("#destinatarios").clone();
    var new_input = dest.html();
    var more_dest = $("#more-destinatarios");

    more_dest.html(more_dest.html() + new_input);
}