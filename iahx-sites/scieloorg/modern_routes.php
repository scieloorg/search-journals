<?php

foreach (array(
    'advanced.php',
    'bookmark.php',
    'history.php',
    'list_filter.php',
    'resource.php',
) as $routeFile) {
    require_once VIEWS_PATH . $routeFile;
}
