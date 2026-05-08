<?php
error_reporting(E_ALL & ~E_DEPRECATED);

$PATH = str_replace("modern_index.php", "", $_SERVER['PHP_SELF'] ?? '/');
$PATH_DATA = __DIR__ . "/";
$ROOT_PATH = dirname(__DIR__, 2) . "/";

$serverName = $_SERVER["HTTP_HOST"] ?? "localhost";
$documentRoot = $_SERVER["DOCUMENT_ROOT"] ?? $PATH_DATA;

define("SERVERNAME", $serverName);
define("PATH_DATA", $PATH_DATA);
define("DOCUMENT_ROOT", $documentRoot);
define("APP_PATH", $PATH_DATA);
define("TEMPLATE_PATH", APP_PATH . "templates/");
define("VIEWS_PATH", APP_PATH . "views/");
define("TRANSLATE_PATH", APP_PATH . "locale/");
define("CACHE_PATH", APP_PATH . "cache/");
define("CUSTOM_TEMPLATE_PATH", TEMPLATE_PATH . "custom/");
set_include_path(APP_PATH . PATH_SEPARATOR . get_include_path());

$config = simplexml_load_file($PATH_DATA . 'config/config.xml');
$config->search_server = getenv('SEARCH_SOLR_SERVER') ?: $config->search_server;

$lang = $config->default_lang;
$config->site = getenv('SEARCH_SOLR_CORE') ?: $config->site;

$DEFAULT_PARAMS = array();
$DEFAULT_PARAMS['lang'] = $lang;
$DEFAULT_PARAMS['defaultCollectionData'] = $config->search_collection_list->collection[0];

if (!is_array($DEFAULT_PARAMS['defaultCollectionData'])) {
    $DEFAULT_PARAMS['defaultCollectionData'] = $config->search_collection_list->collection;
}

$DEFAULT_PARAMS['defaultCollection'] = $DEFAULT_PARAMS['defaultCollectionData']->name;
$DEFAULT_PARAMS['defaultSite'] = $DEFAULT_PARAMS['defaultCollectionData']->site;

if ($DEFAULT_PARAMS['defaultSite'] == "") {
    $DEFAULT_PARAMS['defaultSite'] = $config->site;
}

$DEFAULT_PARAMS['defaultDisplayFormat'] = (string) $DEFAULT_PARAMS['defaultCollectionData']->format_list[0]->format[0]->name;

$config->use_https = getenv('SEARCH_USE_HTTPS') ?: $config->site;

$protocol = ((isset($config->use_https) && $config->use_https == 'true') ? 'https' : 'http');

define("SEARCH_URL", $protocol . "://" . SERVERNAME . $PATH);
define("STATIC_URL", SEARCH_URL . "static/");
define(" STATIC_URL", STATIC_URL);

$config->cookie_policy_enabled = getenv('COOKIE_POLICY_ENABLED') ? getenv('COOKIE_POLICY_ENABLED') : $config->cookie_policy_enabled;
define("COOKIE_POLICY_ENABLED", $config->cookie_policy_enabled);

$config->cookie_policy_script_url = getenv('COOKIE_POLICY_SCRIPT_URL') ? getenv('COOKIE_POLICY_SCRIPT_URL') : $config->cookie_policy_script_url;
define("COOKIE_POLICY_SCRIPT_URL", $config->cookie_policy_script_url);

$logDir = (isset($config->log_dir) ? (string) $config->log_dir : "logs/");
if ($logDir !== '' && $logDir[0] !== '/') {
    $logDir = APP_PATH . $logDir;
}
define('LOG_FILE', "log" . date('Ymd') . "_search.txt");
define('LOG_DIR', $logDir);

require_once $ROOT_PATH . 'vendor-modern/autoload.php';
require_once APP_PATH . 'lib/class/dia.class.php';
require_once APP_PATH . 'lib/class/log.class.php';
require_once APP_PATH . 'lib/Mobile_Detect.php';
require_once APP_PATH . 'lib/functions.php';
require_once APP_PATH . 'lib/modern/app.php';
require_once APP_PATH . 'config/config-mail.php';

$app = iahx_modern_create_search_application(
    TEMPLATE_PATH,
    array(
        'debug' => ((string) $config->debug) === 'true',
        'cache_path' => CACHE_PATH,
        'smtp_host' => getenv('SEARCH_SMTP_SERVER') ?: (defined('SMTP_SERVER') ? SMTP_SERVER : null),
        'smtp_port' => getenv('SEARCH_SMTP_PORT') ?: (defined('SMTP_PORT') ? SMTP_PORT : null),
        'smtp_username' => getenv('SEARCH_SMTP_USERNAME') ?: null,
        'smtp_password' => getenv('SEARCH_SMTP_PASSWORD') ?: null,
        'smtp_encryption' => getenv('SEARCH_SMTP_ENCRYPTION') ?: null,
        'session' => array(
            'name' => preg_replace('/[^A-Za-z0-9_]/', '_', 'iahx_' . SERVERNAME),
        ),
    )
);
