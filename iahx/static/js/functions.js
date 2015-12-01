// usado para fazer paginação
function go_to_page(page) {
    var form = document.searchForm;
    var count = document.searchForm.count.value;
    var from = (page*count)-count+1;
    
    form.from.value = from;    
    form.page.value = page;

    $("#q").focus();            // prevent submit of default placeholder text
    $("#searchForm").submit();
    $("#q").blur();
}

// usado para mudar a forma de exibição do dado (xml/rss/print/site)
function change_output(output) {
    var form = document.searchForm;
    form.output.value = output;

    $("#searchForm").submit();
    form.output.value = "site"; //return to default output
}

// muda a quantidade de resultados exibidos
function change_count(elem) {
    var form = document.searchForm;
    form.count.value = elem.value;

    $("#searchForm").submit();   
}

// muda o parâmetro lang
function change_language(lang) {
    document.language.lang.value = lang;
    document.language.submit();
}

// muda a quantidade de resultados exibidos
function change_format(elem) {
    var form = document.searchForm;
    form.format.value = elem.value;

    $("#searchForm").submit();
}

// leva para output "print", passando o count
function print(count) {

    var form = document.searchForm;
    if(count)
        form.count.value = count;
    else 
        form.count.value = 300;

    change_output("print");
}

// leva para output "ris/citation/csv", passando o count
function export_result(count) {

    var form = document.searchForm;
    var previous_count = form.count.value;
    var output = getCheckedValue(document.exportForm.format);

    if(count)
        form.count.value = count;
    else 
        form.count.value = -1;

    change_output(output);
    form.count.value = previous_count;    //return to previous value
}

// advanced search
function decs_locator(base_url) {
    $("#searchForm").attr("action",base_url + "decs-locator/");
    $("#searchForm").submit();
}


/**
 * Mostra janela com grafico do cluster selecionado
 * @param {Node} obj
 * @param {String} titulo
 * @param {String} id
 */
function open_chart(obj, titulo, id){
    var regex = /\(\d+\)/;
    var params= "";

    var grupo = document.getElementById("ul_" + id);
    var lista = grupo.getElementsByTagName('li');

    for (i = 0; i < lista.length; i++){
        cluster = lista[i].innerHTML;
        clusterLabel = lista[i].getElementsByTagName('a')[0].innerHTML;

        ma = regex.exec(cluster);
        if (ma != null) {
            clusterTotal = ma[0].replace(/[()]/g,'');
            params += "&l[]=" + clusterLabel.trim() + "&d[]=" + clusterTotal.trim();
        }
    }
    // caso seja o cluster de ano passa parametro para realizar sort
    if (id == 'year_cluster'){
        params += "&sort=true";
    }
    url = "chart/?title=" + titulo + params + "&KeepThis=true&TB_iframe=true&height=480&width=650";
    obj.href = url;
}

// return the value of the radio button that is checked
// return an empty string if none are checked, or
// there are no radio buttons
function getCheckedValue(radioObj) {
    if(!radioObj)
        return "";
    var radioLength = radioObj.length;
    if(radioLength == undefined)
        if(radioObj.checked)
            return radioObj.value;
        else
            return "";
    for(var i = 0; i < radioLength; i++) {
        if(radioObj[i].checked) {
            return radioObj[i].value;
        }
    }
    return "";
}

function change_sort(obj){
    var sort = obj.options[obj.selectedIndex].value;
    var form = document.searchForm;

    form.sort.value = sort;
    $("#searchForm").submit();
}

function cochrane_lnk( lnk,refDB,refID ){

    form = document.searchForm;
    lang = form.lang.value;
    if (lang == "pt"){ oneLetterLang = "p"; }
    if (lang == "es"){ oneLetterLang = "e"; }
    if (lang == "en"){ oneLetterLang = "i"; }

    db = refDB.substr(refDB.indexOf("-")+1);
    db = db.toLowerCase();

    if (db == 'bandolier' || db == 'agencias' || db == 'kovacs' || db == 'evidargent' || db == 'clibplusrefs' || db == 'gestion' || db == 'reviews-plus'){
        lib = 'BCP';
    }else{
        lib = 'COC';
    }

    if (db == 'reviews-plus'){
        db = 'reviews';
        refID = refID.substr(0, refID.indexOf('_'));
    }

    refUrl = "http://cochrane.bvsalud.org/doc.php?db=" + db + "&id=" + refID + "&lib=" + lib;

    lnk.href = refUrl;

    return true;
}