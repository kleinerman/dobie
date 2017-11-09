<?
//$requirelogin=0;
//require_once("../config.php");

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
//	error_log($response);
//	error_log(grab_dump($response));
	//var_dump($response);
//	$response_info=curl_getinfo($ch);
//	var_dump($response_info);
	$response_decoded= new stdClass();
	if($response) {
		$response_decoded->response_status=curl_getinfo($ch, CURLINFO_HTTP_CODE);
		$response_decoded->data=json_decode($response);
	} else {
		$response_decoded->success = false;
		$response_decoded->error = new stdClass();
		$response_decoded->error->mensaje = "Error when trying to get data";
	}
	curl_close($ch);
	return $response_decoded;
}

// do auth
function do_auth($user,$pass){
	global $config;
	$response=send_request($config->api_fullpath."login",$user,$pass);
	//error_log(grab_dump($response));
	return (isset($response->response_status) and $response->response_status=="200");
}

// get user (system)

//organizations

// get organizations
function get_organizations($user,$pass){
	global $config;
	$response=send_request($config->api_fullpath."organization",$user,$pass);
	if($response->response_status != "200") return false;
	else return $response->data;
}

// get single organization
function get_organization($user,$pass,$id){
	global $config;
	$response=send_request($config->api_fullpath."organization/$id",$user,$pass);
	if($response->response_status != "200") return false;
	else return $response->data;
}

function set_organization($user,$pass,$id,$name){
	global $config;
	$payload_obj = new stdClass();
	$payload_obj->name= $name;
	$response=send_request($config->api_fullpath."organization/$id",$user,$pass,"put",json_encode($payload_obj));
	if($response->response_status != "200") return false;
	else return $response->data;
}

function add_organization($user,$pass,$name){
	global $config;
	$payload_obj = new stdClass();
	$payload_obj->name= $name;
	$response=send_request($config->api_fullpath."organization",$user,$pass,"post",json_encode($payload_obj));
	if($response->response_status != "201") return false;
	else return $response->data;
}

function delete_organization($user,$pass,$id){
	global $config;
	$response=send_request($config->api_fullpath."organization/$id",$user,$pass,"delete");
	if($response->response_status != "200") return false;
	else return $response->data;
}

//Persons

function get_persons($user,$pass,$id){
	global $config;
	$response=send_request($config->api_fullpath."organization/$id/person",$user,$pass);
	if($response->response_status != "200") return false;
	else return $response->data;
}

function get_person($user,$pass,$id){
	global $config;
	$response=send_request($config->api_fullpath."person/$id",$user,$pass);
	if($response->response_status != "200") return false;
	else return $response->data;
}

function add_person($user,$pass,$orgid,$name,$idnum,$cardnum){
	global $config;
	$payload_obj = new stdClass();
	$payload_obj->orgId= $orgid;
	$payload_obj->name= $name;
	$payload_obj->identNumber= $idnum;
	$payload_obj->cardNumber= $cardnum;
	$payload_obj->visitedOrgId= null;
	$response=send_request($config->api_fullpath."person",$user,$pass,"post",json_encode($payload_obj));
	if($response->response_status != "201") return false;
	else return $response->data;
}

function set_person($user,$pass,$id,$orgid,$name,$idnum,$cardnum){
	global $config;
	$payload_obj = new stdClass();
	$payload_obj->orgId= $orgid;
	$payload_obj->name= $name;
	$payload_obj->identNumber= $idnum;
	$payload_obj->cardNumber= $cardnum;
	$payload_obj->visitedOrgId= null;
	$response=send_request($config->api_fullpath."person/$id",$user,$pass,"put",json_encode($payload_obj));
	if($response->response_status != "200") return false;
	else return $response->data;
}

function delete_person($user,$pass,$id){
	global $config;
	$response=send_request($config->api_fullpath."person/$id",$user,$pass,"delete");
	if($response->response_status != "200") return false;
	else return $response->data;
}


//$res=get_organizations("admin","admin");
//$res=do_auth("admin","admin");
//echo "<pre>";
//var_dump($res);

// get person
// get credential
// get events
?>