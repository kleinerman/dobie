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

<div class="select-container">
<form action="javascript:void(0)">
<div class="select-container-body">
<input type="text" name="filter" placeholder="Filter options..." class="form-control data-filter" data-filter="controllers-select">
<select id="controllers-select" class="select-options form-control" name="controllers-select" size="2" onchange="updateButtons(this.id)"></select>
</div>
<div class="select-container-footer">
<button id="controllers-select-add" class="btn btn-success" type="button" data-toggle="modal" data-target="#modal-new">New</button>
<button id="controllers-select-edit" class="btn btn-primary" type="button" data-toggle="modal" data-target="#modal-new" disabled>Edit</button>
<button id="controllers-select-del" class="btn btn-danger" type="button" data-toggle="modal" data-target="#modal-delete" disabled>Delete</button>
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

<!-- delete modal -->
<div class="modal fade" id="modal-delete" tabindex="-1" role="dialog" aria-hidden="true">
<div class="modal-dialog">
<div class="modal-content">
<div class="modal-body center">
Deleting this controller will remove all doors and accesses that belong to it.<br>
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
populateList("controllers-select","controllers");
	
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

//fetch info for edit
$("#controllers-select-edit").click(function(){
	resetForm();
	var controllerId = $("#controllers-select").val();
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
$("#controllers-select-add").click(function(){
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
					//repopulate select box
					populateList("controllers-select","controllers");
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
	var controllerId = $("#controllers-select").val();

	if(!isNaN(controllerId)){
		$.ajax({
			type: "POST",
			url: "process",
			data: "action=delete_controller&id=" + controllerId,
			success: function(resp){
				if(resp[0]=='1'){
					//close modal
					$("#modal-delete").modal("hide");
					//repopulate select box
					populateList("controllers-select","controllers");
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