<?php
require_once("config.php");

$person_id = (isset($_GET["id"]) and is_numeric($_GET["id"])) ? $_GET["id"] : "";
$nophoto=0;

if($person_id){
	$persons_rec = get_person_image($logged->name, $logged->pw, $person_id);
	$check_res = json_decode($persons_rec);

	if(json_last_error() != JSON_ERROR_NONE){
		//person has image
		header("Content-type: image/jpeg");
		echo $persons_rec;
	} else $nophoto=1; //echo "Person does not have image";
} else $nophoto=1;//echo "Invalid id sent";

if($nophoto){
	//display dummy photo in case of error
	echo file_get_contents("img/logo.png");
}

?>