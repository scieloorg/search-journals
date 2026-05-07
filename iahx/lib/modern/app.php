<?php

require_once __DIR__ . '/http.php';
require_once __DIR__ . '/mailer.php';
require_once __DIR__ . '/twig.php';

function iahx_modern_create_search_application($templatePath, array $options = array()) {
    $debug = isset($options['debug']) ? (bool) $options['debug'] : false;
    $cachePath = array_key_exists('cache_path', $options) ? $options['cache_path'] : false;

    $services = array(
        'twig' => iahx_modern_create_twig($templatePath, $cachePath, $debug),
        'mailer' => iahx_modern_create_mailer(
            $options['smtp_host'] ?? null,
            $options['smtp_port'] ?? null,
            $options['smtp_username'] ?? null,
            $options['smtp_password'] ?? null,
            $options['smtp_encryption'] ?? null
        ),
    );

    return iahx_modern_create_application($services);
}
