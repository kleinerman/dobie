<?
$leavebodyopen=1;
$requirerole=2;
include("header.php");
?>
<div id="page-wrapper">

<div class="row">
<div class="col-lg-12">
<h1 class="page-header"><?=get_text("Doors",$lang);?></h1>
</div>
</div>

<div class="row">
<div class="col-lg-12">

<div class="select-container">
<form action="javascript:void(0)">
<div class="select-container-title"><?=get_text("Zones",$lang);?></div>
<div class="select-container-body">
<input type="text" name="filter" placeholder="<?=get_text("Filter options",$lang);?>..." class="form-control data-filter" data-filter="zones-select">
<select id="zones-select" class="select-options form-control" name="zones-select" size="2"></select>
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
<select id="doors-select" class="select-options form-control" name="doors-select" size="2" onchange="updateButtons(this.id)"></select>
</div>
<div class="select-container-footer">
<button id="doors-select-add" class="btn btn-success" type="button" data-toggle="modal" data-target="#modal-new"><?=get_text("New",$lang);?></button>
<button id="doors-select-edit" class="btn btn-primary" type="button" data-toggle="modal" data-target="#modal-new" disabled><?=get_text("Edit",$lang);?></button>
<button id="doors-select-del" class="btn btn-danger" type="button" data-toggle="modal" data-target="#modal-delete" disabled><?=get_text("Delete",$lang);?></button>
</div>
</form>
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
<div class="modal-dialog modal-wide-mid">
<div class="modal-content">
<div class="modal-header">
<button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>
<h4 class="modal-title" id="modal-new-label"><?=get_text("New Door",$lang);?></h4>
</div>
<form class="form-horizontal" id="door-new-form" action="#">
<div class="modal-body">

<div class="form-group">
 <label class="control-label col-sm-2"><?=get_text("Name",$lang);?>:</label>
 <div class="col-sm-10">
      <input type="text" class="form-control" id="door-new-name" name="name" value="" required maxlength="64">
 </div>
</div>

<div class="form-group">
<div class="col-sm-5" id="controller-select">
<div class="select-container">
<div class="select-container-title"><?=get_text("Controller",$lang);?></div>
<div class="select-container-body">
<input type="text" name="filter" placeholder="<?=get_text("Filter options",$lang);?>..." class="form-control data-filter" data-filter="controllers-select">
<select id="controllers-select" class="select-options select-options-small form-control" name="controllers-select" size="2" required></select>
</div>
<div class="select-container-footer">
&nbsp;
</div>
</div>
</div>

<div class="col-sm-3">
<div class="select-container" style="width:130px !important">
<div class="select-container-title"><?=get_text("Door Number",$lang);?></div>
<div class="select-container-body">
<select id="door-number-select" class="small_input form-control" name="door-number-select" size="3" required>
<option value="0" disabled><?=get_text("None",$lang);?>
</select>
</div>
<div class="select-container-footer">
<div class="left">
<label><input type="checkbox" name="door-visit-exit" id="door-visit-exit"> <?=get_text("Visit Exit",$lang);?></label>
</div>
</div>
</div>
</div>

<div class="col-sm-4">
<div class="select-container">
<div class="select-container-title"><?=get_text("Times",$lang);?></div>
<div class="select-container-body">
<div class="displaytable table_padding">
<div class="displayrow"><div class="displaycell left"><?=get_text("Release Time (s)",$lang);?></div><div class="displaycell"> <input class="smaller_input" type="number" name="door-release-t" id="door-release-t" max="99" min="0" value="7" required></div></div>
<div class="displayrow"><div class="displaycell left"><?=get_text("Buzzer Time (s)",$lang);?></div><div class="displaycell"><input class="smaller_input" type="number" name="door-buzzer-t" id="door-buzzer-t" max="99" min="0" value="2" required>
</div></div>
<div class="displayrow"><div class="displaycell left"><?=get_text("Alarm Timeout (s)",$lang);?></div><div class="displaycell"><input class="smaller_input" type="number" name="door-alarm-t" id="door-alarm-t" max="99" min="0" value="60" required>
</div></div></div>
<br>
<div class="select-container-title"><?=get_text("Door Sensor",$lang);?></div>
<label><input type="radio" name="door-sensor" value="1"> <?=get_text("NC (Normally Closed)",$lang);?></label>
<label><input type="radio" name="door-sensor" value="0"> <?=get_text("NO (Normally Open)",$lang);?></label>
</div>
</div>
</div>

</div>

</div>
<div class="modal-footer">
<button class="btn btn-success" id="door-new-submit"><?=get_text("Save",$lang);?></button>
</div>
</form>
</div>
</div>
<!-- /.modal -->
</div>

<!-- delete modal -->
<div class="modal fade" id="modal-delete" tabindex="-1" role="dialog" aria-hidden="true">
<div class="modal-dialog">
<div class="modal-content">
<div class="modal-body center">
<?=get_text("Deleting this door will remove all events that belong to it",$lang);?>.<br>
<?=get_text("Are you sure",$lang);?>?
</div>
<div class="modal-footer center">
<form class="form-horizontal" id="door-delete-form" action="#">
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

<script type="text/javascript">
//init filters
setFilterAction();
//init vars
var editId=0;
var editDoorNum=0;

var zoneId;

//populate select list
populateList("zones-select","zones");

//populate doors on zones change
$("#zones-select").change(function(){
	zoneId=$("#zones-select").val();
	if(!isNaN(zoneId) && zoneId!="undefined"){
		//populate list
		populateList("doors-select","doors",zoneId);
		//show list
		$("#select-container-doors").fadeIn();
		//disable buttons
		$("#doors-select-edit,#doors-select-del").prop("disabled",true);
	}
});

//populate doors nums on controller change
$("#controllers-select").change(function(){
	controllerId=$("#controllers-select").val();
	if(!isNaN(controllerId) && controllerId!="undefined"){
		//populate list with disableds and hl
		populateListDoorNums("door-number-select",controllerId);
	}
});

//fetch info for new
$('#modal-new').on('show.bs.modal', function (event){
	//clear all previous values
	resetForm();
	//populate select 
	populateList("controllers-select","controllers",0,"","",1);
});

function resetForm(){
	//group name
	$("#door-new-name").val("");
	//empty selects
	$("#controllers-select").empty();
	//unselect options in fixed selects
	$('#door-number-select').empty();
	$('#door-number-select').append("<option value='0' disabled><?=get_text("None",$lang);?>");
	//clear visit exit
	$('#door-visit-exit').prop("checked",false);
	//clear group id value if edit
	editId=0;
	editDoorNum=0;
	//modal title
	$("#modal-new-label").text("<?=get_text("New Door",$lang);?>");
	$('#door-release-t').val(7);
	$('#door-buzzer-t').val(2);
	$('#door-alarm-t').val(60);
	$("input[name=door-sensor][value=1]").prop("checked",true);
	$("#controller-select").show();
}

function populateListDoorNums(selectId,id=0,hlvalue=""){
	$.ajax({
		type: "POST",
		url: "process",
		data: "action=get_controller&id="+id,
		success: function(resp){
			$("#"+selectId).empty();
			var optionsHtml="";
			if(resp[0]=='1'){
				var values = resp[1];
				//show door nums
				//show current door numb if edit
				if(editDoorNum>0 && editControllerId==id){
					//show hl
					optionsHtml+="<option value='"+editDoorNum+"' selected>"+editDoorNum;
				}
				//show all available door nums
				values.availDoors.forEach(function(item,index){
					if(editDoorNum!=item || editControllerId!=id){
 						//show as available
						optionsHtml+="<option value='"+item+"'>"+item;
					}
				});
				//in case none available
				if(optionsHtml=="") optionsHtml = "<option value='' disabled>None";

				$("#"+selectId).append(optionsHtml);
			} else {
				//show error option
				$("#"+selectId).append("<option value='' disabled>"+ resp[1] +"</option>");
			}
		},
		failure: function(){
				//show error option
				$("#"+selectId).append("<option value=''><?=get_text("Operation failed, please try again",$lang);?></option>");
		}
	});
}

//fetch info for edit
$("#doors-select-edit").click(function(){
	//clear all previous values
	var doorId = $("#doors-select").val();
	$.ajax({
		type: "POST",
		url: "process",
		data: "action=get_door&id=" + doorId,
		success: function(resp){
			if(resp[0]=='1'){
				//populate fields with rec info
				var values = resp[1];
				editId=doorId;
				editDoorNum=values.doorNum;
				editControllerId=values.controllerId;
				$('#door-new-name').val(values.name);
				//populate controllers hl the correct one
				populateList("controllers-select","controllers",0,"",values.controllerId);
				//select correct door number
				//$('#door-number-select option[value='+values.doorNum+']').prop("selected",true);
				populateListDoorNums("door-number-select",values.controllerId);
				//check visit exit
				if(values.isVisitExit) $('#door-visit-exit').prop("checked",true);
				else $('#door-visit-exit').prop("checked",false);
				//modal title
				$("#modal-new-label").text("<?=get_text("Edit Door",$lang);?>");
				//fill time number fields
				$('#door-release-t').val(values.rlseTime);
				$('#door-buzzer-t').val(values.bzzrTime);
				$('#door-alarm-t').val(values.alrmTime);
				$("input[name=door-sensor][value="+values.snsrType+"]").prop("checked",true);
				//hide controller select > door cant be changed from controller (issue #24)
				$("#controller-select").hide();
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
});

//new action
$("#door-new-form").submit(function(){
	var doorName = $("#door-new-name").val();
	var controllerId = $("#controllers-select").val();
	var doorNumber = $("#door-number-select").val();
	if(typeof($('#door-visit-exit:checked').val())=="undefined") {var isVisitExit = 0} else {var isVisitExit = 1}
	var releaseTime = $('#door-release-t').val();
	var buzzerTime = $('#door-buzzer-t').val();
	var alrmTime = $('#door-alarm-t').val();
	var snsrType = $("input[name=door-sensor]:checked").val();
	snsrType = (snsrType%2);

	if(editId!=0 && !isNaN(editId)) action_str="action=edit_door&id=" + editId + "&zoneid=" + zoneId + "&name=" + doorName + "&controllerid=" + controllerId + "&doornum=" + doorNumber + "&isvisitexit=" + isVisitExit + "&rlsetime=" + releaseTime + "&bzzrtime=" + buzzerTime + "&alrmtime=" + alrmTime + "&snsrtype=" + snsrType;
	else action_str="action=add_door&zoneid=" + zoneId + "&name=" + doorName + "&controllerid=" + controllerId + "&doornum=" + doorNumber + "&isvisitexit=" + isVisitExit + "&rlsetime=" + releaseTime + "&bzzrtime=" + buzzerTime + "&alrmtime=" + alrmTime + "&snsrtype=" + snsrType;

	if(doorName!="" && doorName!='undefined' && !isNaN(zoneId) && !isNaN(controllerId) && !isNaN(doorNumber)  && !isNaN(isVisitExit) && !isNaN(releaseTime) && !isNaN(buzzerTime) && !isNaN(alrmTime) && !isNaN(snsrType)){
		$.ajax({
			type: "POST",
			url: "process",
			data: action_str,
			success: function(resp){
				if(resp[0]=='1'){
					//close modal
					$("#modal-new").modal("hide");
					//repopulate select box
					populateList("doors-select","doors",zoneId);
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
		$('#modal-error .modal-body').text("<?=get_text("Invalid values sent",$lang);?>");
		$("#modal-error").modal("show");
	}
	return false;
});

//delete action
$("#door-delete-form").submit(function(){
	var doorId = $("#doors-select").val();

	if(!isNaN(doorId)){
		$.ajax({
			type: "POST",
			url: "process",
			data: "action=delete_door&id=" + doorId,
			success: function(resp){
				if(resp[0]=='1'){
					//close modal
					$("#modal-delete").modal("hide");
					//repopulate select box
					populateList("doors-select","doors",zoneId);
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
		$('#modal-error .modal-body').text("<?=get_text("Invalid values sent",$lang);?>");
		$("#modal-error").modal("show");
	}
	return false;
});
</script>

</body>
</html>