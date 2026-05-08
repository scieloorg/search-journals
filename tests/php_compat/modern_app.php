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

$texts = array(
    'SEARCH_HOME' => 'Search',
);
$lang = 'en';

require_once $autoload;
require_once $rootDir . '/iahx/lib/functions.php';
require_once $rootDir . '/iahx/lib/modern/app.php';

use Symfony\Component\HttpFoundation\Request;
use Symfony\Component\Mailer\MailerInterface;
use Twig\Environment;

$app = iahx_modern_create_search_application(
    TEMPLATE_PATH,
    array(
        'debug' => true,
        'smtp_host' => getenv('SEARCH_SMTP_SERVER') ?: 'host.docker.internal',
        'smtp_port' => getenv('SEARCH_SMTP_PORT') ?: 1025,
        'session' => array('mock' => true),
    )
);

if (!$app['twig'] instanceof Environment) {
    fwrite(STDERR, "Missing modern Twig service.\n");
    exit(1);
}

if (!$app['mailer'] instanceof MailerInterface) {
    fwrite(STDERR, "Missing modern Mailer service.\n");
    exit(1);
}

$app['session']->start();
$app['session']->set('bookmark', array('S1020' => array('id' => 'S1020')));
$app['session']->save();

$app->match('/probe/{name}/', function (Request $request, $name) use ($app) {
    $template = $app['twig']->createTemplate(
        '{{ translate("SEARCH_HOME") }}|' .
        '{{ name }}|' .
        '{{ check }}|' .
        '{{ custom_template("index.html") }}'
    );

    return $template->render(array(
        'name' => $name,
        'check' => $app['request']->query->get('check'),
    ));
});

$app->match('/bookmark/{action}/{id}', function (Request $request, $action, $id) use ($app) {
    return $action . ':' . ($id ?: 'none') . ':' . count($app['session']->get('bookmark'));
})->value('id', null);

$response = $app->handle(Request::create('/probe/scielo/', 'GET', array('check' => 'ok')));
if ($response->getStatusCode() !== 200 || $response->getContent() !== 'Search|scielo|ok|custom/index.html') {
    fwrite(STDERR, "Unexpected modern application response: " . $response->getContent() . "\n");
    exit(1);
}

$response = $app->handle(Request::create('/bookmark/list', 'GET'));
if ($response->getStatusCode() !== 200 || $response->getContent() !== 'list:none:1') {
    fwrite(STDERR, "Unexpected modern session/default route response: " . $response->getContent() . "\n");
    exit(1);
}

echo "Modern application bootstrap passed\n";
