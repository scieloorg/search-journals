<?php

$rootDir = dirname(__DIR__, 2);
$autoload = $rootDir . '/vendor-modern/autoload.php';

if (!file_exists($autoload)) {
    fwrite(STDERR, "Missing vendor-modern/autoload.php. Run composer install with composer.modern.json first.\n");
    exit(1);
}

require_once $autoload;
require_once $rootDir . '/iahx/lib/modern/http.php';

use Symfony\Component\HttpFoundation\Request;
use Symfony\Component\HttpFoundation\Response;

$app = iahx_modern_create_application(array('name' => 'SciELO'));

$app->get('health/{name}/', function (Request $request, $name) use ($app) {
    return $app['name'] . ':' . $request->query->get('check') . ':' . $name;
});

$app->match('/', function (Request $request) {
    return new Response($request->getMethod() . ':home', 201, array('X-IAHX' => 'modern'));
});

$response = $app->handle(Request::create('/health/search/', 'GET', array('check' => 'ok')));
if ($response->getStatusCode() !== 200 || $response->getContent() !== 'SciELO:ok:search') {
    fwrite(STDERR, "Unexpected GET route response.\n");
    exit(1);
}

$response = $app->handle(Request::create('/', 'POST'));
if ($response->getStatusCode() !== 201 || $response->headers->get('X-IAHX') !== 'modern' || $response->getContent() !== 'POST:home') {
    fwrite(STDERR, "Unexpected match route response.\n");
    exit(1);
}

echo "Modern HTTP bootstrap passed\n";
