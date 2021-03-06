<?
$leavebodyopen=1;
require_once("config.php");

$user_obj=do_auth_user($logged->name,$logged->pw);

if(!empty($_POST)){
	$fullname= isset($_POST["fullname"]) ? trim($_POST["fullname"]) : "";
	$password= isset($_POST["password"]) ? $_POST["password"] : "";
	$cpassword= isset($_POST["cpassword"]) ? $_POST["cpassword"] : "";
	$userlang= isset($_POST["userlang"]) ? $_POST["userlang"] : "";
	$errortxt="";

	if($user_obj->id!=1 and $fullname=="") $errortxt= get_text("Please fill the field: Full name",$lang);
	else if($password!=$cpassword) $errortxt= get_text("Password and Confirmation don't match",$lang);
	else if(!in_array($userlang,$config->valid_langs)) $errortxt= get_text("Language sent is not supported: ".$userlang,$lang);
	else {
		if($user_obj->id==1) $fullname=$user_obj->fullName;
		$response = set_user($logged->name,$logged->pw,$user_obj->id,$fullname,$logged->name,$password,$user_obj->roleId,$user_obj->active,$userlang);
		if(!$response) $errortxt = get_text("Could not save new settings",$lang);
		else {
			$errortxt = false;
			//update session and cookie values
			$EnDecryptText = new EnDecryptText();
			if($password!=""){
				$passw_enc = $EnDecryptText->Encrypt_Text($password);
				$_SESSION[$config->sesskey."pw"] = $passw_enc;
			} else $passw_enc = $logged->pw;
			$roleid_enc=$EnDecryptText->Encrypt_Text($user_obj->roleId);
			$_SESSION[$config->sesskey."lang"] = $userlang;
			$lang=$userlang;
			//update cookie
			setcookie($config->sesskeycookiename, $passw_enc ."|". $roleid_enc ."|".  $logged->name."|".md5($_SERVER["HTTP_USER_AGENT"])."|".$userlang, time() + $config->cookie_lifetime);
			//sets new full name to show on the form in case it has changed
			$user_obj->fullName=$fullname;
			$user_obj->language=$userlang;
		}
	}
}

include("header.php");
?>

<div id="page-wrapper">

<div class="row">
<div class="col-lg-12">
<h1 class="page-header"><?=get_text("Settings",$lang);?></h1>
</div>
</div>

<div class="row">
<div class="col-lg-12">
<?if($user_obj){
	if(isset($errortxt)){
		if($errortxt===false) echo "<div class='alert alert-success'><span class='fa fa-check'></span> ". get_text("Settings saved",$lang)."!</div>";
		else if($errortxt!="") echo "<div class='alert alert-danger'><span class='fa fa-times-circle'></span> $errortxt</div>";
	 }
?>
<form class="form-horizontal" id="user-new-form" method="post">
<div class="form-group">
 <label class="control-label col-sm-2"><?=get_text("Full Name",$lang);?>:</label>
 <div class="col-sm-10">
      <input type="text" class="form-control" name="fullname" value="<?=$user_obj->fullName?>" required maxlength="64"<?if($user_obj->id==1) echo " disabled"; ?>>
 </div>
</div>
<div class="form-group">
 <label class="control-label col-sm-2"><?=get_text("Password",$lang);?>:</label>
 <div class="col-sm-10">
      <input type="password" class="form-control" name="password" value="" placeholder="****">
 </div>
</div>
<div class="form-group">
 <label class="control-label col-sm-2"><?=get_text("Confirm Password",$lang);?>:</label>
 <div class="col-sm-10">
      <input type="password" class="form-control" name="cpassword" value="" placeholder="****">
 </div>
</div>
<div class="form-group">
 <label class="control-label col-sm-2"><?=get_text("Language",$lang);?>:</label>
 <div class="col-sm-10">
      <select class="form-control" name="userlang">
<?foreach($config->valid_langs as $langval){
	echo "<option value='$langval'";
	if($user_obj->language==$langval) echo " selected";
	echo ">".$config->valid_langs_names[$langval];
}
?>
	</select>
 </div>
</div>
<button class="btn btn-success" id="user-new-submit"><?=get_text("Save",$lang);?></button>
</form>
<?} else echo get_text("Could not get user information",$lang);?>

</div>
</div>
</div>

<? include("footer.php"); ?>
</body>
</html>