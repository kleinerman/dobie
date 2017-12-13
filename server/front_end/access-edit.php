<?
$leavebodyopen=1;
$innerheader=1;
$include_extra_js=array("clockpicker","datepicker");

//get access ID or create mode
$id = (isset($_GET["id"]) & is_numeric($_GET["id"])) ? $_GET["id"] : "";
$error="";

include("header.php");
?>
<div id="wrapper" class="container-fluid">
<!--END HEADER - START BODY-->

<div class="row">
<!-- /.col-lg-12 -->
<div class="col-lg-12">
<h3 class="page-header" id="page-header"></h3>
</div>
<!-- /.col-lg-12 -->
</div>

<div class="row">

<?if(!$id){?>
<!-- left column start -->
<div class="col-lg-3">

<div class="select-container">
<form action="javascript:void(0)">
<div class="select-container-title">Zone</div>
<div class="select-container-body">
<input type="text" name="filter" placeholder="Filter options..." class="form-control data-filter" data-filter="zones-select">
<select id="zones-select" class="select-options form-control" name="zones-select" size="2"></select>
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
<select id="doors-select" class="select-options form-control" name="doors-select" size="2" onchange="updateButtons(this.id)"></select>
</div>
</form>
</div>

</div>

<?}?>
<div class="col-lg-9 center">
<br>

<div class="row">

<div class="col-lg-12 center">
<div class="select-container-title">Schedule</div>
<div class="schedule-container">
<form>
<table id="schedule-table" class="table-condensed table-responsive left">
<tr><th>Day</th><th>Time interval</th><th class="center">Incoming</th><th class="center">Outgoing</th><th class="center">Both</th></tr>
<tr><td><label><input type="checkbox" name="days" value="" checked> All</label></td>
<td>
<div class="input-group clockpicker" data-placement="bottom" data-align="top" data-autoclose="true" data-toggle="tooltip" title="From"><input type="text" class="form-control" value="08:00" name="from0"><span class="input-group-addon"><span class="fa fa-clock-o"></span></span></div>
<div class="input-group clockpicker" data-placement="bottom" data-align="top" data-autoclose="true" data-toggle="tooltip" title="Until"><input type="text" class="form-control" value="18:00" name="to0"><span class="input-group-addon"><span class="fa fa-clock-o"></span></span></div>
</td><td class="center"><input type="radio" name="way0" value="1" checked>
</td><td class="center"><input type="radio" name="way0" value="2">
</td><td class="center"><input type="radio" name="way0" value="3">
</td>
</tr>

<tr class="dayrow"><td><label><input type="checkbox" name="days" value="1"> Monday</label></td>
<td>
<div class="input-group clockpicker" data-placement="bottom" data-align="top" data-autoclose="true" data-toggle="tooltip" title="From"><input type="text" class="form-control" value="08:00" name="from1"><span class="input-group-addon"><span class="fa fa-clock-o"></span></span></div>
<div class="input-group clockpicker" data-placement="bottom" data-align="top" data-autoclose="true" data-toggle="tooltip" title="Until"><input type="text" class="form-control" value="18:00" name="to1"><span class="input-group-addon"><span class="fa fa-clock-o"></span></span></div>
</td><td class="center"><input type="radio" name="way1" value="1" checked>
</td><td class="center"><input type="radio" name="way1" value="2">
</td><td class="center"><input type="radio" name="way1" value="3">
</td>
</tr>

<tr class="dayrow"><td><label><input type="checkbox" name="days" value="2"> Tuesday</label></td>
<td>
<div class="input-group clockpicker" data-placement="bottom" data-align="top" data-autoclose="true" data-toggle="tooltip" title="From"><input type="text" class="form-control" value="08:00" name="from2"><span class="input-group-addon"><span class="fa fa-clock-o"></span></span></div>
<div class="input-group clockpicker" data-placement="bottom" data-align="top" data-autoclose="true" data-toggle="tooltip" title="Until"><input type="text" class="form-control" value="18:00" name="to2"><span class="input-group-addon"><span class="fa fa-clock-o"></span></span></div>
</td><td class="center"><input type="radio" name="way2" value="1" checked>
</td><td class="center"><input type="radio" name="way2" value="2">
</td><td class="center"><input type="radio" name="way2" value="3">
</td>
</tr>

<tr class="dayrow"><td><label><input type="checkbox" name="days" value="3"> Wednesday</label></td>
<td>
<div class="input-group clockpicker" data-placement="bottom" data-align="top" data-autoclose="true" data-toggle="tooltip" title="From"><input type="text" class="form-control" value="08:00" name="from3"><span class="input-group-addon"><span class="fa fa-clock-o"></span></span></div>
<div class="input-group clockpicker" data-placement="bottom" data-align="top" data-autoclose="true" data-toggle="tooltip" title="Until"><input type="text" class="form-control" value="18:00" name="to3"><span class="input-group-addon"><span class="fa fa-clock-o"></span></span></div>
</td><td class="center"><input type="radio" name="way3" value="1" checked>
</td><td class="center"><input type="radio" name="way3" value="2">
</td><td class="center"><input type="radio" name="way3" value="3">
</td>
</tr>

<tr class="dayrow"><td><label><input type="checkbox" name="days" value="4"> Thursday</label></td>
<td>
<div class="input-group clockpicker" data-placement="bottom" data-align="top" data-autoclose="true" data-toggle="tooltip" title="From"><input type="text" class="form-control" value="08:00" name="from4"><span class="input-group-addon"><span class="fa fa-clock-o"></span></span></div>
<div class="input-group clockpicker" data-placement="bottom" data-align="top" data-autoclose="true" data-toggle="tooltip" title="Until"><input type="text" class="form-control" value="18:00" name="to4"><span class="input-group-addon"><span class="fa fa-clock-o"></span></span></div>
</td><td class="center"><input type="radio" name="way4" value="1" checked>
</td><td class="center"><input type="radio" name="way4" value="2">
</td><td class="center"><input type="radio" name="way4" value="3">
</td>
</tr>

<tr class="dayrow"><td><label><input type="checkbox" name="days" value="5"> Friday</label></td>
<td>
<div class="input-group clockpicker" data-placement="bottom" data-align="top" data-autoclose="true" data-toggle="tooltip" title="From"><input type="text" class="form-control" value="08:00" name="from5"><span class="input-group-addon"><span class="fa fa-clock-o"></span></span></div>
<div class="input-group clockpicker" data-placement="bottom" data-align="top" data-autoclose="true" data-toggle="tooltip" title="Until"><input type="text" class="form-control" value="18:00" name="to5"><span class="input-group-addon"><span class="fa fa-clock-o"></span></span></div>
</td><td class="center"><input type="radio" name="way5" value="1" checked>
</td><td class="center"><input type="radio" name="way5" value="2">
</td><td class="center"><input type="radio" name="way5" value="3">
</td>
</tr>

<tr class="dayrow"><td><label><input type="checkbox" name="days" value="6"> Saturday</label></td>
<td>
<div class="input-group clockpicker" data-placement="bottom" data-align="top" data-autoclose="true" data-toggle="tooltip" title="From"><input type="text" class="form-control" value="08:00" name="from6"><span class="input-group-addon"><span class="fa fa-clock-o"></span></span></div>
<div class="input-group clockpicker" data-placement="bottom" data-align="top" data-autoclose="true" data-toggle="tooltip" title="Until"><input type="text" class="form-control" value="18:00" name="to6"><span class="input-group-addon"><span class="fa fa-clock-o"></span></span></div>
</td><td class="center"><input type="radio" name="way6" value="1" checked>
</td><td class="center"><input type="radio" name="way6" value="2">
</td><td class="center"><input type="radio" name="way6" value="3">
</td>
</tr>

<tr class="dayrow"><td><label><input type="checkbox" name="days" value="7"> Sunday</label></td>
<td>
<div class="input-group clockpicker" data-placement="bottom" data-align="top" data-autoclose="true" data-toggle="tooltip" title="From"><input type="text" class="form-control" value="08:00" name="from7"><span class="input-group-addon"><span class="fa fa-clock-o"></span></span></div>
<div class="input-group clockpicker" data-placement="bottom" data-align="top" data-autoclose="true" data-toggle="tooltip" title="Until"><input type="text" class="form-control" value="18:00" name="to7"><span class="input-group-addon"><span class="fa fa-clock-o"></span></span></div>
</td><td class="center"><input type="radio" name="way7" value="1" checked>
</td><td class="center"><input type="radio" name="way7" value="2">
</td><td class="center"><input type="radio" name="way7" value="3">
</td>
</tr>
</table>
<br>

<div class="left">
Expiration Date: <label><input type="radio" name="expiration" value="0" checked> No</label> <label><input type="radio" name="expiration" value="1"> Yes</label>  
</div>

<div class="left">
<input type="text" class="form-control center" name="expiration_date" id="expiration_date" value="2017-11-17">

<br><br>
<button class="btn btn-success" type="submit">Save</button>
</div>

</form>
</div>
</div>
</div>
</div>

<br><br><br>
<!--END BODY -->
</div>
<!-- /#page-wrapper -->
</div>
<!-- /#wrapper -->

<?
include("footer.php");
?>


<style type="text/css">
.select-options{
	height:200px !important;
}

.clockpicker{
	display:inline-table;
	width:100px;
}

#expiration_date{
	display:none;
	width: 100px;
}

#schedule-table{
	border: 1px solid #ccc;
	width: 100%;
}
</style>

<script type="text/javascript">
//init filters
setFilterAction();

var zoneId;

//populate select list
populateList("zones-select","zones");

$("#zones-select").change(function(){
	zoneId=$("#zones-select").val();
	if(!isNaN(zoneId) && zoneId!="undefined"){
		//populate list
		populateList("doors-select","doors",zoneId);
		//show list
		$("#select-container-doors").fadeIn();
	}
});

$(".data-filter").keyup(function(){
	var options=$("#"+$(this).data("filter") + " option");
	var filterValue=$(this).val().toLowerCase();
	options.each(function(){
		if($(this).text().toLowerCase().includes(filterValue)) $(this).show();
		else $(this).hide();
	})
});

$(".data-filter-table").keyup(function(){
	var rows=$("#"+$(this).data("filter") + " tr");
	var filterValue=$(this).val().toLowerCase();
	rows.each(function(){
		if($(this).find("td").text().toLowerCase().includes(filterValue)) $(this).show();
		else $(this).hide();
	})
	//show header row
	$("#"+$(this).data("filter") + " tr:first-child").show();
});

//expiration date
$("input[name=expiration]").change(function(){
	if($(this).prop("checked") && $(this).val()==1) {
		$("#expiration_date").fadeIn();
	} else $("#expiration_date").fadeOut();
});

//initial show/hide
if($("input[name=expiration]:checked").val()!=0) $("#expiration_date").fadeIn();
</script>

<script type="text/javascript">
$('.clockpicker').clockpicker();

//init date picker
$(function(){
	$("#expiration_date").datepicker({dateFormat: "yy-mm-dd"});
});

$("input[name=days]").click(function(){
	if($(this).val()==""){
		//if All button
		if($(this).prop("checked")) {
			$("input[name=days]").prop("checked",true);
		} 
		else {
			$("input[name=days]").prop("checked",false);
		}
	} else {
		//rest of buttons
		$("input[name=days]:first").prop("checked",false);
	}
});

//initial check all days
$("input[name=days]").prop("checked",true);
/*
TODO:
- tomar id como parámetro del opener, luego decidir si:
	- if create:
		- popular header como New Access for Door/Person xxx
		- check All days
		- set all other days the same time as All
	- else edit:
		- popular header como Edit Access for Door/Person xxx
		- mark checkboxes acording to days
		- populate date boxes for each access in and out
- make delete function getting all row ids and deleting each one. Hide rows once finished.
- for Add new access, access-edit?personid=selpersonid

Make a edit-access.php that fetches an access ID and sets values for edit
and also taking a personid and allowing the access to be defined
*/


//fetch info for edit
/*
$('#modal-edit').on('show.bs.modal', function (event){
	// If necessary, you could initiate an AJAX request here (and then do the updating in a callback).
	var personId = $("#persons-select").val();
	$.ajax({
		type: "POST",
		url: "process",
		data: "action=get_person&id=" + personId,
		success: function(resp){
			if(resp[0]=='1'){
				//populate fields with rec info
				var values = resp[1];
				$('#person-edit-id').val(personId);
				$('#person-edit-name').val(values.name);
				$('#person-edit-idnum').val(values.identNumber);
				$('#person-edit-cardnum').val(values.cardNumber);
			} else {
				//show modal error
				$('#modal-error .modal-body').text(resp[1]);
				$("#modal-error").modal("show");
			}
		},
		failure: function(){
			//show modal error
			$('#modal-error .modal-body').text("Operation failed, please try again");
			$("#modal-error").modal("show");
		}
	});
});

//new action
$("#person-new-form").submit(function(){
	var personName = $("#person-new-name").val();
	var personIdNum = $("#person-new-idnum").val();
	var personCardNum = $("#person-new-cardnum").val();

	if(personName!="" && personName!='undefined'){
		$.ajax({
			type: "POST",
			url: "process",
			data: "action=add_person&orgid=" + organizationId +"&name=" + personName + "&idnum=" + personIdNum + "&cardnum=" + personCardNum,
			success: function(resp){
				if(resp[0]=='1'){
					//close modal
					$("#modal-new").modal("hide");
					//repopulate select box
					populateList("persons-select","persons",organizationId);
				} else {
					//show modal error
					$('#modal-error .modal-body').text(resp[1]);
					$("#modal-error").modal("show");
				}
			},
			failure: function(){
				//show modal error
				$('#modal-error .modal-body').text("Operation failed, please try again");
				$("#modal-error").modal("show");
			}
		});
	} else {
		//invalid values sent
		$('#modal-error .modal-body').text("Invalid values sent");
		$("#modal-error").modal("show");
	}
	return false;
});

//edit action
$("#person-edit-form").submit(function(){
	var personId = $("#person-edit-id").val();
	var personName = $("#person-edit-name").val();
	var personIdNum = $("#person-edit-idnum").val();
	var personCardNum = $("#person-edit-cardnum").val();

	if(!isNaN(personId) && personName!="" && personName!='undefined'){
		$.ajax({
			type: "POST",
			url: "process",
			data: "action=edit_person&id=" + personId+"&orgid=" + organizationId + "&name=" + personName + "&idnum=" + personIdNum + "&cardnum=" + personCardNum,
			success: function(resp){
				if(resp[0]=='1'){
					//close modal
					$("#modal-edit").modal("hide");
					//repopulate select box
					populateList("persons-select","persons",organizationId);
				} else {
					//show modal error
					$('#modal-error .modal-body').text(resp[1]);
					$("#modal-error").modal("show");
				}
			},
			failure: function(){
				//show modal error
				$('#modal-error .modal-body').text("Operation failed, please try again");
				$("#modal-error").modal("show");
			}
		});
	} else {
		//invalid values sent
		$('#modal-error .modal-body').text("Invalid values sent");
		$("#modal-error").modal("show");
	}
	return false;
});

//delete action
$("#person-delete-form").submit(function(){
	var personId = $("#persons-select").val();

	if(!isNaN(personId)){
		$.ajax({
			type: "POST",
			url: "process",
			data: "action=delete_person&id=" + personId,
			success: function(resp){
				if(resp[0]=='1'){
					//close modal
					$("#modal-delete").modal("hide");
					//repopulate select box
					populateList("persons-select","persons",organizationId);
				} else {
					//show modal error
					$('#modal-error .modal-body').text(resp[1]);
					$("#modal-error").modal("show");
				}
			},
			failure: function(){
				//show modal error
				$('#modal-error .modal-body').text("Operation failed, please try again");
				$("#modal-error").modal("show");
			}
		});
	} else {
		//invalid values sent
		$('#modal-error .modal-body').text("Invalid values sent");
		$("#modal-error").modal("show");
	}
	return false;
});*/
</script>

</body>
</html>