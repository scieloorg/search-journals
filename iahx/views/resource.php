<?php
use Symfony\Component\HttpFoundation\Request;

$app->get('resource/{lang}/{id}', function (Request $request, $lang, $id) use ($app, $DEFAULT_PARAMS, $config) {

    global $texts;

    $collectionData = $DEFAULT_PARAMS['defaultCollectionData'];
    $site = $DEFAULT_PARAMS['defaultSite'];
    $col = $DEFAULT_PARAMS['defaultCollection'];

    // check if is present the lang param and overwrite the url lang param
    $param_lang =  $request->get('lang');
    if(isset($param_lang) and $param_lang != "") {
        $lang = $param_lang;
    }

    // controller response
    $dia = new Dia($site, $col, 1, "site", $lang);

    if ($config->show_related_docs == "true"){
        $dia_response = $dia->related($id);
    }else{
        if ($config->check_alternate_id == "true"){
            $dia_response = $dia->search('id:"' . $id . '" OR alternate_id:"' . $id . '"');
        }else{
            $dia_response = $dia->search('id:"' . $id . '"');
        }
    }
    $result = json_decode($dia_response, true);

    $total_found = $result['diaServerResponse'][0]['response']['numFound'];

    // translate
    $texts = parse_ini_file(TRANSLATE_PATH . $lang . "/texts.ini", true);

    // output vars
    $output_array = array();
    $output_array['lang'] = $lang;
    $output_array['col'] = $col;
    $output_array['site'] = $site;
    $output_array['docs'] = $result['diaServerResponse'][0]['response']['docs'];
    $output_array['collectionData'] = $collectionData;
    $output_array['current_page'] = 'detail';
    $output_array['q'] = 'id:' . $id;

    if ( $config->show_related_docs == "true"){
        $output_array['doc'] = $result['diaServerResponse'][0]['match']['docs'][0];
        $output_array['maxScore'] = $result['diaServerResponse'][0]['response']['maxScore'];
        $output_array['related_docs'] = $result['diaServerResponse'][0]['response']['docs'];
    }else{
        $output_array['doc'] = $result['diaServerResponse'][0]['response']['docs'][0];
    }
    $output_array['config'] = $config;
    $output_array['texts'] = $texts;

    // start session
    $SESSION = $app['session'];
    $SESSION->start();

    // log user action
    log_user_action($lang, $col, $site, 'id:' . $id, '', '', '', '', 'detail', $SESSION->getId());

    $check_mobile = (bool)$config->mobile_version;
    $view = $request->get("view");

    if( $view == 'desktop' ) {   // forced by user desktop version
        $view = '';              // use default view
    }
/*
    else{
        if ($check_mobile){      //configured to present mobile version
            $detect = new Mobile_Detect();
            if ($view == 'mobile' || ($detect->isMobile() && !$detect->isTablet()) )   {
                $view = 'mobile';
            }
        }
    }
*/
    if( !isset($view) ) {
        $view = '';
    }

    // return 404 if document not found
    if (intval($total_found) == 0){
        header("HTTP/1.0 404 Not Found");
    }

    echo $app['twig']->render( custom_template($view . '/result-detail.html'), $output_array );

});

?>
