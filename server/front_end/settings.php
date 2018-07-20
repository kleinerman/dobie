<?
$leavebodyopen=1;
require_once("config.php");

$user_obj=do_auth_user($logged->name,$logged->pw);

if(!empty($_POST)){
	$fullname= isset($_POST["fullname"]) ? trim($_POST["fullname"]) : "";
	$password= isset($_POST["password"]) ? $_POST["password"] : "";
	$cpassword= isset($_POST["cpassword"]) ? $_POST["cpassword"] : "";
	$errortxt="";

	if($user_obj->id!=1 and $fullname=="") $errortxt= "Please fill the field: Full name";
	else if($password!=$cpassword) $errortxt= "Password and Confirmation don't match";
	else {
		if($user_obj->id==1) $fullname=$user_obj->fullName;
		$response = set_user($logged->name,$logged->pw,$user_obj->id,$fullname,$logged->name,$password,$user_obj->roleId,$user_obj->active);
		if(!$response) $errortxt = "Could not save new settings";
		else {
			$errortxt = false;
			//update session and cookie values
			$EnDecryptText = new EnDecryptText();
			$passw_enc = $EnDecryptText->Encrypt_Text($password);
			$_SESSION[$config->sesskey."pw"] = $passw_enc;
			$roleid_enc=$EnDecryptText->Encrypt_Text($user_obj->roleId);
			//update cookie
			setcookie($config->sesskeycookiename, $passw_enc ."|". $roleid_enc ."|".  $logged->name."|".md5($_SERVER["HTTP_USER_AGENT"]), time() + $config->cookie_lifetime);
			//sets new full name to show on the form in case it has changed
			$user_obj->fullName=$fullname;
		}
	}
}

include("header.php");
?>

<div id="page-wrapper">

<div class="row">
<div class="col-lg-12">
<h1 class="page-header">Settings</h1>
</div>
</div>

<div class="row">
<div class="col-lg-12">
<?if($user_obj){
	if(isset($errortxt)){
		if($errortxt===false) echo "<div class='alert alert-success'><span class='fa fa-check'></span> Settings saved!</div>";
		else if($errortxt!="") echo "<div class='alert alert-danger'><span class='fa fa-times-circle'></span> $errortxt</div>";
	 }
?>
<form class="form-horizontal" id="user-new-form" method="post">
<div class="form-group">
 <label class="control-label col-sm-2">Full Name:</label>
 <div class="col-sm-10">
      <input type="text" class="form-control" name="fullname" value="<?=$user_obj->fullName?>" required maxlength="64"<?if($user_obj->id==1) echo " disabled"; ?>>
 </div>
</div>
<div class="form-group">
 <label class="control-label col-sm-2">Password:</label>
 <div class="col-sm-10">
      <input type="password" class="form-control" name="password" value="" placeholder="****">
 </div>
</div>
<div class="form-group">
 <label class="control-label col-sm-2">Confirm Password:</label>
 <div class="col-sm-10">
      <input type="password" class="form-control" name="cpassword" value="" placeholder="****">
 </div>
</div>
<button class="btn btn-success" id="user-new-submit">Save</button>
</form>
<?} else echo "Could not get user information";?>

</div>
</div>
</div>

<? include("footer.php"); ?>
</body>
</html>