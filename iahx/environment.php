<?php

// ENVIRONMENT CONSTANTS
$PATH = str_replace("index.php", "", $_SERVER['PHP_SELF']);
$PATH_DATA = __DIR__ . "/";

$config["PATH_DATA"] = $PATH_DATA;
$config["DOCUMENT_ROOT"] = $_SERVER["DOCUMENT_ROOT"];
$config["SERVERNAME"] = $_SERVER["HTTP_HOST"];

define("SERVERNAME", $config["SERVERNAME"]);
define("PATH_DATA" , $config["PATH_DATA"]);
define("DOCUMENT_ROOT", $config["DOCUMENT_ROOT"]);
define("APP_PATH", $PATH_DATA);

define("TEMPLATE_PATH", APP_PATH . "templates/");
define("VIEWS_PATH", APP_PATH . "views/");
define("TRANSLATE_PATH", APP_PATH . "locale/");
define("CACHE_PATH", APP_PATH . "cache/");

// custom applications/interface
define("CUSTOM_TEMPLATE_PATH", TEMPLATE_PATH . "custom/");

// CONFIGURATION
$config = simplexml_load_file($PATH_DATA . 'config/config.xml');
$config->search_server = getenv('SEARCH_SOLR_SERVER', true) ?: $config->search_server;

$lang = $config->default_lang;

$config->site = getenv('SEARCH_SOLR_CORE', true) ?: $config->site;

$DEFAULT_PARAMS = array();
$DEFAULT_PARAMS['lang'] = $lang;
$DEFAULT_PARAMS['defaultCollectionData'] = $config->search_collection_list->collection[0];

// verifica se existe apenas uma colecao definida no config.xml
if ( !is_array($DEFAULT_PARAMS['defaultCollectionData']) ){
    $DEFAULT_PARAMS['defaultCollectionData'] = $config->search_collection_list->collection;
}
$DEFAULT_PARAMS['defaultCollection'] = $DEFAULT_PARAMS['defaultCollectionData']->name;
$DEFAULT_PARAMS['defaultSite'] = $DEFAULT_PARAMS['defaultCollectionData']->site;

if ($DEFAULT_PARAMS['defaultSite'] == ""){
    $DEFAULT_PARAMS['defaultSite'] = $config->site;
}

$DEFAULT_PARAMS['defaultDisplayFormat'] = (string) $DEFAULT_PARAMS['defaultCollectionData']->format_list[0]->format[0]->name;

$config->use_https = getenv('SEARCH_USE_HTTPS', true) ?: $config->site;

// urls
$protocol = ( (isset($config->use_https) && $config->use_https == 'true') ? 'https' : 'http');

define("SEARCH_URL",  $protocol . "://" . $_SERVER['HTTP_HOST'] . $PATH);
define("STATIC_URL",  SEARCH_URL . "static/");

// check if cookie policy bar is enabled = cookie_policy_enabled
$config->cookie_policy_enabled = getenv('COOKIE_POLICY_ENABLED') ? getenv('COOKIE_POLICY_ENABLED') : $config->cookie_policy_enabled;
define("COOKIE_POLICY_ENABLED",  $config->cookie_policy_enabled);

// src of cookie policy bar script
$config->cookie_policy_script_url = getenv('COOKIE_POLICY_SCRIPT_URL') ? getenv('COOKIE_POLICY_SCRIPT_URL') : $config->cookie_policy_script_url;
define("COOKIE_POLICY_SCRIPT_URL",  $config->cookie_policy_script_url);

// log's configuration
$logDir = ( isset( $config->log_dir ) ? $config->log_dir : "logs/");
define('LOG_FILE',"log" . date('Ymd') . "_search.txt");
define('LOG_DIR', $logDir);

// FRAMEWORK
// Initiating Silex framework
require_once 'lib/silex/vendor/autoload.php';
require_once 'lib/framework.php';
$app = iahx_create_application(TEMPLATE_PATH);
iahx_configure_debug($app, $config);

// registering email
require_once "config/config-mail.php";
iahx_register_mailer($app);

// if isn't in debug ambient, create de cache dir and set to be cacheable
iahx_configure_twig_cache($app, CACHE_PATH);


// PREPARING THE ENVIRONMENT
// requiring custom functions
require_once "lib/functions.php";

// registering sessions
iahx_register_session($app, SERVERNAME);
iahx_register_twig_extensions($app);

?>
