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
						//yield record
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
					//yield record
					array_push($ret,1,$organizations_rec);
				} else array_push($ret,0,"Organizations could not be retrieved");
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
					//yield record
					array_push($ret,1,$persons_rec);
				} else array_push($ret,0,"Persons could not be retrieved");
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
						//yield record
						array_push($ret,1,$persons_rec);
					} else array_push($ret,0,"Organization could not be retrieved");
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
				if($persons_rec) array_push($ret,1,"Information saved successfully!");
				else array_push($ret,0,"Person could not be added");
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
		default:
			array_push($ret,0,"Operation not defined"); //send out error
		break;
	}
}

header("Content-type: application/json");
echo json_encode($ret);
?>