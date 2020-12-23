<?php

// SMTP for send mail configuration
define('FROM_MAIL', getenv("SEARCH_FROM_MAIL"));
define('SMTP_SERVER', getenv("SEARCH_SMTP_SERVER"));
define('SMTP_PORT', intval(getenv("SEARCH_SMTP_PORT")));
define('SMTP_ENCRYPTION',  getenv("SEARCH_SMTP_ENCRYPTION")); // 'ssl'
define('SMTP_USERNAME',  getenv("SEARCH_SMTP_USERNAME"));
define('SMTP_USERPASSWORD', getenv("SEARCH_SMTP_USERPASSWORD"));

?>
