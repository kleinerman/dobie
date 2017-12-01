<?php
error_reporting(E_ALL);
$config=new stdClass();
$config->sitetitle="Dobie";
$config->sitedesc="Dobie Access Control";
if(isset($windowtitle)) $config->sitetitle.= " - $windowtitle";
$config->tableprefix="";
$wwwroot = "//";
$config->wwwroot = $wwwroot;

//api config
$config->api_protocol="http";
$config->api_hostname="backend";
$config->api_port="5000";
$config->api_path="/api/v1.0/";
if($config->api_port!="") $config->api_fullpath=$config->api_protocol."://".$config->api_hostname.":".$config->api_port.$config->api_path;
else $config->api_fullpath=$config->api_protocol."://".$config->api_hostname.$config->api_path;

//session settings
$config->sesskeycookiename='dobiesesslog';
$config->sesskey='xf89fSjM1';
$config->cookie_lifetime=1296000;
//extend session timeout to 15 days
ini_set("session.gc_maxlifetime",1296000);
ini_set("session.cookie_lifetime",1296000);
session_set_cookie_params(1296000);

//js extra includes array init
$include_extra_js=array();

//define common libraries
require_once("lib/lib.php");
require_once("lib/api-functions.php");

//define islogged global variable and trigger db connection in case it is
session_start();
persistsession();

//logged in check
$islogged = (isset($_SESSION[$config->sesskey])) ? 1 : 0;
$logged=new stdClass();
//check if requires login
$requirelogin = !isset($requirelogin) ? 1 : $requirelogin;
$lang="en";

//get user record and info if logged
if($islogged){
	require_once("lib/EnDecryptText.php");
	$EnDecryptText = new EnDecryptText();
	$logged->name=$_SESSION[$config->sesskey];
	$logged->pw=$EnDecryptText->Decrypt_Text($_SESSION[$config->sesskey."pw"]);
} else {
	if($requirelogin){
		//page requested doesnt allow unlogged users > logout
		//destroy cookies
		setcookie($config->sesskeycookiename, "", time() - $config->cookie_lifetime);
		//destroy session
		session_start();
		session_unset();
		session_destroy();
		header("Location:$config->wwwroot");
		die();
	} else $logged="";
}
?>
