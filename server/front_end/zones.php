<?
$leavebodyopen=1;
include("header.php");
?>
<div id="page-wrapper">

<div class="row">
<div class="col-lg-12">
<h1 class="page-header">Zones</h1>
</div>
</div>

<div class="row">
<div class="col-lg-12">

<div class="select-container">
<form action="javascript:void(0)">
<div class="select-container-body">
<input type="text" name="filter" placeholder="Filter options..." class="form-control data-filter" data-filter="zones-select">
<select id="zones-select" class="select-options form-control" name="zones-select" size="2" onchange="updateButtons(this.id)"></select>
</div>
<div class="select-container-footer">
<button id="zones-select-add" class="btn btn-success" type="button" data-toggle="modal" data-target="#modal-new">New</button>
<button id="zones-select-edit" class="btn btn-primary" type="button" data-toggle="modal" data-target="#modal-edit" disabled>Edit</button>
<button id="zones-select-del" class="btn btn-danger" type="button" data-toggle="modal" data-target="#modal-delete" disabled>Delete</button>
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
<h4 class="modal-title" id="modal-new-label">New Zone</h4>
</div>
<form class="form-horizontal" id="zone-new-form" action="#">
<div class="modal-body">
<div class="form-group">
 <label class="control-label col-sm-2">Name:</label>
 <div class="col-sm-10">
      <input type="text" class="form-control" id="zone-new-name" name="name" value="" required>
 </div>
</div>
</div>
<div class="modal-footer">
<button class="btn btn-success" id="zone-new-submit">Save</button>
</div>
</form>
</div>
</div>
<!-- /.modal -->
</div>

<!-- Edit modal -->
<div class="modal fade" id="modal-edit" tabindex="-1" role="dialog" aria-labelledby="modal-edit-label" aria-hidden="true">
<div class="modal-dialog">
<div class="modal-content">
<div class="modal-header">
<button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>
<h4 class="modal-title" id="modal-edit-label">Edit Zone</h4>
</div>
<form class="form-horizontal" id="zone-edit-form" action="#">
<div class="modal-body">
<div class="form-group">
 <label class="control-label col-sm-2">Name:</label>
 <div class="col-sm-10">
      <input type="text" class="form-control" id="zone-edit-name" name="name" value="" required>
      <input type="hidden" id="zone-edit-id" name="id" value="">
 </div>
</div>
</div>
<div class="modal-footer">
<button class="btn btn-success" id="zone-edit-submit">Save</button>
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
Deleting this zone will remove all doors that belong to it.<br>
Are you sure?
</div>
<div class="modal-footer center">
<form class="form-horizontal" id="zone-delete-form" action="#">
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

//populate select list
populateList("zones-select","zones");

//clear form for new
$('#modal-new').on('show.bs.modal', function (event){
	//reset form
	$('#zone-new-name').val("");
});

//fetch info for edit
$('#modal-edit').on('show.bs.modal', function (event){
	// If necessary, you could initiate an AJAX request here (and then do the updating in a callback).
	var zoneId = $("#zones-select").val();
	$.ajax({
		type: "POST",
		url: "process",
		data: "action=get_zone&id=" + zoneId,
		success: function(resp){
			if(resp[0]=='1'){
				//populate fields with rec info
				var values = resp[1];
				$('#zone-edit-id').val(zoneId);
				$('#zone-edit-name').val(values.name);
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
$("#zone-new-form").submit(function(){
	var zoneName = $("#zone-new-name").val();
	if(zoneName!="" && zoneName!='undefined'){
		$.ajax({
			type: "POST",
			url: "process",
			data: "action=add_zone&name=" + zoneName,
			success: function(resp){
				if(resp[0]=='1'){
					//close modal
					$("#modal-new").modal("hide");
					//repopulate select box
					populateList("zones-select","zones");
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
$("#zone-edit-form").submit(function(){
	var zoneId = $("#zone-edit-id").val();
	var zoneName = $("#zone-edit-name").val();
	if(!isNaN(zoneId) && zoneName!="" && zoneName!='undefined'){
		$.ajax({
			type: "POST",
			url: "process",
			data: "action=edit_zone&id=" + zoneId+"&name=" + zoneName,
			success: function(resp){
				if(resp[0]=='1'){
					//close modal
					$("#modal-edit").modal("hide");
					//repopulate select box
					populateList("zones-select","zones");
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
$("#zone-delete-form").submit(function(){
	var zoneId = $("#zones-select").val();

	if(!isNaN(zoneId)){
		$.ajax({
			type: "POST",
			url: "process",
			data: "action=delete_zone&id=" + zoneId,
			success: function(resp){
				if(resp[0]=='1'){
					//close modal
					$("#modal-delete").modal("hide");
					//repopulate select box
					populateList("zones-select","zones");
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