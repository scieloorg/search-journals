<?php

use Symfony\Component\HttpFoundation\Request;
use Symfony\Component\HttpFoundation\Response;

$app->match('bookmark/{action}/{id}', function (Request $request, $action, $id) use ($app) {

    $SESSION = $app['session'];
    $SESSION->start();
    if(!$SESSION->has("bookmark")) {
        $SESSION->set('bookmark', array());   
    }
    
    $bookmark = $SESSION->get('bookmark');

    if($action == 'a') {
        $item = array('id' => $id, 'timestamp' => time());
        $bookmark[$id] = $item;
    }

    if($action == 'c') {
        $bookmark = array();
    }

    if($action == 'd') {
        if(isset($bookmark[$id])) {
            unset($bookmark[$id]);
        }
    }
    
    $count = count($bookmark);
    $SESSION->set('bookmark', $bookmark);   
    $SESSION->save();

    if($action == 'list') {
        $q = '+id:("' . join(array_keys($bookmark), '" OR "') . '")';
        return new Response($q);    
    }
    
    return new Response($count);    

})->value('id', NULL);

?>