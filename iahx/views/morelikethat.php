<?php

use Symfony\Component\HttpFoundation\Request;

$app->get('morelikethat/{lang}/', function (Request $request, $lang) use ($app, $DEFAULT_PARAMS, $config) {

    global $lang, $texts;

    $collectionData = $DEFAULT_PARAMS['defaultCollectionData'];
    $site = $DEFAULT_PARAMS['defaultSite'];
    $col = $DEFAULT_PARAMS['defaultCollection'];

    $query = $request->get("q");

    $service_url = $config->more_like_that_url . "/MoreLikeThat?content=" . $query . "&fieldsName=ti,ab";

    // Dia response
    $dia = new Dia($site, $col, 1, "site", $lang);
    $dia_response = $dia->morelikethat($service_url);
    $result = json_decode($dia_response, true);

     // translate
    $texts = parse_ini_file(TRANSLATE_PATH . $lang . "/texts.ini", true);

    // start session
    $SESSION = $app['session'];
    $SESSION->start();    

    // log user action
    log_user_action($lang, $col, $site, 'id:' . $id, '', '', '', '', 'morelikethat', $SESSION->getId());

    // output vars
    $output_array = array();
    $output_array['query'] = $query;
    $output_array['lang'] = $lang;
    $output_array['col'] = $col;
    $output_array['site'] = $site;
    $output_array['maxScore'] =  $result['match']['maxScore'];
    $output_array['related_docs'] = $result['response']['docs'];
    $output_array['config'] = $config;
    $output_array['texts'] = $texts;
    $output_array['debug'] = $app['request']->get('debug');
    
    return $app['twig']->render('morelikethat.html', $output_array);     

});

?>