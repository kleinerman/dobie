<?
$leavebodyopen=1;
$include_extra_js=array("clockpicker","datepicker");
include("header.php");
?>
<div id="page-wrapper">

<div class="row">
<div class="col-lg-12">
<h1 class="page-header">Manage Visitors</h1>
</div>
</div>

<div class="row">
<div class="col-lg-5">

<div class="select-container">
<div class="select-container-title">Visit Door Groups</div>
<div class="select-container-body">
<input type="text" name="filter" placeholder="Filter options..." class="form-control data-filter" data-filter="visit-door-groups-select">
<select id="visit-door-groups-select" class="select-options form-control select-options-small" name="visit-door-groups-select" size="2"></select>
</div>
<div class="select-container-footer">
&nbsp;
</div>
</div>

<div class="select-container">
<div class="select-container-title">Visiting Organization</div>
<div class="select-container-body">
<input type="text" name="filter" placeholder="Filter options..." class="form-control data-filter" data-filter="organizations-select">
<select id="organizations-select" class="select-options form-control select-options-small" name="organizations-select" size="2"></select>
</div>
<div class="select-container-footer">
&nbsp;
</div>
</div>

<div class="select-container">
<div class="select-container-title">Card Number</div>
<div class="select-container-body">
<input type="text" name="cardnum" class="form-control data-filter" id="cardnum">
</div>
<div class="select-container-footer">
<button type="button" class="btn btn-success" id="visitors-search">Search</button> 
<button id="visitors-search-reset" class="btn btn-warning" type="button">Reset</button>
</div>
</div>

</div>

<div class="col-lg-7">
<div class="select-container" id="visitors-select-container">
<div class="select-container-title">Visitors</div>
<div class="select-container-body">
<input type="text" name="filter" placeholder="Filter options..." class="form-control data-filter" data-filter="visitors-select">
<select id="visitors-select" class="select-options form-control" name="visitors-select" size="2"></select>
</div>
<div class="select-container-footer">
<button type="button" class="btn btn-success" id="visitors-add" data-toggle="modal" data-target="#modal-new">Add</button> 
<button type="button" class="btn btn-danger" id="visitors-del" data-toggle="modal" data-target="#modal-delete" disabled>Remove</button>
</div>
</div>
</div>

</div>

</div>

<?
include("footer.php");
?>

<!-- MODALS -->
<!-- create modal -->
<div class="modal fade" id="modal-new" tabindex="-1" role="dialog" aria-labelledby="modal-new-label" aria-hidden="true">
<div class="modal-dialog">
<div class="modal-content">
<div class="modal-header">
<button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>
<h4 class="modal-title" id="modal-new-label">Add Visitor</h4>
</div>

<form class="form-horizontal" id="visit-new-form" action="#">
<div class="modal-body">

<div class="wrapper">
<div class="row">

<div class="col-sm-6">
<label class="control-label">Name:</label><br>
<input type="text" class="form-control" id="visit-name" name="name" value="" required maxlength="64">
<br>
<label class="control-label">Identification Number:</label><br>
<input type="text" class="form-control" id="visit-idnum" name="idnum" value="" required maxlength="64">
<br>
<label class="control-label">Card Number:</label><br>
<input type="number" class="form-control" id="visit-cardnum" name="cardnum" value="" min="0" max="2147483646" required>
<br>
<label class="control-label">Expiration:</label><br>
<div class="input-group input_date_container" data-placement="left" data-align="top" data-autoclose="true" title="Expiration Date"><input type="text" class="form-control input_date center" id="expiration-date" value="<?=date("Y-m-d",mktime(0,0,0))?>" required><span class="input-group-addon"><span class="fa fa-calendar"></span></span></div>

<div class="input-group clockpicker" data-placement="bottom" data-align="top" data-autoclose="true" title="Expiration Hour"><input type="text" class="form-control from-input" value="23:59" id="expiration-hour" required><span class="input-group-addon"><span class="fa fa-clock-o"></span></span></div>
</div>

<div class="col-sm-6">

<div class="select-container">
<div class="select-container-title">Visit Door Group</div>
<div class="select-container-body">
<input type="text" name="filter" placeholder="Filter options..." class="form-control data-filter" data-filter="visit-door-groups-select-new">
<select id="visit-door-groups-select-new" class="select-options select-options-small form-control" name="visit-door-groups-select" size="2" multiple required></select>
</div>
<div class="select-container-footer">
</div>
</div>

<div class="select-container">
<div class="select-container-title">Visiting Organization</div>
<div class="select-container-body">
<input type="text" name="filter" placeholder="Filter options..." class="form-control data-filter" data-filter="organizations-select-new">
<select id="organizations-select-new" class="select-options select-options-small form-control" name="organizations-select-new" size="2" required></select>
</div>
<div class="select-container-footer">
</div>
</div>

</div>
</div>
</div>

</div>
<div class="modal-footer">
<button class="btn btn-success" id="visit-new-submit">Save</button>
</div>
</form>
</div>
<!-- /.modal -->
</div>
</div>
<!-- delete modal -->
<div class="modal fade" id="modal-delete" tabindex="-1" role="dialog" aria-hidden="true">
<div class="modal-dialog">
<div class="modal-content">
<div class="modal-body center">
Are you sure?
</div>
<div class="modal-footer center">
<form class="form-horizontal" id="visitors-delete-form" action="#">
<button class="btn btn-success">Ok</button>
<button type="button" class="btn btn-danger" onclick="$('#modal-delete').modal('hide');">Cancel</button>
</form>
</div>
</div>
</div>
<!-- /.modal -->
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

<style>
@media(min-width:768px){
#modal-new .modal-dialog{
	width:670px;
}
}
</style>

<script type="text/javascript">
//init filters
setFilterAction();

//init vars for array values
var visitDoorGroupId;
var organizationId;

//populate select lists
populateList("visit-door-groups-select","visit_door_groups");
populateList("organizations-select","organizations");
populateList("visitors-select","visitors");

//fetch info for new
$('#modal-new').on('show.bs.modal', function (event){
	//populate zones select list
	populateList("visit-door-groups-select-new","visit_door_groups");
	populateList("organizations-select-new","organizations");
	//clear all previous values
	resetForm();
	//init date picker
	$(".input_date").datepicker({dateFormat: "yy-mm-dd"});
	//init clockpicker
	$('.clockpicker').clockpicker();
});

//form reset
$("#visitors-search-reset").click(function(){
	location.reload();
});

//form search
$("#visitors-search").click(function(){
	//get params for post
	var searchVisitDoorGroupId = $('#visit-door-groups-select').val();
	var searchVisitOrgId = $('#organizations-select').val();
	var searchCardnum = $('#cardnum').val();

	//build post action string
	var actionStr="action=get_visitors";
	var actionStrParams=[];

	if(searchVisitDoorGroupId != null && searchVisitDoorGroupId>0) actionStrParams.push("visitdoorgroupid="+searchVisitDoorGroupId);
	if(searchVisitOrgId != null && searchVisitOrgId>0) actionStrParams.push("orgid="+searchVisitOrgId);
	if(searchCardnum != null && searchCardnum>0) actionStrParams.push("cardnum="+searchCardnum);

	//join all params and build string
	if(actionStrParams.length>0) actionStr+="&"+actionStrParams.join("&");

	//populate filtered select list
	populateList("visitors-select","visitors","",actionStr);
});

//toggle buttons
$("#visitors-select").change(function(){
	visitorId=$("#visitors-select").val();
	if(!isNaN(visitorId) && visitorId!="undefined"){
		$("#visitors-del").prop("disabled",false);
	} else {
		$("#visitors-del").prop("disabled",true);
	}
});

function resetForm(){
	//name, id and cardnum
	$("#visit-name,#visit-idnum,#visit-cardnum").val("");
	//clear date and time to defaults
	var dateobj = new Date();
	$("#expiration-date").val(dateobj.getFullYear() + "-" + addZeroPaddingSingle((dateobj.getMonth()+1)) + "-" + addZeroPaddingSingle(dateobj.getDate()));
	$("#expiration-hour").val("23:59");
	//clear visit door group selection
	$("#visit-door-groups-select-new").val([]);
	//clear visiting org
	$("#organizations-select-new").empty();
	//modal title
	$("#modal-new-label").text("Add Visitor");
}

//new/edit action
$("#visit-new-form").submit(function(){
	var visitName = $('#visit-name').val();
	var visitIdNum = $('#visit-idnum').val();
	var visitCardNum = $('#visit-cardnum').val();
	var visitVisitedOrgId = $('#organizations-select-new').val();
	var expirationDate = $("#expiration-date").val();
	var expirationHour = $("#expiration-hour").val();
	//get all visit door groups doors
	var visitDoorGroupIds=[];
	$.each($("#visit-door-groups-select-new option:selected"), function(){
		visitDoorGroupIds.push($(this).val());
	});

	var error = "";

	//validate fields
	if(visitName=="" || visitName == null){
		error = "Please fill the Visit Name field";
	} else if(visitIdNum=="" || visitIdNum == null){
		error = "Please fill the Identification Number field";
	} else if(visitCardNum=="" || visitCardNum == null){
		error = "Please fill the Card Number field";
	} else if(isNaN(visitVisitedOrgId)){
		error = "Please select an Organization";
	} else if(visitDoorGroupIds.length<1){
		error = "Please select at least one Door Group";
	} else {
		$.ajax({
			type: "POST",
			url: "process",
			data: "action=add_visit&name=" + visitName + "&idnum=" + visitIdNum + "&cardnum=" + visitCardNum + "&orgid=" + visitVisitedOrgId + "&expirationdate=" + expirationDate + "&expirationhour=" + expirationHour + "&doorgroupids=" + visitDoorGroupIds.join("|"),
			complete: function(resp){console.log(resp)},
			success: function(resp){
				if(resp[0]=='1'){
					//close modal
					$("#modal-new").modal("hide");
					//repopulate select box
					populateList("visitors-select","visitors");
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
	}

	if(error!=""){
		$('#modal-error .modal-body').text(error);
		$("#modal-error").modal("show");
	}
	return false;
});

//delete action
$("#visitors-delete-form").submit(function(){
	var visitId = $("#visitors-select").val();

	if(!isNaN(visitId)){
		$.ajax({
			type: "POST",
			url: "process",
			data: "action=delete_person&id=" + visitId,
			success: function(resp){
				if(resp[0]=='1'){
					//close modal
					$("#modal-delete").modal("hide");
					//repopulate select box
					populateList("visitors-select","visitors");
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
</script>

</body>
</html>