<?
$leavebodyopen=1;
$requirerole=1;
$include_extra_js=array("clockpicker","datepicker");
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

<div class="select-container valigntop">
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

<div class="select-container valigntop" id="select-container-doors" style="display:none">
<form action="javascript:void(0)">
<div class="select-container-title"><?=get_text("Doors",$lang);?></div>
<div class="select-container-body">
<input type="text" name="filter" placeholder="<?=get_text("Filter options",$lang);?>..." class="form-control data-filter" data-filter="doors-select">
<select id="doors-select" class="select-options form-control" name="doors-select" size="2"<?php if($logged->roleid<2){?> onchange="updateButtons(this.id)"<?}?>></select>
</div>
<div class="select-container-footer">
<button id="doors-select-add" class="btn btn-success" type="button" data-toggle="modal" data-target="#modal-new"><span class="fa fa-plus"></span><span class="hidden-xs"> <?=get_text("Add",$lang);?></span></button>
<button id="doors-select-edit" class="btn btn-primary" type="button" data-toggle="modal" data-target="#modal-new" disabled><span class="fa fa-pen"></span><span class="hidden-xs"> <?=get_text("Edit",$lang);?></span></button>
<button id="doors-select-del" class="btn btn-danger" type="button" data-toggle="modal" data-target="#modal-delete" disabled><span class="fa fa-times"></span><span class="hidden-xs"> <?=get_text("Delete",$lang);?></span></button>
<button id="doors-refresh" class="btn btn-warning" type="button"><span class="fa fa-sync-alt"></span> <span class="hidden-xs"><?=get_text("Refresh",$lang);?></span></button>
</div>
</form>
</div>

<div id="select-container-doors-details" class="details-box" style="display:none">Details</div>

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

<div class="col-sm-4 valigntop" id="timesdoor-container">
<div class="select-container floatleft" style="width:180px !important">
<div class="select-container-title"><?=get_text("Times",$lang);?></div>
<div class="select-container-body">

<div class="displaytable table_padding">
<div class="displayrow"><div class="displaycell left"><?=get_text("Unlock Time (s)",$lang);?></div><div class="displaycell"> <input class="smaller_input" type="number" name="door-unlock-t" id="door-unlock-t" max="99" min="0" value="7" required></div></div>
<div class="displayrow"><div class="displaycell left"><?=get_text("Buzzer Time (s)",$lang);?></div><div class="displaycell"><input class="smaller_input" type="number" name="door-buzzer-t" id="door-buzzer-t" max="99" min="0" value="2" required>
</div></div>
<div class="displayrow"><div class="displaycell left"><?=get_text("Alarm Timeout (s)",$lang);?></div><div class="displaycell"><input class="smaller_input" type="number" name="door-alarm-t" id="door-alarm-t" max="99" min="0" value="60" required><br><br>
</div></div></div>
</div>
</div>

<div class="select-container floatleft" style="width:180px !important">
<div class="select-container-title"><?=get_text("Door Sensor",$lang);?></div>
<div class="select-container-body">
<label><input type="radio" name="door-sensor" value="1"> <?=get_text("NC (Normally Closed)",$lang);?></label>
<label><input type="radio" name="door-sensor" value="0"> <?=get_text("NO (Normally Open)",$lang);?></label>
</div>
</div>
</div>

</div>

<div class="select-container-title"><?=get_text("Unlock Door by Schedule",$lang);?></div>
<br>
<div class="form-group">

<div class="col-xs-5 center">
<table id="profile_weekdays"><tr>
<td id="weekday1" onclick="paintWeekDay(this.id)"><?=get_text("Mon",$lang);?></td><td id="weekday2" onclick="paintWeekDay(this.id)"><?=get_text("Tue",$lang);?></td><td id="weekday3" onclick="paintWeekDay(this.id)"><?=get_text("Wed",$lang);?></td><td id="weekday4" onclick="paintWeekDay(this.id)"><?=get_text("Thu",$lang);?></td><td id="weekday5" onclick="paintWeekDay(this.id)"><?=get_text("Fri",$lang);?></td><td id="weekday6" onclick="paintWeekDay(this.id)"><?=get_text("Sat",$lang);?></td><td id="weekday7" onclick="paintWeekDay(this.id)"><?=get_text("Sun",$lang);?></td>
</tr></table>
<input type="hidden" value="" name="daysofweek" id="daysofweek">
<br>

<div class="input-group clockpicker" data-placement="top" data-align="top" data-autoclose="true" title="<?=get_text("From",$lang);?>"><input type="text" class="form-control from-input" value="00:00" id="schedule-from" name="schedule-from"><span class="input-group-addon"><span class="far fa-clock"></span></span></div>

<div class="input-group clockpicker" data-placement="top" data-align="top" data-autoclose="true" title="<?=get_text("Until",$lang);?>"><input type="text" class="form-control until-input" value="23:59" id="schedule-until" name="schedule-until"><span class="input-group-addon"><span class="far fa-clock"></span></span></div>
</div>

<div class="col-xs-2 center">
<button type="button" class="btn btn-primary" id="btn-schedule-item-add" disabled><span class="fa fa-chevron-right"></span><span class="fa fa-chevron-right"></span></button>
<button type="button" class="btn btn-primary" id="btn-schedule-item-delete" disabled><span class="fa fa-chevron-left"></span><span class="fa fa-chevron-left"></span></button>
</div>

<div class="col-xs-5">

<div class="select-container" id="select-container-schedule-current">
<div class="select-container-body">
<select id="schedule-current-select" class="select-options select-options-small form-control" name="schedule-current-select" size="2" multiple></select>
</div>
<div class="select-container-footer">
</div>
</div>

</div>
</div>

<div class="select-container-title"><?=get_text("Exception Days",$lang);?></div>
<div><?=get_text("Days which the door will not be automatically unlocked (very common for holidays)",$lang);?></div>
<br>

<div class="form-group">

<div class="col-xs-5">
<div class="input-group input_date_container" data-placement="left" data-align="top" data-autoclose="true" title="<?=get_text("Expiration Date",$lang);?>"><input type="text" class="form-control input_date center" id="except-expiration-date" value="<?=date("Y-m-d",mktime(0,0,0))?>" required><span class="input-group-addon"><span class="far fa-calendar-alt"></span></span></div>
</div>

<div class="col-xs-2">
<button type="button" class="btn btn-primary" id="btn-except-item-add"><span class="fa fa-chevron-right"></span><span class="fa fa-chevron-right"></span></button>
<button type="button" class="btn btn-primary" id="btn-except-item-delete" disabled><span class="fa fa-chevron-left"></span><span class="fa fa-chevron-left"></span></button>
</div>

<div class="col-xs-5">
<div class="select-container" id="select-container-except-current">
<div class="select-container-body">
<select id="except-current-select" class="select-options select-options-small form-control" name="except-current-select" size="2" multiple></select>
</div>
<div class="select-container-footer">
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
var controllerArr=[];
var toWeekDayName=["","<?=get_text("Mon",$lang);?>","<?=get_text("Tue",$lang);?>","<?=get_text("Wed",$lang);?>","<?=get_text("Thu",$lang);?>","<?=get_text("Fri",$lang);?>","<?=get_text("Sat",$lang);?>","<?=get_text("Sun",$lang);?>"];
var currSchedules=[];
var currExceptions=[];

var zoneId;

//populate select list
populateList("zones-select","zones");

//function to paint a table cell, allowing multiple days and updating the value in a html var
function paintWeekDay(cellid){
	weekdayobj = document.getElementById(cellid);
	if(weekdayobj){
		targetvalue = document.getElementById("daysofweek").value;
		if(weekdayobj.className=="clicked"){
			weekdayobj.className="";
			document.getElementById("daysofweek").value = targetvalue.replace(new RegExp(cellid, 'g'),"");
			//if no days selected > disable right
			if(document.getElementById("daysofweek").value=="") $("#btn-schedule-item-add").prop("disabled",true);
		} else {
			weekdayobj.className="clicked";
			document.getElementById("daysofweek").value = targetvalue+cellid;
			//enable right
			$("#btn-schedule-item-add").prop("disabled",false);
		}
	}
	//console.log(document.getElementById("daysofweek").value);
}

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
		//hide details
		$('#select-container-doors-details').hide()
	}
});

//populate controller array for details box join
$.ajax({
	type: "POST",
	url: "process",
	data: "action=get_controllers",
	success: function(resp){
		if(resp[0]=='1'){
			//populate controllerArr with [id]=name
			var values = resp[1];
			for(i=0;i<values.length;i++){
				controllerArr[values[i].id]=values[i].name;
			}
		}
	}
});

//populate quick details box on door change
$("#doors-select").change(function(){
	var doorId = $(this).val();
	if(!isNaN(doorId)){
		$.ajax({
			type: "POST",
			url: "process",
			data: "action=get_door&id=" + doorId,
			success: function(resp){
				if(resp[0]=='1'){
					//populate details with rec info
					var values = resp[1];
					if(typeof controllerArr[values.controllerId] != "undefined") $('#select-container-doors-details').html("<?=get_text("Controller",$lang);?>: "+ controllerArr[values.controllerId] + "<br>"); else $('#select-container-doors-details').html("");
					if(values.isVisitExit==1) var isVisitExitText = "<?=get_text("Yes",$lang);?>"; else var isVisitExitText = "<?=get_text("No",$lang);?>";
					if(values.snsrType==1) var snsrTypeText = "<?=get_text("NC (Normally Closed)",$lang);?>"; else var snsrTypeText = "<?=get_text("NO (Normally Open)",$lang);?>";

					$('#select-container-doors-details').append("<?=get_text("Door Number",$lang);?>: "+ values.doorNum +
					"<br><?=get_text("Visit Exit",$lang);?>: " + isVisitExitText + 
					"<br><?=get_text("Unlock Time (s)",$lang);?>: " + values.unlkTime +
					"<br><?=get_text("Buzzer Time (s)",$lang);?>: " + values.bzzrTime + 
					"<br><?=get_text("Alarm Timeout (s)",$lang);?>: " + values.alrmTime + 
                    "<br><?=get_text("Door Sensor",$lang);?>: " + snsrTypeText +
                    "<br><br><a href='javascript:void(0)' onclick='openDoor("+values.id+")' class='btn btn-default btn-xs'><span class='fas fa-door-open'></span> <?=get_text("Open Door",$lang);?></a>");
					//show details
					$('#select-container-doors-details').show()
				} else {
					//hide details
					$('#select-container-doors-details').hide()
				}
			},
			failure: function(){
				//hide details
				$('#select-container-doors-details').hide()
			}
		});
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
	//init date pickers
	$(".input_date").datepicker({dateFormat: "yy-mm-dd"});
	//init clockpickers
	$('.clockpicker').clockpicker();
	//populate select 
	populateList("controllers-select","controllers",0,"","",1);
});

function resetForm(){
	//group name
	$("#door-new-name").val("");
	//empty selects
	$("#controllers-select").empty();
	//disable all buttons
	$("#btn-item-add,#btn-item-delete").prop("disabled",true);
	//unselect options in fixed selects
	$('#door-number-select').empty();
	$('#door-number-select').append("<option value='0' disabled><?=get_text("None",$lang);?>");
	//clear visit exit
	$('#door-visit-exit').prop("checked",false);
	//clear group id value if edit
	editId=0;
	editDoorNum=0;
	//clear schedules
	currSchedules=[];
	$("#schedule-current-select").empty();
	//clear exception days
	currExceptions=[];
	$("#except-current-select").empty();
	//modal title
	$("#modal-new-label").text("<?=get_text("New Door",$lang);?>");
	$('#door-unlock-t').val(7);
	$('#door-buzzer-t').val(2);
	$('#door-alarm-t').val(60);
	$("input[name=door-sensor][value=1]").prop("checked",true);
	$("#controller-select").show();
	//this is to make the last col wider so both times and sensor fit correctly
	$("#timesdoor-container").removeClass("col-sm-9").addClass("col-sm-4");
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

<?php
if($logged->roleid<2){
?>

function populateScheduleList(selectId,id=0){
	$.ajax({
		type: "POST",
		url: "process",
		data: "action=get_uds_door&id="+id,
		success: function(resp){
			//clear current options
			$("#"+selectId).empty();
			if(resp[0]=='1'){
				//append values as options
				var values = resp[1];
				currSchedules=[];
				//console.log(values);
				values.forEach(function(item,index){
					if(item.resStateId!=5){
						itemClass="";
						if(item.resStateId==1) itemClass=" class='toadd' disabled ";
						else if(item.resStateId==2) itemClass=" class='toupd' disabled ";
						else if(item.resStateId==4) itemClass=" class='todel' disabled ";
						$("#"+selectId).append("<option value='"+item.id+"'"+itemClass+">" + toWeekDayName[item.weekDay] + " " + addZeroPadding(item.startTime.slice(0,-3)) + " to " + addZeroPadding(item.endTime.slice(0,-3)));
						//add to current schedules array
						currSchedules.push(item.id);
					}
				});
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

function populateExceptionList(selectId,id=0){
	$.ajax({
		type: "POST",
		url: "process",
		data: "action=get_excdayuds_door&id="+id,
		success: function(resp){
			//clear current options
			$("#"+selectId).empty();
			if(resp[0]=='1'){
				//append values as options
				var values = resp[1];
				//console.log(values);
				values.forEach(function(item,index){
					if(item.resStateId!=5){
						itemClass="";
						if(item.resStateId==1) itemClass=" class='toadd' disabled ";
						else if(item.resStateId==2) itemClass=" class='toupd' disabled ";
						else if(item.resStateId==4) itemClass=" class='todel' disabled ";
						$("#"+selectId).append("<option value='"+item.id+"'"+itemClass+">" + item.excDay);
						//add to current exceptions array
						currExceptions.push(item.id);
					}
				});
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

//open door action
function openDoor(id){
    $.ajax({
        type: "POST",
        url: "process",
        data: "action=open_door&id="+id,
        success: function(resp){
            if(resp[0]=='1'){
                //show success
                $('#modal-error .modal-body').text("<?=get_text("Door has been opened!",$lang);?>");
                $("#modal-error").modal("show");
            } else {
                //show error
                $('#modal-error .modal-body').text("<?=get_text("Operation failed, please try again",$lang);?>");
                $("#modal-error").modal("show");
            }
       },
       failure: function(){
          //show error
          $('#modal-error .modal-body').text("<?=get_text("Operation failed, please try again",$lang);?>");
          $("#modal-error").modal("show");
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
				$('#door-unlock-t').val(values.unlkTime);
				$('#door-buzzer-t').val(values.bzzrTime);
				$('#door-alarm-t').val(values.alrmTime);
				$("input[name=door-sensor][value="+values.snsrType+"]").prop("checked",true);
				//hide controller select > door cant be changed from controller (issue #24)
				$("#controller-select").hide();
				//this is to make the last col wider so both times and sensor fit correctly
				$("#timesdoor-container").removeClass("col-sm-4").addClass("col-sm-9");

				//populate uds
				currSchedules=[];
				populateScheduleList("schedule-current-select",doorId);
				//populate excdayuds
				currExceptions=[];
				populateExceptionList("except-current-select",doorId);
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


//actions for addleft and addright buttons
//on change weekday > enable / disable right arrow button

//on change current schedule select > enable / left right arrow button
$("#schedule-current-select").change(function(){
	if($(this).val()!="undefined") $("#btn-schedule-item-delete").prop("disabled",false);
	else $("#btn-schedule-item-delete").prop("disabled",true);
});

//item add button click action
$("#btn-schedule-item-add").click(function(){
	//split selected days of week
	var boxOptions=$("#daysofweek").val().split("weekday");
	//console.log(boxOptions);
	$.each(boxOptions,function(key,elemid){
		//get dayofweek int
		if(elemid!=""){
			//show in new box
			$("#schedule-current-select").append("<option value='' data-weekday='"+elemid+"' data-from='"+$("#schedule-from").val()+"' data-until='"+$("#schedule-until").val()+"'>"+toWeekDayName[elemid]+" "+$("#schedule-from").val()+" to "+ $("#schedule-until").val() +"</option>");
		}
	});
});

//item delete button click action
$("#btn-schedule-item-delete").click(function(){
	var boxOptions=$("#schedule-current-select option:selected");
	$.each(boxOptions,function(){
		//hide from older box
		$(this).hide().prop("disabled",true);
	});
	//clear current selection
	$("#schedule-current-select").val([]);
	//disable del button
	$("#btn-schedule-item-delete").prop("disabled",true);
});

//now the same but for exceptions

//on change current except select > enable / disable left arrow button
$("#except-current-select").change(function(){
	if($(this).val()!="undefined") $("#btn-except-item-delete").prop("disabled",false);
	else $("#btn-except-item-delete").prop("disabled",true);
});

//item add button click action
$("#btn-except-item-add").click(function(){
	var elemval=$("#except-expiration-date").val();
	//show in current select box
	if($("#except-current-select option[data-value='"+elemval+"']").length>0){
		//toggle if exists
		$("#except-current-select option[data-value='"+elemval+"']").show();
		$("#except-current-select option[data-value='"+elemval+"']").prop("disabled",false);
	} else {
		//if not, append html
		$("#except-current-select").append("<option value='' data-value='"+elemval+"'>"+elemval+"</option>");
	}
});

//item delete button click action
$("#btn-except-item-delete").click(function(){
	var boxOptions=$("#except-current-select option:selected");
	$.each(boxOptions,function(){
		//hide from older box
		$(this).hide().prop("disabled",true);
	});
	//clear current selection
	$("#except-current-select").val([]);
	//disable del button
	$("#btn-except-item-delete").prop("disabled",true);
});


//new action
$("#door-new-form").submit(function(){
	var doorName = $("#door-new-name").val();
	var controllerId = $("#controllers-select").val();
	var doorNumber = $("#door-number-select").val();
	if(typeof($('#door-visit-exit:checked').val())=="undefined") {var isVisitExit = 0} else {var isVisitExit = 1}
	var unlockTime = $('#door-unlock-t').val();
	var buzzerTime = $('#door-buzzer-t').val();
	var alrmTime = $('#door-alarm-t').val();
	var snsrType = $("input[name=door-sensor]:checked").val();
	snsrType = (snsrType%2);

	if(editId!=0 && !isNaN(editId)) action_str="action=edit_door&id=" + editId + "&zoneid=" + zoneId + "&name=" + doorName + "&controllerid=" + controllerId + "&doornum=" + doorNumber + "&isvisitexit=" + isVisitExit + "&unlktime=" + unlockTime + "&bzzrtime=" + buzzerTime + "&alrmtime=" + alrmTime + "&snsrtype=" + snsrType;
	else action_str="action=add_door&zoneid=" + zoneId + "&name=" + doorName + "&controllerid=" + controllerId + "&doornum=" + doorNumber + "&isvisitexit=" + isVisitExit + "&unlktime=" + unlockTime + "&bzzrtime=" + buzzerTime + "&alrmtime=" + alrmTime + "&snsrtype=" + snsrType;


	if(doorName!="" && doorName!='undefined' && !isNaN(zoneId) && !isNaN(controllerId) && !isNaN(doorNumber)  && !isNaN(isVisitExit) && !isNaN(unlockTime) && !isNaN(buzzerTime) && !isNaN(alrmTime) && !isNaN(snsrType)){

		$.ajax({
			type: "POST",
			url: "process",
			data: action_str,
			complete: function(resp){
				//console.log(resp);
			},
			success: function(resp){
				//console.log(resp);
				if(resp[0]=='1'){
					//Update Schedules and Exception Days

					//set door id if edit or create
					if(editId!=0 && !isNaN(editId)) var selDoorId=editId;
					else var selDoorId=resp[2];

					//Schedules:
					var sentSchedules = $("#schedule-current-select option:not([disabled])");
					var valuesKeep = [];

					$.each(sentSchedules,function(key,elem){
						if(elem.value!="") valuesKeep.push(parseInt(elem.value));
						else {
							//add schedule
							$.ajax({
								type: "POST",
								url: "process",
								data: "action=add_uds&doorid=" + selDoorId + "&weekday=" + elem.dataset.weekday + "&starttime=" + elem.dataset.from + "&endtime=" + elem.dataset.until,
								success: function(resp1){
									//console.log(resp1);
								},
								failure: function(){
									//show modal error
									$('#modal-error .modal-body').text("<?=get_text("Operation failed, please try again",$lang);?>");
									$("#modal-error").modal("show");
								}
							});
						}
					});

					//console.log(currSchedules);
					//console.log(valuesKeep);
					//if edit mode > remove deleted schedules from current
					if(editId!=0 && !isNaN(editId) && currSchedules.length>0 && (valuesKeep.length!=currSchedules.length)){
						//get all scheds of door > already on currSchedules[]
						$.each(currSchedules,function(key,elem){
							if(!valuesKeep.includes(elem)){
								//rem schedule
								$.ajax({
									type: "POST",
									url: "process",
									data: "action=delete_uds&id=" + elem,
									success: function(resp2){
										//console.log("removing sched id "+elem);
										//console.log(resp2);
									},
									failure: function(){
										//console.log("Error removing schedule id " + elem);
									}
								});
							}
						});
					}

					//Exception Days:
					var sentExceptions = $("#except-current-select option:not([disabled])");
					valuesKeep = [];
					$.each(sentExceptions,function(key,elem){
						if(elem.value!="") valuesKeep.push(parseInt(elem.value));
						else {
							//console.log(elem);
							//add exception
							$.ajax({
								type: "POST",
								url: "process",
								data: "action=add_excdayuds&doorid=" + selDoorId + "&excday=" + elem.dataset.value,
								success: function(resp3){
									//console.log(resp3);
								},
								failure: function(){
									//show modal error
									$('#modal-error .modal-body').text("<?=get_text("Operation failed, please try again",$lang);?>");
									$("#modal-error").modal("show");
								}
							});
						}
					});

					//console.log(currExceptions);
					//console.log(valuesKeep);
					//if edit mode > remove deleted excepts from current
					if(editId!=0 && !isNaN(editId) && currExceptions.length>0 && (valuesKeep.length!=currExceptions.length)){
						//get all scheds of door > already on currExceptions[]
						$.each(currExceptions,function(key,elem){
							if(!valuesKeep.includes(elem)){
								//rem schedule
								$.ajax({
									type: "POST",
									url: "process",
									data: "action=delete_excdayuds&id=" + elem,
									success: function(resp4){
										//console.log("removing except id "+elem);
										//console.log(resp4);
									},
									failure: function(){
										//console.log("Error removing except id " + elem);
									}
								});
							}
						});
					}
					
					//close modal
					$("#modal-new").modal("hide");
					//repopulate select box
					populateList("doors-select","doors",zoneId);
					//hide details
					$('#select-container-doors-details').hide();

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
					//hide details
					$('#select-container-doors-details').hide();
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

//focus success button on delete modal shown
$("#modal-delete").on("shown.bs.modal",function(){
	$("#door-delete-form .btn-success").focus();
});

<?php
} else {
	//disable all buttons but the refresh one in case of viewer
	echo "$('#doors-select-add,#doors-select-edit,#doors-select-del').prop('disabled', true)";
}
?>

//Refresh button > repopulate list
$("#doors-refresh").click(function(){
	if(!isNaN(zoneId) && zoneId!="undefined") populateList("doors-select","doors",zoneId);
	//disable edit and del buttons
	$("#doors-select-del, #doors-select-edit").prop("disabled",1);
	//hide details
	$('#select-container-doors-details').hide()
});
</script>
</body>
</html>
