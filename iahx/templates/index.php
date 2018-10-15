<?php

require_once 'environment.php';

// include all views created in views path
foreach(glob(VIEWS_PATH . "*.php") as $file) {
    require_once $file;
}

// running the framework
$app->run();

?>