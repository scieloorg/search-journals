<?php

use Symfony\Component\HttpFoundation\Request;

$app->match('decs/{lang}/{term}', function (Request $request, $lang, $term) use ($app, $DEFAULT_PARAMS, $config) {

    $texts = parse_ini_file(TRANSLATE_PATH . $lang . "/texts.ini", true);
    $lang_one_letter = ($lang == "en") ? "i" : substr($lang, 0, 1);

    $bool = array(
        "101", // Termo autorizado
        "102", // Sinônimo
        "104"  // Termo histórico
    );

    $term = stripcslashes($term);
    $term = strtoupper($term);
    $term = urlencode($term);

    $concept = 0;
    for( $i = 0; !$concept && ($i < sizeof($bool)); $i = $i + 1 ){
        $query = "http://decs.bvsalud.org/cgi-bin/mx/cgi=@vmx/decs/?bool=".$bool[$i]."%20$term&lang=$lang";
        $decs = @simplexml_load_file($query);
        if ($decs){
            $concept = (String) @$decs->decsws_response->record_list->record->definition->occ['n'];
        }
    }
    $i = $i - 1;

    $href = "http://decs.bvsalud.org/cgi-bin/wxis1660.exe/decsserver/" .
    "?IsisScript=../cgi-bin/decsserver/decsserver.xis" .
    "&search_language=".$lang_one_letter .
    "&interface_language=".$lang_one_letter .
    "&previous_page=homepage&task=exact_term&search_exp=" . $term;

    $output_array = array();
    $output_array['texts'] = $texts;
    $output_array['concept'] = $concept;
    $output_array['decs'] = $decs;
    $output_array['href'] = $href;

    return $app['twig']->render('decs.html', $output_array);

});

?>