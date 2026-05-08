<?php

$rootDir = dirname(__DIR__, 2);
$autoload = $rootDir . '/vendor-modern/autoload.php';

if (!file_exists($autoload)) {
    fwrite(STDERR, "Missing vendor-modern/autoload.php. Run composer install with composer.modern.json first.\n");
    exit(1);
}

class Dia {
    public $params = array();

    public function __construct($site, $collection, $count, $output, $lang) {
    }

    public function setParam($name, $value) {
        $this->params[$name] = $value;
    }

    public function search($q, $index, $filter) {
        return json_encode(array(
            'diaServerResponse' => array(
                array(
                    'facet_counts' => array(
                        'facet_fields' => array(
                            'year_cluster' => array(
                                array('2024', 10),
                                array('2023', 7),
                            ),
                            'la' => array(
                                array('en', 12),
                                array('pt', 9),
                            ),
                        ),
                    ),
                ),
            ),
        ));
    }
}

define('FROM_MAIL', 'suporte.aplicacao@scielo.org');
define('APP_PATH', $rootDir . '/iahx-sites/scieloorg/');
define('TEMPLATE_PATH', APP_PATH . 'templates/');
define('CUSTOM_TEMPLATE_PATH', TEMPLATE_PATH . 'custom/');
define('TRANSLATE_PATH', APP_PATH . 'locale/');
define('SEARCH_URL', 'http://example.test/');
define('STATIC_URL', SEARCH_URL . 'static/');

require_once $autoload;
require_once $rootDir . '/iahx/lib/functions.php';
require_once $rootDir . '/iahx/lib/modern/app.php';

use Symfony\Component\HttpFoundation\Request;

$config = simplexml_load_file(APP_PATH . 'config/config.xml');
$collectionData = $config->search_collection_list->collection[0];
$DEFAULT_PARAMS = array(
    'lang' => 'en',
    'defaultCollectionData' => $collectionData,
    'defaultCollection' => (string) $collectionData->name,
    'defaultSite' => (string) $config->site,
);

$app = iahx_modern_create_search_application(
    TEMPLATE_PATH,
    array(
        'debug' => true,
        'smtp_host' => getenv('SEARCH_SMTP_SERVER') ?: 'host.docker.internal',
        'smtp_port' => getenv('SEARCH_SMTP_PORT') ?: 1025,
        'session' => array('mock' => true),
    )
);

require $rootDir . '/iahx/views/list_filter.php';

$response = $app->handle(Request::create('/list-filter/year_cluster', 'GET', array(
    'lang' => 'en',
    'q' => 'malaria',
    'limit' => '2',
)));
$content = $response->getContent();

foreach (array('filter_year_cluster', '2024', '2023', '10', '7') as $expected) {
    if (strpos($content, $expected) === false) {
        fwrite(STDERR, "List-filter route did not render expected content: {$expected}\n");
        exit(1);
    }
}

$response = $app->handle(Request::create('/list-filter/la', 'GET', array(
    'lang' => 'en',
    'q' => 'malaria',
)));
$content = $response->getContent();

foreach (array('mainLanguageSelect', 'en', 'pt') as $expected) {
    if (strpos($content, $expected) === false) {
        fwrite(STDERR, "List-filter language route did not render expected content: {$expected}\n");
        exit(1);
    }
}

echo "Modern list-filter route passed\n";
