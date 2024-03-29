<?
$leavebodyopen=1;
$requirerole=1;
include("header.php");
?>
<div id="page-wrapper">

<div class="row">
<div class="col-lg-12">
<h1 class="page-header"><?=get_text("Controllers",$lang);?></h1>
</div>
</div>

<div class="row">
<div class="col-lg-12">

<div class="table-container" id="rows-table-container">
<input type="text" name="filter" placeholder="<?=get_text("Filter names",$lang);?>..." class="form-control data-filter-table" data-filter="rows-table">
<div class="table-responsive">
<table id="rows-table" class="table table-bordered table-hover table-condensed table-striped left"></table>
</div>
</div>

<br><br>
<div class="row" id="buttons-row">
<div class="col-md-12 center">
<div class="buttoncontainer"><button id="rows-new" class="btn btn-success" type="button" data-toggle="modal" data-target="#modal-new"><span class="fa fa-plus"></span><span class="hidden-xs"> <?=get_text("Add",$lang);?></button></div>
<div class="buttoncontainer"><button id="rows-edit" class="btn btn-primary" type="button" data-toggle="modal" data-target="#modal-new" disabled><span class="fa fa-pen"></span><span class="hidden-xs"> <?=get_text("Edit",$lang);?></span></button></div>
<div class="buttoncontainer"><button id="rows-refresh" class="btn btn-warning" type="button"><span class="fa fa-sync-alt"></span><span class="hidden-xs"> <?=get_text("Refresh",$lang);?></span></button></div>
<div class="buttoncontainer"><button id="rows-resync" class="btn btn-violet" type="button" data-toggle="modal" data-target="#modal-resync" disabled><span class="fa fa-redo-alt"></span><span class="hidden-xs"> <?=get_text("Resync",$lang);?></span></button></div>
<div class="buttoncontainer"><button id="rows-considersynced" class="btn btn-brown" type="button" data-toggle="modal" data-target="#modal-considersynced" disabled><span class="fa fa-check"></span><span class="hidden-xs"> <?=get_text("Consider Synced",$lang);?></span></button></div>
<div class="buttoncontainer"><button id="rows-poweroff" class="btn btn-info" type="button" data-toggle="modal" data-target="#modal-poweroff" disabled><span class="fa fa-power-off"></span><span class="hidden-xs"> <?=get_text("Power Off",$lang);?></span></button></div>
<div class="buttoncontainer"><button id="rows-del" class="btn btn-danger" type="button" data-toggle="modal" data-target="#modal-delete" disabled><span class="fa fa-times"></span><span class="hidden-xs"> <?=get_text("Delete",$lang);?></span></button></div>
</div>
</div>

</div>
</div>

</div>

<?php
include("footer.php");
?>

<!-- MODALS -->
<!-- create modal -->
<div class="modal fade" id="modal-new" tabindex="-1" role="dialog" aria-labelledby="modal-new-label" aria-hidden="true">
<div class="modal-dialog">
<div class="modal-content">
<div class="modal-header">
<button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>
<h4 class="modal-title" id="modal-new-label"><?=get_text("New Controller",$lang);?></h4>
</div>
<form class="form-horizontal" id="controller-form" action="#">
<div class="modal-body">
<div class="form-group">
 <label class="control-label col-sm-2"><?=get_text("Name",$lang);?>:</label>
 <div class="col-sm-10">
      <input type="text" class="form-control" id="controller-name" name="name" value="" required>
 </div>
</div>
<div class="form-group">
 <label class="control-label col-sm-2"><?=get_text("Controller Model",$lang);?>:</label>
 <div class="col-sm-10">
	<input type="text" name="filter" placeholder="<?=get_text("Filter options",$lang);?>..." class="form-control data-filter" data-filter="controller-model-select">
	<select id="controller-model-select" class="select-options select-options-small form-control" name="controller-model-select" size="2" required></select>
 </div>
</div>
<div class="form-group">
 <label class="control-label col-sm-2"><?=get_text("MAC Address",$lang);?>:</label>
 <div class="col-sm-10">
      <input type="text" class="form-control" id="controller-mac" name="mac" value="" required>
 </div>
</div>
</div>
<div class="modal-footer">
<button class="btn btn-success" id="controller-submit"><?=get_text("Save",$lang);?></button>
</div>
</form>
</div>
</div>
<!-- /.modal -->
</div>

<!-- resync modal -->
<div class="modal fade" id="modal-resync" tabindex="-1" role="dialog" aria-hidden="true">
<div class="modal-dialog">
<div class="modal-content">
<div class="modal-body center">
<?=get_text("Are you sure you want to resync this controller",$lang);?>?
</div>
<div class="modal-footer center">
<form class="form-horizontal" id="controller-resync-form" action="#">
<button class="btn btn-success"><?=get_text("Yes",$lang);?></button>
<button type="button" class="btn btn-danger" onclick="$('#modal-resync').modal('hide');"><?=get_text("Cancel",$lang);?></button>
</form>
</div>
</div>
</div>
<!-- /.modal -->
</div>

<!-- considersynced modal -->
<div class="modal fade" id="modal-considersynced" tabindex="-1" role="dialog" aria-hidden="true">
<div class="modal-dialog">
<div class="modal-content">
<div class="modal-body center">
<?=get_text("Are you sure you want to consider this controller synced",$lang);?>?
</div>
<div class="modal-footer center">
<form class="form-horizontal" id="controller-considersynced-form" action="#">
<button class="btn btn-success"><?=get_text("Yes",$lang);?></button>
<button type="button" class="btn btn-danger" onclick="$('#modal-considersynced').modal('hide');"><?=get_text("Cancel",$lang);?></button>
</form>
</div>
</div>
</div>
<!-- /.modal -->
</div>

<!-- poweroff modal -->
<div class="modal fade" id="modal-poweroff" tabindex="-1" role="dialog" aria-hidden="true">
<div class="modal-dialog">
<div class="modal-content">
<div class="modal-body center">
<?=get_text("Are you sure you want to power off this controller",$lang);?>?
</div>
<div class="modal-footer center">
<form class="form-horizontal" id="controller-poweroff-form" action="#">
<button class="btn btn-success"><?=get_text("Yes",$lang);?></button>
<button type="button" class="btn btn-danger" onclick="$('#modal-poweroff').modal('hide');"><?=get_text("Cancel",$lang);?></button>
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
<form class="form-horizontal" id="controller-delete-form" action="#">
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

//populate select list
populateTable("rows-table");


function resetForm(){
	//text inputs
	$("#controller-name,#controller-mac").val("");
	//selects
	$("#controller-model-select").empty();
	//modal title
	$("#modal-new-label").text("<?=get_text("New Controller",$lang);?>");
	//clear id value if edit
	editId=0;
}

//populate editable table
function populateTable(tableId){
	//clear table
	$('#'+tableId).empty();
	$.ajax({
		type: "POST",
		url: "process",
		data: "action=get_controllers",
		success: function(resp){
			if(resp[0]=='1'){
				var values = resp[1];
				//console.log(values);
				//set table headers
				$('#'+tableId).append("<tr><th class=\"smallcol\"><input type=\"checkbox\" id=\"rowsAll\" name=\"rowsAll\" value=\"1\"></th><th><?=get_text("Name",$lang);?></th><th>MAC</th><th><?=get_text("IP Address",$lang);?></th><th><?=get_text("Last Seen",$lang);?></th><th class=\"center\"><?=get_text("Reachable",$lang);?></th><th class=\"center\"><?=get_text("All Synced",$lang);?></th><th class=\"center\"><?=get_text("Needs Resync",$lang);?></th></tr>");
				//populate fields with rec info
				for(i=0;i<values.length;i++){
					//show row
					if(values[i].ipAddress === null) values[i].ipAddress="";
					//pre process MAC
					macStr = buildMacFromString(values[i].macAddress);
					//pre process date
					if(!values[i].lastSeen) lastSeenStr = "";
					else {
						var dateobj = new Date(values[i].lastSeen);
						lastSeenStr = dateobj.getFullYear() + "-" + addZeroPaddingSingle((dateobj.getMonth()+1)) + "-" + addZeroPaddingSingle(dateobj.getDate()) + " " + addZeroPaddingSingle(dateobj.getHours()) + ":" +
						addZeroPaddingSingle(dateobj.getMinutes()) + ":" +
						addZeroPaddingSingle(dateobj.getSeconds());
					}
					//pre process reachable icon
					var checkStr="<span class=\"fa fa-check\"></span>";
					var warningStr="<span class=\"fa fa-exclamation-triangle\"></span>";
					if(values[i].reachable=="1") reachableStr=checkStr;
					else reachableStr= "";
					//pre process allsynced icon
					if(values[i].allSynced=="1") allsyncedStr=checkStr;
					else allsyncedStr= "";
					//pre process needresync icon
					if(values[i].needResync=="1") needresyncStr=warningStr;
					else needresyncStr= "";
					$('#'+tableId).append("<tr><td><input type=\"checkbox\" name=\"controllers[]\" value="+values[i].id+"></td><td>"+values[i].name+"</td><td>"+macStr+"</td><td>"+values[i].ipAddress+"</td><td>"+lastSeenStr+"</td><td class=\"center\">"+reachableStr+"</td><td class=\"center\">"+allsyncedStr+"</td><td class=\"center\">"+needresyncStr+"</td></tr>");
				}
				//add trigger events for rows
				<?php if($logged->roleid<2){?>tableClickEvents2(); <?php } else {?>
				$('#rows-table input[type=checkbox]').hide();
				<?php }?>
			} else {
				//show error in table
				$('#'+tableId).append("<tr><td class='center'>"+resp[1]+"</td></tr>");
			}
		},
		failure: function(){
			//show modal error
			$('#modal-error .modal-body').text("<?=get_text("Operation failed, please try again",$lang);?>");
			$("#modal-error").modal("show");
		}
	});
}

//filter for tables
$(".data-filter-table").keyup(function(){
	var rows=$("#"+$(this).data("filter") + " tr:nth-child(n+2)");
	var filterValue=$(this).val().toLowerCase();
	rows.each(function(){
		if($(this).find("td").text().toLowerCase().includes(filterValue)) $(this).show();
		else $(this).hide();
	})
});

<?php
if($logged->roleid<2){
?>

//events for table checkboxes
function tableClickEvents2(){
	//clickable rows for editable tables
	$("#rows-table tr td:nth-child(n+2)").click(function(){
		$(this).parent().find("input[type=checkbox]").click();
	})

	//unclick All checkbox on row click
	$("#rows-table tr td input[type=checkbox]").click(function(){
		if($("#rowsAll").prop("checked")) $("#rowsAll").prop("checked",false);
	})

	//click All event
	$("#rowsAll").click(function(){
		if($(this).prop("checked")) {
			$("#rows-table td input[type=checkbox]").prop("checked",true);
			//$("#rows-del").prop("disabled",false);
			if($('#rows-table tr td input[type=checkbox]:checked').length == 1) $("#rows-edit,#rows-del,#rows-resync,#rows-poweroff,#rows-considersynced").prop("disabled",false);
		} else {
			$("#rows-table td input[type=checkbox]").prop("checked",false);
			//no rows selected > disable both
			$("#rows-edit,#rows-del,#rows-resync,#rows-poweroff,#rows-considersynced").prop("disabled",true);
		}
	})
	
	//edit / delete  button toggle
	$('#rows-table tr td input:checkbox').change(function(){
		if($('#rows-table tr td input[type=checkbox]:checked').length > 0) {
			//if at least 1 row selected > enable delete
			//$("#rows-del").prop("disabled",false);
			//enable edit only if 1 row is selected
			if($('#rows-table tr td input[type=checkbox]:checked').length > 1) $("#rows-edit,#rows-del,#rows-resync,#rows-poweroff,#rows-considersynced").prop("disabled",true);
			else $("#rows-edit,#rows-del,#rows-resync,#rows-poweroff,#rows-considersynced").prop("disabled",false);
		} else {
			//no rows selected > disable both
			$("#rows-edit,#rows-del,#rows-resync,#rows-poweroff,#rows-considersynced").prop("disabled",true);
		}
	});
}

//fetch info for edit
$("#rows-edit").click(function(){
	resetForm();
	//var controllerId = $("#controllers-select").val();
	var controllerId = $('#rows-table tr td input[type=checkbox]:checked')[0].value;
	$.ajax({
		type: "POST",
		url: "process",
		data: "action=get_controller&id=" + controllerId,
		success: function(resp){
			if(resp[0]=='1'){
				//populate fields with rec info
				var values = resp[1];
				$("#modal-new-label").text("<?=get_text("Edit Controller",$lang);?>");
				$("#controller-name").val(values.name);
				$('#controller-mac').val(values.macAddress);
				editId=values.id;
				//highlight current value
				populateList("controller-model-select","controller_models",0,"",values.ctrllerModelId);
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

//fetch info for new
$("#rows-new").click(function(){
	resetForm();
	populateList("controller-model-select","controller_models");
});

//new action
$("#controller-form").submit(function(){
	var controllerName = $("#controller-name").val();
	var controllerMac = $("#controller-mac").val().toLowerCase().replace(/-/g,"").replace(/:/g,"").replace(/ /g,"");
	var controllerModelId = $("#controller-model-select").val();
	
	//validate mac address
	var regex = /^([0-9a-f]{2}[:-]?){5}([0-9a-f]{2})$/;
	var isValidMac=regex.test(controllerMac);

	if(editId!=0 && !isNaN(editId)) action_str = "action=edit_controller&id="+editId+"&name=" + controllerName + "&model_id=" + controllerModelId + "&mac=" + controllerMac;//edit
	else action_str = "action=add_controller&name=" + controllerName + "&model_id=" + controllerModelId + "&mac=" + controllerMac;//create

	if(!isValidMac){
		//invalid mac sent
		$('#modal-error .modal-body').text("<?=get_text("MAC address sent is not valid",$lang);?>");
		$("#modal-error").modal("show");
	} else if(controllerName!="" && controllerName!='undefined' && !isNaN(controllerModelId)){
		$.ajax({
			type: "POST",
			url: "process",
			data: action_str,
			success: function(resp){
				if(resp[0]=='1'){
					//close modal
					$("#modal-new").modal("hide");
					//repopulate table
					populateTable("rows-table");
					//disable parametric buttons
					$("#rows-edit,#rows-del,#rows-resync,#rows-poweroff,#rows-considersynced").prop("disabled",1);
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

//resync action
$("#controller-resync-form").submit(function(){
	var controllerId = $('#rows-table tr td input[type=checkbox]:checked')[0].value;
	if(!isNaN(controllerId)){
		$.ajax({
			type: "POST",
			url: "process",
			data: "action=resync_controller&id=" + controllerId,
			success: function(resp){
				if(resp[0]=='1'){
					//close modal
					$("#modal-resync").modal("hide");
					//repopulate table
					populateTable("rows-table");
					//disable parametric buttons
					$("#rows-edit,#rows-del,#rows-resync,#rows-poweroff,#rows-considersynced").prop("disabled",1);
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

//considersynced action
$("#controller-considersynced-form").submit(function(){
	var controllerId = $('#rows-table tr td input[type=checkbox]:checked')[0].value;
	if(!isNaN(controllerId)){
		$.ajax({
			type: "POST",
			url: "process",
			data: "action=considersynced_controller&id=" + controllerId,
			success: function(resp){
				if(resp[0]=='1'){
					//close modal
					$("#modal-considersynced").modal("hide");
					//repopulate table
					populateTable("rows-table");
					//disable parametric buttons
					$("#rows-edit,#rows-del,#rows-resync,#rows-poweroff,#rows-considersynced").prop("disabled",1);
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

//poweroff action
$("#controller-poweroff-form").submit(function(){
	var controllerId = $('#rows-table tr td input[type=checkbox]:checked')[0].value;
	if(!isNaN(controllerId)){
		$.ajax({
			type: "POST",
			url: "process",
			data: "action=poweroff_controller&id=" + controllerId,
			success: function(resp){
				if(resp[0]=='1'){
					//close modal
					$("#modal-poweroff").modal("hide");
					//repopulate table
					populateTable("rows-table");
					//disable parametric buttons
					$("#rows-edit,#rows-del,#rows-resync,#rows-poweroff,#rows-considersynced").prop("disabled",1);
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
$("#controller-delete-form").submit(function(){
	var controllerId = $('#rows-table tr td input[type=checkbox]:checked')[0].value;
	if(!isNaN(controllerId)){
		$.ajax({
			type: "POST",
			url: "process",
			data: "action=delete_controller&id=" + controllerId,
			success: function(resp){
				if(resp[0]=='1'){
					//close modal
					$("#modal-delete").modal("hide");
					//repopulate table
					populateTable("rows-table");
					//disable parametric buttons
					$("#rows-edit,#rows-del,#rows-resync,#rows-poweroff,#rows-considersynced").prop("disabled",1);
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
	$("#controller-delete-form .btn-success").focus();
});

<?php
} else {
	//disable all buttons but the refresh one in case of viewer
	echo "$('#rows-new,#rows-edit,#rows-resync,#rows-poweroff,#rows-del,#rows-considersynced').prop('disabled', true);
	$('#rows-table input[type=checkbox]').hide();";
}
?>

//Refresh button > repopulate list
$("#rows-refresh").click(function(){
	populateTable("rows-table");
	//disable parametric buttons
	$("#rows-edit,#rows-del,#rows-resync,#rows-poweroff,#rows-considersynced").prop("disabled",1);
});
</script>
</body>
</html>
