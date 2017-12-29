<?
$DEBUG=0;

if($DEBUG){
	$requirelogin=0;
	require_once("../config.php");
}

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
//$response_info=curl_getinfo($ch);
//var_dump($response_info);
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

//Accesses

//get person accesses
function get_person_accesses($user,$pass,$id){
	global $config;
	$response=send_request($config->api_fullpath."person/$id/access",$user,$pass);
	if($response->response_status != "200") return false;
	else return $response->data;
}

function get_access($user,$pass,$id){
	global $config;
	$response=send_request($config->api_fullpath."access/$id",$user,$pass);
	if($response->response_status != "200") return false;
	else return $response->data;
}

//not working
// function get_door_accesses($user,$pass,$id){
// 	global $config;
// 	$response=send_request($config->api_fullpath."door/$id/access",$user,$pass);
// 	if($response->response_status != "200") return false;
// 	else return $response->data;
// }

function get_door($user,$pass,$id){
	global $config;
	$response=send_request($config->api_fullpath."door/$id",$user,$pass);
	if($response->response_status != "200") return false;
	else return $response->data;
}

function get_zones($user,$pass){
	global $config;
	$response=send_request($config->api_fullpath."zone",$user,$pass);
	if($response->response_status != "200") return false;
	else {
		for($i=0;$i<count($response->data);$i++){
			if(!isset($response->data[$i]->id)) {
				$uri_parts=explode("/",$response->data[$i]->uri);
				$response->data[$i]->id = end($uri_parts);
			}
		}
		return $response->data;
	}
}

function get_zone($user,$pass,$id){
	global $config;
	$response=send_request($config->api_fullpath."zone/$id",$user,$pass);
	if($response->response_status != "200") return false;
	else return $response->data;
}

//get doors in a zone
function get_doors($user,$pass,$id){
	global $config;
	$response=send_request($config->api_fullpath."zone/$id/door",$user,$pass);
	if($response->response_status != "200") return false;
	else {
		for($i=0;$i<count($response->data);$i++){
			if(!isset($response->data[$i]->name)) {
				$response->data[$i]->name = $response->data[$i]->description;
			}
		}
		return $response->data;
	}
}

function delete_access($user,$pass,$id,$is_allweek){
	global $config;
	if($is_allweek) $endpoint="access";
	else $endpoint="liaccess";
	$response=send_request($config->api_fullpath."$endpoint/$id",$user,$pass,"delete");
	$response->sentdata="send_request($config->api_fullpath$endpoint/$id,$user,$pass,delete)";
	return $response;
}

function add_access_allweek($user,$pass,$doorid,$personid,$iside,$oside,$starttime,$endtime,$expiredate){
	global $config;
	$payload_obj = new stdClass();
	$payload_obj->doorId = $doorid;
	$payload_obj->personId = $personid;
	$payload_obj->iSide = $iside;
	$payload_obj->oSide = $oside;
	$payload_obj->startTime = $starttime;
	$payload_obj->endTime = $endtime;
	$payload_obj->expireDate = $expiredate;
	$response=send_request($config->api_fullpath."access",$user,$pass,"post",json_encode($payload_obj));
	if($response->response_status != "201") return false;
	else return $response->data;
}

function edit_access_allweek($user,$pass,$id,$iside,$oside,$starttime,$endtime,$expiredate){
	global $config;
	$payload_obj = new stdClass();
	$payload_obj->iSide = $iside;
	$payload_obj->oSide = $oside;
	$payload_obj->startTime = $starttime;
	$payload_obj->endTime = $endtime;
	$payload_obj->expireDate = $expiredate;
	$response=send_request($config->api_fullpath."access/$id",$user,$pass,"put",json_encode($payload_obj));
	if($response->response_status != "200") return false;
	else return $response->data;
}

function add_access_liaccess($user,$pass,$doorid,$personid,$weekday,$iside,$oside,$starttime,$endtime,$expiredate){
	global $config;
	$payload_obj = new stdClass();
	$payload_obj->doorId = $doorid;
	$payload_obj->personId = $personid;
	$payload_obj->weekDay = $weekday;
	$payload_obj->iSide = $iside;
	$payload_obj->oSide = $oside;
	$payload_obj->startTime = $starttime;
	$payload_obj->endTime = $endtime;
	$payload_obj->expireDate = $expiredate;
	$response=send_request($config->api_fullpath."liaccess",$user,$pass,"post",json_encode($payload_obj));
	//$response->sent_data = $payload_obj;
	//if($response->response_status != "201") return false;
	//else return $response->data;
	//INSTEAD, return the entire response with error texts for debug
	return $response;
}

function edit_access_liaccess($user,$pass,$doorid,$personid,$id,$days_payload,$expiredate){
	global $config;
	//make a delete access first
	$response=delete_access($user,$pass,$id,1); //parameter allWeek as true for deleting all liaccess accesses

	if($response->response_status == "200"){
		$payload_obj = new stdClass();
		//add fixed values
		$payload_obj->doorId = $doorid;
		$payload_obj->personId = $personid;
		$payload_obj->expireDate = $expiredate;
		//then for each days_payload, make an add liaccess
		//explode days liaccesses in a | separated string
		$days_payload_arr=explode("|",$days_payload);
		foreach($days_payload_arr as $day_payload){
			//decode each day payload
			$day_payload_decoded=json_decode($day_payload);
			//copy values to new access object
			$payload_obj->weekDay = $day_payload_decoded->weekDay;
			$payload_obj->iSide = $day_payload_decoded->iSide;
			$payload_obj->oSide = $day_payload_decoded->oSide;
			$payload_obj->startTime = $day_payload_decoded->startTime;
			$payload_obj->endTime = $day_payload_decoded->endTime;
			//send an add request for liaccess day
			$response_inner=send_request($config->api_fullpath."liaccess",$user,$pass,"post",json_encode($payload_obj));
			if($response_inner->response_status != "201") $response=$response_inner;
			var_dump($response_inner);
		}
	}
	return $response;
}

function delete_access_bulk($user,$pass, $ids){
	global $config;
	$ids_arr=explode("|",$ids);
	$success=1;
	foreach($ids_arr as $id){
		if(is_numeric($id)) $response=delete_access($user,$pass,$id,1);
		$success = $success and ($response->response_status == "200");
	}
	return $success;
}

if($DEBUG){
	//$res=get_organizations("admin","admin");
	//$res=do_auth("admin","admin");
	//$res=get_organizations("admin","admin",2);

	//$res=get_person_accesses("admin","admin",3);
//	$res=get_access("admin","admin",32);
//	$res=get_door_accesses("admin","admin",3);
	//$res=get_zones("admin","admin");
	//$res=get_zone("admin","admin",1);
//	$res=get_doors("admin","admin",1);
	//$res=add_access_allweek("admin","admin",3,1,1,1,"08:00:00","18:00:00","9999-12-31 00:00");
	//$res=edit_access_allweek("admin","admin",19,0,1,"08:00:00","18:00:00","9999-12-31 00:00");
	//$res=delete_access("admin","admin",1,1);
	//$res=add_access_liaccess("admin","admin",1,1,1,0,1,"01:00:00","23:00:00","9999-12-31 00:00");
	//$res=add_access_liaccess("admin","admin",1,3,1,1,1,"08:00:00","18:00:00","9999-12-31 00:00");
	//$res=add_access_liaccess("admin", "admin", 4, 3, 2, 1, 1, "08:00:00", "18:00:00", "9999-12-31 00:00");
	//$res=delete_access("admin","admin",11,0);
	$res=edit_access_liaccess("admin","admin",32,'{"expireDate":"2018-12-28","weekDay":1,"startTime":"9:00","endTime":"18:00","iSide":1,"oSide":1}|{"expireDate":"2018-12-28","weekDay":3,"startTime":"9:00","endTime":"18:00","iSide":1,"oSide":0}|{"expireDate":"2018-12-28","weekDay":5,"startTime":"9:00","endTime":"18:00","iSide":1,"oSide":1}|{"expireDate":"2018-12-28","weekDay":6,"startTime":"08:00","endTime":"18:00","iSide":1,"oSide":1}',"2018-12-28");
	echo "<pre>";
	var_dump($res);
}
?>