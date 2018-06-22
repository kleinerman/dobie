<?
require_once("config.php");

if(isset($requirelogin) and $requirelogin and !$islogged) {
	redirect_to("logout",1);
	//echo "not logged";
	//die();
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
<meta name="viewport" content="width=device-width, initial-scale=1">
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
<meta name="theme-color" content="#ffffff">

<link rel="apple-touch-icon" sizes="180x180" href="<?=$config->wwwroot?>apple-touch-icon.png">
<link rel="icon" type="image/png" sizes="32x32" href="<?=$config->wwwroot?>favicon-32x32.png">
<link rel="icon" type="image/png" sizes="16x16" href="<?=$config->wwwroot?>favicon-16x16.png">
<link rel="manifest" href="<?=$config->wwwroot?>manifest.json">
<link rel="mask-icon" href="<?=$config->wwwroot?>safari-pinned-tab.svg" color="#5bbad5">

<link href="dist/css/bootstrap.min.css" type="text/css" rel="stylesheet" property='stylesheet'>
<link href="dist/css/font-awesome.min.css" type="text/css" rel="stylesheet" property='stylesheet'>
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
<link href='dist/css/custom.css' rel='stylesheet' type='text/css'>
</head>
<body>
<?if(!isset($innerheader)){?>
<div id="wrapper">
<?if($islogged){?>
<!-- Navigation -->
<nav class="navbar navbar-default navbar-static-top">
<div class="navbar-header">
<button type="button" class="navbar-toggle" data-toggle="collapse" data-target=".navbar-collapse">
<span class="sr-only"><?print_text($lang,"Toggle navigation","Cambiar navegación");?></span>
<span class="icon-bar"></span>
<span class="icon-bar"></span>
<span class="icon-bar"></span>
</button>
<a class="navbar-brand" href="events-live"> <?=$config->sitedesc?></a>
</div>
<!-- /.navbar-header -->
<ul class="nav navbar-top-links navbar-right">
<li class="dropdown">
<span id="plan_length"><?print_text($lang,"Hello","Hola");?>, <span class='bold'><?=$logged->name?>!</span></span>
</li>
<!-- /.dropdown -->
<li class="dropdown">
<a class="dropdown-toggle" data-toggle="dropdown" href="#">
<i class="fa fa-user fa-fw"></i> <i class="fa fa-caret-down"></i>
</a>
<ul class="dropdown-menu dropdown-user">
<li><a href="settings"><i class="fa fa-gear fa-fw"></i> <?print_text($lang,"Settings","Configuración");?></a></li>
<li><a href="help"><i class="fa fa-life-saver fa-fw"></i> <?print_text($lang,"Help","Ayuda");?></a></li>
<li class="divider"></li>
<li><a href="logout"><i class="fa fa-sign-out fa-fw"></i> <?print_text($lang,"Log out","Salir");?></a>
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
<a href="dashboard"><i class="fa fa-list-ul fa-fw"></i> <?print_text($lang,"Events","Events");?><span class="fa arrow"></span></a>
<ul class="nav nav-second-level">
<li>
<a href="events-live"><?print_text($lang,"Live","En vivo");?></a>
</li>
<li>
<a href="events-search"><?print_text($lang,"Search","Búsqueda");?></a>
</li>
</ul>
</li>
<li>
<a href="#"><i class="fa fa-male fa-fw"></i> <?print_text($lang,"Visitors","Visitas");?><span class="fa arrow"></span></a>
<ul class="nav nav-second-level">
<li>
<a href="visit-door-groups"><?print_text($lang,"Visit Door Groups","Grupos de Puertas de Visitas");?></a>
</li>
<li>
<a href="visitors"><?print_text($lang,"Manage Visitors","Administrar Visitas");?></a>
</li>
</ul>
</li>
<li>
<a href="organizations"><i class="fa fa-sitemap fa-fw"></i> <?print_text($lang,"Organizations","Organizaciones");?></a>
</li>
<li>
<a href="persons"><i class="fa fa-users fa-fw"></i> <?print_text($lang,"Persons","Personas");?></a>
</li>
<li>
<a href="controllers"><i class="fa fa-gamepad fa-fw"></i> <?print_text($lang,"Controllers","Controladores");?></a>
</li>
<li>
<a href="zones"><i class="fa fa-object-ungroup fa-fw"></i> <?print_text($lang,"Zones","Zonas");?></a>
</li>
<li>
<a href="doors"><i class="fa fa-building-o fa-fw"></i> <?print_text($lang,"Doors","Puertas");?></a>
</li>
<li>
<a href="access"><i class="fa fa-handshake-o fa-fw"></i> <?print_text($lang,"Accesses","Accesos");?><span class="fa arrow"></span></a>
<ul class="nav nav-second-level">
<li>
<a href="accesses-person"><?print_text($lang,"Person","Persona");?> <span class="fa fa-long-arrow-right"></span> <?print_text($lang,"Door","Puerta");?></a>
</li>
<li>
<a href="accesses-door"><?print_text($lang,"Door","Puerta");?> <span class="fa fa-long-arrow-right"></span> <?print_text($lang,"Person","Persona");?></a>
</li>
</ul>
</li>
<?if($logged->name=="admin"){?>
<li>
<a href="system-users"><i class="fa fa-lock fa-fw"></i> <?print_text($lang,"System Users","Usuarios de sistema");?></a>
</li>
<?}?>
</ul>
</div>



<!-- /.sidebar-collapse -->
</div>
<!-- /.navbar-static-side -->
</nav>
<?}}?>