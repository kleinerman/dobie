<?
$leavebodyopen=1;
include("header.php");
?>
<div id="page-wrapper">

<div class="row">
<div class="col-lg-12">
<h1 class="page-header">Doors</h1>
</div>
</div>

<div class="row">
<div class="col-lg-12">

<div class="select-container">
<form action="javascript:void(0)">
<div class="select-container-title">Zones</div>
<div class="select-container-body">
<input type="text" name="filter" placeholder="Filter options..." class="form-control data-filter" data-filter="zones-select">
<select id="zones-select" class="select-options form-control" name="zones-select" size="2"></select>
</div>
<div class="select-container-footer">
&nbsp;
</div>
</form>
</div>

<div class="select-container" id="select-container-doors" style="display:none">
<form action="javascript:void(0)">
<div class="select-container-title">Doors</div>
<div class="select-container-body">
<input type="text" name="filter" placeholder="Filter options..." class="form-control data-filter" data-filter="doors-select">
<select id="doors-select" class="select-options form-control" name="doors-select" size="2" onchange="updateButtons(this.id)"></select>
</div>
<div class="select-container-footer">
<button id="doors-select-add" class="btn btn-success" type="button" data-toggle="modal" data-target="#modal-new">New</button>
<button id="doors-select-edit" class="btn btn-primary" type="button" data-toggle="modal" data-target="#modal-add" disabled>Edit</button>
<button id="doors-select-del" class="btn btn-danger" type="button" data-toggle="modal" data-target="#modal-delete" disabled>Delete</button>
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
<h4 class="modal-title" id="modal-new-label">New Door</h4>
</div>
<form class="form-horizontal" id="door-new-form" action="#">
<div class="modal-body">

<div class="form-group">
 <label class="control-label col-sm-2">Name:</label>
 <div class="col-sm-10">
      <input type="text" class="form-control" id="door-new-name" name="name" value="" required maxlength="64">
 </div>
</div>

</div>
<div class="modal-footer">
<button class="btn btn-success" id="door-new-submit">Save</button>
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
<form class="form-horizontal" id="door-delete-form" action="#">
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

var zoneId;

//populate select list
populateList("zones-select","zones");

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

//fetch info for edit
$('#modal-edit').on('show.bs.modal', function (event){
	// If necessary, you could initiate an AJAX request here (and then do the updating in a callback).
	var doorId = $("#doors-select").val();
	$.ajax({
		type: "POST",
		url: "process",
		data: "action=get_door&id=" + doorId,
		success: function(resp){
			if(resp[0]=='1'){
				//populate fields with rec info
				var values = resp[1];
				$('#door-edit-id').val(doorId);
				$('#door-edit-name').val(values.name);
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
$("#door-new-form").submit(function(){
	var doorName = $("#door-new-name").val();

	if(doorName!="" && doorName!='undefined'){
		$.ajax({
			type: "POST",
			url: "process",
			data: "action=add_door&zoneid=" + zoneId +"&name=" + doorName,
			//data: "action=edit_door&id=" + doorId+"&zoneid=" + zoneId + "&name=" + doorName,
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