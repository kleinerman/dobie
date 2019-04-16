<?
$leavebodyopen=1;
$include_extra_js=array("clockpicker","datepicker");
include("header.php");
?>
<div id="page-wrapper">

<div class="row">
<div class="col-lg-12">
<h1 class="page-header"><?=get_text("Manage Visitors",$lang);?></h1>
</div>
</div>

<div class="row">
<div class="col-md-4">

<div class="select-container">
<div class="select-container-title"><?=get_text("Visit Door Groups",$lang);?></div>
<div class="select-container-body">
<input type="text" name="filter" placeholder="<?=get_text("Filter options",$lang);?>..." class="form-control data-filter" data-filter="visit-door-groups-select">
<select id="visit-door-groups-select" class="select-options form-control select-options-small" name="visit-door-groups-select" size="2"></select>
</div>
<div class="select-container-footer">
&nbsp;
</div>
</div>

<div class="select-container">
<div class="select-container-title"><?=get_text("Visiting Organization",$lang);?></div>
<div class="select-container-body">
<input type="text" name="filter" placeholder="<?=get_text("Filter options",$lang);?>..." class="form-control data-filter" data-filter="organizations-select">
<select id="organizations-select" class="select-options form-control select-options-small" name="organizations-select" size="2"></select>
</div>
<div class="select-container-footer">
&nbsp;
</div>
</div>

<div class="select-container">
<div class="select-container-title"><?=get_text("Card Number",$lang);?></div>
<div class="select-container-body">
<input type="text" name="cardnum" class="form-control data-filter" id="cardnum">
</div>
<div class="select-container-footer">
<button type="button" class="btn btn-success" id="visitors-search"><span class="fa fa-search"></span> <span class="hidden-xs"><?=get_text("Search",$lang);?></span></button> 
<button id="visitors-search-reset" class="btn btn-warning" type="button"><span class="fa fa-power-off"></span> <span class="hidden-xs"><?=get_text("Reset",$lang);?></span></button>
</div>
</div>

</div>

<div class="col-md-4">
<div class="select-container" id="visitors-select-container">
<div class="select-container-title"><?=get_text("Visitors",$lang);?></div>
<div class="select-container-body">
<input type="text" name="filter" placeholder="<?=get_text("Filter options",$lang);?>..." class="form-control data-filter" data-filter="visitors-select">
<select id="visitors-select" class="select-options form-control" name="visitors-select" size="2"></select>
</div>
<div class="select-container-footer">
<button type="button" class="btn btn-success" id="visitors-add" data-toggle="modal" data-target="#modal-new"><span class="fa fa-plus"></span> <span class="hidden-xs"><?=get_text("Add",$lang);?></span></button>
<button type="button" class="btn btn-primary" id="visitors-edit" data-toggle="modal" data-target="#modal-edit" disabled><span class="fa fa-pen"></span> <span class="hidden-xs"><?=get_text("Edit",$lang);?></span></button> 
<button type="button" class="btn btn-danger" id="visitors-del" data-toggle="modal" data-target="#modal-delete" disabled><span class="fa fa-times"></span> <span class="hidden-xs"><?=get_text("Remove",$lang);?></span></button>
<button id="visitors-refresh" class="btn btn-warning" type="button"><span class="fa fa-sync-alt"></span> <span class="hidden-xs"><?=get_text("Refresh",$lang);?></span></button>
</div>
</div>
</div>

<div class="col-md-4">
<div id="select-container-visitors-details"></div>
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
<h4 class="modal-title" id="modal-new-label"><?=get_text("Add Visitor",$lang);?></h4>
</div>

<form class="form-horizontal" id="visit-new-form" action="#">
<div class="modal-body">

<div class="wrapper">
<div class="row">

<div class="col-sm-6">
<label class="control-label"><?=get_text("Identification Number",$lang);?>:</label><br>
<input type="text" class="form-control" id="visit-idnum" name="idnum" value="" required maxlength="64">
<br>
<label class="control-label"><?=get_text("First Name",$lang);?>:</label><br>
<input type="text" class="form-control" id="visit-names" name="names" value="" required maxlength="64">
<br>
<label class="control-label"><?=get_text("Last Name",$lang);?>:</label><br>
<input type="text" class="form-control" id="visit-lastname" name="lastname" value="" required maxlength="64">
<br>
<label class="control-label"><?=get_text("Note",$lang);?>:</label><br>
<input type="text" class="form-control" id="visit-new-note" name="note" value="" maxlength="256">
<br>
<label class="control-label"><?=get_text("Card Number",$lang);?> (Raw):</label><br>
<input type="number" class="form-control" id="visit-new-cardnum" name="cardnum" value="" min="0" max="2147483646" required>
<br>
<label class="control-label"><?=get_text("Card Number",$lang);?> (FC):</label><br>
<input type="text" class="form-control small_input" id="visit-new-cardnum-fc-1" name="cardnumfc1" value="" maxlength="3"> , <input type="text" class="form-control" id="visit-new-cardnum-fc-2" name="cardnumfc2" value="" maxlength="32">
<br><br>
<label class="control-label"><?=get_text("Expiration",$lang);?>:</label><br>
<div class="input-group input_date_container" data-placement="left" data-align="top" data-autoclose="true" title="<?=get_text("Expiration Date",$lang);?>"><input type="text" class="form-control input_date center" id="expiration-date" value="<?=date("Y-m-d",mktime(0,0,0))?>" required><span class="input-group-addon"><span class="far fa-calendar-alt"></span></span></div>

<div class="input-group clockpicker" data-placement="bottom" data-align="top" data-autoclose="true" title="<?=get_text("Expiration Hour",$lang);?>"><input type="text" class="form-control from-input" value="23:59" id="expiration-hour" required><span class="input-group-addon"><span class="far fa-clock"></span></span></div>
</div>

<div class="col-sm-6">

<div class="select-container">
<div class="select-container-title"><?=get_text("Visit Door Group",$lang);?></div>
<div class="select-container-body">
<input type="text" name="filter" placeholder="<?=get_text("Filter options",$lang);?>..." class="form-control data-filter" data-filter="visit-door-groups-select-new">
<select id="visit-door-groups-select-new" class="select-options select-options-small form-control" name="visit-door-groups-select" size="2" multiple required></select>
</div>
<div class="select-container-footer">
</div>
</div>

<div class="select-container">
<div class="select-container-title"><?=get_text("Visiting Organization",$lang);?></div>
<div class="select-container-body">
<input type="text" name="filter" placeholder="<?=get_text("Filter options",$lang);?>..." class="form-control data-filter" data-filter="organizations-select-new">
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
<button class="btn btn-success" id="visit-new-submit"><?=get_text("Save",$lang);?></button>
</div>
</form>
</div>
<!-- /.modal -->
</div>
</div>

<!-- edit modal -->
<div class="modal fade" id="modal-edit" tabindex="-1" role="dialog" aria-labelledby="modal-edit-label" aria-hidden="true">
<div class="modal-dialog">
<div class="modal-content">
<div class="modal-header">
<button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>
<h4 class="modal-title" id="modal-edit-label"><?=get_text("Edit Visitor",$lang);?></h4>
</div>

<form class="form-horizontal" id="visit-edit-form" action="#">
<div class="modal-body">

<div class="wrapper">
<div class="row">

<div class="col-sm-6">
<label class="control-label"><?=get_text("Identification Number",$lang);?>:</label><br>
<input type="text" class="form-control" id="visit-edit-idnum" name="idnum" value="" required maxlength="64">
<br>
<label class="control-label"><?=get_text("First Name",$lang);?>:</label><br>
<input type="text" class="form-control" id="visit-edit-names" name="names" value="" required maxlength="64">
<br>
<label class="control-label"><?=get_text("Last Name",$lang);?>:</label><br>
<input type="text" class="form-control" id="visit-edit-lastname" name="lastname" value="" required maxlength="64">
<br>
<label class="control-label"><?=get_text("Note",$lang);?>:</label><br>
<input type="text" class="form-control" id="visit-edit-note" name="note" value="" maxlength="256">
<br>
<label class="control-label"><?=get_text("Card Number",$lang);?> (Raw):</label><br>
<input type="number" class="form-control" id="visit-edit-cardnum" name="cardnum" value="" min="0" max="2147483646" required>
<br>
<label class="control-label"><?=get_text("Card Number",$lang);?> (FC):</label><br>
<input type="text" class="form-control small_input" id="visit-edit-cardnum-fc-1" name="cardnumfc1" value="" maxlength="3"> , <input type="text" class="form-control" id="visit-edit-cardnum-fc-2" name="cardnumfc2" value="" maxlength="32">
<br>
</div>

<div class="col-sm-6">

<div class="select-container">
<div class="select-container-title"><?=get_text("Visiting Organization",$lang);?></div>
<div class="select-container-body">
<input type="text" name="filter" placeholder="<?=get_text("Filter options",$lang);?>..." class="form-control data-filter" data-filter="organizations-select-edit">
<select id="organizations-select-edit" class="select-options select-options-small form-control" name="organizations-select-edit" size="2" required></select>
</div>
<div class="select-container-footer">
</div>
</div>

</div>
</div>
</div>

</div>
<div class="modal-footer">
<button class="btn btn-success" id="visit-edit-submit"><?=get_text("Save",$lang);?></button>
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
<?=get_text("Are you sure",$lang);?>?
</div>
<div class="modal-footer center">
<form class="form-horizontal" id="visitors-delete-form" action="#">
<button class="btn btn-success"><?=get_text("Yes",$lang);?></button>
<button type="button" class="btn btn-danger" onclick="$('#modal-delete').modal('hide');"><?=get_text("Cancel",$lang);?></button>
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
#modal-new .modal-dialog, #modal-edit .modal-dialog{
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
var editId=0;

//populate select lists
populateList("visit-door-groups-select","visit_door_groups");
populateList("organizations-select","organizations");
populateList("visitors-select","visitors");

//init events for cardnum fields (update and live calculation on input)
addCardnumEvents("visit-edit");
addCardnumEvents("visit-new");

//fetch info for new
$('#modal-new').on('show.bs.modal', function (event){
	//populate select lists
	populateList("visit-door-groups-select-new","visit_door_groups");
	populateList("organizations-select-new","organizations");
	//clear all previous values
	resetForm();
	//init date pickers
	$(".input_date").datepicker({dateFormat: "yy-mm-dd"});
	//init clockpickers
	$('.clockpicker').clockpicker();
});

//fetch info for edit
$('#modal-edit').on('show.bs.modal', function (event){
	var visitId = $("#visitors-select").val();
	if(!isNaN(visitId)){
		$.ajax({
			type: "POST",
			url: "process",
			data: "action=get_person&id=" + visitId,
			success: function(resp){
				if(resp[0]=='1'){
					//clear all previous values
					resetFormEdit();
					//populate fields with rec info
					var values = resp[1];
					editId=visitId;
					$('#visit-edit-id').val(visitId);
					$('#visit-edit-names').val(values.names);
					$('#visit-edit-lastname').val(values.lastName);
					$('#visit-edit-idnum').val(values.identNumber);
					$('#visit-edit-cardnum').val(values.cardNumber);
					$('#visit-edit-note').val(values.note);
					var tempfc=rawToFC(values.cardNumber).split(",");
					if(tempfc.length==2) {
						$('#visit-edit-cardnum-fc-1').val(myTrim(tempfc[0]));
						$('#visit-edit-cardnum-fc-2').val(myTrim(tempfc[1]));
					} else {
						$('#visit-edit-cardnum-fc-1').val("");
						$('#visit-edit-cardnum-fc-2').val("");
					}
					//populate select lists
					populateList("organizations-select-edit","organizations",0,"",values.visitedOrgId);
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
	}
});

//form reset
$("#visitors-search-reset").click(function(){
	location.reload();
});

//form search
$("#visitors-search, #visitors-refresh").click(function(){
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
	//hide details
	$('#select-container-visitors-details').hide();
	//clear filter values
	$('#visitors-select-container .data-filter').val("");

});

//toggle buttons and populate details
$("#visitors-select").change(function(){
	visitorId=$("#visitors-select").val();
	if(!isNaN(visitorId) && visitorId!="undefined"){
		$("#visitors-del,#visitors-edit").prop("disabled",false);
		$.ajax({
			type: "POST",
			url: "process",
			data: "action=get_person&id=" + visitorId,
			success: function(resp){
				if(resp[0]=='1'){
					//populate details with rec info
					var values = resp[1];
					$('#select-container-visitors-details').html("<?=get_text("Identification Number",$lang);?>: "+ values.identNumber +
					"<br><?=get_text("Card Number",$lang);?>: " + values.cardNumber + " - " + rawToFC(values.cardNumber));
					if(values.note!="") $('#select-container-visitors-details').append("<br><?=get_text("Note",$lang);?>: " + values.note);
					//show details
					$('#select-container-visitors-details').show()
				} else {
					//hide details
					$('#select-container-visitors-details').hide()
				}
			},
			failure: function(){
				//hide details
				$('#select-container-visitors-details').hide()
			}
		});
	} else {
		$("#visitors-del,#visitors-edit").prop("disabled",true);
	}
});

function resetForm(){
	//name, id and cardnum
	$("#visit-names,#visit-lastname,#visit-idnum,#visit-new-cardnum,#visit-new-cardnum-fc-1,#visit-new-cardnum-fc-2,#visit-new-note").val("");
	//clear date and time to defaults
	var dateobj = new Date();
	$("#expiration-date").val(dateobj.getFullYear() + "-" + addZeroPaddingSingle((dateobj.getMonth()+1)) + "-" + addZeroPaddingSingle(dateobj.getDate()));
	$("#expiration-hour").val("23:59");
	//clear visit door group selection
	$("#visit-door-groups-select-new").val([]);
	//clear visiting org
	$("#organizations-select-new").empty();
	editId=0;
}

function resetFormEdit(){
	//clear all previous values
	$("#visit-edit-names,#visit-edit-lastname,#visit-edit-idnum,#visit-edit-cardnum,#visit-edit-cardnum-fc-1,#visit-edit-cardnum-fc-2,#visit-edit-note").val("");
	//clear visiting org
	$("#organizations-select-edit").empty();
	//modal title
	$("#modal-new-label").text("<?=get_text("Edit Visitor",$lang);?>");
	editId=0;
}

//get visitor if exists and populate details on add
$("#visit-idnum").change(function(){
	visitIdNum=$(this).val();
	if(visitIdNum!="" && !isNaN(visitIdNum)){
		$.ajax({
			type: "POST",
			url: "process",
			data: "action=get_visitors&idnum=" + visitIdNum,
			success: function(resp){
				if(resp[0]=='1'){
					var values = resp[1];
					if(values.length>0){
						//get the first result of the query
						values=values[0];
						$('#visit-names').val(values.names);
						$('#visit-lastname').val(values.lastName);
						$('#visit-new-note').val(values.note);
						$('#organizations-select-new option[value='+values.visitedOrgId+']').prop("selected",true);
					}
				}
			}
		});
	}
});

//new action
$("#visit-new-form").submit(function(){
	var visitNames = $('#visit-names').val();
	var visitLastName = $('#visit-lastname').val();
	var visitIdNum = $('#visit-idnum').val();
	var visitCardNum = $('#visit-new-cardnum').val();
	var visitVisitedOrgId = $('#organizations-select-new').val();
	var expirationDate = $("#expiration-date").val();
	var expirationHour = $("#expiration-hour").val();
	var visitNote = $("#visit-new-note").val();
	//get all visit door groups doors
	var visitDoorGroupIds=[];
	$.each($("#visit-door-groups-select-new option:selected"), function(){
		visitDoorGroupIds.push($(this).val());
	});

	var error = "";

	//validate fields
	if(visitNames=="" || visitNames == null){
		error = "<?=get_text("Please fill the Visit Names field",$lang);?>";
	} else if(visitLastName=="" || visitLastName == null){
		error = "<?=get_text("Please fill the Visit Last Name field",$lang);?>";
	} else if(visitIdNum=="" || visitIdNum == null){
		error = "<?=get_text("Please fill the Identification Number field",$lang);?>";
	} else if(visitCardNum=="" || visitCardNum == null){
		error = "<?=get_text("Please fill the Card Number field",$lang);?>";
	} else if(isNaN(visitVisitedOrgId)){
		error = "<?=get_text("Please select an Organization",$lang);?>";
	} else if(visitDoorGroupIds.length<1){
		error = "<?=get_text("Please select at least one Door Group",$lang);?>";
	} else {
		$.ajax({
			type: "POST",
			url: "process",
			data: "action=add_visit&names=" + visitNames + "&lastname=" + visitLastName + "&idnum=" + visitIdNum + "&cardnum=" + visitCardNum + "&orgid=" + visitVisitedOrgId + "&expirationdate=" + expirationDate + "&expirationhour=" + expirationHour + "&note=" + visitNote + "&doorgroupids=" + visitDoorGroupIds.join("|"),
			success: function(resp){
				if(resp[0]=='1'){
					//close modal
					$("#modal-new").modal("hide");
					//repopulate select box
					//populateList("visitors-select","visitors");
					//do it with the search button instead
					$("#visitors-search").click();
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
	}

	if(error!=""){
		$('#modal-error .modal-body').text(error);
		$("#modal-error").modal("show");
	}
	return false;
});

//edit action
$("#visit-edit-form").submit(function(){
	var visitNames = $('#visit-edit-names').val();
	var visitLastName = $('#visit-edit-lastname').val();
	var visitIdNum = $('#visit-edit-idnum').val();
	var visitCardNum = $('#visit-edit-cardnum').val();
	var visitVisitedOrgId = $('#organizations-select-edit').val();
	var visitNote = $("#visit-edit-note").val();

	var error = "";

	//validate fields
	if(visitNames=="" || visitNames == null){
		error = "<?=get_text("Please fill the Visit Names field",$lang);?>";
	} else if(visitLastName=="" || visitLastName == null){
		error = "<?=get_text("Please fill the Visit Last Name field",$lang);?>";
	} else if(visitIdNum=="" || visitIdNum == null){
		error = "<?=get_text("Please fill the Identification Number field",$lang);?>";
	} else if(visitCardNum=="" || visitCardNum == null){
		error = "<?=get_text("Please fill the Card Number field",$lang);?>";
	} else if(isNaN(visitVisitedOrgId)){
		error = "<?=get_text("Please select an Organization",$lang);?>";
	} else if(isNaN(editId)){
		error = "<?=get_text("Invalid visit selected",$lang);?>";
	} else {
		$.ajax({
			type: "POST",
			url: "process",
			data: "action=edit_visit&id="+ editId +"&names=" + visitNames + "&lastname=" + visitLastName + "&idnum=" + visitIdNum + "&cardnum=" + visitCardNum + "&orgid=" + visitVisitedOrgId + "&note=" + visitNote,
			success: function(resp){
				if(resp[0]=='1'){
					//close modal
					$("#modal-edit").modal("hide");
					//repopulate select box
					//populateList("visitors-select","visitors");
					//do it with the search button instead
					$("#visitors-search").click();
					//hide details
					//$('#select-container-visitors-details').hide()
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
					//populateList("visitors-select","visitors");
					//do it with the search button instead
					$("#visitors-search").click();
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
		//invalid values sent
		$('#modal-error .modal-body').text("Invalid values sent");
		$("#modal-error").modal("show");
	}
	return false;
});
/*
//Refresh button > repopulate list
$("#visitors-refresh").click(function(){
	populateList("visitors-select","visitors");
	//hide details
	$('#select-container-visitors-details').hide();
	//disable edit and del buttons
	$("#visitors-del,#visitors-edit").prop("disabled",1);
	//clear filter values
	$('#visit-door-groups-select option, #organizations-select option').prop("selected",false);
	$('#cardnum').val("");
});*/
</script>

</body>
</html>