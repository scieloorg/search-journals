<?php

use Symfony\Component\Mailer\Mailer;
use Symfony\Component\Mailer\MailerInterface;
use Symfony\Component\Mailer\Transport\Smtp\EsmtpTransport;
use Symfony\Component\Mime\Address;
use Symfony\Component\Mime\Email;

function iahx_modern_create_mailer($host = null, $port = null, $username = null, $password = null, $encryption = null) {
    $host = $host !== null ? $host : (defined('SMTP_SERVER') ? SMTP_SERVER : 'localhost');
    $port = $port !== null ? $port : (defined('SMTP_PORT') && SMTP_PORT ? SMTP_PORT : 25);
    $username = $username !== null ? $username : (defined('SMTP_USERNAME') ? SMTP_USERNAME : '');
    $password = $password !== null ? $password : (defined('SMTP_USERPASSWORD') ? SMTP_USERPASSWORD : '');
    $encryption = $encryption !== null ? $encryption : (defined('SMTP_ENCRYPTION') ? SMTP_ENCRYPTION : '');

    $transport = new EsmtpTransport($host, (int) $port, iahx_modern_mailer_uses_tls($encryption));

    if ($username !== '') {
        $transport->setUsername($username);
        $transport->setPassword($password);
    }

    return new Mailer($transport);
}

function iahx_modern_mailer_uses_tls($encryption) {
    return in_array(strtolower((string) $encryption), array('ssl', 'tls', 'smtps'), true);
}

function iahx_modern_send_search_email(MailerInterface $mailer, $subject, $fromName, $toEmail, $htmlBody) {
    $message = (new Email())
        ->subject($subject)
        ->from(new Address(FROM_MAIL, $fromName))
        ->html($htmlBody);

    foreach (iahx_modern_normalize_recipients($toEmail) as $recipient) {
        $message->addTo($recipient);
    }

    $mailer->send($message);

    return true;
}

function iahx_modern_normalize_recipients($toEmail) {
    if (!is_array($toEmail)) {
        $toEmail = explode(';', $toEmail);
    }

    $recipients = array();
    foreach ($toEmail as $recipient) {
        $recipient = trim($recipient);
        if ($recipient !== '') {
            $recipients[] = $recipient;
        }
    }

    return $recipients;
}
