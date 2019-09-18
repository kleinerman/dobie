<?
require_once("config.php");

//if login required
if(isset($requirelogin) and $requirelogin and !$islogged) {
	redirect_to("logout",1);
}

//if section role is required
if($islogged and isset($requirerole) and $requirerole<$logged->roleid){
	redirect_to($home_url,1);
}

header("Content-type:text/html; charset=utf-8");
ob_start('ob_gzhandler');
?>
<!DOCTYPE html>
<html lang="en-us">
<head>
<meta charset="utf-8">
<meta http-equiv="X-UA-Compatible" content="IE=edge">
<title><?=$config->sitetitle?></title>
<meta name="keywords" content="dobie, access, doors">
<meta name="description" content="<?=$config->sitedesc?>">
<meta name="author" content="Dobie">
<meta name="robots" content="all">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta property="og:title" content="<?=$config->sitetitle?>">
<meta property="og:description" content="<?=$config->sitedesc?>">
<meta property="og:type" content="website">
<meta property="og:url" content="<?=$config->wwwroot?>">
<meta property="og:image" content="<?=$config->wwwroot?>img/logo.png">
<meta property="og:site_name" content="<?=$config->sitedesc?>">

<link rel="apple-touch-icon" sizes="180x180" href="<?=$config->wwwroot?>apple-touch-icon.png">
<link rel="icon" type="image/png" sizes="32x32" href="<?=$config->wwwroot?>favicon-32x32.png">
<link rel="icon" type="image/png" sizes="16x16" href="<?=$config->wwwroot?>favicon-16x16.png">
<link rel="manifest" href="<?=$config->wwwroot?>site.webmanifest">
<link rel="mask-icon" href="<?=$config->wwwroot?>safari-pinned-tab.svg" color="#000000">
<meta name="msapplication-TileColor" content="#ffffff">
<meta name="theme-color" content="#ffffff">

<link href="dist/css/bootstrap.min.css" type="text/css" rel="stylesheet" property='stylesheet'>
<link href="dist/fontawesome/css/all.min.css" type="text/css" rel="stylesheet" property='stylesheet'>
<?if(!isset($innerheader)){?>
<!-- MetisMenu CSS -->
<link href="bower_components/metisMenu/dist/metisMenu.min.css" rel="stylesheet" type='text/css'>
<?}?>
<!-- Custom CSS -->
<link href="dist/css/sb-admin-2.css" rel="stylesheet" type='text/css'>
<?if(in_array("graphics",$include_extra_js)){?>
<!-- Morris Charts CSS -->
<link href="bower_components/morrisjs/morris.css" rel="stylesheet" type='text/css'>
<?}?>
<?if(in_array("jqueryui",$include_extra_js) or in_array("datepicker",$include_extra_js)){?>
<!-- jqueryUI CSS -->
<link href="dist/css/jquery-ui.css" type="text/css" rel="stylesheet" property='stylesheet'>
<?}?>
<?if(in_array("clockpicker",$include_extra_js)){?>
<!-- Clockpicker CSS -->
<link href="dist/css/bootstrap-clockpicker.min.css" type="text/css" rel="stylesheet" property='stylesheet'>
<?}?>
<!-- More Custom CSS -->
<link href='dist/css/custom.css?v=9' rel='stylesheet' type='text/css'>
</head>
<body>
<?if(!isset($innerheader)){?>
<div id="wrapper">
<?if($islogged){?>
<!-- Navigation -->
<nav class="navbar navbar-default navbar-static-top">
<div class="navbar-header">
<button type="button" class="navbar-toggle" data-toggle="collapse" data-target=".navbar-collapse">
<span class="sr-only"><?=get_text("Toggle navigation",$lang);?></span>
<span class="icon-bar"></span>
<span class="icon-bar"></span>
<span class="icon-bar"></span>
</button>
<a class="navbar-brand" href="<?=$home_url?>"></a>
</div>
<!-- /.navbar-header -->
<ul class="nav navbar-top-links navbar-right">
<li class="dropdown">
<span id="plan_length"><?=get_text("Hello",$lang);?>, <span class='bold'><?=$logged->name?>!</span></span>
</li>
<!-- /.dropdown -->
<li class="dropdown">
<a class="dropdown-toggle" data-toggle="dropdown" href="#">
<span class="fa fa-user fa-fw"></span> <span class="fa fa-caret-down"></span>
</a>
<ul class="dropdown-menu dropdown-user">
<li><a href="settings"><span class="fa fa-cog fa-fw"></span> <?=get_text("Settings",$lang);?></a></li>
<li><a href="help"><span class="fa fa-life-ring fa-fw"></span> <?=get_text("Help",$lang);?></a></li>
<li class="divider"></li>
<li><a href="logout"><span class="fa fa-sign-out-alt fa-fw"></span> <?=get_text("Log out",$lang);?></a>
</li>
</ul>
<!-- /.dropdown-user -->
</li>
<!-- /.dropdown -->
</ul>
<!-- /.navbar-top-links -->

<div class="navbar-default sidebar" role="navigation">
<div class="sidebar-nav navbar-collapse">
<ul class="nav" id="side-menu">
<li>
<a href="dashboard"><span class="fa fa-list-ol fa-fw"></span> <?=get_text("Events",$lang);?><span class="fa arrow"></span></a>
<ul class="nav nav-second-level">
<li>
<a href="events-live"><span class="fa fa-bolt fa-fw"></span> <?=get_text("Live",$lang);?></a>
</li>
<?if($logged->roleid<3){?>
<li>
<a href="events-search"><span class="fa fa-search fa-fw"></span> <?=get_text("Search",$lang);?></a>
</li>
<li>
<a href="events-purge"><span class="fa fa-trash fa-fw"></span><?=get_text("Purge",$lang);?></a>
</li>
<?}?>
</ul>
</li>
<li>
<a href="visitors"><span class="fa fa-male fa-fw"></span> <?=get_text("Visitors",$lang);?></a>
</li>
<?if($logged->roleid<3){?>
<li>
<a href="organizations"><span class="fa fa-sitemap fa-fw"></span> <?=get_text("Organizations",$lang);?></a>
</li>
<?}?>
<li>
<a href="#"><span class="fa fa-users fa-fw"></span> <?=get_text("Persons",$lang);?><span class="fa arrow"></span></a>
<ul class="nav nav-second-level">
<?if($logged->roleid<3){?>
<li>
<a href="persons"><span class="fa fa-users fa-fw"></span> <?=get_text("Manage Persons",$lang);?></a>
</li>
<?}?>
<li>
<a href="persons-search"><span class="fa fa-search fa-fw"></span> <?=get_text("Search Persons",$lang);?></a>
</li>
</ul>
</li>
<?if($logged->roleid<3){
	if($logged->roleid==1){
?>
<li>
<a href="controllers"><span class="fa fa-gamepad fa-fw"></span> <?=get_text("Controllers",$lang);?></a>
</li>
<li>
<a href="zones"><span class="far fa-object-ungroup fa-fw"></span> <?=get_text("Zones",$lang);?></a>
</li>
<li>
<a href="#"><span class="fa fa-building fa-fw"></span> <?=get_text("Doors",$lang);?><span class="fa arrow"></span></a>
<ul class="nav nav-second-level">
<li>
<a href="doors"><?=get_text("Manage Doors",$lang);?></a>
</li>
<li>
<a href="door-groups"><?=get_text("Door Groups",$lang);?></a>
</li>
</ul>
<?	}?>
<li>
<a href="access"><span class="fa fa-handshake fa-fw"></span> <?=get_text("Accesses",$lang);?><span class="fa arrow"></span></a>
<ul class="nav nav-second-level">
<li>
<a href="accesses-person"><?=get_text("Person",$lang);?> <span class="fa fa-arrow-right"></span> <?=get_text("Door",$lang);?></a>
</li>
<li>
<a href="accesses-door"><?=get_text("Door",$lang);?> <span class="fa fa-arrow-right"></span> <?=get_text("Person",$lang);?></a>
</li>
</ul>
</li>
<?	if($logged->roleid==1){?>
<li>
<a href="system-users"><span class="fa fa-lock fa-fw"></span> <?=get_text("System Users",$lang);?></a>
</li>
<?	}?>
<?}?>
</ul>
<div id="event-photo-container"><img src="persons-image" class="hidden"></div>
</div>
<!-- /.sidebar-collapse -->
</div>
<!-- /.navbar-static-side -->
</nav>
<?}}?>