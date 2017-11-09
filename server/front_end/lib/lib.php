<?
function print_text($lang, $texteng, $textesp, $textger="",$textpor="",$textfrench="",$do_get=0){
	switch($lang){
		case "spa": $ret = $textesp; break;
		case "ger": $ret = $textger; break;
		case "por": $ret = $textpor; break;
		case "fre": $ret = $textfrench; break;
		default: $ret = $texteng; break;
	}

	$valret = ($ret!="") ? $ret : $texteng;

	if($do_get) return $valret;
	else echo $valret;
}

/* string version of print_text */
function get_text($lang, $texteng, $textesp, $textger="",$textpor="",$textfrench=""){
	return print_text($lang, $texteng, $textesp, $textger,$textpor,$textfrench,1);
}

function print_note($string, $stringspa="", $lang="eng", $color="red", $stringger="", $stringpor="", $stringfrench=""){
	echo "<p style='font-weight:bold;color:" . $color . ";'>";
	print_text($lang, $string, $stringspa, $stringger, $stringpor, $stringfrench);
	echo "</p>";
}

function redirect_to($url,$forceparent=0){
	if($forceparent){
		echo "<script type='text/javascript'>
if(parent.location != window.location) parent.location.href = '$url';
else window.location.href='$url';
</script>";
	} else echo "<script type='text/javascript'>window.location.href='$url';</script>";
}


//restore login from cookie if existent and if session has expired
function persistsession(){
	global $config;

	$has_session = isset($_SESSION[$config->sesskey]);
	$has_cookie = (isset($_COOKIE[$config->sesskeycookiename]) and $_COOKIE[$config->sesskeycookiename]!= '');
	if(!$has_session and $has_cookie){
		//perform login from cookie
		$cookieparts=explode("|",$_COOKIE[$config->sesskeycookiename]);
		//cookie should contain md5(md5(password))|username|md5(http_user_agent)
		if(count($cookieparts)==3){
			$remoteuseragent= trim($cookieparts[2]);
			$username= trim($cookieparts[1]);
			$password= trim($cookieparts[0]);
			require_once("EnDecryptText.php");
			$EnDecryptText = new EnDecryptText();
			require_once("api-functions.php");
			//only is cookie has correct data, do login. otherwise, unlog user.
			if(do_auth($username,$EnDecryptText->Decrypt_Text($password)) and $remoteuseragent==md5($_SERVER["HTTP_USER_AGENT"])){
		      		//restore session
		      		$_SESSION[$config->sesskey] = $username;
		      		$_SESSION[$config->sesskey."pw"] = $password;
			} else {
				//destroy cookies
				setcookie($config->sesskeycookiename, "", time() - $config->cookie_lifetime);
				//destroy session
				session_unset();
				session_destroy();
			}
		}
	}
}

if(!function_exists("is_valid_ajax_ref")){
	function is_valid_ajax_ref($ref){
		global $config;
		return (substr_count($ref,$config->wwwroot)>0);
	}
}

//gets var_dump contents inside a string
function grab_dump($var)
{
    ob_start();
    var_dump($var);
    return ob_get_clean();
}

/*
function is_admin($name){
	$admins = array('gaf210');
	return in_array($name, $admins);
}

function sanitarize_txtinput($s){

	$invalids = array("<", "bitch", "puta","sucks", "puto", "fuck", "\"");

	foreach($invalids as $word) $s=str_replace($word, '', $s);

	return $s;
}

//gmt adjust for click date prints
function gmt_adjust($timestamp){
	$db_gmt_hours_offset=-10; //finland=+2 -- pst=-8 = difference is -10
	return $timestamp + (60*60*$db_gmt_hours_offset);
}

function print_alert($lang, $texteng, $textesp="", $textger="",$textpor="",$textfrench=""){
	switch($lang){
		case "spa": $ret = $textesp; break;
		case "ger": $ret = $textger; break;
		case "por": $ret = $textpor; break;
		case "fre": $ret = $textfrench; break;
		default: $ret = $texteng; break;
	}

	echo "<script type='text/javascript'>alert('";
	echo ($ret!="") ? addslashes($ret) : addslashes($texteng);
	echo "');</script>";
}

//FILE HANDLING FUNCTIONS
function is_valid_referal($url){
	global $wwwroot;
	return (substr_count($url,$wwwroot)>0);
}

function check_file_type($type){
	$valid_types = array('image/jpeg','image/png','image/pjpeg','image/jpg','image/x-png','image/gif');
	return in_array(strtolower($type), $valid_types);
}

function valid_ext($extension){
	$valid_types = array('jpg','jpeg','png','gif');
	return in_array(strtolower($extension), $valid_types);
}

function get_file_ext($filename){
	$extparts=explode('.',$filename);
	return strtolower(end($extparts));
}

function has_valid_dimensions($filename,$dimensions){

	global $BANNER_DIMENSIONS;

	return in_array($dimensions,$BANNER_DIMENSIONS);
}

function bytesToKB($bytes){
	return round($bytes/1024, 2);
}

function bytesToMB($bytes){
	return round($bytes/(pow(1024,2)), 2);
}

function bytesToReadable($bytes){
	switch($bytes) {
		case ($bytes<1024) : $r = $bytes . " B"; break;
		case (($bytes>=1024) AND ($bytes<(pow(1024,2)))) : $r = bytesToKB($bytes) . " KB"; break;
		case ($bytes>=(pow(1024,2)) AND $bytes<(pow(1024,3))) : $r = bytesToMB($bytes) . " MB"; break;
		default: $r = $bytes; break;
	}
	return $r;
}

// recurses into a directory and empties it
// call it like this: purgeDirectory("/dir/")
// remember the trailing slash!
function purgeDirectory($dir, $remove_this_dir=0){

	$handle = opendir($dir);

	while (false !== ($file = readdir($handle))){

		if ($file != "." && $file != ".."){

			if (is_dir($dir.$file)){
				purgeDirectory($dir.$file."/");
				rmdir($dir.$file);
			} else {
				unlink($dir.$file);
			}
		}
	}

	closedir($handle);
	if($remove_this_dir) rmdir($dir);
}

//LOG FUNCTIONS
function addtolog($username, $event){
	$event = real_escape_string($event);
	$username = real_escape_string($username);
	$query = exec_query("INSERT INTO adplan_log (username, event, date) VALUES('$username', '$event',UNIX_TIMESTAMP())");
}

//limit log to $limit records
function clear_log($limit=300){

    $result = get_records_sql("SELECT id FROM adplan_log");
    $q = count($result);
    if($q>$limit){
        $result = exec_query("DELETE FROM adplan_log order by id asc limit ". ($q-$limit));
     }
}

function print_logbox($autoclear=1){

	if($autoclear) clear_log();
	$result = get_records_sql("SELECT * FROM adplan_log ORDER BY date DESC LIMIT 300");
	if(count($result) >0){
		echo "System Log:<br><select id='loglist' size='5' class='form-control'>";
		foreach($result as $row){
			echo "<option>" . date("Y-m-d H:i:s",$row->date) . " : $row->username $row->event"; 
		}
		echo "</select>";
	}
}

function print_query_results($q,$qname){

	$error=0;
	$show =0;
	//validate query
	if($q!=''){
		if((substr_count(strtolower($q) , "insert") + substr_count(strtolower($q) , "update") + substr_count(strtolower($q) , "delete") + substr_count(strtolower($q) , "drop")) > 0 OR substr_count(strtolower($q) , "select")==0){
			$error = "Invalid query. Maybe trying to insert/update/delete/drop? :)";
		} else {
			//exec query
			$result = get_records_sql(stripslashes($q));
			$resource=get_query_resource(stripslashes($q));
			if(!$resource) $error = get_query_error();
			if(empty($error)) $show =1;
		}
	}

	if($error) print_note("Query error: " . $error);

	if($show){
		// get column metadata
		$i = 0;
		$q_fields = num_fields($resource);
		$q_rows = num_rows($resource);

		//get field names
		while ($i<$q_fields){
			$meta = fetch_field($resource);
			if ($meta){
				$field_names[$i] = $meta->name;
				$i++;
			}
		}

		if($q_rows<1){
			echo("<div class='emptyresult_box'>No results matching your query.</div>");
		} else {
			//print table header
			echo "<table id='search_table' class='table table-responsive center'><thead>";
			echo "<tr><th colspan='$q_fields'>".$qname." ($q_rows rows)</th></tr>";
			echo "<tr>";
			for($i=0; $i<count($field_names); $i++){
				echo "<th>" . $field_names[$i] . "</th>";
			}
			echo "</tr><tbody>";

			$row_index = 0;
			$row_limit = 100;

			foreach($result as $row){
				echo "<tr>";
				for($i=0; $i<count($field_names); $i++){
					echo "<td>" . truncate_name($row->$field_names[$i],100) . "</td>";
				}
				echo "</tr>";
				$row_index++;
				if($row_limit<$row_index) break;
			}
			echo "</tbody></table>";
			if($row_limit < $q_rows) echo "<div class='emptyresult_box'>The query result has more than $row_limit rows.</div><br><br>";
		}
	}
}
*/
?>