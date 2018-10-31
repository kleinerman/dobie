<?
$innerheader=1;
$requirelogin=0;

require_once("config.php");
//if already logged > redirect
if($islogged) header("Location: $home_url");

$error_catch = array();

if(isset($_POST['username'])){

	//get posted values
	$username= trim($_POST['username']);
	$password= trim($_POST['password']);

	if($user_obj=do_auth_user($username,$password)){
		if($user_obj->active==1){
			//register _SESSION
			$_SESSION[$config->sesskey] = $username;
			require_once("lib/EnDecryptText.php");
			$EnDecryptText = new EnDecryptText();
			$passw_enc = $EnDecryptText->Encrypt_Text($password);
			$_SESSION[$config->sesskey."pw"] = $passw_enc;
			$roleid_enc=$EnDecryptText->Encrypt_Text($user_obj->roleId);
			$_SESSION[$config->sesskey."rl"] = $roleid_enc;
			$_SESSION[$config->sesskey."lang"] = $user_obj->language;
			//create cookie
			setcookie($config->sesskeycookiename, $passw_enc ."|". $roleid_enc ."|".  $username."|".md5($_SERVER["HTTP_USER_AGENT"]) . "|" . $user_obj->language, time() + $config->cookie_lifetime);
			//redirect to main page
			header("Location: $home_url");
			die();
		} else $error_catch['username'] = get_text("This user is disabled. Contact the administrator",$lang);
	} else {
		$error_catch['username'] = get_text("Invalid login",$lang);
	}
}

include("header.php");
?>
<div id="contextbody_wide" class="center">
<div class="container">
<div class="row">
<div class="col-md-4 col-md-offset-4">
<div class="login-panel panel panel-default">
<div class="panel-heading"><img src="img/logo.png" alt="<?=$config->sitetitle?>" title="<?=$config->sitetitle?>"> <br> <?=$config->sitedesc?></div>
<div class="panel-body">
<?if(isset($error_catch['username'])) print_note($error_catch['username']); ?>
<form method="post">
<fieldset>
<div class="form-group">
<input type='text' name='username' class='form-control' maxlength="64" placeholder='<?=get_text("User Name",$lang)?>' autofocus value='<? if(isset($_POST['username'])) echo $_POST['username']?>' required>
</div>
<div class="form-group">
<input id="password" type='password' name='password' class='form-control' placeholder="<?=get_text("Password",$lang)?>" value="" maxlength="64" required>
</div>
<button class="btn btn-lg btn-success btn-block" type="submit"><?=get_text("Sign In",$lang)?></button>
</fieldset>
</form>
</div>
</div>
</div>
</div>
</div>
<br><br><br>
<div id="copyright-container" class="hidden-xs hidden-sm"></div>
</div>
<? include("footer.php");?>