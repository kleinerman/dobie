<?php 
require_once("config.php");

if(isset($_SESSION[$config->sesskey])){
	//session variable is registered, the user is ready to logout 
	//destroy session
	session_unset(); 
	session_destroy();
}

//destroy cookies
setcookie($config->sesskeycookiename, "", time() - $config->cookie_lifetime);

header("Location: login");
?>