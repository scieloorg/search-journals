<?php

$rootDir = dirname(__DIR__, 2);
$autoload = $rootDir . '/vendor-modern/autoload.php';

if (!file_exists($autoload)) {
    fwrite(STDERR, "Missing vendor-modern/autoload.php. Run composer install with composer.modern.json first.\n");
    exit(1);
}

define('FROM_MAIL', 'suporte.aplicacao@scielo.org');
define('APP_PATH', $rootDir . '/iahx-sites/scieloorg/');
define('TEMPLATE_PATH', APP_PATH . 'templates/');
define('CUSTOM_TEMPLATE_PATH', TEMPLATE_PATH . 'custom/');
define('TRANSLATE_PATH', APP_PATH . 'locale/');
define('SEARCH_URL', 'http://example.test/');
define('STATIC_URL', SEARCH_URL . 'static/');
define(' STATIC_URL', STATIC_URL);
define('COOKIE_POLICY_ENABLED', 'false');
define('COOKIE_POLICY_SCRIPT_URL', '');

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

$app['session']->start();
$app['session']->set('history', array(
    array(
        'q' => 'malaria',
        'filter' => array(),
        'total' => 7,
        'detailed_query' => 'malaria',
    ),
    array(
        'q' => 'dengue',
        'filter' => array(),
        'total' => 0,
        'detailed_query' => 'dengue',
    ),
));
$app['session']->save();

require $rootDir . '/iahx/views/history.php';

$response = $app->handle(Request::create('/history/', 'GET', array('lang' => 'en')));
$content = $response->getContent();

foreach (array('History', 'malaria', 'dengue') as $expected) {
    if (strpos($content, $expected) === false) {
        fwrite(STDERR, "History route did not render expected content: {$expected}\n");
        exit(1);
    }
}

$response = $app->handle(Request::create('/history/', 'GET', array('lang' => 'en', 'remove' => 'true', 'item' => '1')));
if (strpos($response->getContent(), 'malaria') !== false || strpos($response->getContent(), 'dengue') === false) {
    fwrite(STDERR, "History route did not remove the expected item.\n");
    exit(1);
}

$response = $app->handle(Request::create('/history/', 'GET', array('lang' => 'en', 'clear' => 'true')));
if (strpos($response->getContent(), 'No stored search in your history') === false) {
    fwrite(STDERR, "History route did not clear the session history.\n");
    exit(1);
}

echo "Modern history route passed\n";
