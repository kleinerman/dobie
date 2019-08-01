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

function print_note($string, $stringspa="", $lang="eng", $color="red", $stringger="", $stringpor="", $stringfrench=""){
	echo "<p style='font-weight:bold;color:" . $color . ";'>";
	print_text($lang, $string, $stringspa, $stringger, $stringpor, $stringfrench);
	echo "</p>";
}

function redirect_to($url,$forceparent=0){
	if($forceparent){
		echo "<script>
if(parent.location != window.location) parent.location.href = '$url';
else window.location.href='$url';
</script>";
	} else echo "<script>window.location.href='$url';</script>";
}


//restore login from cookie if existent and if session has expired
function persistsession(){
	global $config;

	$has_session = isset($_SESSION[$config->sesskey]);
	$has_cookie = (isset($_COOKIE[$config->sesskeycookiename]) and $_COOKIE[$config->sesskeycookiename]!= '');
	if(!$has_session and $has_cookie){
		//perform login from cookie
		$cookieparts=explode("|",$_COOKIE[$config->sesskeycookiename]);
		//cookie should contain encrypt(password)|encrypt(roleid)|username|md5(http_user_agent)|lang
		if(count($cookieparts)==5){
			$lang= trim($cookieparts[4]);
			$remoteuseragent= trim($cookieparts[3]);
			$username= trim($cookieparts[2]);
			$roleid_enc= trim($cookieparts[1]);
			$password= trim($cookieparts[0]);
			require_once("EnDecryptText.php");
			$EnDecryptText = new EnDecryptText();
			require_once("api-functions.php");
			//only if cookie has correct data, do login. otherwise, unlog user.
			if(do_auth($username,$EnDecryptText->Decrypt_Text($password)) and $remoteuseragent==md5($_SERVER["HTTP_USER_AGENT"])){
		      		//restore session
		      		$_SESSION[$config->sesskey] = $username;
		      		$_SESSION[$config->sesskey."pw"] = $password;
		      		$_SESSION[$config->sesskey."rl"] = $roleid_enc;
		      		$_SESSION[$config->sesskey."lang"] = $lang;
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

?>