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
define('LOG_DIR', sys_get_temp_dir() . '/iahx-modern-advanced-logs/');
define('LOG_FILE', 'advanced.log');

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

require $rootDir . '/iahx/views/advanced.php';

$response = $app->handle(Request::create('/advanced/', 'GET', array('lang' => 'en')));
$content = $response->getContent();

foreach (array('Advanced Search', 'advanced.js', 'advanced.min.css', 'name="advanced"', 'SEARCH_URL') as $expected) {
    if (strpos($content, $expected) === false) {
        fwrite(STDERR, "Advanced route did not render expected content: {$expected}\n");
        exit(1);
    }
}

if (!is_file(LOG_DIR . LOG_FILE)) {
    fwrite(STDERR, "Advanced route did not write a log entry.\n");
    exit(1);
}

echo "Modern advanced route passed\n";
