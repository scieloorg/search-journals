<?php

$rootDir = dirname(__DIR__, 2);
$autoload = $rootDir . '/vendor-modern/autoload.php';

if (!file_exists($autoload)) {
    fwrite(STDERR, "Missing vendor-modern/autoload.php. Run composer install with composer.modern.json first.\n");
    exit(1);
}

class Dia {
    public function __construct($site, $collection, $count, $output, $lang) {
    }

    public function search($q) {
        return json_encode(array(
            'diaServerResponse' => array(
                array(
                    'response' => array(
                        'numFound' => 1,
                        'docs' => array(
                            array(
                                'id' => 'S0100-00002024000100001',
                                'ti' => array('Modern PHP resource route'),
                                'au' => array('SciELO Team'),
                                'in' => array('scl'),
                                'la' => array('en'),
                                'type' => array('article'),
                                'journal_title' => 'SciELO Journal',
                                'issn' => array('1234-5678'),
                                'publisher' => 'SciELO',
                                'da' => '2024-01-15',
                                'volume' => '1',
                                'issue' => '1',
                                'start_page' => '1',
                                'end_page' => '10',
                                'ab_en' => array('The resource route renders under the modern bootstrap.'),
                                'ur' => array('https://example.test/article/S0100-00002024000100001'),
                            ),
                        ),
                    ),
                ),
            ),
        ));
    }

    public function related($id) {
        return $this->search('id:"' . $id . '"');
    }
}

class Mobile_Detect {
    public function isMobile() {
        return true;
    }

    public function isTablet() {
        return false;
    }
}

define('FROM_MAIL', 'suporte.aplicacao@scielo.org');
define('APP_PATH', $rootDir . '/iahx-sites/scieloorg/');
define('TEMPLATE_PATH', APP_PATH . 'templates/');
define('CUSTOM_TEMPLATE_PATH', TEMPLATE_PATH . 'custom/');
define('TRANSLATE_PATH', APP_PATH . 'locale/');
define('SEARCH_URL', 'http://example.test/');
define('STATIC_URL', SEARCH_URL . 'static/');
define('COOKIE_POLICY_ENABLED', 'false');
define('COOKIE_POLICY_SCRIPT_URL', '');
define('LOG_DIR', sys_get_temp_dir() . '/iahx-modern-resource-logs/');
define('LOG_FILE', 'resource.log');

$_SERVER['REMOTE_ADDR'] = '127.0.0.1';
$_SERVER['HTTP_REFERER'] = 'http://example.test/';

require_once $autoload;
require_once $rootDir . '/iahx/lib/class/log.class.php';
require_once $rootDir . '/iahx/lib/functions.php';
require_once $rootDir . '/iahx/lib/modern/app.php';
set_include_path($rootDir . '/iahx' . PATH_SEPARATOR . get_include_path());

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

require $rootDir . '/iahx/views/resource.php';

$response = $app->handle(Request::create(
    '/resource/en/S0100-00002024000100001',
    'GET',
    array('view' => 'mobile')
));

if ($response->getStatusCode() !== 200) {
    fwrite(STDERR, "Unexpected resource status: " . $response->getStatusCode() . "\n");
    exit(1);
}

$content = $response->getContent();
foreach (array('Modern PHP resource route', 'SciELO Team', 'SciELO', 'modern bootstrap') as $expected) {
    if (strpos($content, $expected) === false) {
        fwrite(STDERR, "Resource route did not render expected content: {$expected}\n");
        exit(1);
    }
}

if (!is_file(LOG_DIR . LOG_FILE)) {
    fwrite(STDERR, "Resource route did not write a log entry.\n");
    exit(1);
}

echo "Modern resource route passed\n";
