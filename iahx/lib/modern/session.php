<?php

use Symfony\Component\HttpFoundation\Session\Session;
use Symfony\Component\HttpFoundation\Session\Storage\MockFileSessionStorage;
use Symfony\Component\HttpFoundation\Session\Storage\NativeSessionStorage;

function iahx_modern_create_session(array $options = array()) {
    $savePath = $options['save_path'] ?? '/tmp/sessions/iahx';
    $sessionOptions = array(
        'name' => $options['name'] ?? 'iahx',
        'cookie_path' => $options['cookie_path'] ?? '/',
        'cookie_domain' => $options['cookie_domain'] ?? '',
        'cookie_lifetime' => $options['cookie_lifetime'] ?? 604800 * 4,
        'save_path' => $savePath,
    );

    if (!empty($options['mock'])) {
        return new Session(new MockFileSessionStorage($savePath));
    }

    if (!is_dir($savePath)) {
        mkdir($savePath, 0777, true);
    }

    return new Session(new NativeSessionStorage($sessionOptions));
}
