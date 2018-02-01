<?
$requirelogin=0;
require_once("config.php");
ob_start('ob_gzhandler');

$ret=array();

if(!empty($_POST) and is_valid_ajax_ref($_SERVER['HTTP_REFERER'])){

	//get posted values 
	$action = trim($_POST['action']);
	$error = "";

	switch($action){
		case "get_organization":
			if(!$islogged) array_push($ret,0,"Action needs authentication");
			else {
				$organization_id = (isset($_POST["id"]) and is_numeric($_POST["id"])) ? $_POST["id"] : "";

				if($organization_id=="") array_push($ret,0,"Invalid values sent");
				else {
					//get record
					$organization_rec = get_organization($logged->name, $logged->pw,$organization_id);
					if($organization_rec){
						//return record
						array_push($ret,1,$organization_rec);
					} else array_push($ret,0,"Organization could not be retrieved");
				}
			}
		break;
		case "get_organizations":
			if(!$islogged) array_push($ret,0,"Action needs authentication");
			else {
				//get record
				$organizations_rec = get_organizations($logged->name, $logged->pw);
				if($organizations_rec){
					//return record
					array_push($ret,1,$organizations_rec);
				} else array_push($ret,0,"Organizations not found");
			}
		break;
		case "edit_organization":
			if(!$islogged) array_push($ret,0,"Action needs authentication");
			else {
				$id = (isset($_POST['id']) and is_numeric($_POST['id'])) ? $_POST['id'] : "";
				$name = isset($_POST['name']) ? $_POST['name'] : "";

				if($id=="") array_push($ret,0,"Invalid values sent");
				//empty name can be considered as a valid scenario
	    			else {
					$organizations_rec = set_organization($logged->name, $logged->pw,$id, $name);

					if($organizations_rec) array_push($ret,1,"Information saved successfully!");
					else array_push($ret,0,"Organization could not be updated");
				}
			}
		break;
		case "add_organization":
			if(!$islogged) array_push($ret,0,"Action needs authentication");
			else {
				$name = isset($_POST['name']) ? $_POST['name'] : "";

				$organizations_rec = add_organization($logged->name, $logged->pw, $name);
				if($organizations_rec) array_push($ret,1,"Information saved successfully!");
				else array_push($ret,0,"Organization could not be added");
			}
		break;
		case "delete_organization":
			if(!$islogged) array_push($ret,0,"Action needs authentication");
			else {
				$id = (isset($_POST['id']) and is_numeric($_POST['id'])) ? $_POST['id'] : "";

				$organizations_rec = delete_organization($logged->name,$logged->pw, $id);

				if($organizations_rec) array_push($ret,1,"Information saved successfully!");
				else array_push($ret,0,"Organization could not be deleted");
			}
		break;

		case "get_persons":
			if(!$islogged) array_push($ret,0,"Action needs authentication");
			else {
				$id = (isset($_POST['id']) and is_numeric($_POST['id'])) ? $_POST['id'] : "";
				//get record
				$persons_rec = get_persons($logged->name, $logged->pw,$id);
				if($persons_rec){
					//return record
					array_push($ret,1,$persons_rec);
				} else array_push($ret,0,"Persons not found");
			}
		break;
		case "get_person":
			if(!$islogged) array_push($ret,0,"Action needs authentication");
			else {
				$id = (isset($_POST["id"]) and is_numeric($_POST["id"])) ? $_POST["id"] : "";

				if($id=="") array_push($ret,0,"Invalid values sent");
				else {
					//get record
					$persons_rec = get_person($logged->name, $logged->pw,$id);
					if($persons_rec){
						//return record
						array_push($ret,1,$persons_rec);
					} else array_push($ret,0,"Person could not be retrieved");
				}
			}
		break;
		case "add_person":
			if(!$islogged) array_push($ret,0,"Action needs authentication");
			else {
				$orgid = isset($_POST['orgid']) ? $_POST['orgid'] : "";
				$name = isset($_POST['name']) ? $_POST['name'] : "";
				$idnum = isset($_POST['idnum']) ? $_POST['idnum'] : "";
				$cardnum = isset($_POST['cardnum']) ? $_POST['cardnum'] : "";

				$persons_rec = add_person($logged->name, $logged->pw, $orgid, $name, $idnum, $cardnum);
				//if($persons_rec) array_push($ret,1,"Information saved successfully!");
				//else array_push($ret,0,"Person could not be added");
				if($persons_rec->response_status == "201") array_push($ret,1,"Information saved successfully!");
				else array_push($ret,0,$persons_rec->data->message);
			}
		break;
		case "edit_person":
			if(!$islogged) array_push($ret,0,"Action needs authentication");
			else {
				$id = (isset($_POST['id']) and is_numeric($_POST['id'])) ? $_POST['id'] : "";
				$orgid = isset($_POST['orgid']) ? $_POST['orgid'] : "";
				$name = isset($_POST['name']) ? $_POST['name'] : "";
				$idnum = isset($_POST['idnum']) ? $_POST['idnum'] : "";
				$cardnum = isset($_POST['cardnum']) ? $_POST['cardnum'] : "";

				if($id=="") array_push($ret,0,"Invalid values sent");
	    			else {
					$persons_rec = set_person($logged->name, $logged->pw,$id, $orgid, $name, $idnum, $cardnum);

					if($persons_rec) array_push($ret,1,"Information saved successfully!");
					else array_push($ret,0,"Person could not be updated");
				}
			}
		break;
		case "delete_person":
			if(!$islogged) array_push($ret,0,"Action needs authentication");
			else {
				$id = (isset($_POST['id']) and is_numeric($_POST['id'])) ? $_POST['id'] : "";

				$persons_rec = delete_person($logged->name,$logged->pw, $id);

				if($persons_rec) array_push($ret,1,"Information saved successfully!");
				else array_push($ret,0,"Person could not be deleted");
			}
		break;
		
		case "get_person_accesses":
			if(!$islogged) array_push($ret,0,"Action needs authentication");
			else {
				$id = (isset($_POST['id']) and is_numeric($_POST['id'])) ? $_POST['id'] : "";
				//get records
				$access_rec = get_person_accesses($logged->name, $logged->pw,$id);
				if($access_rec){
					//return records
					array_push($ret,1,$access_rec);
				} else array_push($ret,0,"No accesses found");
			}
		break;
		case "get_access":
			if(!$islogged) array_push($ret,0,"Action needs authentication");
			else {
				$id = (isset($_POST['id']) and is_numeric($_POST['id'])) ? $_POST['id'] : "";
				//get records
				$access_rec = get_access($logged->name, $logged->pw,$id);
				if($access_rec){
					//return records
					array_push($ret,1,$access_rec);
				} else array_push($ret,0,"No accesses found");
			}
		break;
		case "get_door_accesses":
			if(!$islogged) array_push($ret,0,"Action needs authentication");
			else {
				$id = (isset($_POST['id']) and is_numeric($_POST['id'])) ? $_POST['id'] : "";
				//get records
				$access_rec = get_door_accesses($logged->name, $logged->pw,$id);
				if($access_rec){
					//return records
					array_push($ret,1,$access_rec);
				} else array_push($ret,0,"No accesses found");
			}
		break;
		case "get_door":
			if(!$islogged) array_push($ret,0,"Action needs authentication");
			else {
				$id = (isset($_POST['id']) and is_numeric($_POST['id'])) ? $_POST['id'] : "";
				//get records
				$door_rec = get_door($logged->name, $logged->pw,$id);
				if($door_rec){
					//return records
					array_push($ret,1,$door_rec);
				} else array_push($ret,0,"Door could not be retrieved");
			}
		break;
		case "get_zones":
			if(!$islogged) array_push($ret,0,"Action needs authentication");
			else {
				//get record
				$zones_rec = get_zones($logged->name, $logged->pw);
				if($zones_rec){
					//return record
					array_push($ret,1,$zones_rec);
				} else array_push($ret,0,"Zones could not be retrieved");
			}
		break;
		case "get_zone":
			if(!$islogged) array_push($ret,0,"Action needs authentication");
			else {
				$id = (isset($_POST['id']) and is_numeric($_POST['id'])) ? $_POST['id'] : "";
				//get records
				$zone_rec = get_zone($logged->name, $logged->pw,$id);
				if($zone_rec){
					//return records
					array_push($ret,1,$zone_rec);
				} else array_push($ret,0,"Zone could not be retrieved");
			}
		break;
		case "get_doors":
			if(!$islogged) array_push($ret,0,"Action needs authentication");
			else {
				$id = (isset($_POST['id']) and is_numeric($_POST['id'])) ? $_POST['id'] : "";
				//get records
				$doors_rec = get_doors($logged->name, $logged->pw,$id);
				if($doors_rec){
					//return records
					array_push($ret,1,$doors_rec);
				} else array_push($ret,0,"No doors found");
			}
		break;
		case "add_access_allweek":
			if(!$islogged) array_push($ret,0,"Action needs authentication");
			else {
				$doorid = (isset($_POST['doorid']) and is_numeric($_POST['doorid'])) ? intval($_POST['doorid']) : "";
				$personid = (isset($_POST['personid']) and is_numeric($_POST['personid'])) ? intval($_POST['personid']) : "";
				$iside = (isset($_POST['iside']) and is_numeric($_POST['iside'])) ? intval($_POST['iside']) : "";
				$oside = (isset($_POST['oside']) and is_numeric($_POST['oside'])) ? intval($_POST['oside']) : "";
				$starttime = (isset($_POST['starttime'])) ? $_POST['starttime'] : "00:00";
				$endtime = (isset($_POST['endtime'])) ? $_POST['endtime'] : "23:59";
				$expiredate = (isset($_POST['expiredate'])) ? $_POST['expiredate'] : "9999-12-31";

				$access_rec = add_access_allweek($logged->name, $logged->pw, $doorid, $personid, $iside, $oside,$starttime,$endtime,$expiredate);
				if($access_rec) array_push($ret,1,"Information saved successfully!");
				else array_push($ret,0,"Access could not be added");
			}
		break;
		case "add_access_liaccess":
			if(!$islogged) array_push($ret,0,"Action needs authentication");
			else {
				$doorid = (isset($_POST['doorid']) and is_numeric($_POST['doorid'])) ? intval($_POST['doorid']) : "";
				$personid = (isset($_POST['personid']) and is_numeric($_POST['personid'])) ? intval($_POST['personid']) : "";
				$weekday = (isset($_POST['weekday']) and is_numeric($_POST['weekday'])) ? intval($_POST['weekday']) : "";
				$iside = (isset($_POST['iside']) and is_numeric($_POST['iside'])) ? intval($_POST['iside']) : "";
				$oside = (isset($_POST['oside']) and is_numeric($_POST['oside'])) ? intval($_POST['oside']) : "";
				$starttime = (isset($_POST['starttime'])) ? $_POST['starttime'] : "00:00";
				$endtime = (isset($_POST['endtime'])) ? $_POST['endtime'] : "23:59";
				$expiredate = (isset($_POST['expiredate'])) ? $_POST['expiredate'] : "9999-12-31";

				$access_rec = add_access_liaccess($logged->name, $logged->pw, $doorid, $personid, $weekday, $iside, $oside, $starttime, $endtime, $expiredate);
				//if($access_rec) array_push($ret,1,"Information saved successfully!");
				//else array_push($ret,0,"Access could not be added");
				//INSTEAD, entire response received. show error accordingly
				if($access_rec->response_status != "201") array_push($ret,0,$access_rec->data->message);
				else array_push($ret,1,"Information saved successfully!");
			}
		break;
		case "edit_access_allweek":
			if(!$islogged) array_push($ret,0,"Action needs authentication");
			else {
				$id = (isset($_POST['id']) and is_numeric($_POST['id'])) ? intval($_POST['id']) : "";
				$iside = (isset($_POST['iside']) and is_numeric($_POST['iside'])) ? intval($_POST['iside']) : "";
				$oside = (isset($_POST['oside']) and is_numeric($_POST['oside'])) ? intval($_POST['oside']) : "";
				$starttime = (isset($_POST['starttime'])) ? $_POST['starttime'] : "00:00";
				$endtime = (isset($_POST['endtime'])) ? $_POST['endtime'] : "23:59";
				$expiredate = (isset($_POST['expiredate'])) ? $_POST['expiredate'] : "9999-12-31";

				if($id==""){
					array_push($ret,0,"Invalid id sent");
				} else {
					$access_rec = edit_access_allweek($logged->name, $logged->pw, $id, $iside, $oside, $starttime, $endtime, $expiredate);
					if($access_rec) array_push($ret,1,"Information saved successfully!");
					else array_push($ret,0,"Access could not be modified");
				}
			}
		break;
		case "edit_access_liaccess":
			if(!$islogged) array_push($ret,0,"Action needs authentication");
			else {
				$id = (isset($_POST['id']) and is_numeric($_POST['id'])) ? intval($_POST['id']) : "";
				$doorid = (isset($_POST['doorid']) and is_numeric($_POST['doorid'])) ? intval($_POST['doorid']) : "";
				$personid = (isset($_POST['personid']) and is_numeric($_POST['personid'])) ? intval($_POST['personid']) : "";
				$days_payload = (isset($_POST['days_payload'])) ? $_POST['days_payload'] : "";
				$expiredate = (isset($_POST['expiredate'])) ? $_POST['expiredate'] : "9999-12-31";

				if($id==""){
					array_push($ret,0,"Invalid id sent");
				} else {
					$access_rec = edit_access_liaccess($logged->name, $logged->pw, $doorid, $personid, $id, $days_payload, $expiredate);
					if($access_rec and ($access_rec->response_status==200 or $access_rec->response_status==201)) array_push($ret,1,"Information saved successfully!");
					else array_push($ret,0,"Access could not be modified");
				}
			}
		break;
		case "delete_access_bulk":
			if(!$islogged) array_push($ret,0,"Action needs authentication");
			else {
				$ids = (isset($_POST['ids'])) ? $_POST['ids'] : "";

				if($ids==""){
					array_push($ret,0,"No ids sent");
				} else {
					$access_rec = delete_access_bulk($logged->name, $logged->pw, $ids);
					if($access_rec) array_push($ret,1,"Accesses deleted successfully!");
					else array_push($ret,0,"Accesses could not be deleted");
				}
			}
		break;
		case "add_access_allweek_organization":
			if(!$islogged) array_push($ret,0,"Action needs authentication");
			else {
				$doorid = (isset($_POST['doorid']) and is_numeric($_POST['doorid'])) ? intval($_POST['doorid']) : "";
				$orgid = (isset($_POST['orgid']) and is_numeric($_POST['orgid'])) ? intval($_POST['orgid']) : "";
				$iside = (isset($_POST['iside']) and is_numeric($_POST['iside'])) ? intval($_POST['iside']) : "";
				$oside = (isset($_POST['oside']) and is_numeric($_POST['oside'])) ? intval($_POST['oside']) : "";
				$starttime = (isset($_POST['starttime'])) ? $_POST['starttime'] : "00:00";
				$endtime = (isset($_POST['endtime'])) ? $_POST['endtime'] : "23:59";
				$expiredate = (isset($_POST['expiredate'])) ? $_POST['expiredate'] : "9999-12-31";

				add_access_allweek_organization($logged->name, $logged->pw, $doorid, $orgid, $iside, $oside,$starttime,$endtime,$expiredate);

				//function doesnt return any value > return success always
				array_push($ret,1,"Accesses added to all persons in organization");
			}
		break;
		case "add_access_liaccess_organization":
			if(!$islogged) array_push($ret,0,"Action needs authentication");
			else {
				$doorid = (isset($_POST['doorid']) and is_numeric($_POST['doorid'])) ? intval($_POST['doorid']) : "";
				$orgid = (isset($_POST['orgid']) and is_numeric($_POST['orgid'])) ? intval($_POST['orgid']) : "";
				$weekday = (isset($_POST['weekday']) and is_numeric($_POST['weekday'])) ? intval($_POST['weekday']) : "";
				$iside = (isset($_POST['iside']) and is_numeric($_POST['iside'])) ? intval($_POST['iside']) : "";
				$oside = (isset($_POST['oside']) and is_numeric($_POST['oside'])) ? intval($_POST['oside']) : "";
				$starttime = (isset($_POST['starttime'])) ? $_POST['starttime'] : "00:00";
				$endtime = (isset($_POST['endtime'])) ? $_POST['endtime'] : "23:59";
				$expiredate = (isset($_POST['expiredate'])) ? $_POST['expiredate'] : "9999-12-31";

				$access_rec = add_access_liaccess_organization($logged->name, $logged->pw, $doorid, $orgid, $weekday, $iside, $oside, $starttime, $endtime, $expiredate);

				//function doesnt return any value > return success always
				array_push($ret,1,"Accesses added to all persons in organization");
			}
		break;
		case "add_access_allweek_zone":
			if(!$islogged) array_push($ret,0,"Action needs authentication");
			else {
				$personid = (isset($_POST['personid']) and is_numeric($_POST['personid'])) ? intval($_POST['personid']) : "";
				$zoneid = (isset($_POST['zoneid']) and is_numeric($_POST['zoneid'])) ? intval($_POST['zoneid']) : "";
				$iside = (isset($_POST['iside']) and is_numeric($_POST['iside'])) ? intval($_POST['iside']) : "";
				$oside = (isset($_POST['oside']) and is_numeric($_POST['oside'])) ? intval($_POST['oside']) : "";
				$starttime = (isset($_POST['starttime'])) ? $_POST['starttime'] : "00:00";
				$endtime = (isset($_POST['endtime'])) ? $_POST['endtime'] : "23:59";
				$expiredate = (isset($_POST['expiredate'])) ? $_POST['expiredate'] : "9999-12-31";

				add_access_allweek_zone($logged->name, $logged->pw, $personid, $zoneid, $iside, $oside,$starttime,$endtime,$expiredate);

				//function doesnt return any value > return success always
				array_push($ret,1,"Accesses added to all doors in zone");
			}
		break;
		case "add_access_liaccess_zone":
			if(!$islogged) array_push($ret,0,"Action needs authentication");
			else {
				$personid = (isset($_POST['personid']) and is_numeric($_POST['personid'])) ? intval($_POST['personid']) : "";
				$zoneid = (isset($_POST['zoneid']) and is_numeric($_POST['zoneid'])) ? intval($_POST['zoneid']) : "";
				$weekday = (isset($_POST['weekday']) and is_numeric($_POST['weekday'])) ? intval($_POST['weekday']) : "";
				$iside = (isset($_POST['iside']) and is_numeric($_POST['iside'])) ? intval($_POST['iside']) : "";
				$oside = (isset($_POST['oside']) and is_numeric($_POST['oside'])) ? intval($_POST['oside']) : "";
				$starttime = (isset($_POST['starttime'])) ? $_POST['starttime'] : "00:00";
				$endtime = (isset($_POST['endtime'])) ? $_POST['endtime'] : "23:59";
				$expiredate = (isset($_POST['expiredate'])) ? $_POST['expiredate'] : "9999-12-31";

				add_access_liaccess_zone($logged->name, $logged->pw, $personid, $zoneid, $weekday, $iside, $oside, $starttime, $endtime, $expiredate);

				//function doesnt return any value > return success always
				array_push($ret,1,"Accesses added to all doors in zone");
			}
		break;
		case "add_access_allweek_organization_zone":
			if(!$islogged) array_push($ret,0,"Action needs authentication");
			else {
				$zoneid = (isset($_POST['zoneid']) and is_numeric($_POST['zoneid'])) ? intval($_POST['zoneid']) : "";
				$orgid = (isset($_POST['orgid']) and is_numeric($_POST['orgid'])) ? intval($_POST['orgid']) : "";
				$iside = (isset($_POST['iside']) and is_numeric($_POST['iside'])) ? intval($_POST['iside']) : "";
				$oside = (isset($_POST['oside']) and is_numeric($_POST['oside'])) ? intval($_POST['oside']) : "";
				$starttime = (isset($_POST['starttime'])) ? $_POST['starttime'] : "00:00";
				$endtime = (isset($_POST['endtime'])) ? $_POST['endtime'] : "23:59";
				$expiredate = (isset($_POST['expiredate'])) ? $_POST['expiredate'] : "9999-12-31";

				add_access_allweek_organization_zone($logged->name, $logged->pw, $zoneid, $orgid, $iside, $oside,$starttime,$endtime,$expiredate);

				//function doesnt return any value > return success always
				array_push($ret,1,"Accesses added to all doors in zone");
			}
		break;
		case "add_access_liaccess_organization_zone":
			if(!$islogged) array_push($ret,0,"Action needs authentication");
			else {
				$zoneid = (isset($_POST['zoneid']) and is_numeric($_POST['zoneid'])) ? intval($_POST['zoneid']) : "";
				$orgid = (isset($_POST['orgid']) and is_numeric($_POST['orgid'])) ? intval($_POST['orgid']) : "";
				$weekday = (isset($_POST['weekday']) and is_numeric($_POST['weekday'])) ? intval($_POST['weekday']) : "";
				$iside = (isset($_POST['iside']) and is_numeric($_POST['iside'])) ? intval($_POST['iside']) : "";
				$oside = (isset($_POST['oside']) and is_numeric($_POST['oside'])) ? intval($_POST['oside']) : "";
				$starttime = (isset($_POST['starttime'])) ? $_POST['starttime'] : "00:00";
				$endtime = (isset($_POST['endtime'])) ? $_POST['endtime'] : "23:59";
				$expiredate = (isset($_POST['expiredate'])) ? $_POST['expiredate'] : "9999-12-31";

				add_access_liaccess_organization_zone($logged->name, $logged->pw, $zoneid, $orgid, $weekday, $iside, $oside, $starttime, $endtime, $expiredate);

				//function doesnt return any value > return success always
				array_push($ret,1,"Accesses added to all doors in zone");
			}
		break;
		default:
			array_push($ret,0,"Operation not defined"); //send out error
		break;
	}
}

header("Content-type: application/json");
echo json_encode($ret);
?>