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
					$organization_rec = get_organization($logged->name, $logged->pw, $organization_id);
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
					$organizations_rec = set_organization($logged->name, $logged->pw, $id, $name);

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

				$organizations_rec = delete_organization($logged->name, $logged->pw, $id);

				if($organizations_rec) array_push($ret,1,"Information saved successfully!");
				else array_push($ret,0,"Organization could not be deleted");
			}
		break;
		case "get_persons":
			if(!$islogged) array_push($ret,0,"Action needs authentication");
			else {
				$id = (isset($_POST['id']) and is_numeric($_POST['id'])) ? $_POST['id'] : "";
				//get record
				$persons_rec = get_persons($logged->name, $logged->pw, $id);
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
					$persons_rec = get_person($logged->name, $logged->pw, $id);
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
				$names = isset($_POST['names']) ? $_POST['names'] : "";
				$lastname = isset($_POST['lastname']) ? $_POST['lastname'] : "";
				$idnum = isset($_POST['idnum']) ? $_POST['idnum'] : "";
				$cardnum = isset($_POST['cardnum']) ? $_POST['cardnum'] : "";
				$note = isset($_POST['note']) ? $_POST['note'] : "";

				$persons_rec = add_person($logged->name, $logged->pw, $orgid, $names, $lastname, $idnum, $cardnum, $note);
				//if($persons_rec) array_push($ret,1,"Information saved successfully!");
				//else array_push($ret,0,"Person could not be added");
				if($persons_rec->response_status == "201"){
					array_push($ret,1,"Information saved successfully!");
					//return in third field, the added person id
					$uri_parts=explode("/",$persons_rec->data->uri);
					array_push($ret, intval(end($uri_parts)));
				} else array_push($ret,0,$persons_rec->data->message);
			}
		break;
		case "edit_person":
			if(!$islogged) array_push($ret,0,"Action needs authentication");
			else {
				$id = (isset($_POST['id']) and is_numeric($_POST['id'])) ? $_POST['id'] : "";
				$orgid = isset($_POST['orgid']) ? $_POST['orgid'] : "";
				$names = isset($_POST['names']) ? $_POST['names'] : "";
				$lastname = isset($_POST['lastname']) ? $_POST['lastname'] : "";
				$idnum = isset($_POST['idnum']) ? $_POST['idnum'] : "";
				$cardnum = isset($_POST['cardnum']) ? $_POST['cardnum'] : "";
				$note = isset($_POST['note']) ? $_POST['note'] : "";

				if($id=="") array_push($ret,0,"Invalid values sent");
	    			else {
					$persons_rec = set_person($logged->name, $logged->pw, $id, $orgid, $names, $lastname, $idnum, $cardnum, $note);

					if($persons_rec) array_push($ret,1,"Information saved successfully!");
					else array_push($ret,0,"Person could not be updated");
				}
			}
		break;
		case "edit_person_image":
			if(!$islogged) array_push($ret,0,"Action needs authentication");
			else {
				$id = (isset($_POST['id']) and is_numeric($_POST['id'])) ? $_POST['id'] : "";
				$filename = isset($_POST['filename']) ? $_POST['filename'] : "";

				if($id=="") array_push($ret,0,"Invalid values sent");
	    			else {
					$persons_rec = set_person_image($logged->name, $logged->pw, $id, $filename);

					if($persons_rec) array_push($ret,1,"Information saved successfully!");
					else array_push($ret,0,"Person could not be updated");
				}
			}
		break;
		case "person_has_image":
			if(!$islogged) array_push($ret,0,"Action needs authentication");
			else {
				$id = (isset($_POST['id']) and is_numeric($_POST['id'])) ? $_POST['id'] : "";

				if($id=="") array_push($ret,0,"Invalid values sent");
	    			else {
					$persons_rec = get_person_image($logged->name, $logged->pw, $id);
					$check_res = json_decode($persons_rec);

					if(json_last_error() != JSON_ERROR_NONE) array_push($ret,1,"Person has image");
					else array_push($ret,0,"Person does not have image");
				}
			}
		break;
		case "delete_person":
			if(!$islogged) array_push($ret,0,"Action needs authentication");
			else {
				$id = (isset($_POST['id']) and is_numeric($_POST['id'])) ? $_POST['id'] : "";

				$persons_rec = delete_person($logged->name, $logged->pw, $id);

				if($persons_rec) array_push($ret,1,"Information saved successfully!");
				else array_push($ret,0,"Person could not be deleted");
			}
		break;
		case "search_person":
			if(!$islogged) array_push($ret,0,"Action needs authentication");
			else {
				$names = isset($_POST['names']) ? $_POST['names'] : "";
				$lastname = isset($_POST['lastname']) ? $_POST['lastname'] : "";
				$idnum = isset($_POST['idnum']) ? $_POST['idnum'] : "";
				$cardnum = isset($_POST['cardnum']) ? $_POST['cardnum'] : "";

				$persons_rec = search_person($logged->name, $logged->pw, $names, $lastname, $idnum, $cardnum);
				if($persons_rec and $persons_rec->response_status==200) array_push($ret,1,$persons_rec->data);
				else array_push($ret,0,$persons_rec->data->message);
			}
		break;
		case "import_persons":
			if(!$islogged) array_push($ret,0,"Action needs authentication");
			else {
				$orgid = (isset($_POST['orgid']) or !is_numeric($_POST['orgid'])) ? $_POST['orgid'] : "";
				$ignore_first_line = isset($_POST['form-import-ignore']) ? $_POST['form-import-ignore'] : 0;
				$file = (isset($_FILES['form-import-input']) and is_array($_FILES['form-import-input'])) ? $_FILES['form-import-input'] : "";

				//validate file
				if((substr_count($file["type"], "text",0)<1) or ($file["error"]!=0) or ($file["size"]<1)){
					array_push($ret,0,"File sent is invalid");
				} elseif($orgid==""){
					array_push($ret,0,"No organization specified");
				} else {
					//file and arguments look good
					$rows_imported=0;
					//parse each line
					$file_lines = file($file["tmp_name"]);
					if(count($file_lines)>0){
						//ignore first line if specified
						if($ignore_first_line) $start_from=1;
						else $start_from=0;
						for($i=$start_from;$i<count($file_lines);$i++){
//$file_lines[$i] = mb_convert_encoding($file_lines[$i],"UTF-8",'UTF-16LE');
							//parse line values
							$line_parts = explode(",",$file_lines[$i]);
							if(count($line_parts)==4){
								$names = trim($line_parts[0]);
								$lastname = trim($line_parts[1]);
								$idnum = trim($line_parts[2]);
								$cardnum = trim($line_parts[3]);
								//check that fields are valid for person > if not, ignore line
								if($names!="" and $lastname!="" and is_numeric($idnum) and is_numeric($cardnum)){
									$persons_rec = add_person($logged->name, $logged->pw, $orgid, $names, $lastname, $idnum, $cardnum);
									if($persons_rec->response_status == "201") $rows_imported++;
								} //else an argument in the file is incorrect

							} //else line has incorrect number of values
						}
					} //else empty line
					array_push($ret,1,$rows_imported);
				}
			}
		break;

		case "get_person_accesses":
			if(!$islogged) array_push($ret,0,"Action needs authentication");
			else {
				$id = (isset($_POST['id']) and is_numeric($_POST['id'])) ? $_POST['id'] : "";
				//get records
				$access_rec = get_person_accesses($logged->name, $logged->pw, $id);
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
				$access_rec = get_access($logged->name, $logged->pw, $id);
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
				$access_rec = get_door_accesses($logged->name, $logged->pw, $id);
				if($access_rec){
					//return records
					array_push($ret,1,$access_rec);
				} else array_push($ret,0,"No accesses found");
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

				$access_rec = add_access_allweek($logged->name, $logged->pw, $doorid, $personid, $iside, $oside, $starttime, $endtime, $expiredate);
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
				$personid = (isset($_POST['personid'])) ? ($_POST['personid']) : "";

				add_access_allweek_organization($logged->name, $logged->pw, $doorid, $orgid, $iside, $oside, $starttime, $endtime, $expiredate, $personid);

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
				$personid = (isset($_POST['personid'])) ? ($_POST['personid']) : "";

				$access_rec = add_access_liaccess_organization($logged->name, $logged->pw, $doorid, $orgid, $weekday, $iside, $oside, $starttime, $endtime, $expiredate, $personid);

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
				$doorid = (isset($_POST['doorid'])) ? ($_POST['doorid']) : "";
				$doorgroupid = (isset($_POST['doorgroupid'])) ? ($_POST['doorgroupid']) : "";

				add_access_allweek_zone($logged->name, $logged->pw, $personid, $zoneid, $iside, $oside,$starttime, $endtime, $expiredate, $doorid, $doorgroupid);

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
				$doorid = (isset($_POST['doorid'])) ? ($_POST['doorid']) : "";
				$doorgroupid = (isset($_POST['doorgroupid'])) ? ($_POST['doorgroupid']) : "";

				add_access_liaccess_zone($logged->name, $logged->pw, $personid, $zoneid, $weekday, $iside, $oside, $starttime, $endtime, $expiredate, $doorid, $doorgroupid);

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
				$personid = (isset($_POST['personid'])) ? ($_POST['personid']) : "";
				$doorid = (isset($_POST['doorid'])) ? ($_POST['doorid']) : "";
				$doorgroupid = (isset($_POST['doorgroupid'])) ? ($_POST['doorgroupid']) : "";

				add_access_allweek_organization_zone($logged->name, $logged->pw, $zoneid, $orgid, $iside, $oside, $starttime, $endtime, $expiredate, $personid, $doorid, $doorgroupid);

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
				$personid = (isset($_POST['personid'])) ? ($_POST['personid']) : "";
				$doorid = (isset($_POST['doorid'])) ? ($_POST['doorid']) : "";
				$doorgroupid = (isset($_POST['doorgroupid'])) ? ($_POST['doorgroupid']) : "";

				add_access_liaccess_organization_zone($logged->name, $logged->pw, $zoneid, $orgid, $weekday, $iside, $oside, $starttime, $endtime, $expiredate, $personid, $doorid,$doorgroupid);

				//function doesnt return any value > return success always
				array_push($ret,1,"Accesses added to all doors in zone");
			}
		break;
		case "get_events":
			if(!$islogged) array_push($ret,0,"Action needs authentication");
			else {
				$orgid = (isset($_POST['orgid']) and is_numeric($_POST['orgid'])) ? intval($_POST['orgid']) : "";
				$visitedorgid = (isset($_POST['visitedorgid']) and is_numeric($_POST['visitedorgid'])) ? intval($_POST['visitedorgid']) : "";
				$personid = (isset($_POST['personid']) and is_numeric($_POST['personid'])) ? intval($_POST['personid']) : "";
				$zoneid = (isset($_POST['zoneid']) and is_numeric($_POST['zoneid'])) ? intval($_POST['zoneid']) : "";
				$doorid = (isset($_POST['doorid']) and is_numeric($_POST['doorid'])) ? intval($_POST['doorid']) : "";
				$side = (isset($_POST['side']) and is_numeric($_POST['side'])) ? $_POST['side'] : "";
				$startdate = (isset($_POST['startdate'])) ? $_POST['startdate'] : "2000-01-01";
				$starttime = (isset($_POST['starttime'])) ? $_POST['starttime'] : "00:00";
				$enddate = (isset($_POST['enddate'])) ? $_POST['enddate'] : "9999-12-31";
				$endtime = (isset($_POST['endtime'])) ? $_POST['endtime'] : "00:00";
				$startevt = (isset($_POST['startevt']) and is_numeric($_POST['startevt'])) ? intval($_POST['startevt']) : 1;
				$evtsqtty = (isset($_POST['evtsqtty']) and is_numeric($_POST['evtsqtty'])) ? intval($_POST['evtsqtty']) : 15;
				$isprov = (isset($_POST['isprov']) and is_numeric($_POST['isprov'])) ? intval($_POST['isprov']) : "";

				$events_rec=get_events($logged->name, $logged->pw, $orgid, $personid, $zoneid, $doorid, $side, $startdate, $starttime, $enddate, $endtime, $startevt, $evtsqtty, $visitedorgid, $isprov);

				if($events_rec and $events_rec->response_status==200) array_push($ret,1,$events_rec->data);
				else array_push($ret,0,$events_rec->data->message);
			}
		break;
		case "purge_events":
			if(!$islogged) array_push($ret,0,"Action needs authentication");
			else {
				$untildatetime = (isset($_POST["untildatetime"]) and $_POST["untildatetime"]!="") ? $_POST["untildatetime"] : "";

				if($untildatetime=="") array_push($ret,0,"Invalid values sent");
				else {
					//purge events
					$events_rec = purge_events($logged->name, $logged->pw, $untildatetime);
					if($events_rec and $events_rec->response_status==200) array_push($ret,1,$events_rec->data);
					else array_push($ret,0,$events_rec->data->message);
				}
			}
		break;

		case "get_zone":
			if(!$islogged) array_push($ret,0,"Action needs authentication");
			else {
				$zone_id = (isset($_POST["id"]) and is_numeric($_POST["id"])) ? $_POST["id"] : "";

				if($zone_id=="") array_push($ret,0,"Invalid values sent");
				else {
					//get record
					$zone_rec = get_zone($logged->name, $logged->pw,$zone_id);
					if($zone_rec) array_push($ret,1,$zone_rec);
					else array_push($ret,0,"Zone could not be retrieved");
				}
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
				} else array_push($ret,0,"Zones not found");
			}
		break;
		case "edit_zone":
			if(!$islogged) array_push($ret,0,"Action needs authentication");
			else {
				$id = (isset($_POST['id']) and is_numeric($_POST['id'])) ? $_POST['id'] : "";
				$name = isset($_POST['name']) ? $_POST['name'] : "";

				if($id=="") array_push($ret,0,"Invalid values sent");
				//empty name can be considered as a valid scenario
	    			else {
					$zones_rec = set_zone($logged->name, $logged->pw, $id, $name);
					if($zones_rec) array_push($ret,1,"Information saved successfully!");
					else array_push($ret,0,"Zone could not be updated");
				}
			}
		break;
		case "add_zone":
			if(!$islogged) array_push($ret,0,"Action needs authentication");
			else {
				$name = isset($_POST['name']) ? $_POST['name'] : "";

				$zones_rec = add_zone($logged->name, $logged->pw, $name);
				if($zones_rec) array_push($ret,1,"Information saved successfully!");
				else array_push($ret,0,"Zone could not be added");
			}
		break;
		case "delete_zone":
			if(!$islogged) array_push($ret,0,"Action needs authentication");
			else {
				$id = (isset($_POST['id']) and is_numeric($_POST['id'])) ? $_POST['id'] : "";

				$zones_rec = delete_zone($logged->name, $logged->pw, $id);
				if($zones_rec) array_push($ret,1,"Information saved successfully!");
				else array_push($ret,0,"Zone could not be deleted");
			}
		break;

		case "get_door":
			if(!$islogged) array_push($ret,0,"Action needs authentication");
			else {
				$id = (isset($_POST["id"]) and is_numeric($_POST["id"])) ? $_POST["id"] : "";

				if($id=="") array_push($ret,0,"Invalid values sent");
				else {
					//get record
					$doors_rec = get_door($logged->name, $logged->pw, $id);
					if($doors_rec) array_push($ret,1,$doors_rec);
					else array_push($ret,0,"Door could not be retrieved");
				}
			}
		break;
		case "get_doors":
			if(!$islogged) array_push($ret,0,"Action needs authentication");
			else {
				$id = (isset($_POST['id']) and is_numeric($_POST['id'])) ? $_POST['id'] : "";
				//get record
				$doors_rec = get_doors($logged->name, $logged->pw, $id);
				if($doors_rec) array_push($ret,1,$doors_rec);
				else array_push($ret,0,"Doors not found");
			}
		break;
		case "add_door":
			if(!$islogged) array_push($ret,0,"Action needs authentication");
			else {
				$zoneid = isset($_POST['zoneid']) ? $_POST['zoneid'] : "";
				$name = isset($_POST['name']) ? $_POST['name'] : "";
				$controllerid = isset($_POST['controllerid']) ? $_POST['controllerid'] : "";
				$doornum = isset($_POST['doornum']) ? $_POST['doornum'] : "";
				$isvisitexit = isset($_POST['isvisitexit']) ? $_POST['isvisitexit'] : "";
				$rlsetime = isset($_POST['rlsetime']) ? $_POST['rlsetime'] : "";
				$bzzrtime = isset($_POST['bzzrtime']) ? $_POST['bzzrtime'] : "";
				$alrmtime = isset($_POST['alrmtime']) ? $_POST['alrmtime'] : "";
				$snsrtype = isset($_POST['snsrtype']) ? $_POST['snsrtype'] : "";

				$doors_rec = add_door($logged->name, $logged->pw, $zoneid, $name, $controllerid, $doornum, $isvisitexit, $rlsetime, $bzzrtime, $alrmtime, $snsrtype);
				//if($doors_rec) array_push($ret,1,"Information saved successfully!");
				//else array_push($ret,0,"Door could not be added");
				if($doors_rec->response_status == "201"){
					array_push($ret,1,"Information saved successfully!");
					//return in third field, the added door id
					$uri_parts=explode("/",$doors_rec->data->uri);
					array_push($ret, intval(end($uri_parts)));
				} else array_push($ret,0,$doors_rec->data->message);
			}
		break;
		case "edit_door":
			if(!$islogged) array_push($ret,0,"Action needs authentication");
			else {
				$id = (isset($_POST['id']) and is_numeric($_POST['id'])) ? $_POST['id'] : "";
				$zoneid = isset($_POST['zoneid']) ? $_POST['zoneid'] : "";
				$name = isset($_POST['name']) ? $_POST['name'] : "";
				$controllerid = isset($_POST['controllerid']) ? $_POST['controllerid'] : "";
				$doornum = isset($_POST['doornum']) ? $_POST['doornum'] : "";
				$isvisitexit = isset($_POST['isvisitexit']) ? $_POST['isvisitexit'] : "";
				$rlsetime = isset($_POST['rlsetime']) ? $_POST['rlsetime'] : "";
				$bzzrtime = isset($_POST['bzzrtime']) ? $_POST['bzzrtime'] : "";
				$alrmtime = isset($_POST['alrmtime']) ? $_POST['alrmtime'] : "";
				$snsrtype = isset($_POST['snsrtype']) ? $_POST['snsrtype'] : "";

				if($id=="") array_push($ret,0,"Invalid values sent");
	    			else {
					$doors_rec = set_door($logged->name, $logged->pw, $id, $zoneid, $name, $controllerid, $doornum, $isvisitexit, $rlsetime, $bzzrtime, $alrmtime, $snsrtype);

					if($doors_rec) array_push($ret,1,"Information saved successfully!");
					else array_push($ret,0,"Door could not be updated");
				}
			}
		break;
		case "delete_door":
			if(!$islogged) array_push($ret,0,"Action needs authentication");
			else {
				$id = (isset($_POST['id']) and is_numeric($_POST['id'])) ? $_POST['id'] : "";

				$doors_rec = delete_door($logged->name, $logged->pw, $id);

				if($doors_rec) array_push($ret,1,"Information saved successfully!");
				else array_push($ret,0,"Door could not be deleted");
			}
		break;
        case "open_door":
            if(!$islogged) array_push($ret,0,"Action needs authentication");
            else {
               $id = (isset($_POST['id']) and is_numeric($_POST['id'])) ? $_POST['id'] : "";

               $doors_rec = open_door($logged->name, $logged->pw, $id);

               if($doors_rec) array_push($ret,1,"Door has been opened");
               else array_push($ret,0,"Door could not be opened");
            }
        break;

		case "get_uds_door":
			if(!$islogged) array_push($ret,0,"Action needs authentication");
			else {
				$id = (isset($_POST["id"]) and is_numeric($_POST["id"])) ? $_POST["id"] : "";

				if($id=="") array_push($ret,0,"Invalid values sent");
				else {
					//get record
					$uds_rec = get_uds_door($logged->name, $logged->pw, $id);
					if($uds_rec) array_push($ret,1,$uds_rec);
					//else array_push($ret,0,"Schedules could not be retrieved");
					else array_push($ret,0,array());
				}
			}
		break;
		case "get_uds":
			if(!$islogged) array_push($ret,0,"Action needs authentication");
			else {
				$id = (isset($_POST["id"]) and is_numeric($_POST["id"])) ? $_POST["id"] : "";

				if($id=="") array_push($ret,0,"Invalid values sent");
				else {
					//get record
					$uds_rec = get_uds($logged->name, $logged->pw, $id);
					if($uds_rec) array_push($ret,1,$uds_rec);
					else array_push($ret,0,"Schedule could not be retrieved");
				}
			}
		break;
		case "add_uds":
			if(!$islogged) array_push($ret,0,"Action needs authentication");
			else {
				$doorid = (isset($_POST["doorid"]) and is_numeric($_POST["doorid"])) ? $_POST["doorid"] : "";
				$weekday = (isset($_POST["weekday"]) and is_numeric($_POST["weekday"])) ? $_POST["weekday"] : 0;
				$starttime = isset($_POST['starttime']) ? $_POST['starttime'] : "";
				$endtime = isset($_POST['endtime']) ? $_POST['endtime'] : "";

				if($doorid=="" or ($weekday>7) or ($weekday<1) or (!is_valid_time($starttime)) or (!is_valid_time($endtime))) array_push($ret,0,"Invalid values sent");
				else {
					$uds_rec = add_uds($logged->name, $logged->pw, $doorid, $weekday, $starttime, $endtime);
					if($uds_rec->response_status == "201") array_push($ret,1,"Information saved successfully!");
					else array_push($ret,0,$uds_rec->data->message);
				}
			}
		break;
		case "delete_uds":
			if(!$islogged) array_push($ret,0,"Action needs authentication");
			else {
				$id = (isset($_POST['id']) and is_numeric($_POST['id'])) ? $_POST['id'] : "";

				$uds_rec = delete_uds($logged->name, $logged->pw, $id);

				if($uds_rec) array_push($ret,1,"Information saved successfully!");
				else array_push($ret,0,"Schedule could not be deleted");
			}
		break;

		case "get_excdayuds_door":
			if(!$islogged) array_push($ret,0,"Action needs authentication");
			else {
				$id = (isset($_POST["id"]) and is_numeric($_POST["id"])) ? $_POST["id"] : "";

				if($id=="") array_push($ret,0,"Invalid values sent");
				else {
					//get record
					$excdayuds_rec = get_excdayuds_door($logged->name, $logged->pw, $id);
					if($excdayuds_rec) array_push($ret,1,$excdayuds_rec);
					//else array_push($ret,0,"Exception could not be retrieved");
					else array_push($ret,0,array());
				}
			}
		break;
		case "get_excdayuds":
			if(!$islogged) array_push($ret,0,"Action needs authentication");
			else {
				$id = (isset($_POST["id"]) and is_numeric($_POST["id"])) ? $_POST["id"] : "";

				if($id=="") array_push($ret,0,"Invalid values sent");
				else {
					//get record
					$excdayuds_rec = get_excdayuds($logged->name, $logged->pw, $id);
					if($excdayuds_rec) array_push($ret,1,$excdayuds_rec);
					else array_push($ret,0,"Exception could not be retrieved");
				}
			}
		break;
		case "add_excdayuds":
			if(!$islogged) array_push($ret,0,"Action needs authentication");
			else {
				$doorid = (isset($_POST["doorid"]) and is_numeric($_POST["doorid"])) ? $_POST["doorid"] : "";
				$excday = (isset($_POST["excday"]) and $_POST["excday"]!="") ? $_POST["excday"] : 0;

				if($doorid=="" or !is_valid_date($excday)) array_push($ret,0,"Invalid values sent");
				else {
					$excdayuds_rec = add_excdayuds($logged->name, $logged->pw, $doorid, $excday);
					if($excdayuds_rec->response_status == "201") array_push($ret,1,"Information saved successfully!");
					else array_push($ret,0,$excdayuds_rec->data->message);
				}
			}
		break;
		case "delete_excdayuds":
			if(!$islogged) array_push($ret,0,"Action needs authentication");
			else {
				$id = (isset($_POST['id']) and is_numeric($_POST['id'])) ? $_POST['id'] : "";

				$excdayuds_rec = delete_excdayuds($logged->name, $logged->pw, $id);

				if($excdayuds_rec) array_push($ret,1,"Information saved successfully!");
				else array_push($ret,0,"Exception could not be deleted");
			}
		break;

		case "get_door_groups":
			if(!$islogged) array_push($ret,0,"Action needs authentication");
			else {
				//get record
				$vdg_rec = get_door_groups($logged->name, $logged->pw);
				if($vdg_rec){
					//return record
					array_push($ret,1,$vdg_rec);
				} else array_push($ret,0,"Door groups not found");
			}
		break;
		case "get_visit_door_groups":
			if(!$islogged) array_push($ret,0,"Action needs authentication");
			else {
				//get record
				$vdg_rec = get_visit_door_groups($logged->name, $logged->pw);
				if($vdg_rec){
					//return record
					array_push($ret,1,$vdg_rec);
				} else array_push($ret,0,"Visit door groups not found");
			}
		break;
		case "get_door_group":
			if(!$islogged) array_push($ret,0,"Action needs authentication");
			else {
				$vdg_id = (isset($_POST["id"]) and is_numeric($_POST["id"])) ? $_POST["id"] : "";

				if($vdg_id=="") array_push($ret,0,"Invalid values sent");
				else {
					//get record
					$vdg_rec = get_door_group($logged->name, $logged->pw, $vdg_id);
					if($vdg_rec){
						//return record
						array_push($ret,1,$vdg_rec);
					} else array_push($ret,0,"Door group could not be retrieved");
				}
			}
		break;
		case "edit_door_group":
			if(!$islogged) array_push($ret,0,"Action needs authentication");
			else {
				$id = (isset($_POST['id']) and is_numeric($_POST['id'])) ? $_POST['id'] : "";
				$name = isset($_POST['name']) ? $_POST['name'] : "";
				$doorids = (isset($_POST['doorids'])) ? $_POST['doorids'] : "";
				$isvisit = (isset($_POST['isvisit'])) ? $_POST['isvisit'] : 1;

				if($id=="") array_push($ret,0,"Invalid values sent");
				//empty name can be considered as a valid scenario
	    			else {
					$vdg_rec = set_door_group($logged->name, $logged->pw, $id, $name, $doorids,$isvisit);

					if($vdg_rec) array_push($ret,1,"Information saved successfully!");
					else array_push($ret,0,"Door group could not be updated");
				}
			}
		break;
		case "add_door_group":
			if(!$islogged) array_push($ret,0,"Action needs authentication");
			else {
				$name = isset($_POST['name']) ? $_POST['name'] : "";
				$doorids = (isset($_POST['doorids'])) ? $_POST['doorids'] : "";
				$isvisit = (isset($_POST['isvisit'])) ? $_POST['isvisit'] : 1;

				$vdg_rec = add_door_group($logged->name, $logged->pw, $name, $doorids, $isvisit);
				if($vdg_rec) array_push($ret,1,"Information saved successfully!");
				else array_push($ret,0,"Door group could not be added");
			}
		break;
		case "delete_door_group":
			if(!$islogged) array_push($ret,0,"Action needs authentication");
			else {
				$id = (isset($_POST['id']) and is_numeric($_POST['id'])) ? $_POST['id'] : "";

				$vdg_rec = delete_door_group($logged->name, $logged->pw, $id);

				if($vdg_rec) array_push($ret,1,"Information saved successfully!");
				else array_push($ret,0,"Door group could not be deleted");
			}
		break;
		case "get_door_group_doors":
			if(!$islogged) array_push($ret,0,"Action needs authentication");
			else {
				$vdg_id = (isset($_POST["id"]) and is_numeric($_POST["id"])) ? $_POST["id"] : "";

				if($vdg_id=="") array_push($ret,0,"Invalid values sent");
				else {
					//get record
					$vdg_rec = get_door_group_doors($logged->name, $logged->pw, $vdg_id);
					if($vdg_rec){
						//return record
						array_push($ret,1,$vdg_rec);
					} else array_push($ret,0,"Door group doors could not found");
				}
			}
		break;

		case "get_visitors":
			if(!$islogged) array_push($ret,0,"Action needs authentication");
			else {
				$visitdoorgroupid = (isset($_POST['visitdoorgroupid']) and is_numeric($_POST['visitdoorgroupid'])) ? intval($_POST['visitdoorgroupid']) : "";
				$orgid = (isset($_POST['orgid']) and is_numeric($_POST['orgid'])) ? intval($_POST['orgid']) : "";
				$cardnum = isset($_POST['cardnum']) ? $_POST['cardnum'] : "";
				$idnum = isset($_POST['idnum']) ? $_POST['idnum'] : "";
				$isprov = (isset($_POST['isprov']) and is_numeric($_POST['isprov'])) ? intval($_POST['isprov']) : "";

				$visitors_rec=get_visitors($logged->name, $logged->pw, $visitdoorgroupid, $orgid, $cardnum, $idnum, $isprov);

				if($visitors_rec and $visitors_rec->response_status==200) array_push($ret,1,$visitors_rec->data);
				else array_push($ret,0,$visitors_rec->data->message);
			}
		break;
		case "add_visit":
			if(!$islogged) array_push($ret,0,"Action needs authentication");
			else {
				$names = isset($_POST['names']) ? $_POST['names'] : "";
				$lastname = isset($_POST['lastname']) ? $_POST['lastname'] : "";
				$idnum = isset($_POST['idnum']) ? $_POST['idnum'] : "";
				$cardnum = isset($_POST['cardnum']) ? $_POST['cardnum'] : "";
				$orgid = isset($_POST['orgid']) ? $_POST['orgid'] : "";
				$expirationdate = isset($_POST['expirationdate']) ? $_POST['expirationdate'] : "";
				$expirationhour = isset($_POST['expirationhour']) ? $_POST['expirationhour'] : "23:59";
				$doorgroupids = isset($_POST['doorgroupids']) ? $_POST['doorgroupids'] : "";
				$note = isset($_POST['note']) ? $_POST['note'] : "";
				$isprov = (isset($_POST['isprov']) and is_numeric($_POST['isprov'])) ? intval($_POST['isprov']) : "";

				$visit_rec = add_visit($logged->name, $logged->pw, $names, $lastname, $idnum, $cardnum, $orgid, $expirationdate, $expirationhour, $doorgroupids, $note, $isprov);

				//if($visit_rec->response_status == "201") array_push($ret,1,"Information saved successfully!");
				//else array_push($ret,0,$visit_rec->data->message);
				if($visit_rec->response_status == "201"){
					array_push($ret,1,"Information saved successfully!");
					//return in third field, the added visit id
					$uri_parts=explode("/",$visit_rec->data->uri);
					array_push($ret, intval(end($uri_parts)));
				} else array_push($ret,0,$persons_rec->data->message);
			}
		break;
		case "edit_visit":
			if(!$islogged) array_push($ret,0,"Action needs authentication");
			else {
				$id = (isset($_POST['id']) and is_numeric($_POST['id'])) ? $_POST['id'] : "";
				$names = isset($_POST['names']) ? $_POST['names'] : "";
				$lastname = isset($_POST['lastname']) ? $_POST['lastname'] : "";
				$idnum = isset($_POST['idnum']) ? $_POST['idnum'] : "";
				$cardnum = isset($_POST['cardnum']) ? $_POST['cardnum'] : "";
				$note = isset($_POST['note']) ? $_POST['note'] : "";
				$orgid = isset($_POST['orgid']) ? $_POST['orgid'] : "";
				$isprov = (isset($_POST['isprov']) and is_numeric($_POST['isprov'])) ? intval($_POST['isprov']) : "";

				if($id=="") array_push($ret,0,"Invalid values sent");
	    			else {
					$persons_rec = set_visit($logged->name, $logged->pw, $id, $names, $lastname, $idnum, $cardnum, $note, $orgid, $isprov);

					if($persons_rec) array_push($ret,1,"Information saved successfully!");
					else array_push($ret,0,"Person could not be updated");
				}
			}
		break;
		case "get_controller":
			if(!$islogged) array_push($ret,0,"Action needs authentication");
			else {
				$controller_id = (isset($_POST["id"]) and is_numeric($_POST["id"])) ? $_POST["id"] : "";

				if($controller_id=="") array_push($ret,0,"Invalid values sent");
				else {
					//get record
					$controller_rec = get_controller($logged->name, $logged->pw, $controller_id);
					if($controller_rec){
						//return record
						array_push($ret,1,$controller_rec);
					} else array_push($ret,0,"Controller could not be retrieved");
				}
			}
		break;
		case "get_controllers":
			if(!$islogged) array_push($ret,0,"Action needs authentication");
			else {
				//get record
				$controllers_rec = get_controllers($logged->name, $logged->pw);
				if($controllers_rec){
					//return record
					array_push($ret,1,$controllers_rec);
				} else array_push($ret,0,"Controllers not found");
			}
		break;
		case "get_controller_models":
			if(!$islogged) array_push($ret,0,"Action needs authentication");
			else {
				//get record
				$controllers_rec = get_controller_models($logged->name, $logged->pw);
				if($controllers_rec){
					//return record
					array_push($ret,1,$controllers_rec);
				} else array_push($ret,0,"Controller models not found");
			}
		break;
		case "edit_controller":
			if(!$islogged) array_push($ret,0,"Action needs authentication");
			else {
				$id = (isset($_POST['id']) and is_numeric($_POST['id'])) ? $_POST['id'] : "";
				$name = isset($_POST['name']) ? $_POST['name'] : "";
				$model_id = isset($_POST['model_id']) ? $_POST['model_id'] : "";
				$mac = isset($_POST['mac']) ? $_POST['mac'] : "";

				if($id=="") array_push($ret,0,"Invalid values sent");
				else if($name=="") array_push($ret,0,"Name not set");
				else if(!is_numeric($model_id)) array_push($ret,0,"Invalid model ID sent");
				else if($mac=="") array_push($ret,0,"MAC not set");
	    			else {
					$controllers_rec = set_controller($logged->name, $logged->pw, $id, $name,$model_id, $mac);

					if($controllers_rec) array_push($ret,1,"Information saved successfully!");
					else array_push($ret,0,"Controller could not be updated");
				}
			}
		break;
		case "add_controller":
			if(!$islogged) array_push($ret,0,"Action needs authentication");
			else {
				$name = isset($_POST['name']) ? $_POST['name'] : "";
				$model_id = isset($_POST['model_id']) ? $_POST['model_id'] : "";
				$mac = isset($_POST['mac']) ? $_POST['mac'] : "";

				if($name=="") array_push($ret,0,"Name not set");
				else if(!is_numeric($model_id)) array_push($ret,0,"Invalid model ID sent");
				else if($mac=="") array_push($ret,0,"MAC not set");
	    			else {
					$controllers_rec = add_controller($logged->name, $logged->pw, $name, $model_id, $mac);
					if($controllers_rec) array_push($ret,1,"Information saved successfully!");
					else array_push($ret,0,"Controller could not be added");
				}
			}
		break;
		case "delete_controller":
			if(!$islogged) array_push($ret,0,"Action needs authentication");
			else {
				$id = (isset($_POST['id']) and is_numeric($_POST['id'])) ? $_POST['id'] : "";

				$controllers_rec = delete_controller($logged->name, $logged->pw, $id);

				if($controllers_rec->response_status != "200") array_push($ret,0,$controllers_rec->data->message);
				else array_push($ret,1,"Information saved successfully!");
			}
		break;
		case "reprov_controller":
			if(!$islogged) array_push($ret,0,"Action needs authentication");
			else {
				$id = (isset($_POST['id']) and is_numeric($_POST['id'])) ? $_POST['id'] : "";

				$controllers_rec = reprov_controller($logged->name, $logged->pw, $id);

				if($controllers_rec) array_push($ret,1,"Controller reprogrammed successfully");
				else array_push($ret,0,"Controller could not be reprogrammed");
			}
		break;
		case "poweroff_controller":
			if(!$islogged) array_push($ret,0,"Action needs authentication");
			else {
				$id = (isset($_POST['id']) and is_numeric($_POST['id'])) ? $_POST['id'] : "";

				$controllers_rec = poweroff_controller($logged->name, $logged->pw, $id);

				if($controllers_rec) array_push($ret,1,"Controller turned off successfully");
				else array_push($ret,0,"Controller could not be turned off");
			}
		break;

		case "get_user":
			if(!$islogged) array_push($ret,0,"Action needs authentication");
			else {
				$user_id = (isset($_POST["id"]) and is_numeric($_POST["id"])) ? $_POST["id"] : "";

				if($user_id=="") array_push($ret,0,"Invalid values sent");
				else {
					//get record
					$user_rec = get_user($logged->name, $logged->pw, $user_id);
					if($user_rec){
						//return record
						array_push($ret,1,$user_rec);
					} else array_push($ret,0,"User could not be retrieved");
				}
			}
		break;
		case "get_users":
			if(!$islogged) array_push($ret,0,"Action needs authentication");
			else {
				//get record
				$users_rec = get_users($logged->name, $logged->pw);
				if($users_rec){
					//return record
					array_push($ret,1,$users_rec);
				} else array_push($ret,0,"Users not found");
			}
		break;
		case "edit_user":
			if(!$islogged) array_push($ret,0,"Action needs authentication");
			else {
				$id = (isset($_POST['id']) and is_numeric($_POST['id'])) ? $_POST['id'] : "";
				$fullname = isset($_POST['fullname']) ? $_POST['fullname'] : "";
				$username = isset($_POST['username']) ? $_POST['username'] : "";
				$password = isset($_POST['password']) ? $_POST['password'] : "";
				$roleid = (isset($_POST['roleid']) and is_numeric($_POST['roleid'])) ? $_POST['roleid'] : "";
				$active = (isset($_POST['active']) and is_numeric($_POST['active'])) ? $_POST['active'] : "";
				$lang = (isset($_POST['lang'])) ? $_POST['lang'] : "";

				if($id=="") array_push($ret,0,"Invalid values sent");
	    			else {
					$users_rec = set_user($logged->name, $logged->pw, $id, $fullname, $username, $password, $roleid, $active, $lang);

					if($users_rec) array_push($ret,1,"Information saved successfully!");
					else array_push($ret,0,"User could not be updated");
				}
			}
		break;
		case "add_user":
			if(!$islogged) array_push($ret,0,"Action needs authentication");
			else {
				$fullname = isset($_POST['fullname']) ? $_POST['fullname'] : "";
				$username = isset($_POST['username']) ? $_POST['username'] : "";
				$password = isset($_POST['password']) ? $_POST['password'] : "";
				$roleid = (isset($_POST['roleid']) and is_numeric($_POST['roleid'])) ? $_POST['roleid'] : "";
				$active = (isset($_POST['active']) and is_numeric($_POST['active'])) ? $_POST['active'] : "";
				$lang = (isset($_POST['lang'])) ? $_POST['lang'] : "";

				$users_rec = add_user($logged->name, $logged->pw, $fullname, $username, $password, $roleid, $active, $lang);

				if($users_rec) array_push($ret,1,"Information saved successfully!");
				else array_push($ret,0,"User could not be added");
			}
		break;
		case "delete_user":
			if(!$islogged) array_push($ret,0,"Action needs authentication");
			else {
				$id = (isset($_POST['id']) and is_numeric($_POST['id'])) ? $_POST['id'] : "";

				$users_rec = delete_user($logged->name, $logged->pw, $id);

				if($users_rec) array_push($ret,1,"Information saved successfully!");
				else array_push($ret,0,"User could not be deleted");
			}
		break;
		case "get_roles":
			if(!$islogged) array_push($ret,0,"Action needs authentication");
			else {
				//get record
				$roles_rec = get_roles($logged->name, $logged->pw);
				if($roles_rec){
					//return record
					array_push($ret,1,$roles_rec);
				} else array_push($ret,0,"Roles not found");
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
