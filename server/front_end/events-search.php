<?
$leavebodyopen=1;
$include_extra_js=array("clockpicker","datepicker");
include("header.php");
?>
<div id="page-wrapper">

<div class="row">
<div class="col-lg-12">
<h1 class="page-header">Event Search</h1>
</div>
</div>

<div class="row">
<!-- left column start -->
<div class="col-lg-12">
<br>

<div class="row" id="filter-row">

<div class="col-lg-4">

<div class="select-container">
<div class="select-container-title">Organizations</div>
<div class="select-container-body">
<input type="text" name="filter" placeholder="Filter options..." class="form-control data-filter" data-filter="organizations-select">
<select id="organizations-select" class="select-options select-options-small form-control" name="organizations-select" size="2"></select>
</div>
</div>

<br><br><br>

<div class="select-container" id="select-container-persons" style="display:none">
<div class="select-container-title">Person</div>
<div class="select-container-body">
<input type="text" name="filter" placeholder="Filter options..." class="form-control data-filter" data-filter="person-select">
<select id="persons-select" class="select-options select-options-small form-control" name="persons-select" size="2"></select>
</div>
</div>

</div>

<div class="col-lg-4">

<div class="select-container">
<form action="javascript:void(0)">
<div class="select-container-title">Zone</div>
<div class="select-container-body">
<input type="text" name="filter" placeholder="Filter options..." class="form-control data-filter" data-filter="zones-select">
<select id="zones-select" class="select-options select-options-small form-control" name="zones-select" size="2"></select>
</div>
<div class="select-container-footer">
&nbsp;
</div>
</form>
</div>

<div class="select-container" id="select-container-doors" style="display:none">
<form action="javascript:void(0)">
<div class="select-container-title">Doors</div>
<div class="select-container-body">
<input type="text" name="filter" placeholder="Filter options..." class="form-control data-filter" data-filter="doors-select">
<select id="doors-select" class="select-options select-options-small form-control" name="doors-select" size="2"></select>
</div>
</form>
</div>

<br><br>

<div class="select-container container-bordered">
<form action="javascript:void(0)">
<div class="select-container-title">Direction</div>
<div class="select-container-body left">
<br>
<label><input type="radio" name="side" value="" checked> Both</label><br>
<label><input type="radio" name="side" value="1"> Incoming</label><br>
<label><input type="radio" name="side" value="0"> Outgoing</label>
</div>
</form>
</div>

</div>

<div class="col-lg-4 center">

<div class="select-container">
<form action="javascript:void(0)">
<div class="select-container-title">Date and Time</div>
<div class="select-container-body left">
<br>
From:<br>
<div class="input-group input_date_container" data-placement="left" data-align="top" data-autoclose="true" title="From Date"><input type="text" class="form-control input_date center" id="startDate" value="<?=date("Y-m-d",mktime(0,0,0)-(60*60*24))?>"><span class="input-group-addon"><span class="fa fa-calendar"></span></span></div>

<div class="input-group clockpicker" data-placement="left" data-align="top" data-autoclose="true" title="From"><input type="text" class="form-control from-input" value="00:00" id="startTime" name="startTime"><span class="input-group-addon"><span class="fa fa-clock-o"></span></span></div>

<br><br>

Until:<br>
<div class="input-group input_date_container" data-placement="left" data-align="top" data-autoclose="true" title="Until Date"><input type="text" class="form-control input_date center" id="endDate" value="<?=date("Y-m-d",mktime(0,0,0))?>"><span class="input-group-addon"><span class="fa fa-calendar"></span></span></div>

<div class="input-group clockpicker" data-placement="left" data-align="top" data-autoclose="true" title="From"><input type="text" class="form-control from-input" value="00:00" id="endTime"><span class="input-group-addon"><span class="fa fa-clock-o"></span></span></div>

</div>
</form>
</div>

<br><br><br>

<button id="events-search-submit" class="btn btn-success" type="button">Search</button>
<button id="events-search-reset" class="btn btn-warning" type="button">Reset</button>

</div>

</div>

<div class="row" id="search-again-row" style="display:none">
<div class="col-sm-12">

<div class="alert alert-warning clickable left">
<span class="fa fa-chevron-left"></span> Go back to search
</div>


</div>
</div>

<div class="row" id="results-row" style="display:none">
<div class="col-sm-12">

<div id="results-container">

<div class="throbber-container"><span class="fa fa-spinner fa-spin fa-4x"></span></div>

<div id="results-container-inner" class="table-container"></div>

<div id="pagination-container" class="center"></div>

</div>


</div>
</div>

<div class="row" id="legend-row" style="display:none">
<div class="col-sm-4">
<h4>Event Type</h4>
<span class="fa fa-fw fa-bullseye"></span> Access with card<br>
<span class="fa fa-fw fa-circle"></span> Access with button<br>
<span class="fa fa-fw fa-chain-broken"></span> Door remains opened<br>
<span class="fa fa-fw fa-bolt"></span> Door was forced
</div>
<div class="col-sm-4">
<h4>Triggered by</h4>
<span class="fa fa-fw fa-feed"></span> Card Reader<br>
<span class="fa fa-fw fa-thumbs-o-up"></span> Fingerprint Reader<br>
<span class="fa fa-fw fa-circle"></span> Button
</div>
<div class="col-sm-4">
<h4>Reason</h4>
<span class="fa fa-fw fa-ban"></span> No Access<br>
<span class="fa fa-fw fa-calendar-times-o "></span> Expired Card<br>
<span class="fa fa-fw fa-clock-o"></span> Out of time
</div>

</div>

</div>

</div>

</div>

<!-- error modal -->
<div class="modal fade" id="modal-error" tabindex="-1" role="dialog" aria-hidden="true">
<div class="modal-dialog">
<div class="modal-content">
<div class="modal-header">
<button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>
<h4 class="modal-title" id="modal-edit-label">&nbsp;</h4>
</div>
<div class="modal-body center">
</div>
</div>
</div>
<!-- /.modal -->
</div>

<style>
.table-container{
	display:grid;
	margin:0px auto;
	max-height:600px;
	overflow:auto;
}

#legend-row{
	padding: 40px;
}
</style>

<?
include("footer.php");
?>

<script type="text/javascript">
//init filters
setFilterAction();

var organizationId;
var zoneId;
//init values to show per page
var perpage = 15;

//populate select list
populateList("organizations-select","organizations");
populateList("zones-select","zones");

//init clockpicker
$('.clockpicker').clockpicker();
//init date picker
$(".input_date").datepicker({dateFormat: "yy-mm-dd"});

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

//form reset
$("#events-search-reset").click(function(){
	location.reload();
});

//form sent
$("#events-search-submit").click(function(){
	populateEventList(1,perpage);
});

//toggle search
$("#search-again-row").click(function(){
	$(this).hide();
	$("#results-row,#legend-row").hide();
	//show filter
	$("#filter-row").slideDown("fast");
});

function populateEventList(startEvt,evtsQtty){
	var orgId = ($("#organizations-select").val()!==null) ? $("#organizations-select").val() : "";
	var personId = ($("#persons-select").val()!==null) ? $("#persons-select").val() : "";
	var zoneId = ($("#zones-select").val()!==null) ? $("#zones-select").val() : "";
	var doorId = ($("#doors-select").val()!==null) ? $("#doors-select").val() : "";
	var side = $("input[name=side]:checked").val();
	var startDate = $("#startDate").val();
	var startTime = $("#startTime").val();
	var endDate = $("#endDate").val();
	var endTime = $("#endTime").val();
	var error = "";

	//validate values > show error modal in case of error
	//send ajax action and show pagination values
	if(orgId!="" && isNaN(orgId)) error = "Invalid value for: organization";
	else if(personId!="" && isNaN(personId)) error = "Invalid value for: person";
	else if(zoneId!="" && isNaN(zoneId)) error = "Invalid value for: zone";
	else if(doorId!="" && isNaN(doorId)) error = "Invalid value for: door";
	else if(side!="" && isNaN(side)) error = "Invalid value for: direction";

	if(error==""){
		//set default values for date vars
		if(startDate=="") startDate = "2000-01-01";
		if(startTime=="") startTime = "00:00";
		if(endDate=="") endDate = "9999-12-31";
		if(endTime=="") endTime = "00:00";
		$.ajax({
			type: "POST",
			url: "process",
			data: "action=get_events&orgid=" + orgId + "&personid=" + personId + "&zoneid=" + zoneId + "&doorid=" + doorId + "&side=" + side + "&startdate=" + startDate + "&starttime=" + startTime + "&enddate=" + endDate + "&endtime=" + endTime + "&startevt=" + startEvt + "&evtsqtty=" + evtsQtty,
			beforeSend: function(){$("#results-container-inner,#legend-row").hide();$("#pagination-container").html(""); $(".throbber-container").fadeIn();},
			complete: function(resp){console.log(resp);$(".throbber-container").hide(); $("#results-container-inner").fadeIn()},
			success: function(resp){
				if(resp[0]=='1'){
					//populate event table
					$("#results-container-inner").html(buildEventTable(resp[1].events));
					//show legend
					$("#legend-row").show();
					//show pagination row
					$("#pagination-container").html(showPagination(resp[1]));
				} else {
					//show error
					$("#results-container-inner").html("<div class='center'>"+resp[1]+"</div>");
				}
			},
			failure: function(){
				//show modal error
				$('#modal-error .modal-body').text("Operation failed, please try again");
				$("#modal-error").modal("show");
			}
		});
		//show results
		$("#filter-row").slideUp("fast", function(){$("#results-row,#search-again-row").fadeIn();});
	} else {
		//invalid values sent
		$('#modal-error .modal-body').text(error);
		$("#modal-error").modal("show");
	}
}

//outputs html for event table based on received data from api
function buildEventTable(data){
	//init headers
	var ret_string='<table id="events-table" class="table-bordered table-hover table-condensed table-responsive table-striped left"><tr><th class="center">Type</th><th>Zone</th><th>Door</th><th class="center">Triggered by</th><th class="center">Direction</th><th>Date</th><th>Time</th><th>Organization</th><th>Person</th><th class="center">Allowed</th><th class="center">Reason</th></tr>';
	//console.log(data);

	for(var i=0;i<data.length;i++){
		//set no value for null values
		if(data[i].orgName === null) data[i].orgName="";
		if(data[i].personName === null) data[i].personName="";
		//init date variable for date prints
		var dateobj = new Date(data[i].dateTime);
		//build row
		ret_string+="<tr><td class=\"center\">"+ get_icon(data[i].eventTypeId,"type") +"</td><td>"+ data[i].zoneName +"</td><td>"+ data[i].doorName +"</td><td class=\"center\">"+ get_icon(data[i].doorLockId,"doorlock") +"</td><td class=\"center\">"+ get_icon(data[i].side,"side") +"</td><td>"+ dateobj.getFullYear() + "-" + addZeroPaddingSingle((dateobj.getMonth()+1)) + "-" + addZeroPaddingSingle(dateobj.getDate()) +"</td><td>"+ addZeroPadding(dateobj.getHours() + ":" + dateobj.getMinutes()) +"</td><td>"+ data[i].orgName +"</td><td>"+ data[i].personName +"</td><td class=\"center\">"+ get_icon(data[i].allowed,"allowed") +"</td><td class=\"center\">"+ get_icon(data[i].denialCauseId,"denialcause") +"</td></tr>";
	}

	ret_string+="</table>";
	return ret_string;
}

//outputs html for the fa icon for all events
function get_icon(id,mode){
	if(id===null) return "";
	else {
		var iconstr="";
		switch(mode){
			case "type":
				if(id==1) iconstr="bullseye";
				else if(id==2) iconstr="circle";
				else if(id==3) iconstr="chain-broken";
				else if(id==4) iconstr="bolt";
			break;
			case "doorlock":
				if(id==1) iconstr="feed";
				else if(id==2) iconstr="thumbs-o-up";
				else if(id==3) iconstr="circle";
			break;
			case "denialcause":
				if(id==1) iconstr="ban";
				else if(id==2) iconstr="calendar-times-o";
				else if(id==3) iconstr="clock-o";
			break;
			case "side":
				if(id==0) iconstr="sign-out";
				else if(id==1) iconstr="sign-in";
			break;
			case "allowed":
				if(id==0) iconstr="times";
				else if(id==1) iconstr="check";
			break;
			default: break;
		}
		if(iconstr!="") return "<span class='fa fa-"+ iconstr +"'></span>";
		else return "";
	}
}

//outputs html for pagination bar
function showPagination(data){

	//init pagination html
	var pagination_str="";
	//calculate q pages
	var max_pages = Math.ceil(data.totalEvtsCount/perpage);
	//validate page
	var page = Math.min(Math.max(1,(Math.floor(data.startEvt/perpage))+1),max_pages);
/*console.log(max_pages);
console.log(page);
console.log(data.totalEvtsCount);
*/
	if(max_pages>1){
		//define paging margins for printing many pages
		if(max_pages>30) {
			var paging_left_inter = 10;
			var paging_right_inter = max_pages-1;
		} else {
			var paging_left_inter = 0;
			var paging_right_inter = max_pages;
		}

		//start pagination bar
		pagination_str += "<nav aria-label=\"Paging navigation\"><ul class=\"pagination\">";
		//print previous button
		if(page>1) pagination_str += "<li class=\"page-item\"><a class=\"page-link\" href=\"javascript:void(0)\" onclick=\"populateEventList("+ ((page-2)*perpage+1)+",perpage)\">Previous</a></li>";
		for(var j=1;j<=max_pages;j++){
			//print current page
			if(j==page) pagination_str += "<li class=\"page-item active\"><span class='page-link'>"+j+"</span></li>";
			//print linked page
			else if(max_pages<30 || (paging_left_inter>=j || paging_right_inter<=j)) pagination_str += "<li class=\"hidden-xs page-item\"><a class=\"page-link\" href=\"javascript:void(0)\" onclick=\"populateEventList("+((j-1)*perpage+1)+",perpage)\">"+j+"</a></li>";
			
		}
		//print next button
		if(page<max_pages) pagination_str += "<li class=\"page-item\"><a class=\"page-link\" href=\"javascript:void(0)\" onclick=\"populateEventList("+ (page*perpage+1)+",perpage)\">Next</a></li>";
		pagination_str += "</ul></nav>";
	}

	return pagination_str;
}
</script>
</body>
</html>