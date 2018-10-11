<?php

use Symfony\Component\HttpFoundation\Request;
use Symfony\Component\HttpFoundation\Response;

$app->get('browse-index/{index}/', function (Request $request, $index) use ($app, $DEFAULT_PARAMS, $config) {

    $init = $request->get("init");
    $direction = $request->get("dir");
    if ($init == ''){
        $init = '"';
    }

    if ($direction == ''){
        $direction = 'next';
    }

    $index_name = $config->site;

    $service_url = $config->browse_index_url . "/PreviousTermServlet?index=" . $index_name . "&fields=" . $index . "&init=" . $init . "&maxTerms=200&direction=" . $direction;

    $result = file_get_contents($service_url);

    // start session
    $SESSION = $app['session'];
    $SESSION->start();

    // log user action
    log_user_action($lang, $col, $site, 'id:' . $id, '', '', '', '', 'browseindex', $SESSION->getId());

    // output vars
    $output_array = array();

    $response = new Response($result);
    $response->headers->set('Content-Type', 'application/json');

    return $response;

});

?>
