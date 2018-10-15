<?php
use Symfony\Component\HttpFoundation\Request;
use Symfony\Component\HttpFoundation\Response;

$app->match('pubmed_linkout/{lang}/{pmid}', function (Request $request, $lang, $pmid) use ($app) {

    $pmid = str_replace('mdl-','',$pmid);

    $linkout_url = "http://eutils.ncbi.nlm.nih.gov/entrez/eutils/elink.fcgi?dbfrom=pubmed&id=" . $pmid ."&cmd=llinks";

    $linkout_xml = @simplexml_load_file($linkout_url);
    
    if ($linkout_xml){

        $set = $linkout_xml->LinkSet->IdUrlList->IdUrlSet->ObjUrl;
        // output vars
        $output_array = array();
        $output_array['lang'] = $lang;
        $output_array['set'] = $set;

        // start session
        $SESSION = $app['session'];
        $SESSION->start();    

        // log user action
        log_user_action($lang, '', '', 'PMID:' . $pmid, '', '', '', '', 'pubmed_linkout', $SESSION->getId());

        return $app['twig']->render( 'pubmed_linkout.html', $output_array );     

    }

});

?>
