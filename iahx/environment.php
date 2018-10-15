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
$lang = $config->default_lang;

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

// urls
$protocol = ( (isset($config->use_https) && $config->use_https == 'true') ? 'https' : 'http');

define("SEARCH_URL",  $protocol . "://" . $_SERVER['HTTP_HOST'] . $PATH);
define("STATIC_URL",  SEARCH_URL . "static/");


// log's configuration
$logDir = ( isset( $config->log_dir ) ? $config->log_dir : "logs/");
define('LOG_FILE',"log" . date('Ymd') . "_search.txt");
define('LOG_DIR', $logDir);

// FRAMEWORK
// Initiating Silex framework
require_once 'lib/silex/vendor/autoload.php';
$app = new Silex\Application();

// iniciando o twig, buscando templates em /template
$app->register(new Silex\Provider\TwigServiceProvider(), array(
    'twig.path' => TEMPLATE_PATH,
));

if($config->environment != "production") {
    $app['debug'] = "true";
    define('DEBUG', true);
} else {
    define('DEBUG', false);
}

// registering email
require_once "config/config-mail.php";

$app->register(new Silex\Provider\SwiftmailerServiceProvider());
$app['swiftmailer.options'] = array(
    'transport' => 'smtp',
    'host' => SMTP_SERVER,
    'username' => SMTP_USERNAME,
    'password' => SMTP_USERPASSWORD,
    'port' => ( defined('SMTP_PORT') && SMTP_PORT != '' ? SMTP_PORT : 25 ),
    'encryption' => ( defined('SMTP_ENCRYPTION') && SMTP_ENCRYPTION != '' ? SMTP_ENCRYPTION : '')
);

// if isn't in debug ambient, create de cache dir and set to be cacheable
if (!DEBUG) {
    if(!is_dir(CACHE_PATH)) {
        if(!mkdir(CACHE_PATH)) {
            die("ERROR: can't create cache's directory.");
        }
    }

    $app['twig.options'] = array('strict_variables' => false, 'cache' => CACHE_PATH);

} else {
    $app['twig.options'] = array('strict_variables' => false);
}


// PREPARING THE ENVIRONMENT
// requiring custom functions
require_once "lib/functions.php";

// registering sessions
use Silex\Provider\SessionServiceProvider;
$app->register(new SessionServiceProvider, array(
    'session.storage.save_path' => '/tmp/sessions/iahx',
    'session.storage.options' => array(
        'name' => 'iahx',
        'cookie_path' => $PATH,
        'cookie_domain' => '.' . SERVERNAME,
        'cookie_lifetime' => 604800 * 4,  // 4 weeks
    ),

));

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

?>
