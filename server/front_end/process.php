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
					//return record
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
						//return record
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
				} else array_push($ret,0,"No accesses found");
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
				} else array_push($ret,0,"No accesses found");
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
				if($access_rec->response_status != "201") array_push($ret,0,$access_rec->error);
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
/*		case "login":
			$dbcnx = imvustylez_connect_db();

			$username= isset($_POST['username']) ? real_escape_string($_POST['username']) : "";
			$password= isset($_POST['password']) ? md5($_POST['password']) : "";

			$data = get_record_sql("SELECT * FROM filedrive_users WHERE username = '$username'");
			if($data){
				if(($data->password != $password) || ($data->blocked == 1)){
			      		$error = "Incorrect password";
					addtolog($username, "tries incorrect password in login: ".$_POST['password']);
				}else{
					$_SESSION[$config->sesskey] = $data->username;
					//rotate login dates
					$oldcurrentlogindate=$data->current_login;
					exec_query("UPDATE filedrive_users SET current_login=CURDATE(), last_login='$oldcurrentlogindate' WHERE id=".$data->id);
					addtolog($_SESSION[$config->sesskey], "logs in");
					setcookie($config->sesskeycookiename, md5($password)."|".$data->username."|".md5($_SERVER["HTTP_USER_AGENT"]), time() + $config->cookie_lifetime);
					array_push($ret,1,"Login success! Please wait...");
				}
			} else {
		      		//username not found > fetch avatarid from imvu and try check if avatar id is
		      		$avatar_id = get_avatar_ID($username);
		      		if(is_numeric($avatar_id)){
		      			$data2 = get_record_sql("SELECT * FROM filedrive_users WHERE avatarid = '$avatar_id'");
		      			if(!$data2){
		      				//if not > show invalid login
						$error = "Invalid username: $username";
		      			} else {
		      				//if is > suggest the avatar name that is registed and try again
						$error = "That user is registered on the system under the old name: '".$data2->username."'. Please try to log in with that avatar name and the same password as before. You can update your avatar name once logged in.";
		      			}
		      		} else $error = "Invalid username: $username";
			}
			if($error!="") array_push($ret,0,$error); //send out error
			close_dbcnx($dbcnx);
		break;

		case "logout":
			if(isset($_SESSION[$config->sesskey])){
				//session variable is registered, the user is ready to logout 
				//log action
				$dbcnx = imvustylez_connect_db();
				addtolog($_SESSION[$config->sesskey], "logs out");
				close_dbcnx($dbcnx);
				//destroy cookies
				setcookie($config->sesskeycookiename, "", time() - $config->cookie_lifetime);
				//destroy session
				session_unset(); 
				session_destroy();
			}
		break;

		case "forgot":
			$username= isset($_POST['username']) ? $_POST['username'] : "";
			$email= isset($_POST['email']) ? $_POST["email"] : "";

			if($username=="" || $email=="") $error="Please fill all fields";
			elseif(!check_email_address($email)) $error="Email entered is not valid";
			else {
      				$dbcnx = imvustylez_connect_db();
      				$username = real_escape_string($username);
      				$email = real_escape_string($email);

      				//check if user already exists
      				$username_exist = get_record_sql("SELECT username,avatarid,email FROM filedrive_users WHERE username='$username'");

	      			if(!$username_exist){
	      		     		//username not found > fetch avatarid from imvu and try check if avatar id is
	      		      		$avatar_id = get_avatar_ID($username);
	      		      		if(is_numeric($avatar_id)){
	      		      			$query2 = get_record("users","avatarid",$avatar_id);
	      		      			if(!$query2){
	      		      				//if not > show invalid login
	      						$error="Avatar is not registered on the site yet";
	      		      			} else {
	      		      				//if is > suggest the avatar name that is registed and try again
	      						$error="That user is registered on the system under the old name: '".$query2->username."'<br>Try entering that avatar name instead and submitting again.";
	      		      			}
	      		      		} else $error="Invalid avatar name";
	      			} else {
	      				$user_data = $username_exist;

	      				if($user_data->email != $email){
	      					$error="Email sent doesn't match with registered email. Contact Us for more details";
	      				} else {
	      					// generate new password
	      					$clave=generate_password();
	      					// encode
	      					$newpassword = md5($clave);
	      					// update on database
	      					$query = exec_query("UPDATE filedrive_users SET password='$newpassword' WHERE username='$username'");
	      					// send email with updated password
	      					mail_rememberpass($username, $email, $clave, $config->wwwroot, $config->wwwroot, "Imvustylez Filedrive | Account Password Reminder");
	      					array_push($ret,1,"A new password has been sent to your email address!");
	      					addtolog($username, "remembers password");
	      				}
	      			}
      				close_dbcnx($dbcnx);
			}
			if($error!="") array_push($ret,0,$error); //send out error
		break;

		case "register":
			$username= isset($_POST['username']) ? addslashes($_POST['username']) : "";
			$password= isset($_POST['password']) ? $_POST['password'] : "";
			$cpassword= isset($_POST['cpassword']) ? $_POST['cpassword'] : "";
			$email= isset($_POST['email']) ? $_POST['email'] : "";

			if($username=="" || $password=="" || $cpassword=="" || $email=="") $error="Please fill all fields";
			elseif(!check_email_address($email)) $error="Email entered is not valid";
			elseif($password!=$cpassword) $error="Passwords don't match";
			else {
				$avatarid=get_avatar_ID($username);
				if(!is_numeric($avatarid)) $error="That avatar is banned or doesn't exists";
				else {
					$dbcnx = imvustylez_connect_db();
					$username = real_escape_string($username);
					$password = md5($password);
					$email = real_escape_string($email);

					//check if user already exists
					$username_exist = get_record_sql("SELECT username,avatarid FROM filedrive_users WHERE username='$username' or avatarid='$avatarid' or email='$email'");

					if($username_exist){
						$error="That user (or email) is already registered on the system under the avatar name: $username_exist->username. <br>Please, check again. If you are still having problems registering, contact the administrator of the site clicking on the 'Contact Us' link on the footer.";
					} else {
						//CLEAR OLD EMPTY ACCOUNTS
						//get 1 year old empty accounts 
						$oldemptyaccounts = get_records_sql("SELECT id,username,avatarid FROM filedrive_users where (UNIX_TIMESTAMP() - unix_timestamp(current_login)) > (60*60*24*366) and username not in (select distinct owner_avatarname from filedrive_files)");
						//if theres at least 1, remove it and all of its files
						if($oldemptyaccounts and count($oldemptyaccounts)>0){
							foreach($oldemptyaccounts  as $row) {
								purge_user_from_row($row);
								addtolog("system", "purges old empty account: $row->username");
							}
						}

						//proceed with insert
		      				//check if user is ap
			      			include("/home/imvustyl/public_html/gaf210/gateway-funcs.php");
			      			$has_ap=isApUser($username);
						//insert
						$res=exec_query("INSERT INTO filedrive_users (username, password, email,avatarid, date_added,last_login,current_login,has_ap) VALUES('$username','$password','$email', '$avatarid', CURDATE(),CURDATE(),CURDATE(),'$has_ap')");
						if($res and mkdir($config->filespath.$username, 0755)) {
							addtolog($username, "registers account");
							array_push($ret,1,"Registration success! Now you can Sign in with your recently created credentials");
						} else $error="An error occurred when creating your account. <br>If you are still having problems registering, contact the administrator of the site clicking on the 'Contact Us' link on the footer.";
					}
					close_dbcnx($dbcnx);
				}
			}
			if($error!="") array_push($ret,0,$error); //send out error
		break;

		case "editaccount":
			if(!$islogged) $error="Action needs authentication";
			else {
				$dbcnx = imvustylez_connect_db();
				if(is_admin($_SESSION[$config->sesskey]) && isset($_POST['user_id'])) $user_id = real_escape_string($_POST['user_id']); else $user_id = real_escape_string($logged->id);
				$password= isset($_POST['password']) ? $_POST['password'] : "";
				$cpassword= isset($_POST['cpassword']) ? $_POST['cpassword'] : "";
				$email= isset($_POST['email']) ? real_escape_string($_POST["email"]) : "";

				if(!check_email_address($email)) $error="Email entered is not valid";
				elseif($password!=$cpassword) $error="Passwords don't match";
	    			else {
	      				if($password !=""){
		      				$password = md5($password);
	      					exec_query("UPDATE filedrive_users SET password='$password', email='$email' WHERE id = '$user_id'");
	      				} else {
	      					exec_query("UPDATE filedrive_users SET email='$email' WHERE id = '$user_id'");
	      				}
					if(!is_admin($_SESSION[$config->sesskey])) addtolog($_SESSION[$config->sesskey], "edits account settings");
					array_push($ret,1,"Information saved successfully!");
				}
				close_dbcnx($dbcnx);
			}

			if($error!="") array_push($ret,0,$error); //send out error
		break;

		case "getfile":
			if(!$islogged) array_push($ret,0,"Action needs authentication");
			else {
				$fileid = (isset($_POST["id"]) and is_numeric($_POST["id"])) ? $_POST["id"] : "";
				$getshareid = (isset($_POST["getshareid"]) and is_numeric($_POST["getshareid"]) and $_POST["getshareid"]>0) ? 1 : 0;

				if($fileid=="") array_push($ret,0,"Invalid values sent");
				else {
	      				$dbcnx = imvustylez_connect_db();
					//get file record
					$file_rec = get_record_select("files","id=$fileid");
					if($file_rec){
						//check if logged is owner of file
						if(is_admin($logged->username) or $file_rec->owner_avatarname==$logged->username){
							//add file without extension in response
							$file_rec->filename_noext = get_filename_only($file_rec->filename);
							//generate shareid if not existent
							if($getshareid and $file_rec->shareid==""){
								//generate share id
								$file_rec->shareid=time();
								update_record("files",$file_rec);
							}
							//return file record
							array_push($ret,1,$file_rec);
						} else array_push($ret,0,"File has a different owner");
					} else array_push($ret,0,"File couldn't be retrieved");
	      				close_dbcnx($dbcnx);
				}
			}
		break;

		case "renamefile":
			if(!$islogged) array_push($ret,0,"Action needs authentication");
			else {
				$fileid = (isset($_POST["id"]) and is_numeric($_POST["id"])) ? $_POST["id"] : "";
				$newname = (isset($_POST["filename"]) and $_POST["filename"]!="") ? $_POST["filename"] : "";

				if($fileid=="" or $newname=="") array_push($ret,0,"Invalid values sent");
				else {
	      				$dbcnx = imvustylez_connect_db();
					//fetch file record
					$file_rec = get_record_select("files","id=$fileid","id,filename,type,owner_avatarname");
					if($file_rec){
						//check if logged is owner of file
						if(is_admin($logged->username) or $file_rec->owner_avatarname==$logged->username){
							//check if file exists on filesystem
							$filesurl=$config->filespath.$file_rec->owner_avatarname;
							if(file_exists("$filesurl/$file_rec->filename")){
								//sanitize new file name
								$newname = real_escape_string($newname);
								$new_filename = preg_replace('/[^0-9a-z\_\-]/i','',$newname);
								$new_filename = $new_filename . "." . $file_rec->type;
								//rename file on fs
								if(rename ("$filesurl/$file_rec->filename", "$filesurl/$new_filename")){
									// rename file on db
									addtolog($logged->username, "Renames file: $file_rec->filename to $new_filename");
									$file_rec->filename=$new_filename;
									update_record("files",$file_rec);
									array_push($ret,1,"Changes saved successfully!");
								} else array_push($ret,0,"Couldnt rename file on file system");
							} else array_push($ret,0,"File does not exist on file system");
						} else array_push($ret,0,"File has a different owner");
					} else array_push($ret,0,"File couldn't be retrieved");
	      				close_dbcnx($dbcnx);
				}
			}
		break;

		case "removefile":
			if(!$islogged) array_push($ret,0,"Action needs authentication");
			else {
				$fileid = (isset($_POST["id"]) and is_numeric($_POST["id"])) ? $_POST["id"] : "";

				if($fileid=="") array_push($ret,0,"Invalid values sent");
				else {
	      				$dbcnx = imvustylez_connect_db();
					//fetch file record
					$file_rec = get_record_select("files","id=$fileid","id,filename,size,owner_avatarname");
					if($file_rec){
						//check if logged is owner of file
						if(is_admin($logged->username) or $file_rec->owner_avatarname==$logged->username){
							//delete file on filesystem
							if($file_rec->filename!="" and file_exists($config->filespath."$file_rec->owner_avatarname/$file_rec->filename")) unlink($config->filespath."$file_rec->owner_avatarname/$file_rec->filename");
							//delete file on db
							$query = delete_records("files","id",$file_rec->id);
							//update quota
							$size = $file_rec->size;
							$prev_quota = $logged->quota;
							exec_query("UPDATE filedrive_users SET quota=" . adjust_quota("sum", $prev_quota, $size) . " WHERE id='" . $logged->id ."'");
							addtolog($logged->username, "deletes file: $file_rec->filename");
							array_push($ret,1,"File has been removed succesfully!");
						} else array_push($ret,0,"File has a different owner");
					} else array_push($ret,0,"File couldn't be retrieved");
	      				close_dbcnx($dbcnx);
				}
			}
		break;

		case "bulkremovefiles":
			if(!$islogged) array_push($ret,0,"Action needs authentication");
			else {
				$fileids = (isset($_POST["ids"]) and $_POST["ids"]!="") ? $_POST["ids"] : "";
				//check empty values
				if($fileids=="") array_push($ret,0,"Invalid values sent");
				else {
					$fileids_array=json_decode($fileids);
					//check valid array value
					if(!$fileids_array or !is_array($fileids_array)) array_push($ret,0,"Values sent could not be parsed");
					else {
						//clear valid ids sent
						$final_ids_array=array();
						foreach($fileids_array as $id) if(is_numeric($id) and $id>0) $final_ids_array[]=$id;
						if(empty($final_ids_array)) array_push($ret,0,"No valid values sent");
						else {
			      				$dbcnx = imvustylez_connect_db();
							//fetch file records
							$final_ids_string = implode(",",$final_ids_array);
							if(is_admin($logged->username)) $file_recs = get_records_select("files","id in ($final_ids_string)","id,filename,size,owner_avatarname");
							else $file_recs = get_records_select("files","id in ($final_ids_string) and owner_avatarid='$logged->avatarid'","id,filename,size,owner_avatarname");
							if($file_recs){
								foreach($file_recs as $file_rec){
      									//delete file on filesystem
      									if($file_rec->filename!="" and file_exists($config->filespath."$file_rec->owner_avatarname/$file_rec->filename")) unlink($config->filespath."$file_rec->owner_avatarname/$file_rec->filename");
      									//delete file on db
      									$query = delete_records("files","id",$file_rec->id);
      									//update quota
      									$size = $file_rec->size;
      									$prev_quota = $logged->quota;
      									exec_query("UPDATE filedrive_users SET quota=" . adjust_quota("sum", $prev_quota, $size) . " WHERE id='" . $logged->id ."'");
      									addtolog($logged->username, "deletes file: $file_rec->filename");
      									if(!isset($ret[0]) or $ret[0]!=1) $ret=array(1,"File/s have been removed succesfully!");
								}
							} else array_push($ret,0,"Files couldn't be retrieved");
			      				close_dbcnx($dbcnx);
		      				}
	      				}
				}
			}
		break;

		case "getuser":
			if(!$islogged or !is_admin($logged->username)) array_push($ret,0,"Action needs authentication");
			else {
				$userId = (isset($_POST["id"]) and is_numeric($_POST["id"])) ? $_POST["id"] : "";

				if($userId=="") array_push($ret,0,"Invalid values sent");
				else {
	      				$dbcnx = imvustylez_connect_db();
					//get user record
					$user_rec = get_record_select("users","id=$userId","id,username,email,avatarid,blocked,has_ap");
					if($user_rec){
						//return user record
						array_push($ret,1,$user_rec);
					} else array_push($ret,0,"User couldn't be retrieved");
	      				close_dbcnx($dbcnx);
				}
			}
		break;

		case "removeuser":
			if(!$islogged or !is_admin($logged->username)) array_push($ret,0,"Action needs authentication");
			else {
				$avatarid = (isset($_POST["id"]) and is_numeric($_POST["id"])) ? $_POST["id"] : "";

				if($avatarid=="") array_push($ret,0,"Invalid values sent");
				else {
	      				$dbcnx = imvustylez_connect_db();
	      				//remove user
	      				$user_rec = get_record_select("users","avatarid=$avatarid");
	      				if($user_rec){
						purge_user_from_row($user_rec);
						//log action
						addtolog($logged->username, "removes user: $user_rec->username");
						//show success
						array_push($ret,1,"User has been removed succesfully!");
					} else array_push($ret,0,"User was not found");
	      				close_dbcnx($dbcnx);
				}
			}
		break;

		case "blockuser":
			if(!$islogged or !is_admin($logged->username)) array_push($ret,0,"Action needs authentication");
			else {
				$avatarId = (isset($_POST["id"]) and is_numeric($_POST["id"])) ? $_POST["id"] : "";
				$doblock = (isset($_POST["doblock"]) and is_numeric($_POST["doblock"])) ? $_POST["doblock"] : "";

				if($avatarId=="" or $doblock=="") array_push($ret,0,"Invalid values sent");
				else {
	      				$dbcnx = imvustylez_connect_db();
					//fetch record
					$rec = get_record_select("users","avatarid=$avatarId");
					if($rec){
						//update status on db
						//binarize visibility value
						if($doblock>0) $doblock=1; else $doblock=0;
						block_user_from_row($rec,$doblock);
						//log action
						addtolog($logged->username, "removes user: $user_rec->username");
						array_push($ret,1,"Changes saved successfully!");
					} else array_push($ret,0,"User couldn't be retrieved");
	      				close_dbcnx($dbcnx);
				}
			}
		break;
*/
		default:
			array_push($ret,0,"Operation not defined"); //send out error
		break;
	}
}

header("Content-type: application/json");
echo json_encode($ret);
?>