<?php

use Symfony\Component\HttpFoundation\Request;

$app->get('citation-journal/{id}/', function (Request $request, $id) use ($app, $DEFAULT_PARAMS, $config) {

    $lang = $request->get("lang");
    if (! isset($lang) or ! in_array($lang, array('pt', 'es', 'en'))) {
        $lang = $DEFAULT_PARAMS['lang'];
    }

    global $texts;
    $texts = parse_ini_file(TRANSLATE_PATH . $lang . "/texts.ini", true);

    $view = $request->get("view");
    $site = $DEFAULT_PARAMS['defaultSite'];
    $col = $DEFAULT_PARAMS['defaultCollection'];
    $count = 1;
    $output = "site";

    $q = $id;

    $dia = new Dia($site, $col, $count, $output, $lang);
    $dia_response = $dia->search($q);

    $result = json_decode($dia_response, true);

    $output_array = array();
    $output_array['id'] = $id;
    $output_array['texts'] = $texts;
    $output_array['doc'] = $result['diaServerResponse'][0]['response']['docs'][0];

    echo $app['twig']->render(custom_template($view . '/result-citation-journal.html'), $output_array);

});

?>