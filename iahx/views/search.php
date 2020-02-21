<?php

require_once 'lib/class/dia.class.php';
include 'lib/class/log.class.php';
include 'lib/Mobile_Detect.php';

use Symfony\Component\HttpFoundation\Request;
use Symfony\Component\HttpFoundation\Response;

$app->match('/', function (Request $request) use ($app, $DEFAULT_PARAMS, $config) {

    global $lang, $texts;

    $params = array_merge(
        $app['request']->request->all(),
        $app['request']->query->all()
    );

    // if magic quotes gpc is on, this function clean all parameters and
    // results that was modified by the directive
    if (get_magic_quotes_gpc()) {
        $process = array(&$params);
        while (list($key, $val) = each($process)) {
            foreach ($val as $k => $v) {
                unset($process[$key][$k]);
                if (is_array($v)) {
                    $process[$key][stripslashes($k)] = $v;
                    $process[] = &$process[$key][stripslashes($k)];
                } else {
                    $process[$key][stripslashes($k)] = stripslashes($v);
                }
            }
        }
        unset($process);
    }

    $collectionData = $DEFAULT_PARAMS['defaultCollectionData'];
    $site = $DEFAULT_PARAMS['defaultSite'];
    $col = $DEFAULT_PARAMS['defaultCollection'];

    $fb = "";
    if(isset($params['fb']) and $params['fb'] != "") {
        $fb = $params['fb'];
    }

    $count = $config->documents_per_page;
    if(isset($params['count']) and $params['count'] != "") {
        $count = $params['count'];
        if ($config->max_documents_per_page){
            // if max_documents_per_page is defined check count url param
            if (intval($count) > intval($config->max_documents_per_page)){
                $count = $config->max_documents_per_page;
            }
        }
    }

    $output = "site";
    if(isset($params['output']) and $params['output'] != "") {
        $output = $params['output'];
    }

    $lang = $DEFAULT_PARAMS['lang'];
    if(isset($params['lang']) and $params['lang'] != "") {
        $lang = $params['lang'];
    }

    $q = "";
    if(isset($params['q']) and $params['q'] != "") {
        $q = $params['q'];
    }

    $index = "";
    if(isset($params['index']) and $params['index'] != "") {
        $index = $params['index'];
    }

    // if user submit a new search restart values of from, page
    if( isset($params['search_form_submit']) ){
        $params['from'] = 0;
        $params['page'] = 1;
    }

    // check for reset_filters param
    if( isset($params['reset_filters']) && $params['reset_filters'] == 'ALL' ){
        $params['filter'] = array();
    }


    $from = 0;
    if(isset($params['from']) and $params['from'] != "") {
        $from = $params['from'];
    }

    $page = 1;
    if(isset($params['page'])and $params['page'] != "") {
        $page = $params['page'];
    }

    $where = array();
    if(isset($params['where'])and $params['where'] != "") {

        $where = $params['where'];
        foreach($collectionData->where_list->where as $item) {
            if($item->name == $where) {
                $where = (string) $item->filter;

                if(!empty($where)) {

                    $where = explode(":", $where);
                    $where[1] = str_replace('("', "", $where[1]);
                    $where[1] = str_replace('")', "", $where[1]);
                    $where = array($where[0] => array($where[1]));
                }

                if(!is_array($where)) {
                    $where = array($where);
                }
                break;
            }
        }
    } else {
        list($param_where, $where) = getDefaultWhere($collectionData, $q);
        $params['where'] = $param_where;
    }

    $sort = "";
    $sort_value = "";
    if(isset($params['sort']) and $params['sort'] != "Array") {

        $sort = $params['sort'];

        $exists = false;
        foreach($collectionData->sort_list->sort as $item) {
            if($sort == $item->name) {
                $exists = true;
                $sort_value = (string) $item->value;
                break;
            }
        }

        if(!$exists)
            $sort = "";

    }
    if ($sort == ""){
        $sort_value = getDefaultSort($collectionData, $q);
    }

    $format = $DEFAULT_PARAMS['defaultDisplayFormat'];
    if(isset($params['format'])and $params['format'] != "") {
        $format = $params['format'];
    }

    $filter_boolean_operator = array();
    if(!empty($params['filter_boolean_operator']) and $params['filter_boolean_operator'] != "Array") {
        $filter_boolean_operator = $params['filter_boolean_operator'];
    }

    $filter = array();
    if(!empty($params['filter']) and $params['filter'] != "Array") {
        $filter = $params['filter'];
    }

    // alternative syntax for filter param ==> index:value (ex. db:LILACS)
    if ( !is_array($filter) ) {
        preg_match('/([a-z]+):(.+)/',$filter, $filter_parts);
        if ($filter_parts){
            // convert to internal format
            $filter = array($filter_parts[1] => array($filter_parts[2]));
        }
    }

    foreach($filter as $key => $value) {
        if($value == "Array" or $value == "Array#" or $value == "" or empty($value[0])) {
            unset($filter[$key]);
        }else{
            $filter[$key] = str_replace("#", "", $value);
        }
    }

    // BOOKMARK SESSION
    $SESSION = $app['session'];
    $SESSION->start();
    $bookmark = $SESSION->get('bookmark');


    // initial filter (defined on configuration file)
    $initial_filter = html_entity_decode($collectionData->initial_filter);
    // user selected filters (cluster and where)
    $user_filter = array_merge($filter, $where);

    // if is send email, needs to change the from parameter, or my selection
    if(isset($params['is_email'])) {

        $email = array();
        foreach(array('name', 'your_email', 'email', 'subject', 'comment', 'selection') as $field) {
            if((is_array($params[$field]) and !empty($params[$field])) or ($params[$field] != "")) {
                $email[$field] = $params[$field];
            }
        }

        if(isset($email['selection'])) {
            if($email['selection'] == "my_selection") {

                $from = 1;
                $q = '+id:("' . join(array_keys($bookmark), '" OR "') . '")';
            }
            elseif($email['selection'] == "all_results") {
                $from = 1;
                $count = 300;
            }
        }
    }

    // adjusts parameters for export operation
    if (($output == 'ris' || $output == 'csv' || $output == 'citation' || $output == 'bibtex')){
        if ($count == '-1'){
            $from = 0;
            $count = $config->documents_per_page * 10;  //increase count for export
        }elseif ($count == 'selection'){
            $from = 0;
            $count = $config->documents_per_page * 100; // max for selection option
            $q = '+id:("' . join(array_keys($bookmark), '" OR "') . '")';
        }else{
            $export_total = $from + $count;
        }
    }

    // USER PREFERENCE FILTERS SESSION
    if(!$SESSION->has("user_preference_filter")) {
        $SESSION->set('user_preference_filter', array());
    }

    $user_preference_filter = $SESSION->get('user_preference_filter');

    // add to session filters from form
    if (  isset($params['config_filter_submit']) ) {
        $user_preference_filter = $params['u_filter'];
    }

    $config_cluster_list = $collectionData->cluster_list->cluster;
    $default_cluster_list = getDefaultClusterList($collectionData);

    $SESSION->set('user_preference_filter', $user_preference_filter);

    // HISTORY SESSION
    if(!$SESSION->has("history")) {
        $SESSION->set('history', array());
    }

    $history = $SESSION->get('history');

    // check and replace for history mark at query string
    if (strpos($q, '#') !== false){
        $q = replace_history_mark($q, $history);
    }

    // Dia response
    $dia = new Dia($site, $col, $count, $output, $lang);
    $dia->setParam('fb', $fb);
    $dia->setParam('sort', $sort_value);
    $dia->setParam('initial_filter', $initial_filter );

    if (isset($user_filter) && isset($params['filter_boolean_operator']) && is_array($params['filter_boolean_operator'])) {
        $user_filter["operators"] = $params['filter_boolean_operator'];
    }

    $dia_response = $dia->search($q, $index, $user_filter, $from);
    $result = json_decode($dia_response, true);

    // detailed query
    $solr_param_q = $result['diaServerResponse'][0]['responseHeader']['params']['q'];
    $solr_param_fq = $result['diaServerResponse'][0]['responseHeader']['params']['fq'];
    if ($solr_param_q != '*:*' && $solr_param_fq != ''){
        $detailed_query = $solr_param_q . " AND " . $solr_param_fq ;
    }elseif ($solr_param_q != '*:*'){
        $detailed_query = $solr_param_q;
    }elseif ($solr_param_fq != ''){
        $detailed_query = $solr_param_fq;
    }

    // translate
    $texts = parse_ini_file(TRANSLATE_PATH . $lang . "/texts.ini", true);

    // pagination
    $pag = array();
    if ( isset($result['diaServerResponse'][0]['response']['docs']) )  {
        $pag['total'] = $result['diaServerResponse'][0]['response']['numFound'];
        $pag['total_formatted'] = number_format($pag['total'], 0, ',', '.');
        $pag['start'] = $result['diaServerResponse'][0]['response']['start'];
        $pag['total_pages'] = ($pag['total'] % $count == 0) ? (int)($pag['total']/$count) : (int)($pag['total']/$count+1);
        $pag['count'] = $count;
    }
    $range_min = (($page-5) > 0) ? $page-5 : 1;
    $range_max = (($range_min+10) > $pag['total_pages']) ? $pag['total_pages'] : $range_min+10;
    $range_max_mobile = (($range_min+3) > $pag['total_pages']) ? $pag['total_pages'] : $range_min+3;
    $pag['pages'] = range($range_min, $range_max);
    $pag['pages_mobile'] = range($range_min, $range_max_mobile);

    // check if query alread register in session
    $query_id = md5($detailed_query);

    if($q != "" and find_in_array($history, 'id', $query_id) == false and $output == 'site') {
        $new_history['id'] = $query_id;
        $new_history['q'] = $params['q'];
        $new_history['detailed_query'] = $detailed_query;
        $new_history['filter'] = $filter;
        $new_history['total'] = ($pag['total_formatted'] > 0 ? $pag['total_formatted'] : 0);
        $new_history['time'] = time();

        array_push($history, $new_history);
        $SESSION->set('history', $history);
        $SESSION->save();
    }

    // output vars
    $output_array = array();
    $output_array['bookmark'] = $bookmark;
    $output_array['user_preference_filter'] = (array) $user_preference_filter;
    $output_array['filter_boolean_operator'] = $filter_boolean_operator;
    $output_array['filters'] = $filter;
    $output_array['filters_formatted'] = $filter;
    $output_array['lang'] = $lang;
    $output_array['q'] = $q;
    $output_array['sort'] = $sort;
    $output_array['format'] = $format;
    $output_array['from'] = $from;
    $output_array['count'] = $count;
    $output_array['output'] = $output;
    $output_array['collectionData'] = $collectionData;
    $output_array['params'] = $params;
    $output_array['pag'] = $pag;
    $output_array['config'] = $config;
    $output_array['texts'] = $texts;
    $output_array['current_url'] = $_SERVER['REQUEST_URI'];
    $output_array['display_file'] = "result-format-" . $format . ".html";
    $output_array['debug'] = (isset($params['debug'])) ? $params['debug'] : false;
    $output_array['config_cluster_list'] = $config_cluster_list;
    $output_array['default_cluster_list'] = $default_cluster_list;
    $output_array['history'] = $history;
    $output_array['index'] = $index;
    $output_array['parsing_filters'] = $solr_param_fq;
    $output_array['page'] = $page;
    $output_array['current_page'] = 'result';

    if ( isset($result['diaServerResponse'][0]['response']['docs']) )  {
        $output_array['detailed_query'] = $detailed_query;
        $output_array['docs'] = $result['diaServerResponse'][0]['response']['docs'];
        $output_array['clusters'] = $result['diaServerResponse'][0]['facet_counts']['facet_fields'];
    }

    // if is send email
    if(isset($params['is_email'])) {

        $output_array['email'] = $email;

        $render = $app['twig']->render( custom_template('export-email.html'), $output_array);
        $subject = ($email['subject'] != '' ? $email['subject'] : $texts['SEARCH_HOME'] . ' | ' . $texts['BVS_TITLE']);

        # check if param email (to) is in the format of email list separated by ;
        if ( !is_array($email['email']) && strpos($email['email'], ';') !== false) {
            $to_email = explode(';', $email['email']);
        }else{
            $to_email = $email['email'];
        }

        $message = \Swift_Message::newInstance()
            ->setSubject($subject)
            ->setFrom(array(FROM_MAIL => $email['name'] . ' (' . $texts['BVS_HOME'] . ')') )
            ->setTo($to_email)
            ->setBody($render, 'text/html');

        if ( $app['mailer']->send($message) ){
            $output_array['flash_message'] = 'MAIL_SUCCESS';
        }else{
            $output_array['flash_message'] = 'MAIL_FAIL';
        }

    }

    log_user_action($lang, $col, $site, $q, $index, $params['where'], $solr_param_fq,
                    $page, $output, $SESSION->getId(), $format, $params['sort']);

    // output
    switch($output) {

        case "xml": case "sol":
            return new Response($dia_response, 200, array("Content-type" => "text/xml"));
            break;

        case "print":
            return $app['twig']->render('print.html', $output_array);
            break;

        case "rss":
            $output_array['search_url'] =  'http://' . $_SERVER['HTTP_HOST'] . str_replace('output=rss', 'output=site', $_SERVER['REQUEST_URI']);
            $response = new Response($app['twig']->render( custom_template('export-rss.html'), $output_array));
            $response->headers->set('Content-type', 'text/xml');
            return $response->sendHeaders();
            break;

        case "metasearch":
            $response = new Response($app['twig']->render('export-metasearch.html', $output_array));
            $response->headers->set('Content-type', 'text/xml');
            return $response->sendHeaders();
            break;

        case "citation":
            $export_template = 'export-citation.html';
            $export_filename = 'export.txt';
            $content_type = 'text/plain';
        case "ris":
            if ( !isset($export_template) ){
                $export_template = 'export-ris.html';
                $export_filename = 'export.ris';
                $content_type = 'text/plain';
            }
        case "bibtex":
            if ( !isset($export_template) ){
                $export_template = 'export-bibtex.html';
                $export_filename = 'export.bib';
                $content_type = 'text/plain';
            }
        case "csv":
            if ( !isset($export_template) ){
                $export_template = 'export-csv.txt';
                $export_filename = 'export.csv';
                $content_type = 'text/csv';
            }
            if ( !isset($export_total) ){
                $export_total = ( (isset($config->max_export_records) && $config->max_export_records > 0)  ? $config->max_export_records : $pag['total']);
            }

            $export_content = "";
            while ($from < $export_total){
                $export_content .= $app['twig']->render( custom_template($export_template), $output_array);

                $from = $from + $count;

                // Dia response
                $dia = new Dia($site, $col, $count, $output, $lang);
                $dia->setParam('fb', $fb);
                $dia->setParam('sort', $sort_value);
                $dia->setParam('initial_filter', $initial_filter );

                $dia_response = $dia->search($q, $index, $user_filter, $from);
                $result = json_decode($dia_response, true);

                $output_array['from'] = $from;
                $output_array['config'] = $config;
                $output_array['texts'] = $texts;
                $output_array['current_url'] = $_SERVER['REQUEST_URI'];
                $output_array['display_file'] = "result-format-" . $format . ".html";
                $output_array['debug'] = (isset($params['debug'])) ? $params['debug'] : false;
                $output_array['docs'] = $result['diaServerResponse'][0]['response']['docs'];
            }
            if ($output == 'csv'){
                $export_content = preg_replace("/\n/", " ", $export_content);                 //Remove line end
                $export_content = preg_replace("/#BR#/", "\r\n", $export_content);            //Windows Line end
            }else{
                $export_content = normalize_line_end($export_content);
            }

            $response = new Response($export_content);
            $response->headers->set('Content-Encoding', 'UTF-8');
            $response->headers->set('Content-Type', $content_type .'; charset=UTF-8');
            header('Content-Disposition: attachment; filename=' . $export_filename);
            echo "\xEF\xBB\xBF"; // UTF-8 BOM
            return $response->sendHeaders();
            break;

        default:
            $check_mobile = (bool)$config->mobile_version;
            $view = ( isset($params['view']) ? $params['view'] : '');

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
            return $app['twig']->render( custom_template($view . '/index.html'), $output_array);

            break;
    }

});

?>
