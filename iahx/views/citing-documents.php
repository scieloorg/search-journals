<?php

use Symfony\Component\HttpFoundation\Request;

$app->get('citing-documents/{id}/', function (Request $request, $id) use ($app, $DEFAULT_PARAMS, $config) {

    global $lang, $texts;

    $params = array_merge(
        $app['request']->request->all(),
        $app['request']->query->all()
    );

    $lang = $request->get("lang");
    if (! isset($lang) or ! in_array($lang, array('pt', 'es', 'en'))) {
        $lang = $DEFAULT_PARAMS['lang'];
    }

    $texts = parse_ini_file(TRANSLATE_PATH . $lang . "/texts.ini", true);

    $view = $request->get("view");
    $site = $DEFAULT_PARAMS['defaultSite'];
    $col = $DEFAULT_PARAMS['defaultCollection'];

    # Serão exibidos cinco documentos citantes por vez
    $count = 5;

    $output = "site";

    $q = $id;

    $dia = new Dia($site, $col, $count, $output, $lang);
    $dia_response = $dia->search($q);

    $result = json_decode($dia_response, true);

    $citation = $result['diaServerResponse'][0]['response']['docs'][0];

    $output_array = array();

    if (isset($citation)) {
        $page = 1;
        if (isset($params['page']) and $params['page'] != "") {
            $page = $params['page'];
        }
        if ($page > 1) {
            $from = (($page - 1) * $count);
        } else {
            $from = 0;
        }

        $citing_docs_ids = $citation['document_fk'];

        $pag = array();
        $pag['total'] = sizeof($citing_docs_ids);
        $pag['total_pages'] = ($pag['total'] % $count == 0) ? (int)($pag['total']/$count) : (int)($pag['total']/$count+1);

        # Estratégia para evitar acesso a páginas inválidas
        if ($page > $pag['total_pages']){
            $page = $pag['total_pages'];
            $from = ($page * $count) - $count;
        } else if ($page < 1) {
            $page = 1;
            $from = 0;
        }

        $end_pos = $from + $count;
        $nq = '+id:(';

        # A páginação é controlada pela variável $from, que é incrementada de 5 em 5 documentos
        # A vantagem é que são requisitados ao Solr no máximo cinco documentos por vez
        for ($pos = $from; $pos < $end_pos; $pos += 1) {
            $nq .= '"' . $citing_docs_ids[$pos] . '"';
            if ($pos < $end_pos - 1) {
                $nq .= ' OR ';
            }
        }
        $nq = $nq . ')';

        $dia_response_docs = $dia->search($nq, null, null, 0);
        $result_docs = json_decode($dia_response_docs, true);

        $output_array['lang'] = $lang;
        $output_array['pag'] = $pag;
        $output_array['page'] = $page;
        $output_array['pos'] = $from;
        $output_array['config'] = $config;
        $output_array['texts'] = $texts;
        $output_array['citation_id'] = $id;
        $output_array['citing_docs'] = $result_docs['diaServerResponse'][0]['response']['docs'];
    }

    echo $app['twig']->render(custom_template($view . '/result-citing-docs.html'), $output_array);

});

?>