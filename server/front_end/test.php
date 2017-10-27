<?
error_reporting(0);
$https= ($_SERVER["HTTP_X_FORWARDED_PROTO"]=="https");

var_dump($https);