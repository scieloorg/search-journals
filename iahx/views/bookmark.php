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

    if(strpos($id,",") !== false) {
        $id = explode(",",$id);
        $id = array_filter($id);
    }

    if($action == 'a') {
        if(is_array($id)) {
            for($i=0;$i<count($id);$i++) {
                $item = array('id' => $id[$i], 'timestamp' => time());
                $idi = $id[$i];
                $bookmark[$idi] = $item;        
            }
        } else {
            $item = array('id' => $id, 'timestamp' => time());
            $bookmark[$id] = $item;    
        }
    }

    if($action == 'c') {
        $bookmark = array();
    }

    if($action == 'd') {
        if(is_array($id)) {
            for($i=0;$i<count($id);$i++) {
                $idi = $id[$i];

                if(isset($bookmark[$idi])) {
                    unset($bookmark[$idi]);
                }        
            }
        } else {
            if(isset($bookmark[$id])) {
                unset($bookmark[$id]);
            }    
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