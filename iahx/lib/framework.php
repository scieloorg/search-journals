<?php

function iahx_create_application($templatePath) {
    $app = new Silex\Application();

    $app->register(new Silex\Provider\TwigServiceProvider(), array(
        'twig.path' => $templatePath,
    ));

    return $app;
}

function iahx_configure_debug($app, $config) {
    if ($config->environment != "production") {
        $app['debug'] = "true";
        define('DEBUG', true);
    } else {
        define('DEBUG', false);
    }
}

function iahx_register_mailer($app) {
    $app->register(new Silex\Provider\SwiftmailerServiceProvider());
    $app['swiftmailer.options'] = array(
        'transport' => 'smtp',
        'host' => SMTP_SERVER,
        'username' => SMTP_USERNAME,
        'password' => SMTP_USERPASSWORD,
        'port' => (defined('SMTP_PORT') && SMTP_PORT != '' ? SMTP_PORT : 25),
        'encryption' => (defined('SMTP_ENCRYPTION') && SMTP_ENCRYPTION != '' ? SMTP_ENCRYPTION : '')
    );
}

function iahx_configure_twig_cache($app, $cachePath) {
    if (!DEBUG) {
        if (!is_dir($cachePath)) {
            if (!mkdir($cachePath)) {
                die("ERROR: can't create cache's directory.");
            }
        }

        $app['twig.options'] = array('strict_variables' => false, 'cache' => $cachePath);
    } else {
        $app['twig.options'] = array('strict_variables' => false);
    }
}

function iahx_register_session($app, $serverName) {
    $app->register(new Silex\Provider\SessionServiceProvider(), array(
        'session.storage.save_path' => '/tmp/sessions/iahx',
        'session.storage.options' => array(
            'name' => 'iahx',
            'cookie_path' => "/",
            'cookie_domain' => $serverName,
            'cookie_lifetime' => 604800 * 4,
        ),
    ));
}

function iahx_register_twig_extensions($app) {
    $app['twig']->addFunction('custom_template', new Twig_Function_Function('custom_template'));
    $app['twig']->addFunction('occ', new Twig_Function_Function('occ'));
    $app['twig']->addFunction('translate', new Twig_Function_Function('translate'));
    $app['twig']->addFunction('has_translation', new Twig_Function_Function('has_translation'));
    $app['twig']->addFilter('substring_before', new Twig_Filter_Function('filter_substring_before'));
    $app['twig']->addFilter('substring_after', new Twig_Filter_Function('filter_substring_after'));
    $app['twig']->addFilter('contains', new Twig_Filter_Function('filter_contains'));
    $app['twig']->addFilter('starts_with', new Twig_Filter_Function('filter_starts_with'));
    $app['twig']->addFilter('truncate', new Twig_Filter_Function('filter_truncate'));
    $app['twig']->addFilter('slugify', new Twig_Filter_Function('filter_slugify'));
    $app['twig']->addFilter('subfield', new Twig_Filter_Function('filter_subfield'));
    $app['twig']->addFilter('filters_to_string', new Twig_Filter_Function('filters_to_string'));
}

?>
