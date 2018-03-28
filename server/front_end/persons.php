<?
$leavebodyopen=1;
include("header.php");
?>
<div id="page-wrapper">

<div class="row">
<div class="col-lg-12">
<h1 class="page-header">Persons</h1>
</div>
</div>

<div class="row">
<div class="col-lg-12">

<div class="select-container">
<form action="javascript:void(0)">
<div class="select-container-title">Organizations</div>
<div class="select-container-body">
<input type="text" name="filter" placeholder="Filter options..." class="form-control data-filter" data-filter="organizations-select">
<select id="organizations-select" class="select-options form-control" name="organizations-select" size="2"></select>
</div>
<div class="select-container-footer">
&nbsp;
</div>
</form>
</div>

<div class="select-container" id="select-container-persons" style="display:none">
<form action="javascript:void(0)">
<div class="select-container-title">Persons</div>
<div class="select-container-body">
<input type="text" name="filter" placeholder="Filter options..." class="form-control data-filter" data-filter="persons-select">
<select id="persons-select" class="select-options form-control" name="persons-select" size="2" onchange="updateButtons(this.id)"></select>
</div>
<div class="select-container-footer">
<button id="persons-select-add" class="btn btn-success" type="button" data-toggle="modal" data-target="#modal-new">New</button>
<button id="persons-select-edit" class="btn btn-primary" type="button" data-toggle="modal" data-target="#modal-edit" disabled>Edit</button>
<button id="persons-select-del" class="btn btn-danger" type="button" data-toggle="modal" data-target="#modal-delete" disabled>Delete</button>
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
<h4 class="modal-title" id="modal-new-label">New Person</h4>
</div>
<form class="form-horizontal" id="person-new-form" action="#">
<div class="modal-body">

<div class="form-group">
 <label class="control-label col-sm-2">Name:</label>
 <div class="col-sm-10">
      <input type="text" class="form-control" id="person-new-name" name="name" value="" required maxlength="64">
 </div>
</div>
<div class="form-group">
 <label class="control-label col-sm-2">Identification Number:</label>
 <div class="col-sm-10">
      <input type="text" class="form-control" id="person-new-idnum" name="idnum" value="" maxlength="64">
 </div>
</div>
<div class="form-group">
 <label class="control-label col-sm-2">Card Number:</label>
 <div class="col-sm-10">
      <input type="number" class="form-control" id="person-new-cardnum" name="cardnum" value="" min="0" max="2147483646">
 </div>
</div>

</div>
<div class="modal-footer">
<button class="btn btn-success" id="person-new-submit">Save</button>
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
<h4 class="modal-title" id="modal-edit-label">Edit Person</h4>
</div>
<form class="form-horizontal" id="person-edit-form" action="#">
<div class="modal-body">

<div class="form-group">
 <label class="control-label col-sm-2">Name:</label>
 <div class="col-sm-10">
      <input type="text" class="form-control" id="person-edit-name" name="name" value="" maxlength="64" required>
      <input type="hidden" id="person-edit-id" name="id" value="">
 </div>
</div>
<div class="form-group">
 <label class="control-label col-sm-2">Identification Number:</label>
 <div class="col-sm-10">
      <input type="text" class="form-control" id="person-edit-idnum" name="idnum" value="" maxlength="64">
 </div>
</div>
<div class="form-group">
 <label class="control-label col-sm-2">Card Number:</label>
 <div class="col-sm-10">
      <input type="number" class="form-control" id="person-edit-cardnum" name="cardnum" value="" min="0" max="2147483646">
 </div>
</div>

</div>
<div class="modal-footer">
<button class="btn btn-success" id="person-edit-submit">Save</button>
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
Are you sure?
</div>
<div class="modal-footer center">
<form class="form-horizontal" id="person-delete-form" action="#">
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

var organizationId;

//populate select list
populateList("organizations-select","organizations");

$("#organizations-select").change(function(){
	organizationId=$("#organizations-select").val();
	if(!isNaN(organizationId) && organizationId!="undefined"){
		//populate list
		populateList("persons-select","persons",organizationId);
		//show list
		$("#select-container-persons").fadeIn();
		//disable buttons
		$("#persons-select-edit,#persons-select-del").prop("disabled",true);
	}
});

//fetch info for edit
$('#modal-edit').on('show.bs.modal', function (event){
	// If necessary, you could initiate an AJAX request here (and then do the updating in a callback).
	var personId = $("#persons-select").val();
	$.ajax({
		type: "POST",
		url: "process",
		data: "action=get_person&id=" + personId,
		success: function(resp){
			if(resp[0]=='1'){
				//populate fields with rec info
				var values = resp[1];
				$('#person-edit-id').val(personId);
				$('#person-edit-name').val(values.name);
				$('#person-edit-idnum').val(values.identNumber);
				$('#person-edit-cardnum').val(values.cardNumber);
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
$("#person-new-form").submit(function(){
	var personName = $("#person-new-name").val();
	var personIdNum = $("#person-new-idnum").val();
	var personCardNum = $("#person-new-cardnum").val();

	if(personName!="" && personName!='undefined'){
		$.ajax({
			type: "POST",
			url: "process",
			data: "action=add_person&orgid=" + organizationId +"&name=" + personName + "&idnum=" + personIdNum + "&cardnum=" + personCardNum,
			success: function(resp){
				if(resp[0]=='1'){
					//close modal
					$("#modal-new").modal("hide");
					//repopulate select box
					populateList("persons-select","persons",organizationId);
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
$("#person-edit-form").submit(function(){
	var personId = $("#person-edit-id").val();
	var personName = $("#person-edit-name").val();
	var personIdNum = $("#person-edit-idnum").val();
	var personCardNum = $("#person-edit-cardnum").val();

	if(!isNaN(personId) && personName!="" && personName!='undefined'){
		$.ajax({
			type: "POST",
			url: "process",
			data: "action=edit_person&id=" + personId+"&orgid=" + organizationId + "&name=" + personName + "&idnum=" + personIdNum + "&cardnum=" + personCardNum,
			success: function(resp){
				if(resp[0]=='1'){
					//close modal
					$("#modal-edit").modal("hide");
					//repopulate select box
					populateList("persons-select","persons",organizationId);
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
$("#person-delete-form").submit(function(){
	var personId = $("#persons-select").val();

	if(!isNaN(personId)){
		$.ajax({
			type: "POST",
			url: "process",
			data: "action=delete_person&id=" + personId,
			success: function(resp){
				if(resp[0]=='1'){
					//close modal
					$("#modal-delete").modal("hide");
					//repopulate select box
					populateList("persons-select","persons",organizationId);
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