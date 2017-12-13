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


function build_icon_from_row($row){

	return "<a href='" . $row->link_url . "' target='_blank'><img src='" . str_replace("http://","https://",$row->icon_url) . "' alt=\"" .  str_replace('"','\"',$row->name) . "\" title=\"" .  str_replace('"','\"',$row->name) . "\"></a>";

}

function get_derivable_icon_from_row($row,$derivelistmode=0,$hideonclick=1){

	global $lang;
	$dev_name= truncate_name($row->dev_name,13);
	$dev_id= $row->dev_id;
	$product_name= truncate_name($row->product_name,16);
	$pid= $row->pid;
	$prod_id = $row->prod_id;
	$icon_url= str_replace("http://","https://",$row->icon_url);
	$price= $row->price;

	$r="
<table class=\"prodicontable\" id=\"derivable_$prod_id\">
<tr><td class=\"center\" colspan=\"2\">";
	if(isset($row->derivable_id) and $row->derivable_id==0) $r.="<a href=\"http://www.imvu.com/shop/product.php?products_id=$pid\" target=\"_blank\">";
	else $r.="<a href=\"https://gaf210.imvustylez.net/adplan/goderiv-bid-$row->derivable_id\" target=\"_blank\">";
	$r.="<img src=\"$icon_url\" alt=\"Product\" title=\"$row->product_name\"></a>
</td></tr>
<tr><td valign=\"top\" class=\"left\" colspan=\"2\">
<div class=\"prodname\">&nbsp;$product_name</div>
<div class=\"proddev\">&nbsp;by ";
	if(isset($row->derivable_id) and $row->derivable_id==0) $r.="<a href=\"http://www.imvu.com/shop/web_search.php?manufacturers_id=$dev_id\" target=\"_blank\">";
	else $r.="<a href=\"https://gaf210.imvustylez.net/adplan/godev-bid-". $row->devid ."\" target=\"_blank\">";
	$r.="$dev_name</a></div>
</td></tr>
<tr><td valign=\"top\" class=\"left\">
<span class=\"pricebox\">$price <img src=\"img/credit.png\" alt='cr'></span>
</td><td class=\"right\">";

	if(!$derivelistmode) $r.="
<a href=\"javascript:void(0)\" onclick=\"addToDeriveList('$prod_id',$hideonclick)\"><img src=\"img/plus.png\" alt=\"+\" title=\"".get_text($lang,"Add to Derive List","Agregar a Lista para Derivar")."\"></a>";
	else $r.="
<a href=\"javascript:void(0)\" onclick=\"if(confirm('".get_text($lang,"Are you sure you want to remove this product?","Está seguro que quiere remover este producto?")."')) removeFromDeriveList('$prod_id',$hideonclick);\"><img src=\"img/cross.png\" alt=\"X\" title=\"".get_text($lang,"Remove from Derive List","Remover de Lista para Derivar")."\"></a>";

	if(isset($row->derivable_id) and $row->derivable_id==0) $r.="<a href=\"imvu:DeriveProduct?product_id=$pid\">";
	else $r.="<a href=\"https://gaf210.imvustylez.net/adplan/goderiv-bid-$row->derivable_id&a=deriv\">";

	$r.="<img src=\"img/creator.png\" alt=\"D\" title=\"".get_text($lang,"Derive this product","Derivar este producto")."\"></a>
</td></tr></table>";

	return $r;
}

function get_devid_from_devname($dev_name){
	$result = get_record_sql("SELECT dev_id FROM authorized_devs WHERE dev_name='$dev_name'"); 
	return $result->dev_id;
}

function get_expiry_from_devname($input,$in_human=0,$alertmode=0,$date_input=0){
	if($date_input) $paid_until = $input; //date input mode
	else { //from devname mode
		//get field from user row
		$result = get_record_sql("SELECT paid_until FROM authorized_devs WHERE dev_name='$input'"); 
		$row = $result;
		$paid_until = $row->paid_until;
	}
	if($in_human){
		//translate the date in db format to human: day-monthnameshort-year
		$parts = explode("-",$paid_until);
		//get db date in timestamp
		$ts=mktime(0,0,0,$parts[1],$parts[2],$parts[0]);
		if($alertmode){
			//if alertmode is on, return html string colored depending on days left to expiry date
			$nowts=time();
			//define how many days back for each color
			$yellowalert_days=10;
			$redalert_days=5;
			if($nowts>($ts-(60*60*24*$redalert_days))){
				//red
				$ret = "<span style='color:#DD0000;text-decoration:blink'>".date("d-M-Y",$ts)."</span>";
			}elseif($nowts>($ts-(60*60*24*$yellowalert_days))){
				//yellow
				$ret = "<span style='color:#FFD700'>".date("d-M-Y",$ts)."</span>";
			} else $ret = date("d-M-Y",$ts);
		} else $ret = date("d-M-Y",$ts);
	} else {
		$ret =$paid_until;
	}
	return $ret;
}

function get_qprods($dev_name){
	$result = get_records_sql("SELECT dev_id FROM product_data WHERE dev_id='" . get_devid_from_devname($dev_name). "'"); 
	return count($result);
}

function get_qprods_from_id($dev_id){
	$result = get_records_sql("SELECT id FROM product_data WHERE dev_id='$dev_id'"); 
	return count($result);
}

function get_derivables_from_id($dev_id){
	$result = get_records_sql("SELECT id FROM product_data_derivables WHERE dev_id='$dev_id'"); 
	return count($result);
}

function get_qnews($dev_id){
	$result = get_records_sql("SELECT id FROM authorized_devs WHERE dev_id='$dev_id' and shout_text!=''"); 
	return count($result);
}

function get_qbanners($dev_id){
	$result = get_records_sql("SELECT id FROM adplan_banners WHERE dev_id='$dev_id'"); 
	return count($result);
}

function has_registered_email($username){
	$query = get_record_sql("SELECT id FROM authorized_devs WHERE dev_name='$username' AND email!=''");
	return (count($query) > 0);
}

function has_requested_badge($username){
	$query = get_record_sql("SELECT id FROM authorized_devs WHERE dev_name='$username' AND hasbadge=1");
	return (count($query) > 0);
}

function get_mailinglist(){

	$result = get_records_sql("SELECT DISTINCT email FROM authorized_devs WHERE email!='' and disabled=0");
	$emails="";
	if($result){
		foreach($result as $rows){
			if(!empty($emails)) $emails .= ", ";
			$emails .= $rows->email;
		}
	}
	return $emails;
}

function is_derived_from_imvuinc($pid,$dev_id){

	require_once("/home/imvustyl/public_html/gaf210/default-productpage-funcs.php");

	//first check if pid is already on imvuinc products table
	$query = get_record_sql("SELECT id FROM product_data_roots WHERE pid='$pid'");

	$ret = 0;

	if($query) $ret = 1; //product is already on the list
	else {
		//now fetch the product info and see if its derived from imvu inc
		$product_data = parse_data_from_url("http://www.imvu.com/shop/product.php?products_id=".$pid);
		//check if dev_id is 39 for imvu inc.
		if($product_data['devid']=="39"){
			//product is derived from imvu inc but not on the list > add it
			$ret = 1;
			exec_query("INSERT INTO product_data_roots(pid,name) values ('$pid','".addslashes($product_data['name'])."')") or die(get_query_error());
			//HERE starts the checkup on the parent product
		} elseif($product_data['derivedfrom'] and $product_data['devid']==$dev_id){
			//now check if the parent product is derived from imvu inc
			$query2 = get_record_sql("SELECT id FROM product_data_roots WHERE pid='".$product_data['derivedfrom']."'");

			if($query2) $ret = 1; //product is already on the list
			else{
				//now fetch the parent product info and see if its an own product AND its derived from imvu inc
				$product_data2 = parse_data_from_url("http://www.imvu.com/shop/product.php?products_id=".$product_data['derivedfrom']);
				//check if dev_id is 39 for imvu inc. or simpledevs id
				if($product_data2['devid']=="39" or $product_data2['devid']=="48624480"){
					//product is derived from imvu inc but not on the list > add it
					$ret = 1;
					if($product_data2['devid']=="39") exec_query("INSERT INTO product_data_roots(pid,name) values ('".$product_data['derivedfrom']."','".addslashes($product_data2['name'])."')");
				} else $ret = 0;
			}
			//HERE ends the checkup on the parent product
		} else $ret = 0;
	}
	return $ret;
}

function has_voted_current_survey($dev_id){
	$result = get_record_sql("SELECT id FROM survey_votes WHERE dev_id=$dev_id"); 
	return (count($result)>0);
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