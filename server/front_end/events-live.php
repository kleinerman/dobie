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
<input type="text" name="filter" placeholder="<?=get_text("Filter options",$lang);?>..." class="form-control data-filter" data-filter="person-select">
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

<button id="events-search-submit" class="btn btn-success" type="button"><?=get_text("Search",$lang);?></button>
<button id="events-search-reset" class="btn btn-warning" type="button"><?=get_text("Reset",$lang);?></button>

</div>

</div>

<div class="row" id="search-again-row">
<div class="col-sm-12">

<div class="alert alert-warning clickable left" id="search-again-button">
<span class="fa fa-search"></span> <?=get_text("Filter...",$lang);?>
</div>

</div>

<div class="row">
<div class="col-lg-12">
<hr>

<div id="events-container">

<table id="events-table" class="table-bordered table-hover table-condensed table-responsive table-striped left"><tr id="events-table-header-row">
<th class="center"><?=get_text("Type",$lang);?></th><th><?=get_text("Zone",$lang);?></th><th><?=get_text("Door",$lang);?></th><th class="center"><?=get_text("Lock",$lang);?></th><th class="center"><?=get_text("Direction",$lang);?></th><th><?=get_text("Date",$lang);?></th><th><?=get_text("Time",$lang);?></th><th><?=get_text("Organization",$lang);?></th><th><?=get_text("Person",$lang);?></th><th class="center"><?=get_text("Allowed",$lang);?></th><th class="center"><?=get_text("Denial Cause",$lang);?></th></tr>
<tr id="noevents-row"><td colspan="11"><?=get_text("No events",$lang);?></td></tr>
</table>

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
function addEventInTable(data){
	//set no value for null values
	if(data.orgName === null) data.orgName="";
	if(data.personName === null) data.personName="";
	//init date variable for date prints
	var dateobj = new Date(data.dateTime);
	//set red row if event belongs to a deleted user
	if(data.personDeleted==1) var rowclass=" todel";
	else var rowclass="";
	//build row
	ret_string="<tr style='display:none' class='newevent"+rowclass+"'><td class=\"center\">"+ get_icon(data.eventTypeId,"type") +"</td><td>"+ data.zoneName +"</td><td>"+ data.doorName +"</td><td class=\"center\">"+ get_icon(data.doorLockId,"doorlock") +"</td><td class=\"center\">"+ get_icon(data.side,"side") +"</td><td>"+ dateobj.getFullYear() + "-" + addZeroPaddingSingle((dateobj.getMonth()+1)) + "-" + addZeroPaddingSingle(dateobj.getDate()) +"</td><td>"+ addZeroPadding(dateobj.getHours() + ":" + dateobj.getMinutes()) +"</td><td>"+ data.orgName +"</td><td>"+ data.personName +"</td><td class=\"center\">"+ get_icon(data.allowed,"allowed") +"</td><td class=\"center\">"+ get_icon(data.denialCauseId,"denialcause") +"</td></tr>";
	return ret_string;
}

//toggle search
$("#search-again-button").click(function(){
	$("#search-again-row").hide();
	$("#results-row,#legend-row").hide();
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
			//$("#events-container").append(data + "<br>");
			var dataParsed2=JSON.parse(data);
			//var dataParsed=JSON.parse(dataParsed2.sendval);
			$("#noevents-row").hide();
			$(addEventInTable(dataParsed2)).insertAfter("#events-table-header-row").show("slow").toggleClass("newevent");
			console.log(dataParsed2);
		});
	}
});
</script>

</body>
</html>