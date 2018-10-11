<?php

use Symfony\Component\HttpFoundation\Request;
use Symfony\Component\HttpFoundation\Response;

$app->match('chartjs/', function (Request $request) use ($app, $DEFAULT_PARAMS, $config) {

    $params = array_merge(
        $app['request']->request->all(),
        $app['request']->query->all()
    );

    if(!isset($params['d']) or !isset($params['l'])) 
        die;

    $data = $params['d'];
    $labels = $params['l'];
    $title = $params['title'];

    $type = "";
    if(isset($params['type'])) {
        $type  = $params['type'];
    }

    $sort = "";
    if(isset($params['sort'])) {
        $sort  = $params['sort'];
    }

    $resubmit = $_SERVER['REQUEST_URI'];

    if ($sort == true){
        array_multisort($labels,$data);
    }  

    if ($type == 'export-csv'){

        $csv_out =  "Label,Value\r\n";
        for ( $i = 0; $i < count($data); $i++ ){
            $csv_out .= '"' . $labels[$i] . '","' . $data[$i] . '"' . "\r\n";
        }
        $response = new Response($csv_out);
        $response->headers->set('Content-Encoding', 'UTF-8');
        $response->headers->set('Content-Type', 'text/csv; charset=UTF-8');
        header('Content-Disposition: attachment; filename=export_cluster.csv');
        echo "\xEF\xBB\xBF"; // UTF-8 BOM
        return $response->sendHeaders();

    }else{
        $response = new Response();
        $response->headers->set('Content-Encoding', 'UTF-8');
        $response->headers->set('Content-Type', 'text/json; charset=UTF-8');

        if ($type == 'bar'){
            $json = "{"
                  . '   "labels" :' . json_encode($labels) . ','
                  . '   "datasets" : ['
                  . '       { '
                  . '           "fillColor" : "#6789d3", '
                  . '           "strokeColor" : "#6789d3", ' 
                  . '           "highlightFill": "#3c62b7", '
                  . '           "highlightStroke": "#3c62b7",'
                  . '           "data" : ' . json_encode($data)
                  . '       }'
                  . '   ]'
                  . "}";
        }elseif ($type == 'pie'){
            $colors = array("#1D8BD1", "#F1683C", "#2AD62A", "#DBDC25", "#8FBC8B", "#D2B48C", "#20B2AA",
                            "#B0C4DE", "#DDA0DD", "#9C9AFF", "#9C3063", "#FF8284", "#000084", "#1D8BD1",
                            "#F1683C", "#2AD62A", "#DBDC25");

            $l_total = sizeof($labels);

            $json = "[";
            for($i = 0; $i < $l_total; $i++){
                $json .= '{"value": ' . $data[$i] . ',';
                $json .= ' "label" : "' . $labels[$i] . '", ';
                $json .= ' "color": "' . $colors[$i] . '"}';
                if ($i < ($l_total-1) ){
                  $json .= ',';
                } 
            }
            $json .= "]";
        }
        
        echo $json;
        
        return $response->sendHeaders();
    }   

});

?>