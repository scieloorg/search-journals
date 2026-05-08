<?php

$rootDir = dirname(__DIR__, 2);
$autoload = $rootDir . '/vendor-modern/autoload.php';

if (!file_exists($autoload)) {
    fwrite(STDERR, "Missing vendor-modern/autoload.php. Run composer install with composer.modern.json first.\n");
    exit(1);
}

$_SERVER['PHP_SELF'] = '/modern_index.php';
$_SERVER['DOCUMENT_ROOT'] = $rootDir . '/iahx-sites/scieloorg';
$_SERVER['HTTP_HOST'] = 'example.test';
$_SERVER['REMOTE_ADDR'] = '127.0.0.1';
$_SERVER['HTTP_REFERER'] = 'http://example.test/';

require $rootDir . '/iahx-sites/scieloorg/modern_environment.php';
require $rootDir . '/iahx-sites/scieloorg/modern_routes.php';

use Symfony\Component\HttpFoundation\Request;

$response = $app->handle(Request::create('/advanced/', 'GET', array('lang' => 'en')));
$content = $response->getContent();

if ($response->getStatusCode() !== 200 || strpos($content, 'Advanced Search') === false) {
    fwrite(STDERR, "Modern SciELO index did not serve the advanced route.\n");
    exit(1);
}

$response = $app->handle(Request::create('/bookmark/c', 'GET'));
if ($response->getStatusCode() !== 200 || $response->getContent() !== '0') {
    fwrite(STDERR, "Modern SciELO index did not serve the bookmark route.\n");
    exit(1);
}

echo "Modern SciELO index passed\n";
