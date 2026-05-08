<?php

$rootDir = dirname(__DIR__, 2);
$autoload = $rootDir . '/vendor-modern/autoload.php';

if (!file_exists($autoload)) {
    fwrite(STDERR, "Missing vendor-modern/autoload.php. Run composer install with composer.modern.json first.\n");
    exit(1);
}

define('FROM_MAIL', 'suporte.aplicacao@scielo.org');

require_once $autoload;
require_once $rootDir . '/iahx/lib/modern/mailer.php';

$host = getenv('SEARCH_SMTP_SERVER') ?: 'host.docker.internal';
$port = getenv('SEARCH_SMTP_PORT') ?: 1025;
$mailer = iahx_modern_create_mailer($host, $port);

$recipients = iahx_modern_normalize_recipients('first@example.org; second@example.org;');
if ($recipients !== array('first@example.org', 'second@example.org')) {
    fwrite(STDERR, "Unexpected recipient normalization.\n");
    exit(1);
}

iahx_modern_send_search_email(
    $mailer,
    'Modern mailer smoke',
    'SciELO Search',
    'recipient@example.org',
    '<p>Modern Symfony Mailer bootstrap passed.</p>'
);

$app = array('mailer' => $mailer);
iahx_send_search_email(
    $app,
    'Legacy mailer compatibility smoke',
    'SciELO Search',
    'recipient@example.org',
    '<p>Legacy search mail function delegated to Symfony Mailer.</p>'
);

echo "Modern Mailer bootstrap passed\n";
