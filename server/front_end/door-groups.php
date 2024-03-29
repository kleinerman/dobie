<?php
$leavebodyopen=1;
$requirerole=2;
include("header.php");
?>
<div id="page-wrapper">

<div class="row">
<div class="col-lg-12">
<h1 class="page-header"><?=get_text("Door Groups",$lang);?></h1>
</div>
</div>

<div class="row">
<div class="col-lg-12">

<div class="select-container">
<form action="javascript:void(0)">
<div class="select-container-title"><?=get_text("Groups",$lang);?></div>
<div class="select-container-body">
<input type="text" name="filter" placeholder="<?=get_text("Filter options",$lang);?>..." class="form-control data-filter" data-filter="door-groups-select">
<select id="door-groups-select" class="select-options form-control" name="door-groups-select" size="2"></select>
</div>
<div class="select-container-footer">
<button id="door-groups-select-add" class="btn btn-success" type="button" data-toggle="modal" data-target="#modal-new"><span class="fa fa-plus"></span><span class="hidden-xs"> <?=get_text("Add",$lang);?></span></button>
<button id="door-groups-select-edit" class="btn btn-primary" type="button" data-toggle="modal" data-target="#modal-new" disabled><span class="fa fa-pen"></span><span class="hidden-xs"> <?=get_text("Edit",$lang);?></span></button>
<button id="door-groups-select-del" class="btn btn-danger" type="button" data-toggle="modal" data-target="#modal-delete" disabled><span class="fa fa-times"></span><span class="hidden-xs"> <?=get_text("Delete",$lang);?></span></button>
<div class="legend"><span class="vdg-row">&nbsp;&nbsp;&nbsp;&nbsp;</span> = <?=get_text("Visit Door Groups",$lang);?></div>
<div class="legend"><span class="bdg-row">&nbsp;&nbsp;&nbsp;&nbsp;</span> = <?=get_text("Belongs to Org.",$lang);?></div>
</div>
</form>
</div>

<div id="select-container-door-groups-details" class="details-box" style="display:none">Details</div>

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
<h4 class="modal-title" id="modal-new-label"><?=get_text("New Door Group",$lang);?></h4>
</div>
<div class="modal-body">

<form class="form-horizontal" id="door-groups-new-form" action="#">
<div class="form-group">
 <label class="control-label col-sm-2"><?=get_text("Name",$lang);?>:</label>
 <div class="col-sm-10">
      <input type="text" class="form-control" id="door-groups-new-name" name="name" value="" required maxlength="64">
 </div>
</div>

 <div class="wrapper">
 <div class="row">
 <div class="col-sm-5">
<!--selects--> 
<div class="select-container">
<div class="select-container-title"><?=get_text("Zones",$lang);?></div>
<div class="select-container-body">
<input type="text" name="filter" placeholder="<?=get_text("Filter options",$lang);?>..." class="form-control data-filter" data-filter="zones-select">
<select id="zones-select" class="select-options form-control select-options-small" name="zones-select" size="2"></select>
</div>
<div class="select-container-footer">
&nbsp;
</div>
</div>

<div class="select-container" id="select-container-doors" style="display:none">
<div class="select-container-title"><?=get_text("Doors",$lang);?></div>
<div class="select-container-body">
<input type="text" name="filter" placeholder="<?=get_text("Filter options",$lang);?>..." class="form-control data-filter" data-filter="doors-select">
<select id="doors-select" class="select-options form-control select-options-small" name="doors-select[]" size="2" multiple></select>
</div>
<div class="select-container-footer">
<button type="button" class="btn btn-success" id="doors-group-selectall"><?=get_text("Select all",$lang);?></button>
<br><br>

<div id="direction-container" class="displaytable table_padding margincenter hidden">
<div class="displayrow">
<div class="displaycell"><label><?=get_text("Incoming",$lang);?><br><input type="radio" name="side" value="1"></label></div>
<div class="displaycell"><label><?=get_text("Outgoing",$lang);?><br><input type="radio" name="side" value="0"></label></div>
<div class="displaycell"><label><?=get_text("Both",$lang);?><br><input type="radio" id="side-both" name="side" value="" checked></label></div>
</div></div>
<br>

</div>
</div>
 
 </div>
 <div class="col-sm-2 center valignbottom">
 <div style="margin-top:290px;"> 
<button type="button" class="btn btn-primary" id="btn-item-add" disabled><span class="fa fa-chevron-right"></span><span class="fa fa-chevron-right"></span></button>
<button type="button" class="btn btn-primary" id="btn-item-delete" disabled><span class="fa fa-chevron-left"></span><span class="fa fa-chevron-left"></span></button><br>
</div>
 </div>
 <div class="col-sm-5">

<div class="select-container" id="select-container-doors-group-current">
<div class="select-container-title"><?=get_text("Doors in the group",$lang);?></div>
<div class="select-container-body">
<input type="text" name="filter" placeholder="<?=get_text("Filter options",$lang);?>..." class="form-control data-filter" data-filter="doors-group-current-select">
<select id="doors-group-current-select" class="select-options form-control" name="doors-group-current-select" size="2" multiple></select>
<br>
<div class="legend">
<span class="color-legend side-color1">&nbsp;</span> = <?=get_text("Incoming",$lang);?>
<span class="color-legend side-color0">&nbsp;</span> = <?=get_text("Outgoing",$lang);?>
<span class="color-legend side-color">&nbsp;</span> = <?=get_text("Both",$lang);?>
</div>

<br><br>
<label id="isvisit-container"><input type="checkbox" name="isvisit" id="isvisit" value="1"> <?=get_text("For Visits",$lang);?></label>
<br>

<div id="belongs-container">
<label><input type="checkbox" name="doors-group-orgid-check" id="doors-group-orgid-check" value="1"> <?=get_text("Belongs to Org.",$lang);?></label>
<div id="doors-group-orgid-container">
<select id="doors-group-orgid" name="doors-group-orgid"></select>
</div>
</div>

</div>
<div class="select-container-footer">
</div>
</div>
 
 </div>

 </div>
</div>
<div class="modal-footer">
<button class="btn btn-success" id="door-groups-new-submit"><?=get_text("Save",$lang);?></button>
</div>
</form>
</div>
</div>
</div>
<!-- /.modal -->
</div>

<!-- delete modal -->
<div class="modal fade" id="modal-delete" tabindex="-1" role="dialog" aria-hidden="true">
<div class="modal-dialog">
<div class="modal-content">
<div class="modal-body center">
<?=get_text("Are you sure",$lang);?>?
</div>
<div class="modal-footer center">
<form class="form-horizontal" id="door-groups-delete-form" action="#">
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
#modal-new .modal-dialog{
	width:670px;
}
}
</style>

<script>
//init filters
setFilterAction();

//init vars for array values
var DoorGroupId;
var zoneId;
var arrDoors=[];
var arrGroupDoors=[];
var arrGroupDoorsSides=[];
var editId=0;
var orgNames=[];

//populate select list
populateList("door-groups-select","door_groups");

//populate org names array
$(function(){
	$.ajax({
		type: "POST",
		url: "process",
		data: "action=get_organizations",
		success: function(resp){
			if(resp[0]=='1'){
				var values = resp[1];
				//copy values into orgNames array
				values.forEach(function(item,index){
					if(item.id>1) orgNames[item.id]=item.name; //without Visitors org
				});
			} else {
				//show modal error
				$('#modal-error .modal-body').text("<?=get_text("Could not get organization names",$lang);?>");
				$("#modal-error").modal("show");
			}
		},
		failure: function(){
			//show modal error
			$('#modal-error .modal-body').text("<?=get_text("Could not get organization names",$lang);?>");
			$("#modal-error").modal("show");
		}
	});
});

//onchange action on groups select
$("#door-groups-select").change(function(){
	updateButtons($(this).prop("id"));

	var doorGroupIdDetail = $(this).val();
	if(!isNaN(doorGroupIdDetail)){
		$.ajax({
			type: "POST",
			url: "process",
			data: "action=get_door_group_doors&id=" + doorGroupIdDetail,
			success: function(doors_resp){
				if(doors_resp[0]=='1'){
					$('#select-container-door-groups-details').html("");
					var doors_values = doors_resp[1];
					if(doors_values.length>0){
						$('#select-container-door-groups-details').html("<span class='bold underline'><?=get_text("Doors",$lang);?>:</span> <br>");
						//fill select with door data
						for(var i=0;i<doors_values.length;i++){
							$('#select-container-door-groups-details').append(doors_values[i].name + "<br>");
						}
						//show details
						$('#select-container-door-groups-details').show()
					}
				} else {
					//hide details
					$('#select-container-door-groups-details').hide()
				}
			},
			failure: function(){
				//hide details
				$('#select-container-door-groups-details').hide()
			}
		});
	}
});

//onchange action on zones select
$("#zones-select").change(function(){
	zoneId=$("#zones-select").val();
	if(!isNaN(zoneId) && typeof zoneId!="undefined"){
		//populate list
		populateList("doors-select","doors",zoneId);
		//show list
		$("#select-container-doors").fadeIn(function(){
			//populate arrays initially
			fillArrayDoors();
			fillArrayDoorGroup();
		});
		//disable add button
		$("#btn-item-add").prop("disabled",true);
		//hide direction box
		$("#direction-container").addClass("hidden");
	}
});

//on change door select > enable / disable right arrow button
$("#doors-select").change(function(){
	var doorId=$("#doors-select").val();
	if(typeof doorId!="undefined") {
		$("#btn-item-add").prop("disabled",false);
		//show direction box
		if(typeof($('#isvisit:checked').val())!="undefined") $("#direction-container").removeClass("hidden");
	} else {
		$("#btn-item-add").prop("disabled",true);
		//hide direction box
		$("#direction-container").addClass("hidden");
	}
});

//on change current door select > enable / disable right arrow button
$("#doors-group-current-select").change(function(){
	var groupDoorId=$("#doors-group-current-select").val();
	if(typeof groupDoorId!="undefined") $("#btn-item-delete").prop("disabled",false);
	else $("#btn-item-delete").prop("disabled",true);
});

//item add button click action
$("#btn-item-add").click(function(){
	addRight();
	//clear door selection
	$("#doors-select").val([]);
	//disable add button
	$("#btn-item-add").prop("disabled",true);
	//hide direction box
	$("#direction-container").addClass("hidden");
});

//item delete button click action
$("#btn-item-delete").click(function(){
	//disable del button
	addLeft();
	//clear current selection
	$("#doors-group-current-select").val([]);
	//disable del button
	$("#btn-item-delete").prop("disabled",true);
});

//select all doors action
$("#doors-group-selectall").click(function(){
	$('#doors-select option').not('.toadd').not('.todel').not('.toupd').not(":disabled").prop('selected',true);
	//if no items have been selected, disable add button
	if($("#doors-select option:selected").length>0) {
		$("#btn-item-add").prop("disabled",false);
		//show direction box
		if(typeof($('#isvisit:checked').val())!="undefined") $("#direction-container").removeClass("hidden");
	}
});

//toggle isvisit and belongs containers on change
$("#isvisit").change(function(){
	if($(this).prop("checked")!=false) {
		$("#belongs-container").slideUp();
		//if door selected , show direction options
		if(typeof ($('#doors-select').val())!=="undefined") $("#direction-container").removeClass("hidden");
	} else {
		$("#belongs-container").slideDown();
		//if door selected , show direction options
		$("#direction-container").addClass("hidden");
	}
});
$("#doors-group-orgid-check").change(function(){
	if($(this).prop("checked")!=false) $("#isvisit-container").slideUp();
	else $("#isvisit-container").slideDown();
});

//add element from left to right
function addRight(){
	var boxOptions=$("#doors-select option:selected");
	var side = $("input[name=side]:checked").val();

	$.each(boxOptions,function(){
		var elemid=$(this).val();
		var elemname=$(this).html();
		//add into new array
		arrGroupDoors[elemid]=elemname;
		//remove from old array
		arrDoors[elemid]="";
		//add side value
		arrGroupDoorsSides[elemid]=side;
		//show in new box
		if($("#doors-group-current-select option[value='"+elemid+"']").length>0){
			//toggle if exists
			$("#doors-group-current-select option[value='"+elemid+"']").show();
			$("#doors-group-current-select option[value='"+elemid+"']").prop("disabled",false);
			//set sides
			$("#doors-group-current-select option[value='"+elemid+"']").attr("data-side",side);
		} else {
			//if not, append html
			$("#doors-group-current-select").append("<option value='"+elemid+"' data-side='"+side+"'>"+elemname+"</option>");
		}
		//set color
		$("#doors-group-current-select option[value='"+elemid+"']").removeClass("side-color").removeClass("side-color0").removeClass("side-color1").addClass("side-color"+side);
		//hide from older box
		$("#doors-select option[value='"+elemid+"']").hide();
		$("#doors-select option[value='"+elemid+"']").prop("disabled",true);
	});
}

//remove element from right to left
function addLeft(){
	var boxOptions=$("#doors-group-current-select option:selected");
	$.each(boxOptions,function(){
		elemid=$(this).val();
		elemname=$(this).html();
		//add into new array
		arrDoors[elemid]=elemname;
		//remove from old array
		arrGroupDoors[elemid]="";
		//show in new box
		if($("#doors-select option[value='"+elemid+"']").length>0){
			//toggle if exists
			$("#doors-select option[value='"+elemid+"']").show();
			$("#doors-select option[value='"+elemid+"']").prop("disabled",false);
		} else {
			//if not, append html
			$("#doors-select").append("<option value='"+elemid+"'>"+elemname+"</option>");
		}
		//hide from older box
		$("#doors-group-current-select option[value='"+elemid+"']").hide();
		$("#doors-group-current-select option[value='"+elemid+"']").prop("disabled",true);
	});
}

//init array doors
function fillArrayDoors(){
	arrDoors=[];
	var boxOptions=document.querySelectorAll("#doors-select option");
	var doorid,doorname;
	if(boxOptions.length>0){
		for(var i=0;i<boxOptions.length;i++){
			if(boxOptions[i].className==""){
				doorid=boxOptions[i].value;
				doorname=boxOptions[i].innerHTML;
				arrDoors[doorid]=doorname;
			}
		}
	}
}

//init array door group
function fillArrayDoorGroup(){
	arrGroupDoors=[];
	arrGroupDoorsSides=[];
	var boxOptions=document.querySelectorAll("#doors-group-current-select option");
	var doorid,doorname;
	if(boxOptions.length>0){
		for(var i=0;i<boxOptions.length;i++){
			doorid=boxOptions[i].value;
			doorname=boxOptions[i].innerHTML;
			arrGroupDoors[doorid]=doorname;
			arrGroupDoorsSides[doorid]=boxOptions[i].dataset.side;
		}
	}
}

function resetForm(){
	//empty all arrays
	arrDoors=[];
	arrGroupDoors=[];
	arrGroupDoorsSides=[];
	//group name
	$("#door-groups-new-name").val("");
	//clear all selections
	$("#doors-select,#doors-group-current-select").val([]);
	//disable all buttons
	$("#btn-item-add,#btn-item-delete").prop("disabled",true);
	//hide doors container
	$("#select-container-doors").hide();
	//empty current door group select
	$("#doors-group-current-select").empty();
	//clear is visit checkbox
	$("#isvisit").prop("checked",false);
	//clear belongs to orgid checkbox
	$("#doors-group-orgid-check").prop("checked",false);
	//repopulate belongs to orgid select
	$('#doors-group-orgid').empty();
	orgNames.forEach(function(item,index){$('#doors-group-orgid').append("<option value='"+index+"'>"+item+"</option>");});
	//hide belogs to orgid select
	$('#doors-group-orgid-container').hide();
	//clear group id value if edit
	editId=0;
	//modal title
	$("#modal-new-label").text("<?=get_text("New Door Group",$lang);?>");
	//hide details
	$('#select-container-door-groups-details').hide()
	//hide direction box
	$("#direction-container").addClass("hidden");
	//reset default side
	$("#side-both").click();
}

//fetch info for new
$('#modal-new').on('show.bs.modal', function (event){
	//populate zones select list
	populateList("zones-select","zones");
	//clear all previous values
	resetForm();
});

//fetch info for edit
$('#door-groups-select-edit').click(function (event){
	//clear all previous values
	resetForm();
	var DoorGroupId = $("#door-groups-select").val();
	$.ajax({
		type: "POST",
		url: "process",
		data: "action=get_door_group&id=" + DoorGroupId,
		success: function(resp){
			if(resp[0]=='1'){
				//populate fields with rec info
				var values = resp[1];
				editId=values.id;
				$('#door-groups-new-name').val(values.name);
				//show both isvisit and belongs checkbox
				$("#isvisit-container,#belongs-container").show();
				//set is visit value
				if(values.isForVisit==1){
					$("#isvisit").prop("checked",true);
					$("#belongs-container").hide();
				} else $("#isvisit").prop("checked",false);
				//modal title
				$("#modal-new-label").text("<?=get_text("Edit Door Group",$lang);?>");
				//belongs to org if not null > populate the box with the option selected
				if(values.orgId!=null){
					$("#isvisit-container").hide();
					$("#doors-group-orgid-check").prop("checked",true);
					$('#doors-group-orgid').empty();
					orgNames.forEach(function(v,k){
						if(k==values.orgId) $('#doors-group-orgid').append("<option value='"+k+"' selected>"+v+"</option>");
						else $('#doors-group-orgid').append("<option value='"+k+"'>"+v+"</option>");
					});
					$('#doors-group-orgid-container').show();
				}
				//fetch group doors
				$.ajax({
					type: "POST",
					url: "process",
					data: "action=get_door_group_doors&id=" + DoorGroupId,
					success: function(doors_resp){
						if(doors_resp[0]=='1'){
							//fill select with door data
							var doors_values = doors_resp[1];
							for(var i=0;i<doors_values.length;i++){
								//convert to side value
								var side_value="";
								if(doors_values[i].iSide==1 && doors_values[i].oSide==0){
									//incoming
									side_value="1";
								} else if(doors_values[i].iSide==0 && doors_values[i].oSide==1){
									//outgoing
									side_value="0";
								} //else both
								$("#doors-group-current-select").append("<option value='"+doors_values[i].id+"' class='side-color"+side_value+"' data-side='"+side_value+"'>"+doors_values[i].name+"</option>");
							}
							//fill group door array
							fillArrayDoorGroup();
						}//else skip > door group can have zero doors
					},
					failure: function(){
						//show modal error
						$('#modal-error .modal-body').text("<?=get_text("Operation failed, please try again",$lang);?>");
						$("#modal-error").modal("show");
					}
				});
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

<?
/*
TODO:
- try to make that when populating the door list, to show all the doors as options that are not yet on the door group select
- try to make that when removing a door from the door group, to add it to the door select Only if its part of the same
*/
?>

//new/edit action
$("#door-groups-new-form").submit(function(){

	var DoorGroupName = $("#door-groups-new-name").val();
	if(typeof($('#isvisit:checked').val())=="undefined") var DoorGroupIsVisit = 0;
	else var DoorGroupIsVisit = 1;
	if(typeof($('#doors-group-orgid-check:checked').val())=="undefined") var DoorGroupOrgId = null;
	else var DoorGroupOrgId = $("#doors-group-orgid").val();

	//build door id array with all the values that have a non empty name
	var DoorGroupDoors = [];
	var DoorGroupSides = [];
	for (var k in arrGroupDoors){
		if (typeof arrGroupDoors[k] !== 'function' && arrGroupDoors[k]!=""){
			DoorGroupDoors.push(k);
			DoorGroupSides.push(arrGroupDoorsSides[k]);
		}
	}
	//build action string if its create or edit
	if(editId!=0 && !isNaN(editId)) action_str = "action=edit_door_group&id=" + editId +"&name=" + DoorGroupName + "&isvisit=" + DoorGroupIsVisit + "&orgid=" + DoorGroupOrgId + "&doorids=" + DoorGroupDoors.join("|") + "&doorsides="+DoorGroupSides.join("|");//edit
	else action_str = "action=add_door_group&name=" + DoorGroupName + "&isvisit=" + DoorGroupIsVisit + "&orgid=" + DoorGroupOrgId + "&doorids=" + DoorGroupDoors.join("|") + "&doorsides="+DoorGroupSides.join("|");//create

	$.ajax({
		type: "POST",
		url: "process",
		data: action_str,
		success: function(resp){
			if(resp[0]=='1'){
				//close modal
				$("#modal-new").modal("hide");
				//repopulate select box
				populateList("door-groups-select","door_groups");
				//hide details
				$('#select-container-door-groups-details').hide()
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
	return false;
});

//delete action
$("#door-groups-delete-form").submit(function(){
	var DoorGroupId = $("#door-groups-select").val();

	if(!isNaN(DoorGroupId)){
		$.ajax({
			type: "POST",
			url: "process",
			data: "action=delete_door_group&id=" + DoorGroupId,
			success: function(resp){
				if(resp[0]=='1'){
					//close modal
					$("#modal-delete").modal("hide");
					//repopulate select box
					populateList("door-groups-select","door_groups");
					//hide details
					$('#select-container-door-groups-details').hide()
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
	$("#door-groups-delete-form .btn-success").focus();
});

//toggle orgid select when checkbox is checked
$('#doors-group-orgid-check').change(function(){
	if(typeof($('#doors-group-orgid-check:checked').val())=="undefined"){
		$('#doors-group-orgid-container').slideUp();
	} else {
		$('#doors-group-orgid-container').slideDown();
	}
});
</script>

</body>
</html>