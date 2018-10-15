<?php

include_once 'lib/class/chart.class.php';
use Symfony\Component\HttpFoundation\Request;
use Symfony\Component\HttpFoundation\Response;

$app->match('chart/', function (Request $request) use ($app, $DEFAULT_PARAMS, $config) {

    $params = array_merge(
        $app['request']->request->all(),
        $app['request']->query->all()
    );

    if(!isset($params['d']) or !isset($params['l']) or !isset($params['title'])) 
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

    $g = new graph();
    $g->js_path = STATIC_URL . "js/";
    $g->set_swf_path(STATIC_URL . "swf/");
    $g->title( $title, '{font-size: 18px; color: #A0A0A0;}' );
    $g->set_inner_background( '#E3F0FD', '#CBD7E6', 90 );
    $g->bg_colour = '#FFFFFF';

    if ($sort == true){
        array_multisort($labels,$data);
    }  

    if ($type == 'line'){

        $g->set_data($data);
        $g->line_hollow( 2, 4, '#5E83BF', 'Documentos', 10 );

        $g->set_x_labels($labels);
        $g->set_x_label_style( 10, '0x000000', 0, 2 );

        $g->set_y_max( max($data) );
        $g->y_label_steps(4);

    }else if ($type == 'pie'){

        $g->pie(60,'#505050','{font-size: 11px; color: #404040}');
        
        $g->pie_values( $data, $labels );
        $g->pie_slice_colours( array('#d01f3c','#356aa0','#C79810','#FFCC99','#009933','#FF99FF','#33FFFF','#CCCC99','#330033','#00CCFF','#CCCCCC','#FFCC00','#FF0033','#660000','#FFCCCC','#33FF33','#FF6633' ) );

    }else if ($type == 'export-csv'){

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

        $bar = new bar( 95, '#5E83BF', '#424581' );
        //$bar->key( 'documentos', 10 );
        
        $bar->data = $data;
        
        // set the X axis labels
        $g->set_x_labels( $labels );
        
        //$g->set_data( $data );
        //$g->bar_sketch( 50, 6, '#99FF00', '#7030A0', '% Complete', 10 );
        // add the bar object to the graph
        //
        $g->data_sets[] = $bar;
        
        $g->set_x_max(count($labels));
        $g->set_x_min(count($labels));
        
        $g->set_x_label_style( 11, '#A0A0A0', 2 );
        $g->set_y_label_style( 11, '#A0A0A0' );
        $g->x_axis_colour( '#A0A0A0', '#FFFFFF' );
        
        //$g->set_x_legend( 'Week 1', 12, '#A0A0A0' );
        $g->y_axis_colour( '#A0A0A0', '#FFFFFF' );
        
        
        $g->set_y_min( min($data) );
        $g->set_y_max( max($data) );
        $g->y_label_steps( 2 );
    }

    $g->set_width( 630 );
    $g->set_height( 430 );
    $g->set_output_type('js');

    $output['title'] = $title;
    $output['graph'] = $g->render();
    $output['resubmit'] = $resubmit;

    return $app['twig']->render('chart.html', $output);

});

?>