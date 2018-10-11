<?php

include('functions.php');

$query = trim($_REQUEST['query']);
$count = $_REQUEST['count'];
$query = str_replace(" ","+",$query);
$query = remove_accents($query);
$query = $query . "+OR+" . $query ."*";

$jsoncallback = $_REQUEST['callback'];

$lang = trim($_REQUEST['lang']);

$service_url = "http://srv.bvsalud.org/decsQuickTerm/search?query=" . $query . "&count=" . $count . "&lang=" . $lang;

$service_response = file_get_contents($service_url);
$xml = simplexml_load_string($service_response);


$descriptors = array();
$term_list = array();

foreach ($xml->Result->item as $item ) {
    $attr = $item->attributes();
    $term_name = (string)$attr['term'];
    $term_id = (string)$attr['id'];

    // remove duplications of term name (when term has same name in other languages)
    if ( !in_array($term_name, $term_list)) {
        $descriptors[] = array('name' => $term_name, 'id' => $term_id);
        $term_list[] = $term_name;
    }
}

$result = array(
			'query' => $_REQUEST['query'],
            'descriptors' => $descriptors,
			);
$result_json = json_encode($result);

if (isset($jsoncallback) &&  $jsoncallback != ''){
    $result_json = $jsoncallback . "(" . $result_json . ")";
}

header("Content-type: application/json;charset=UTF-8");
echo trim($result_json);
?>
