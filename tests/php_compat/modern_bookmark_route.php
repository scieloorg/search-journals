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

require_once $autoload;
require_once $rootDir . '/iahx/lib/functions.php';
require_once $rootDir . '/iahx/lib/modern/app.php';

use Symfony\Component\HttpFoundation\Request;

$app = iahx_modern_create_search_application(
    TEMPLATE_PATH,
    array(
        'debug' => true,
        'smtp_host' => getenv('SEARCH_SMTP_SERVER') ?: 'host.docker.internal',
        'smtp_port' => getenv('SEARCH_SMTP_PORT') ?: 1025,
        'session' => array('mock' => true),
    )
);

require $rootDir . '/iahx-sites/scieloorg/views/bookmark.php';

$response = $app->handle(Request::create('/bookmark/a/S1020-49892001000400009-spa', 'GET'));
if ($response->getStatusCode() !== 200 || $response->getContent() !== '1') {
    fwrite(STDERR, "Unexpected bookmark add response: " . $response->getContent() . "\n");
    exit(1);
}

$response = $app->handle(Request::create('/bookmark/a/S0102,S1413', 'GET'));
if ($response->getStatusCode() !== 200 || $response->getContent() !== '3') {
    fwrite(STDERR, "Unexpected bookmark multi-add response: " . $response->getContent() . "\n");
    exit(1);
}

$response = $app->handle(Request::create('/bookmark/d/S0102', 'GET'));
if ($response->getStatusCode() !== 200 || $response->getContent() !== '2') {
    fwrite(STDERR, "Unexpected bookmark delete response: " . $response->getContent() . "\n");
    exit(1);
}

$response = $app->handle(Request::create('/bookmark/list', 'GET'));
$expected = '+id:("S1020-49892001000400009-spa" OR "S1413")';
if ($response->getStatusCode() !== 200 || $response->getContent() !== $expected) {
    fwrite(STDERR, "Unexpected bookmark list response: " . $response->getContent() . "\n");
    exit(1);
}

$response = $app->handle(Request::create('/bookmark/c', 'GET'));
if ($response->getStatusCode() !== 200 || $response->getContent() !== '0') {
    fwrite(STDERR, "Unexpected bookmark clear response: " . $response->getContent() . "\n");
    exit(1);
}

echo "Modern bookmark route passed\n";
