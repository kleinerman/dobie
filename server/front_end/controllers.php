<?
$leavebodyopen=1;
$requirerole=2;
include("header.php");
?>
<div id="page-wrapper">

<div class="row">
<div class="col-lg-12">
<h1 class="page-header">Controllers</h1>
</div>
</div>

<div class="row">
<div class="col-lg-12">

<div class="table-container" id="rows-table-container">
<input type="text" name="filter" placeholder="Filter names..." class="form-control data-filter-table" data-filter="rows-table">
<table id="rows-table" class="table-bordered table-hover table-condensed table-responsive table-striped left">
</table>
</div>

<br><br>
<div class="row" id="buttons-row">
<div class="col-sm-3"><button id="rows-new" class="btn btn-success" type="button" data-toggle="modal" data-target="#modal-new">Add</button></div>
<div class="col-sm-3"><button id="rows-edit" class="btn btn-primary" type="button" data-toggle="modal" data-target="#modal-new" disabled>Edit</button></div>
<div class="col-sm-3"><button id="rows-reprov" class="btn btn-warning" type="button" data-toggle="modal" data-target="#modal-reprov" disabled>Reprogram</button></div>
<div class="col-sm-3"><button id="rows-del" class="btn btn-danger" type="button" data-toggle="modal" data-target="#modal-delete" disabled>Delete</button></div>
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
<h4 class="modal-title" id="modal-new-label">New Controller</h4>
</div>
<form class="form-horizontal" id="controller-form" action="#">
<div class="modal-body">
<div class="form-group">
 <label class="control-label col-sm-2">Name:</label>
 <div class="col-sm-10">
      <input type="text" class="form-control" id="controller-name" name="name" value="" required>
 </div>
</div>
<div class="form-group">
 <label class="control-label col-sm-2">Controller Model:</label>
 <div class="col-sm-10">
	<input type="text" name="filter" placeholder="Filter options..." class="form-control data-filter" data-filter="controller-model-select">
	<select id="controller-model-select" class="select-options select-options-small form-control" name="controller-model-select" size="2" required></select>
 </div>
</div>
<div class="form-group">
 <label class="control-label col-sm-2">MAC Address:</label>
 <div class="col-sm-10">
      <input type="text" class="form-control" id="controller-mac" name="mac" value="" required>
 </div>
</div>
</div>
<div class="modal-footer">
<button class="btn btn-success" id="controller-submit">Save</button>
</div>
</form>
</div>
</div>
<!-- /.modal -->
</div>

<!-- reprov modal -->
<div class="modal fade" id="modal-reprov" tabindex="-1" role="dialog" aria-hidden="true">
<div class="modal-dialog">
<div class="modal-content">
<div class="modal-body center">
Are you sure you want to reprogram this controller?
</div>
<div class="modal-footer center">
<form class="form-horizontal" id="controller-reprov-form" action="#">
<button class="btn btn-success">Ok</button>
<button type="button" class="btn btn-danger" onclick="$('#modal-reprov').modal('hide');">Cancel</button>
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
Are you sure?
</div>
<div class="modal-footer center">
<form class="form-horizontal" id="controller-delete-form" action="#">
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
	$("#modal-new-label").text("New Controller");
	//clear id value if edit
	editId=0;
}

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
			if($('#rows-table tr td input[type=checkbox]:checked').length == 1) $("#rows-edit,#rows-del,#rows-reprov").prop("disabled",false);
		} else {
			$("#rows-table td input[type=checkbox]").prop("checked",false);
			//no rows selected > disable both
			$("#rows-edit,#rows-del,#rows-reprov").prop("disabled",true);
		}
	})
	
	//edit / delete  button toggle
	$('#rows-table tr td input:checkbox').change(function(){
		if($('#rows-table tr td input[type=checkbox]:checked').length > 0) {
			//if at least 1 row selected > enable delete
			//$("#rows-del").prop("disabled",false);
			//enable edit only if 1 row is selected
			if($('#rows-table tr td input[type=checkbox]:checked').length > 1) $("#rows-edit,#rows-del,#rows-reprov").prop("disabled",true);
			else $("#rows-edit,#rows-del,#rows-reprov").prop("disabled",false);
		} else {
			//no rows selected > disable both
			$("#rows-edit,#rows-del,#rows-reprov").prop("disabled",true);
		}
	});
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
				//set table headers
				$('#'+tableId).append("<tr><th class=\"smallcol\"><input type=\"checkbox\" id=\"rowsAll\" name=\"rowsAll\" value=\"1\"></th><th>Name</th><th>MAC</th><th>Last Seen</th><th class=\"center\">Reachable</th></tr>");
				//populate fields with rec info
				for(i=0;i<values.length;i++){
					//show row
					//pre process MAC
					macStr = values[i].macAddress.replace(/(.{2})/g, "$1:").slice(0,-1).toUpperCase();
					//pre process date
					if(!values[i].lastSeen) lastSeenStr = "";
					else {
						var dateobj = new Date(values[i].lastSeen);
						lastSeenStr = dateobj.getFullYear() + "-" + addZeroPaddingSingle((dateobj.getMonth()+1)) + "-" + addZeroPaddingSingle(dateobj.getDate()) + " " + addZeroPaddingSingle(dateobj.getHours()) + ":" +
						addZeroPaddingSingle(dateobj.getMinutes()) + ":" +
						addZeroPaddingSingle(dateobj.getSeconds());
					}
					//pre process reachable icon
					if(values[i].reachable=="1") reachableStr="<span class=\"fa fa-check\"></span>";
					else reachableStr= "";
					$('#'+tableId).append("<tr><td><input type=\"checkbox\" name=\"controllers[]\" value="+values[i].id+"></td><td>"+values[i].name+"</td><td>"+macStr+"</td><td>"+lastSeenStr+"</td><td class=\"center\">"+reachableStr+"</td></tr>");
				}
				//add trigger events for rows
				tableClickEvents2();
			} else {
				//show error in table
				$('#'+tableId).append("<tr><td class='center'>"+resp[1]+"</td></tr>");
			}
		},
		failure: function(){
			//show modal error
			$('#modal-error .modal-body').text("Operation failed, please try again");
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
				$("#modal-new-label").text("Edit Controller");
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
			$('#modal-error .modal-body').text("Operation failed, please try again");
			$("#modal-error").modal("show");
		}
	});
});

//fetch info for edit
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
		$('#modal-error .modal-body').text("MAC address sent is not valid");
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

//reprov action
$("#controller-reprov-form").submit(function(){
	var controllerId = $('#rows-table tr td input[type=checkbox]:checked')[0].value;
	if(!isNaN(controllerId)){
		$.ajax({
			type: "POST",
			url: "process",
			data: "action=reprov_controller&id=" + controllerId,
			success: function(resp){
				if(resp[0]=='1'){
					//close modal
					$("#modal-reprov").modal("hide");
					//repopulate table
					populateTable("rows-table");
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