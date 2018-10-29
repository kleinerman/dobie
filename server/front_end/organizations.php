<?
$leavebodyopen=1;
$requirerole=2;
include("header.php");
?>
<div id="page-wrapper">

<div class="row">
<div class="col-lg-12">
<h1 class="page-header"><?=get_text("Organizations",$lang);?></h1>
</div>
</div>

<div class="row">
<div class="col-lg-12">

<div class="select-container">
<form action="javascript:void(0)">
<div class="select-container-body">
<input type="text" name="filter" placeholder="<?=get_text("Filter options",$lang);?>..." class="form-control data-filter" data-filter="organizations-select">
<select id="organizations-select" class="select-options form-control" name="organizations-select" size="2" onchange="updateButtons(this.id)"></select>
</div>
<div class="select-container-footer">
<button id="organizations-select-add" class="btn btn-success" type="button" data-toggle="modal" data-target="#modal-new"><?=get_text("New",$lang);?></button>
<button id="organizations-select-edit" class="btn btn-primary" type="button" data-toggle="modal" data-target="#modal-edit" disabled><?=get_text("Edit",$lang);?></button>
<button id="organizations-select-del" class="btn btn-danger" type="button" data-toggle="modal" data-target="#modal-delete" disabled><?=get_text("Delete",$lang);?></button>
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
<h4 class="modal-title" id="modal-new-label"><?=get_text("New Organization",$lang);?></h4>
</div>
<form class="form-horizontal" id="organization-new-form" action="#">
<div class="modal-body">
<div class="form-group">
 <label class="control-label col-sm-2"><?=get_text("Name",$lang);?>:</label>
 <div class="col-sm-10">
      <input type="text" class="form-control" id="organization-new-name" name="name" value="" required>
 </div>
</div>
</div>
<div class="modal-footer">
<button class="btn btn-success" id="organization-new-submit"><?=get_text("Save",$lang);?></button>
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
<h4 class="modal-title" id="modal-edit-label"><?=get_text("Edit Organization",$lang);?></h4>
</div>
<form class="form-horizontal" id="organization-edit-form" action="#">
<div class="modal-body">
<div class="form-group">
 <label class="control-label col-sm-2"><?=get_text("Name",$lang);?>:</label>
 <div class="col-sm-10">
      <input type="text" class="form-control" id="organization-edit-name" name="name" value="" required>
      <input type="hidden" id="organization-edit-id" name="id" value="">
 </div>
</div>
</div>
<div class="modal-footer">
<button class="btn btn-success" id="organization-edit-submit"><?=get_text("Save",$lang);?></button>
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
<?=get_text("Deleting this organization will remove all persons that belongs to it",$lang);?>.<br>
<?=get_text("Are you sure",$lang);?>?
</div>
<div class="modal-footer center">
<form class="form-horizontal" id="organization-delete-form" action="#">
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

//populate select list
populateList("organizations-select","organizations");

//clear form for new
$('#modal-new').on('show.bs.modal', function (event){
	//reset form
	$('#organization-new-name').val("");
});

//fetch info for edit
$('#modal-edit').on('show.bs.modal', function (event){
	// If necessary, you could initiate an AJAX request here (and then do the updating in a callback).
	var organizationId = $("#organizations-select").val();
	$.ajax({
		type: "POST",
		url: "process",
		data: "action=get_organization&id=" + organizationId,
		success: function(resp){
			if(resp[0]=='1'){
				//populate fields with rec info
				var values = resp[1];
				$('#organization-edit-id').val(organizationId);
				$('#organization-edit-name').val(values.name);
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
$("#organization-new-form").submit(function(){
	var organizationName = $("#organization-new-name").val();
	if(organizationName!="" && organizationName!='undefined'){
		$.ajax({
			type: "POST",
			url: "process",
			data: "action=add_organization&name=" + organizationName,
			success: function(resp){
				if(resp[0]=='1'){
					//close modal
					$("#modal-new").modal("hide");
					//repopulate select box
					populateList("organizations-select","organizations");
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

//edit action
$("#organization-edit-form").submit(function(){
	var organizationId = $("#organization-edit-id").val();
	var organizationName = $("#organization-edit-name").val();
	if(!isNaN(organizationId) && organizationName!="" && organizationName!='undefined'){
		$.ajax({
			type: "POST",
			url: "process",
			data: "action=edit_organization&id=" + organizationId+"&name=" + organizationName,
			success: function(resp){
				if(resp[0]=='1'){
					//close modal
					$("#modal-edit").modal("hide");
					//repopulate select box
					populateList("organizations-select","organizations");
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
$("#organization-delete-form").submit(function(){
	var organizationId = $("#organizations-select").val();

	if(!isNaN(organizationId)){
		$.ajax({
			type: "POST",
			url: "process",
			data: "action=delete_organization&id=" + organizationId,
			success: function(resp){
				if(resp[0]=='1'){
					//close modal
					$("#modal-delete").modal("hide");
					//repopulate select box
					populateList("organizations-select","organizations");
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