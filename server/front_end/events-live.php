<?
$leavebodyopen=1;
include("header.php");
?>
<div id="page-wrapper">

<div class="row">
<div class="col-lg-12">
<h1 class="page-header"><?=get_text("Events Live",$lang);?> <div class="blinking-dot blink-pulse"></div></h1>
</div>
</div>

<div class="row">
<div class="col-lg-12" id="controller-alerts-container">
</div>
</div>

<div class="row" id="filter-row" style="display:none">

<div class="col-lg-4">

<div class="select-container">
<div class="select-container-title"><?=get_text("Organizations",$lang);?></div>
<div class="select-container-body">
<input type="text" name="filter" placeholder="<?=get_text("Filter options",$lang);?>..." class="form-control data-filter" data-filter="organizations-select">
<select id="organizations-select" class="select-options select-options-small form-control" name="organizations-select" size="2"></select>
</div>
</div>

<br><br><br>

<div class="select-container" id="select-container-persons" style="display:none">
<div class="select-container-title"><?=get_text("Person",$lang);?></div>
<div class="select-container-body">
<input type="text" name="filter" placeholder="<?=get_text("Filter options",$lang);?>..." class="form-control data-filter" data-filter="persons-select">
<select id="persons-select" class="select-options select-options-small form-control" name="persons-select" size="2"></select>
</div>
</div>

</div>

<div class="col-lg-4">

<div class="select-container">
<form action="javascript:void(0)">
<div class="select-container-title"><?=get_text("Zone",$lang);?></div>
<div class="select-container-body">
<input type="text" name="filter" placeholder="<?=get_text("Filter options",$lang);?>..." class="form-control data-filter" data-filter="zones-select">
<select id="zones-select" class="select-options select-options-small form-control" name="zones-select" size="2"></select>
</div>
<div class="select-container-footer">
&nbsp;
</div>
</form>
</div>

<div class="select-container" id="select-container-doors" style="display:none">
<form action="javascript:void(0)">
<div class="select-container-title"><?=get_text("Doors",$lang);?></div>
<div class="select-container-body">
<input type="text" name="filter" placeholder="<?=get_text("Filter options",$lang);?>..." class="form-control data-filter" data-filter="doors-select">
<select id="doors-select" class="select-options select-options-small form-control" name="doors-select" size="2"></select>
</div>
</form>
</div>

</div>

<div class="col-lg-4 center">

<div class="select-container">
<form action="javascript:void(0)">
<div class="select-container-title"><?=get_text("Direction",$lang);?></div>
<div class="select-container-body left">
<br>
<label><input type="radio" name="side" value="" checked> <?=get_text("Both",$lang);?></label><br>
<label><input type="radio" name="side" value="1"> <?=get_text("Incoming",$lang);?></label><br>
<label><input type="radio" name="side" value="0"> <?=get_text("Outgoing",$lang);?></label>
</div>
</form>
</div>

<br><br><br>

<button id="events-search-reset-filter" class="btn btn-warning" type="button"><span class="fa fa-power-off"></span> <?=get_text("Reset filter",$lang);?></button>
<button id="events-search-reset" class="btn btn-danger" type="button"><span class="fa fa-times"></span> <?=get_text("Clear events",$lang);?></button>

</div>

</div>

<div class="row" id="search-again-row">
<div class="col-sm-12">

<div class="alert alert-warning clickable left" id="search-again-button">
<span class="fa fa-search"></span> <?=get_text("Filter",$lang);?>...
</div>

</div>

<div class="row">
<div class="col-lg-12">
<hr>

<div id="events-container" class="table-responsive gowide">

<table id="events-table" class="table table-bordered table-hover table-condensed table-striped left"><tr id="events-table-header-row">
<th class="center hidden-xs"><?=get_text("Type",$lang);?></th><th class="hidden-xs"><?=get_text("Zone",$lang);?></th><th><?=get_text("Door",$lang);?></th><th class="center hidden-xs"><?=get_text("Lock",$lang);?></th><th class="center hidden-xs"><?=get_text("Direction",$lang);?></th><th class="hidden-xs"><?=get_text("Date",$lang);?></th><th><?=get_text("Time",$lang);?></th><th class="hidden-xs"><?=get_text("Organization",$lang);?></th><th><?=get_text("Person",$lang);?></th><th class="center"><?=get_text("Allowed",$lang);?></th><th class="center hidden-xs"><?=get_text("Denial Cause",$lang);?></th></tr>
<tr id="noevents-row"><td colspan="11"><?=get_text("No events",$lang);?></td></tr>
</table>

</div>


<div id="legend-row">

<div class="row">
<div class="col-sm-3">
<h4><?=get_text("Event Type",$lang);?></h4>
<span class="fa fa-fw fa-address-card"></span> <?=get_text("Identified Access",$lang);?><br>
<span class="fa fa-fw fa-circle"></span> <?=get_text("Access with button",$lang);?><br>
<span class="fa fa-fw fa-unlink"></span> <?=get_text("Door remains opened",$lang);?><br>
<span class="fa fa-fw fa-bolt"></span> <?=get_text("Door was forced",$lang);?>
</div>
<div class="col-sm-3">
<h4><?=get_text("Lock",$lang);?></h4>
<span class="fa fa-fw fa-rss"></span> <?=get_text("Card Reader",$lang);?><br>
<span class="fa fa-fw fa-thumbs-up"></span> <?=get_text("Fingerprint Reader",$lang);?><br>
<span class="fa fa-fw fa-circle"></span> <?=get_text("Button",$lang);?>
</div>
<div class="col-sm-3">
<h4><?=get_text("Denial Cause",$lang);?></h4>
<span class="fa fa-fw fa-ban"></span> <?=get_text("No Access",$lang);?><br>
<span class="far fa-fw fa-calendar-times"></span> <?=get_text("Expired Card",$lang);?><br>
<span class="far fa-fw fa-clock"></span> <?=get_text("Out of time",$lang);?>
</div>
<div class="col-sm-3">
<h4><?=get_text("Direction",$lang);?></h4>
<span class="fa fa-fw fa-sign-in-alt"></span> <?=get_text("Incoming",$lang);?><br>
<span class="fa fa-fw fa-sign-out-alt"></span> <?=get_text("Outgoing",$lang);?><br>
</div>

</div>

</div>


</div>
</div>

</div>

<style>
/*n+7 hides over the 22nth child, in this case, shows 20 rows*/
#events-table tr:nth-child(n+22){display:none}
#events-table tr{
	transition: ease 0.8s all;
}
#events-table tr.newevent{
	background:#0f0;
}

#noevents-row{
	text-align:center;
}

#controller-alerts-container{
	overflow:auto;
	max-height:270px;
	margin-bottom:10px;
}

.controller-alert .alert{
	margin:5px auto;
}

.blinking-dot{
	background:#a00;width:10px;height:10px;border-radius:5px;display:inline-block;margin-bottom:5px
}

.blink-pulse {
    animation: blinker 0.8s cubic-bezier(.5, 0, 1, 1) infinite alternate;  
}

@keyframes blinker {
  from { opacity: 1; }
  to { opacity: 0; }
}

</style>

<? include("footer.php");?>

<script type="text/javascript">
//init filters
setFilterAction();

var organizationId="";
var zoneId="";
var filterPersonId="";
var filterDoorId="";
var filterSide="";

//populate select list
populateList("organizations-select","organizations",0,"","",0,1);
populateList("zones-select","zones");

//action for organization select
$("#organizations-select").change(function(){
	organizationId=$("#organizations-select").val();
	if(!isNaN(organizationId) && organizationId!="undefined"){
		//populate list
		populateList("persons-select","persons",organizationId);
		//show list
		$("#select-container-persons").fadeIn();
	}
});

//action for zone select
$("#zones-select").change(function(){
	zoneId=$("#zones-select").val();
	if(!isNaN(zoneId) && zoneId!="undefined"){
		//populate list
		populateList("doors-select","doors",zoneId);
		//show list
		$("#select-container-doors").fadeIn();
	}
});

//this is so filter vars are set
$("#persons-select").change(function(){
	filterPersonId=$("#persons-select").val();
});

$("#doors-select").change(function(){
	filterDoorId=$("#doors-select").val();
});

$("input[name=side]").change(function(){
	filterSide=$("input[name=side]:checked").val();
});

//form reset
$("#events-search-reset").click(function(){
	location.reload();
});

//clear filter
$("#events-search-reset-filter").click(function(){
	organizationId="";
	zoneId="";
	filterPersonId="";
	filterDoorId="";
	filterSide="";
	$("#persons-select option:selected,#doors-select option:selected,#zones-select option:selected,#organizations-select option:selected").prop("selected",false);
	$("input[name=side][value='']").prop("checked",true);
	//show filter button
	$("#filter-row").slideUp("fast");
	$("#search-again-button").show();
	//collapse sub menus
	$("#select-container-doors,#select-container-persons").hide();
	
});

//add events on live table
function addEventInTable(data){
	//set no value for null values
	if(data.orgName === null) data.orgName="";
	if(data.personName === null) data.personName="";
	//init date variable for date prints
	var dateobj = new Date(data.dateTime);
	//set grey row if event belongs to a deleted user
	//red if access was denied
	if(data.allowed==0) var rowclass=" todel";
	else if(data.personDeleted==1) var rowclass=" deleted";
	else var rowclass="";
	//build row
	ret_string="<tr style='display:none' class='newevent"+rowclass+"'><td class=\"center hidden-xs\">"+ get_icon(data.eventTypeId,"type") +"</td><td class=\"hidden-xs\">"+ data.zoneName +"</td><td>"+ data.doorName +"</td><td class=\"center hidden-xs\">"+ get_icon(data.doorLockId,"doorlock") +"</td><td class=\"center hidden-xs\">"+ get_icon(data.side,"side") +"</td><td class=\"hidden-xs\">"+ dateobj.getFullYear() + "-" + addZeroPaddingSingle((dateobj.getMonth()+1)) + "-" + addZeroPaddingSingle(dateobj.getDate()) +"</td><td>"+ addZeroPadding(dateobj.getHours() + ":" + dateobj.getMinutes()) +"</td><td class=\"hidden-xs\">"+ data.orgName +"</td><td>"+ data.personName +"</td><td class=\"center\">"+ get_icon(data.allowed,"allowed") +"</td><td class=\"center hidden-xs\">"+ get_icon(data.denialCauseId,"denialcause") +"</td></tr>";
	return ret_string;
}

//toggle search
$("#search-again-button").click(function(){
	$(this).hide();
	//show filter
	$("#filter-row").slideDown("fast");
});

/*$(document).ready(function(){
	var i = 1;
	var varinterval = setInterval(function(){
		$("#noevents-row").hide();
		$('<tr style="display:none" class="newevent"><td class="center"><span class="fa fa-address-card"></span></td><td>Zona Sur '+i+'</td><td>Puerta Principal</td><td class="center"><span class="fa fa-feed"></span></td><td class="center"><span class="fa fa-sign-in"></span></td><td>2018-10-29</td><td>11:26</td><td>Bonifies Networks</td><td>Jorge Kleinerman</td><td class="center"><span class="fa fa-check"></span></td><td class="center"></td></tr>').insertAfter("#events-table-header-row").show("slow").toggleClass("newevent");
		i++;
	}, 3000)

});*/

$.getScript(window.location.protocol + "//" + window.location.hostname+":<?=$nodejs_port?>/socket.io/socket.io.js", function(){
	if(typeof io !== 'undefined'){
		var socketio = io.connect(window.location.hostname+":<?=$nodejs_port?>");
		socketio.on("message_to_client", function(data){
			var dataParsed=JSON.parse(data);
			//check if controller down event was sent
			if(typeof dataParsed.macAddress !="undefined" && typeof dataParsed.reachable !="undefined"){
				//controller down/up case
				if(dataParsed.reachable==0){
					$("#controller-alerts-container").prepend('<div class="controller-alert"><div class="alert alert-danger alert-message-inner"><button type="button" class="close" data-dismiss="alert">&times;</button>'+dataParsed.lastSeen + ": " + dataParsed.name + " (" + buildMacFromString(dataParsed.macAddress) + ") is down!"+'</div></div>');
				} else {
					$("#controller-alerts-container").prepend('<div class="controller-alert"><div class="alert alert-success alert-message-inner"><button type="button" class="close" data-dismiss="alert">&times;</button>'+dataParsed.lastSeen + ": " + dataParsed.name + " (" + buildMacFromString(dataParsed.macAddress) + ") is back up."+'</div></div>');
				}
			} else {
				//normal live event case
				//if filter vars are not set or they match > show
				if((organizationId=="" || dataParsed.orgId == organizationId)
				&& (zoneId=="" || dataParsed.zoneId == zoneId)
				&& (filterPersonId=="" || dataParsed.personId == filterPersonId)
				&& (filterDoorId=="" || dataParsed.doorId == filterDoorId)
				&& (filterSide=="" || dataParsed.side == filterSide)){
					//hide noevents row
					$("#noevents-row").hide();
					$(addEventInTable(dataParsed)).insertAfter("#events-table-header-row").show("slow").toggleClass("newevent");
				}
			}
		});
	}
});

</script>

</body>
</html>