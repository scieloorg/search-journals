<?php

use Symfony\Component\HttpFoundation\Request;

$app->get('related/{lang}/{id}', function (Request $request, $lang, $id) use ($app, $DEFAULT_PARAMS, $config) {

    global $lang, $texts;

    $view = $request->get("view");
    $collectionData = $DEFAULT_PARAMS['defaultCollectionData'];
    $site = $DEFAULT_PARAMS['defaultSite'];
    $col = $DEFAULT_PARAMS['defaultCollection'];

    // Dia response
    $dia = new Dia($site, $col, 1, "site", $lang);
    $dia_response = $dia->related($id);
    $result = json_decode($dia_response, true);

    // translate
    $texts = parse_ini_file(TRANSLATE_PATH . $lang . "/texts.ini", true);

    // start session
    $SESSION = $app['session'];
    $SESSION->start();    

    // log user action
    log_user_action($lang, $col, $site, 'id:' . $id, '', '', '', '', 'related', $SESSION->getId());

    // output vars
    $output_array = array();
    $output_array['lang'] = $lang;
    $output_array['col'] = $col;
    $output_array['site'] = $site;
    $output_array['maxScore'] = $result['diaServerResponse'][0]['response']['maxScore'];
    $output_array['doc'] = $result['diaServerResponse'][0]['match']['docs'][0];
    $output_array['related_docs'] = $result['diaServerResponse'][0]['response']['docs'];
    $output_array['config'] = $config;
    $output_array['texts'] = $texts;
    $output_array['debug'] = $app['request']->get('debug');

    if ( !isset($view) || $view == 'desktop'){
        $view = ''; // default desktop site
    }
    
    return $app['twig']->render( $view . '/related-docs.html', $output_array);     

});

?>