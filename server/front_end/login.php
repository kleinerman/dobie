<?
$innerheader=1;
$requirelogin=0;
$home_url="organizations";

require_once("config.php");
//if already logged > redirect
if($islogged) header("Location: $home_url");

$error_catch = array();

if(isset($_POST['username'])){

	//get posted values
	$username= trim($_POST['username']);
	$password= trim($_POST['password']);

	if(do_auth($username,$password)){
		//register _SESSION
		$_SESSION[$config->sesskey] =  $username;
		require_once("lib/EnDecryptText.php");
		$EnDecryptText = new EnDecryptText();
		$passw_enc = $EnDecryptText->Encrypt_Text($password);
		$_SESSION[$config->sesskey."pw"] = $passw_enc;
		//create cookie
		setcookie($config->sesskeycookiename, $passw_enc ."|". $username."|".md5($_SERVER["HTTP_USER_AGENT"]), time() + $config->cookie_lifetime);
		//redirect to main page
		//header("Location: events-live");
		header("Location: $home_url");
//		echo "login success!";
//		die();
	} else {
		$error_catch['username'] = "Invalid login";
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
<input type='text' name='username' class='form-control' maxlength="64" placeholder='User Name' autofocus value='<? if(isset($_POST['username'])) echo $_POST['username']?>' required>
</div>
<div class="form-group">
<input id="password" type='password' name='password' class='form-control' placeholder="Password" value="" maxlength="64" required>
</div>
<button class="btn btn-lg btn-success btn-block" type="submit">Sign In</button>
</fieldset>
</form>
</div>
</div>
</div>
</div>
</div>
<br><br><br>
<div id="copyright-container" class="hidden-xs hidden-sm"><?=$config->sitetitle?> &copy; 2009-<?=date("Y")?> | All Rights Reserved.</div>
</div>
<? include("footer.php");?>