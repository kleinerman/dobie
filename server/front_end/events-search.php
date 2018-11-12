<?
$leavebodyopen=1;
$include_extra_js=array("clockpicker","datepicker");
include("header.php");
?>
<div id="page-wrapper">

<div class="row">
<div class="col-lg-12">
<h1 class="page-header"><?=get_text("Event Search",$lang);?></h1>
</div>
</div>

<div class="row">
<!-- left column start -->
<div class="col-lg-12">
<br>

<div class="row" id="filter-row">

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

<br><br>

<div class="select-container container-bordered">
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

</div>

<div class="col-lg-4 center">

<div class="select-container">
<form action="javascript:void(0)">
<div class="select-container-title"><?=get_text("Date and Time",$lang);?></div>
<div class="select-container-body left">
<br>
<?=get_text("From",$lang);?>:<br>
<div class="input-group input_date_container" data-placement="left" data-align="top" data-autoclose="true" title="<?=get_text("From Date",$lang);?>"><input type="text" class="form-control input_date center" id="startDate" value="<?=date("Y-m-d",mktime(0,0,0)-(60*60*24*7))?>"><span class="input-group-addon"><span class="fa fa-calendar"></span></span></div>

<div class="input-group clockpicker" data-placement="left" data-align="top" data-autoclose="true" title="<?=get_text("From",$lang);?>"><input type="text" class="form-control from-input" value="00:00" id="startTime" name="startTime"><span class="input-group-addon"><span class="fa fa-clock-o"></span></span></div>

<br><br>

<?=get_text("Until",$lang);?>:<br>
<div class="input-group input_date_container" data-placement="left" data-align="top" data-autoclose="true" title="<?=get_text("Until Date",$lang);?>"><input type="text" class="form-control input_date center" id="endDate" value="<?=date("Y-m-d",mktime(0,0,0)+(60*60*24))?>"><span class="input-group-addon"><span class="fa fa-calendar"></span></span></div>

<div class="input-group clockpicker" data-placement="left" data-align="top" data-autoclose="true" title="<?=get_text("Until",$lang);?>"><input type="text" class="form-control from-input" value="00:00" id="endTime"><span class="input-group-addon"><span class="fa fa-clock-o"></span></span></div>

</div>
</form>
</div>

<br><br><br>

<button id="events-search-submit" class="btn btn-success" type="button"><?=get_text("Search",$lang);?></button>
<button id="events-search-reset" class="btn btn-warning" type="button"><?=get_text("Reset",$lang);?></button>

</div>

</div>

<div class="row" id="search-again-row" style="display:none">
<div class="col-sm-6">

<div class="alert alert-warning clickable left" id="search-again-button">
<span class="fa fa-chevron-left"></span> <?=get_text("Go back to search",$lang);?>
</div>

</div>

<div class="col-sm-6">

<div class="alert alert-info clickable center" id="search-download-button">
<span class="fa fa-download"></span> <?=get_text("Export spreadsheet",$lang);?> <span class="fa fa-spinner fa-spin download-throbber-container" style="display:none"></span>
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

<div id="legend-row" style="display:none">
<div class="row">
<div class="col-sm-12">
* <?=get_text("Persons in red were deleted or they are visitors that left the building",$lang);?>.
<br>
</div>
</div>

<div class="row">
<div class="col-sm-3">
<h4><?=get_text("Event Type",$lang);?></h4>
<span class="fa fa-fw fa-address-card"></span> <?=get_text("Identified Access",$lang);?><br>
<span class="fa fa-fw fa-circle"></span> <?=get_text("Access with button",$lang);?><br>
<span class="fa fa-fw fa-chain-broken"></span> <?=get_text("Door remains opened",$lang);?><br>
<span class="fa fa-fw fa-bolt"></span> <?=get_text("Door was forced",$lang);?>
</div>
<div class="col-sm-3">
<h4>Lock</h4>
<span class="fa fa-fw fa-feed"></span> <?=get_text("Card Reader",$lang);?><br>
<span class="fa fa-fw fa-thumbs-o-up"></span> <?=get_text("Fingerprint Reader",$lang);?><br>
<span class="fa fa-fw fa-circle"></span> <?=get_text("Button",$lang);?>
</div>
<div class="col-sm-3">
<h4><?=get_text("Denial Cause",$lang);?></h4>
<span class="fa fa-fw fa-ban"></span> <?=get_text("No Access",$lang);?><br>
<span class="fa fa-fw fa-calendar-times-o"></span> <?=get_text("Expired Card",$lang);?><br>
<span class="fa fa-fw fa-clock-o"></span> <?=get_text("Out of time",$lang);?>
</div>
<div class="col-sm-3">
<h4>Direction</h4>
<span class="fa fa-fw fa-sign-in"></span> <?=get_text("Incoming",$lang);?><br>
<span class="fa fa-fw fa-sign-out"></span> <?=get_text("Outgoing",$lang);?><br>
</div>

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
<h4 class="modal-title" id="modal-error-label">&nbsp;</h4>
</div>
<div class="modal-body center">
</div>
</div>
</div>
<!-- /.modal -->
</div>

<? include("footer.php");?>

<script type="text/javascript">
//init filters
setFilterAction();

var organizationId;
var zoneId;
//init values to show per page
var perpage = 15;
//total event count for download csv action
var totalEvents=0;

//populate select list
populateList("organizations-select","organizations",0,"","",0,1);
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
$("#search-again-button").click(function(){
	$("#search-again-row").hide();
	$("#results-row,#legend-row").hide();
	//show filter
	$("#filter-row").slideDown("fast");
});

//make download csv
$("#search-download-button").click(function(){
	populateEventList(1,totalEvents,1);
});

function populateEventList(startEvt,evtsQtty,downloadCsv=0){
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

	//set default values for date vars
	if(startDate=="") startDate = "2000-01-01";
	if(startTime=="") startTime = "00:00";
	if(endDate=="") endDate = "9999-12-31";
	if(endTime=="") endTime = "00:00";

	//validate values > show error modal in case of error
	//send ajax action and show pagination values
	if(orgId!="" && isNaN(orgId)) error = "<?=(get_text("Invalid value for",$lang) . "." . get_text("organization",$lang));?>";
	else if(personId!="" && isNaN(personId)) error = "<?=(get_text("Invalid value for",$lang) . "." . get_text("person",$lang));?>";
	else if(zoneId!="" && isNaN(zoneId)) error = "<?=(get_text("Invalid value for",$lang) . "." . get_text("zone",$lang));?>";
	else if(doorId!="" && isNaN(doorId)) error = "<?=(get_text("Invalid value for",$lang) . "." . get_text("door",$lang));?>";
	else if(side!="" && isNaN(side)) error = "<?=(get_text("Invalid value for",$lang) . "." . get_text("direction",$lang));?>";

	if(error==""){
		if(downloadCsv){
			//download csv
			$.ajax({
				type: "POST",
				url: "process",
				data: "action=get_events&orgid=" + orgId + "&personid=" + personId + "&zoneid=" + zoneId + "&doorid=" + doorId + "&side=" + side + "&startdate=" + startDate + "&starttime=" + startTime + "&enddate=" + endDate + "&endtime=" + endTime + "&startevt=" + startEvt + "&evtsqtty=" + totalEvents,
				beforeSend: function(){$(".download-throbber-container").show()},
				complete: function(resp){$(".download-throbber-container").hide()},
				success: function(resp){
					if(resp[0]=='1'){
						//trigger csv
						downloadCSV(resp[1].events,"dobie-export-event.csv");
					} else {
						//show modal error
						$('#modal-error .modal-body').text(resp[1]);
						$("#modal-error").modal("show");
					}
				},
				failure: function(){
					//show modal error
					$('#modal-error .modal-body').text("<?=get_text("Operation failed, please try again",$lang);?>");
					$("#modal-error").modal("show");
				}
			});
		} else {
			//render events table
			$.ajax({
				type: "POST",
				url: "process",
				data: "action=get_events&orgid=" + orgId + "&personid=" + personId + "&zoneid=" + zoneId + "&doorid=" + doorId + "&side=" + side + "&startdate=" + startDate + "&starttime=" + startTime + "&enddate=" + endDate + "&endtime=" + endTime + "&startevt=" + startEvt + "&evtsqtty=" + evtsQtty,
				beforeSend: function(){$("#results-container-inner,#legend-row").hide();$("#pagination-container").html(""); $(".throbber-container").show();},
				complete: function(resp){/*console.log(resp);*/$(".throbber-container").hide(); $("#results-container-inner").fadeIn()},
				success: function(resp){
					if(resp[0]=='1'){
						//populate event table
						$("#results-container-inner").html(buildEventTable(resp[1].events));
						//show legend
						$("#legend-row").show();
						//show pagination row
						$("#pagination-container").html(showPagination(resp[1]));
						//update total events number for download csv
						totalEvents=resp[1].totalEvtsCount;
						$("#search-download-button").show();
					} else {
						//no results
						$("#results-container-inner").html("<div class='left'>"+resp[1]+"</div>");
						$("#search-download-button").hide();
					}
				},
				failure: function(){
					//show modal error
					$('#modal-error .modal-body').text("<?=get_text("Operation failed, please try again",$lang);?>");
					$("#modal-error").modal("show");
				}
			});
			//show results
			$("#filter-row").slideUp("fast", function(){$("#results-row,#search-again-row").fadeIn();});
		}
	} else {
		//invalid values sent
		$('#modal-error .modal-body').text(error);
		$("#modal-error").modal("show");
	}
}

function downloadCSV(eventsArr,csvFileName){
	// Each column is separated by ";" and new line "\n" for next row
	var separator = ";";
	var linebreak = '\n';
	//add column names in header
	var csvContent = '<?=get_text("Type",$lang);?>'+separator+'<?=get_text("Zone",$lang);?>'+separator+'<?=get_text("Door",$lang);?>'+separator+'<?=get_text("Lock",$lang);?>'+separator+'<?=get_text("Direction",$lang);?>'+separator+'<?=get_text("Date",$lang);?>'+separator+'<?=get_text("Time",$lang);?>'+separator+'<?=get_text("Organization",$lang);?>'+separator+'<?=get_text("Person",$lang);?>'+separator+'<?=get_text("Allowed",$lang);?>'+separator+'<?=get_text("Denial Cause",$lang);?>'+separator+'<?=get_text("Person Deleted",$lang);?>'+linebreak;
	eventsArr.forEach(function(data){
		//set no value for null values
		if(data.orgName === null) data.orgName="";
		if(data.personName === null) data.personName="";
		//if person deleted, show yes as last column
		if(data.personDeleted==1) var isdel="Yes";
		else var isdel="No";
		//init date variable for date prints
		var dateobj = new Date(data.dateTime);
		csvContent += get_event_text(data.eventTypeId,"type") +separator+ data.zoneName +separator+ data.doorName +separator+ get_event_text(data.doorLockId,"doorlock") +separator+ get_event_text(data.side,"side") +separator+ dateobj.getFullYear() + "-" + addZeroPaddingSingle((dateobj.getMonth()+1)) + "-" + addZeroPaddingSingle(dateobj.getDate()) +separator+ addZeroPadding(dateobj.getHours() + ":" + dateobj.getMinutes()) +separator+ data.orgName +separator+ data.personName +separator+ get_event_text(data.allowed,"allowed") +separator+ get_event_text(data.denialCauseId,"denialcause") +separator+ isdel +linebreak;
	});

	// The download function takes a CSV string, the filename and mimeType as parameters
	var download = function(content, fileName, mimeType){
		var a = document.createElement('a');
		mimeType = mimeType || 'application/octet-stream';

		if (navigator.msSaveBlob) { // IE10
			navigator.msSaveBlob(new Blob([content], {
				type: mimeType
			}), fileName);
		} else if (URL && 'download' in a) { //html5 A[download]
			a.href = URL.createObjectURL(new Blob([content], {
				type: mimeType
			}));
			a.setAttribute('download', fileName);
			document.body.appendChild(a);
			a.click();
			document.body.removeChild(a);
		} else {
			location.href = 'data:application/octet-stream,' + encodeURIComponent(content); // only this mime type is supported
		}
	}

	download(csvContent, csvFileName, 'text/csv;encoding:utf-8');
}

//outputs html for event table based on received data from api
function buildEventTable(data){
	//init headers
	var ret_string='<table id="events-table" class="table-bordered table-hover table-condensed table-responsive table-striped left"><tr><th class="center"><?=get_text("Type",$lang);?></th><th><?=get_text("Zone",$lang);?></th><th><?=get_text("Door",$lang);?></th><th class="center"><?=get_text("Lock",$lang);?></th><th class="center"><?=get_text("Direction",$lang);?></th><th><?=get_text("Date",$lang);?></th><th><?=get_text("Time",$lang);?></th><th><?=get_text("Organization",$lang);?></th><th><?=get_text("Person",$lang);?></th><th class="center"><?=get_text("Allowed",$lang);?></th><th class="center"><?=get_text("Denial Cause",$lang);?></th></tr>';

	for(var i=0;i<data.length;i++){
		//set no value for null values
		if(data[i].orgName === null) data[i].orgName="";
		if(data[i].personName === null) data[i].personName="";
		//init date variable for date prints
		var dateobj = new Date(data[i].dateTime);
		//set red row if event belongs to a deleted user
		if(data[i].personDeleted==1) var rowclass=" class='todel'";
		else var rowclass="";
		//build row
		ret_string+="<tr"+rowclass+"><td class=\"center\">"+ get_icon(data[i].eventTypeId,"type") +"</td><td>"+ data[i].zoneName +"</td><td>"+ data[i].doorName +"</td><td class=\"center\">"+ get_icon(data[i].doorLockId,"doorlock") +"</td><td class=\"center\">"+ get_icon(data[i].side,"side") +"</td><td>"+ dateobj.getFullYear() + "-" + addZeroPaddingSingle((dateobj.getMonth()+1)) + "-" + addZeroPaddingSingle(dateobj.getDate()) +"</td><td>"+ addZeroPadding(dateobj.getHours() + ":" + dateobj.getMinutes()) +"</td><td>"+ data[i].orgName +"</td><td>"+ data[i].personName +"</td><td class=\"center\">"+ get_icon(data[i].allowed,"allowed") +"</td><td class=\"center\">"+ get_icon(data[i].denialCauseId,"denialcause") +"</td></tr>";
	}

	ret_string+="</table>";
	return ret_string;
}

//outputs text for all events
function get_event_text(id,mode){
	if(id===null) return "";
	else {
		var iconstr="";
		switch(mode){
			case "type":
				if(id==1) iconstr="<?=get_text("Identified Access",$lang);?>";
				else if(id==2) iconstr="<?=get_text("Access with button",$lang);?>";
				else if(id==3) iconstr="<?=get_text("Door remains opened",$lang);?>";
				else if(id==4) iconstr="<?=get_text("Door was forced",$lang);?>";
			break;
			case "doorlock":
				if(id==1) iconstr="<?=get_text("Card Reader",$lang);?>";
				else if(id==2) iconstr="<?=get_text("Fingerprint Reader",$lang);?>";
				else if(id==3) iconstr="<?=get_text("Button",$lang);?>";
			break;
			case "denialcause":
				if(id==1) iconstr="<?=get_text("No Access",$lang);?>";
				else if(id==2) iconstr="<?=get_text("Expired Card",$lang);?>";
				else if(id==3) iconstr="<?=get_text("Out of time",$lang);?>";
			break;
			case "side":
				if(id==0) iconstr="<?=get_text("Outgoing",$lang);?>";
				else if(id==1) iconstr="<?=get_text("Incoming",$lang);?>";
			break;
			case "allowed":
				if(id==0) iconstr="<?=get_text("No",$lang);?>";
				else if(id==1) iconstr="<?=get_text("Yes",$lang);?>";
			break;
			default: break;
		}
		return iconstr;
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
		pagination_str += "<nav aria-label=\"<?=get_text("Paging navigation",$lang);?>\"><ul class=\"pagination\">";
		//print previous button
		if(page>1) pagination_str += "<li class=\"page-item\"><a class=\"page-link\" href=\"javascript:void(0)\" onclick=\"populateEventList("+ ((page-2)*perpage+1)+",perpage)\"><?=get_text("Previous",$lang);?></a></li>";
		for(var j=1;j<=max_pages;j++){
			//print current page
			if(j==page) pagination_str += "<li class=\"page-item active\"><span class='page-link'>"+j+"</span></li>";
			//print linked page
			else if(max_pages<30 || (paging_left_inter>=j || paging_right_inter<=j)) pagination_str += "<li class=\"hidden-xs page-item\"><a class=\"page-link\" href=\"javascript:void(0)\" onclick=\"populateEventList("+((j-1)*perpage+1)+",perpage)\">"+j+"</a></li>";
			
		}
		//print next button
		if(page<max_pages) pagination_str += "<li class=\"page-item\"><a class=\"page-link\" href=\"javascript:void(0)\" onclick=\"populateEventList("+ (page*perpage+1)+",perpage)\"><?=get_text("Next",$lang);?></a></li>";
		pagination_str += "</ul></nav>";
	}

	return pagination_str;
}
</script>
</body>
</html>