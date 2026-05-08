<?php

use Twig\Environment;
use Twig\Loader\FilesystemLoader;
use Twig\TwigFilter;
use Twig\TwigFunction;

function iahx_modern_create_twig($templatePath, $cachePath = false, $debug = false) {
    $twig = new Environment(
        new FilesystemLoader($templatePath),
        array(
            'strict_variables' => false,
            'cache' => $debug ? false : $cachePath,
            'debug' => $debug,
        )
    );

    iahx_modern_register_twig_extensions($twig);

    return $twig;
}

function iahx_modern_register_twig_extensions(Environment $twig) {
    $twig->addFunction(new TwigFunction('custom_template', 'custom_template'));
    $twig->addFunction(new TwigFunction('occ', 'occ'));
    $twig->addFunction(new TwigFunction('translate', 'translate'));
    $twig->addFunction(new TwigFunction('has_translation', 'has_translation'));
    $twig->addFilter(new TwigFilter('substring_before', 'filter_substring_before'));
    $twig->addFilter(new TwigFilter('substring_after', 'filter_substring_after'));
    $twig->addFilter(new TwigFilter('contains', 'filter_contains'));
    $twig->addFilter(new TwigFilter('starts_with', 'filter_starts_with'));
    $twig->addFilter(new TwigFilter('truncate', 'filter_truncate'));
    $twig->addFilter(new TwigFilter('slugify', 'filter_slugify'));
    $twig->addFilter(new TwigFilter('subfield', 'filter_subfield'));
    $twig->addFilter(new TwigFilter('filters_to_string', 'filters_to_string'));
}

