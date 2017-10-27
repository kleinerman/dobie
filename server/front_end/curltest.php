<?php
function send_request($url,$username,$password,$method="get",$payload="{}"){
	//assumes valid input
	$ch = curl_init();
	curl_setopt($ch, CURLOPT_HTTPHEADER, array('Content-Type: application/json'));
	curl_setopt($ch, CURLOPT_HEADER, 0);
	curl_setopt($ch, CURLOPT_USERPWD, $username . ":" . $password);

	curl_setopt($ch,CURLOPT_URL,$url);
	curl_setopt($ch,CURLOPT_RETURNTRANSFER,true);
	curl_setopt($ch,CURLOPT_CONNECTTIMEOUT,5);
	if($method=="post"){
		curl_setopt($ch, CURLOPT_POST, 1);
	} else if($method=="delete"){
		curl_setopt($ch, CURLOPT_CUSTOMREQUEST, "DELETE");
	} else if($method=="put"){
		curl_setopt($ch, CURLOPT_CUSTOMREQUEST, "PUT");
	}
	if($method=="post" or $method=="put") curl_setopt($ch, CURLOPT_POSTFIELDS, $payload);
	//curl_setopt($ch, CURLOPT_HTTPAUTH, CURLAUTH_ANY);
	$response = curl_exec($ch);
	//var_dump($response);
//	$response_info=curl_getinfo($ch);
//	var_dump($response_info);
	if($response) $response_decoded=json_decode($response);
	else {
		$response_decoded = new stdClass();
		$response_decoded->success = false;
		$response_decoded->error = new stdClass();
		$response_decoded->error->mensaje = "Error when trying to get data";
	}
	$response_decoded->response_status=curl_getinfo($ch, CURLINFO_HTTP_CODE);
	curl_close($ch);
	return $response_decoded;
}

//try login
//$ret = send_request("http://quebec.capitalinasdc.com:5000/api/v1.0/login","admin","admin");

//get organizations
//$ret = send_request("http://quebec.capitalinasdc.com:5000/api/v1.0/organization/2","admin","admin");

echo "<pre>";
var_dump($ret);
?>