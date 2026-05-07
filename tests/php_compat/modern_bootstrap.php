<?php

$rootDir = dirname(__DIR__, 2);
$autoload = $rootDir . '/vendor-modern/autoload.php';

if (!file_exists($autoload)) {
    fwrite(STDERR, "Missing vendor-modern/autoload.php. Run composer install with composer.modern.json first.\n");
    exit(1);
}

define('APP_PATH', $rootDir . '/iahx-sites/scieloorg/');
define('TEMPLATE_PATH', APP_PATH . 'templates/');
define('CUSTOM_TEMPLATE_PATH', TEMPLATE_PATH . 'custom/');
define('TRANSLATE_PATH', APP_PATH . 'locale/');

$texts = array(
    'SEARCH_HOME' => 'Search',
    'BVS_TITLE' => 'SciELO',
);
$lang = 'en';

require_once $autoload;
require_once $rootDir . '/iahx/lib/functions.php';
require_once $rootDir . '/iahx/lib/modern/twig.php';

$twig = iahx_modern_create_twig(TEMPLATE_PATH, false, true);

foreach (array('custom_template', 'occ', 'translate', 'has_translation') as $name) {
    if (!$twig->getFunction($name)) {
        fwrite(STDERR, "Missing Twig function: {$name}\n");
        exit(1);
    }
}

foreach (array('substring_before', 'substring_after', 'contains', 'starts_with', 'truncate', 'slugify', 'subfield', 'filters_to_string') as $name) {
    if (!$twig->getFilter($name)) {
        fwrite(STDERR, "Missing Twig filter: {$name}\n");
        exit(1);
    }
}

$template = $twig->createTemplate(
    '{{ "alpha-beta"|substring_before("-") }}|' .
    '{{ "alpha-beta"|substring_after("-") }}|' .
    '{{ "alpha-beta"|contains("beta") ? "contains" : "missing" }}|' .
    '{{ custom_template("index.html") }}'
);

$output = $template->render();

if ($output !== 'alpha|beta|contains|custom/index.html') {
    fwrite(STDERR, "Unexpected Twig render output: {$output}\n");
    exit(1);
}

echo "Modern Twig bootstrap passed\n";
