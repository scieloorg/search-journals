<?php

use Symfony\Component\HttpFoundation\Request;

$app->get('citing-documents/{id}/', function (Request $request, $id) use ($app, $DEFAULT_PARAMS, $config) {

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

    $citation = $result['diaServerResponse'][0]['response']['docs'][0];

    $output_array = array();

    if (isset($citation)) {
        $citing_docs_ids = $citation['document_fk'];

        $responses = array();
        for ($i = 0; $i < count($citing_docs_ids); $i++) {
            $response_i = $dia->search($citing_docs_ids[$i]);
            $decoded_response_i = json_decode($response_i, true)['diaServerResponse'][0]['response']['docs'][0];

            if (isset($decoded_response_i)) {
                $responses[$i] = $decoded_response_i;
            }
        }

        $output_array['citation_id'] = $id;
        $output_array['citing_docs'] = $responses;
        $output_array['lang'] = $lang;
        $output_array['config'] = $config;
    }

    echo $app['twig']->render(custom_template($view . '/result-citing-docs.html'), $output_array);

});

?>