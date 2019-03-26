<?
$leavebodyopen=1;
$requirerole=2;
include("header.php");
?>
<div id="page-wrapper">

<div class="row">
<div class="col-lg-12">
<h1 class="page-header"><?=get_text("Persons",$lang);?></h1>
</div>
</div>

<div class="row">
<div class="col-lg-12">

<div class="select-container">
<form action="javascript:void(0)">
<div class="select-container-title"><?=get_text("Organizations",$lang);?></div>
<div class="select-container-body">
<input type="text" name="filter" placeholder="<?=get_text("Filter options",$lang);?>..." class="form-control data-filter" data-filter="organizations-select">
<select id="organizations-select" class="select-options form-control" name="organizations-select" size="2"></select>
</div>
<div class="select-container-footer">
&nbsp;
</div>
</form>
</div>

<div class="select-container" id="select-container-persons" style="display:none">
<form action="javascript:void(0)">
<div class="select-container-title"><?=get_text("Persons",$lang);?> <button class="btn btn-primary btn-xs" id="import-csv-button" data-toggle="modal" data-target="#modal-import"><span class="fa fa-plus"></span> <?=get_text("Import CSV",$lang);?></button></div>
<div class="select-container-body">
<input type="text" name="filter" placeholder="<?=get_text("Filter options",$lang);?>..." class="form-control data-filter" data-filter="persons-select">
<select id="persons-select" class="select-options form-control" name="persons-select" size="2" onchange="updateButtons(this.id)"></select>
</div>
<div class="select-container-footer">
<button id="persons-select-add" class="btn btn-success" type="button" data-toggle="modal" data-target="#modal-new"><span class="fa fa-plus"></span><span class="hidden-xs"> <?=get_text("Add",$lang);?></button>
<button id="persons-select-edit" class="btn btn-primary" type="button" data-toggle="modal" data-target="#modal-edit" disabled><span class="fa fa-pen"></span><span class="hidden-xs"> <?=get_text("Edit",$lang);?></span></button>
<button id="persons-select-del" class="btn btn-danger" type="button" data-toggle="modal" data-target="#modal-delete" disabled><span class="fa fa-times"></span><span class="hidden-xs"> <?=get_text("Delete",$lang);?></span></button>
</div>
</form>
</div>

<div id="select-container-persons-details" style="display:none">Details</div>

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
<h4 class="modal-title" id="modal-new-label"><?=get_text("New Person",$lang);?></h4>
</div>
<form class="form-horizontal" id="person-new-form" action="#">
<div class="modal-body">

<div class="form-group">
 <label class="control-label col-sm-2"><?=get_text("First Name",$lang);?>:</label>
 <div class="col-sm-10">
      <input type="text" class="form-control" id="person-new-names" name="names" value="" required maxlength="64">
 </div>
</div>
<div class="form-group">
 <label class="control-label col-sm-2"><?=get_text("Last Name",$lang);?>:</label>
 <div class="col-sm-10">
      <input type="text" class="form-control" id="person-new-lastname" name="lastname" value="" required maxlength="64">
 </div>
</div>
<div class="form-group">
 <label class="control-label col-sm-2"><?=get_text("Identification Number",$lang);?>:</label>
 <div class="col-sm-10">
      <input type="text" class="form-control" id="person-new-idnum" name="idnum" value="" maxlength="64">
 </div>
</div>
<div class="form-group">
 <label class="control-label col-sm-2"><?=get_text("Card Number",$lang);?> (Raw):</label>
 <div class="col-sm-10">
      <input type="number" class="form-control" id="person-new-cardnum" name="cardnum" value="" min="0" max="2147483646">
 </div>
</div>

<div class="form-group">
 <label class="control-label col-sm-2"><?=get_text("Card Number",$lang);?> (FC):</label>
 <div class="col-sm-10">
      <input type="text" class="form-control small_input" id="person-new-cardnum-fc-1" name="cardnumfc1" value="">
       , <input type="text" class="form-control" id="person-new-cardnum-fc-2" name="cardnumfc2" value="">
 </div>
</div>

</div>
<div class="modal-footer">
<button class="btn btn-success" id="person-new-submit"><?=get_text("Save",$lang);?></button>
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
<h4 class="modal-title" id="modal-edit-label"><?=get_text("Edit Person",$lang);?></h4>
</div>
<form class="form-horizontal" id="person-edit-form" action="#">
<div class="modal-body">

<div class="form-group">
 <label class="control-label col-sm-2"><?=get_text("First Name",$lang);?>:</label>
 <div class="col-sm-10">
      <input type="text" class="form-control" id="person-edit-names" name="names" value="" maxlength="64" required>
      <input type="hidden" id="person-edit-id" name="id" value="">
 </div>
</div>
<div class="form-group">
 <label class="control-label col-sm-2"><?=get_text("Last Name",$lang);?>:</label>
 <div class="col-sm-10">
      <input type="text" class="form-control" id="person-edit-lastname" name="lastname" value="" maxlength="64" required>
 </div>
</div>
<div class="form-group">
 <label class="control-label col-sm-2"><?=get_text("Identification Number",$lang);?>:</label>
 <div class="col-sm-10">
      <input type="text" class="form-control" id="person-edit-idnum" name="idnum" value="" maxlength="64">
 </div>
</div>
<div class="form-group">
 <label class="control-label col-sm-2"><?=get_text("Card Number",$lang);?> (Raw):</label>
 <div class="col-sm-10">
      <input type="number" class="form-control" id="person-edit-cardnum" name="cardnum" value="" min="0" max="2147483646">
 </div>
</div>

<div class="form-group">
 <label class="control-label col-sm-2"><?=get_text("Card Number",$lang);?> (FC):</label>
 <div class="col-sm-10">
      <input type="text" class="form-control small_input" id="person-edit-cardnum-fc-1" name="cardnumfc1" value="">
       , <input type="text" class="form-control" id="person-edit-cardnum-fc-2" name="cardnumfc2" value="">
 </div>
</div>

</div>
<div class="modal-footer">
<button class="btn btn-success" id="person-edit-submit"><?=get_text("Save",$lang);?></button>
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
<?=get_text("Are you sure",$lang);?>?
</div>
<div class="modal-footer center">
<form class="form-horizontal" id="person-delete-form" action="#">
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

<!-- import modal -->
<div class="modal fade" id="modal-import" tabindex="-1" role="dialog" aria-hidden="true">
<div class="modal-dialog">
<div class="modal-content">
<div class="modal-header">
<button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>
<h4 class="modal-title" id="modal-import-label"><?=get_text("Import CSV",$lang);?></h4>
</div>
<div class="modal-body center">
<?=get_text("Import a .CSV file with rows with the following format",$lang);?>: <br><br>
<div class="alert alert-warning"><span class="bold"><?=get_text("First Name",$lang);?>, <?=get_text("Last Name",$lang);?>, <?=get_text("Identification Number",$lang);?>, <?=get_text("Card Number",$lang);?></span></div>

<form enctype="multipart/form-data" id="form-import">
<input name="form-import-input" class="form-control" type="file" id="form-import-input" required>
<input name="action" class="form-control" type="hidden" id="form-import-action" value="import_persons">
<input name="orgid" class="form-control" type="hidden" id="form-import-orgid" value="">
<br>
<label><input type="checkbox" id="form-import-ignore" name="form-import-ignore"> <?=get_text("Ignore first line of file (column headers)",$lang);?></label>
<br><br>
<div id="form-import-error" class="red bold"></div>
<input type="button" class="btn btn-success" value="<?=get_text("Send",$lang);?>" id="form-import-submit">
<progress id="form-import-progress" style="display:none"></progress>
<br>
</form>
</div>
</div>
</div>
<!-- /.modal -->
</div>

<style>
#form-import-input{
	width:auto;
	display:inline;
}

#select-container-persons-details{
	display: inline-block;
	vertical-align: top;
	padding-top: 66px;
	color: #aaa;
}

#person-edit-cardnum-fc-2,#person-new-cardnum-fc-2{
	width:80%
}

#person-edit-cardnum-fc-1,#person-edit-cardnum-fc-2,#person-new-cardnum-fc-1,#person-new-cardnum-fc-2{
	display:inline
}
</style>

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
		//hide details
		$('#select-container-persons-details').hide()
	}
});

//populate quick details box on person change
$("#persons-select").change(function(){
	var personId = $(this).val();
	if(!isNaN(personId)){
		$.ajax({
			type: "POST",
			url: "process",
			data: "action=get_person&id=" + personId,
			success: function(resp){
				if(resp[0]=='1'){
					//populate details with rec info
					var values = resp[1];
					$('#select-container-persons-details').html("<?=get_text("Identification Number",$lang);?>: "+ values.identNumber +"<br><?=get_text("Card Number",$lang);?>: " + values.cardNumber + " - " + rawToFC(values.cardNumber));
					//show details
					$('#select-container-persons-details').show()
				} else {
					//hide details
					$('#select-container-persons-details').hide()
				}
			},
			failure: function(){
				//hide details
				$('#select-container-persons-details').hide()
			}
		});
	}
});

//events to live update card number fields
function buildFCnum(mode){
	var part1=$("#person-"+mode+"-cardnum-fc-1").val();
	var part2=$("#person-"+mode+"-cardnum-fc-2").val();
	return (part1 + ", " + part2);
}

$("#person-edit-cardnum").keyup(function(){
	var numparts = rawToFC($(this).val()).split(",");
	if(numparts.length==2){
		$("#person-edit-cardnum-fc-1").val(numparts[0]);
		$("#person-edit-cardnum-fc-2").val(numparts[1]);
	} else {
		$("#person-edit-cardnum-fc-1").val("");
		$("#person-edit-cardnum-fc-2").val("");
	}
});

$("#person-edit-cardnum-fc-1, #person-edit-cardnum-fc-2").keyup(function(){
	$("#person-edit-cardnum").val(FCToRaw(buildFCnum("edit")));
});

$("#person-new-cardnum").keyup(function(){
	var numparts = rawToFC($(this).val()).split(",");
	if(numparts.length==2){
		$("#person-new-cardnum-fc-1").val(numparts[0]);
		$("#person-new-cardnum-fc-2").val(numparts[1]);
	} else {
		$("#person-new-cardnum-fc-1").val("");
		$("#person-new-cardnum-fc-2").val("");
	}
});

$("#person-new-cardnum-fc-1, #person-new-cardnum-fc-2").keyup(function(){
	$("#person-new-cardnum").val(FCToRaw(buildFCnum("new")));
});

//jump to fc2 on 3 nums fc
$("#person-edit-cardnum-fc-1").keyup(function(){
	if($(this).val()>99) $("#person-edit-cardnum-fc-2").focus();
});

$("#person-new-cardnum-fc-1").keyup(function(){
	if($(this).val()>99) $("#person-new-cardnum-fc-2").focus();
});

/*$("#person-new-cardnum").keyup(function(){
	$("#person-new-cardnum-fc").val(rawToFC($(this).val()));
});

$("#person-new-cardnum-fc").keyup(function(){
	$("#person-new-cardnum").val(FCToRaw($(this).val()));
});
*/
//clear form for new
$('#modal-new').on('show.bs.modal', function (event){
	//reset form
	$('#person-new-names, #person-new-lastname, #person-new-idnum, #person-new-cardnum, #person-new-cardnum-fc').val("");
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
				$('#person-edit-names').val(values.names);
				$('#person-edit-lastname').val(values.lastName);
				$('#person-edit-idnum').val(values.identNumber);
				$('#person-edit-cardnum').val(values.cardNumber);
				var tempfc=rawToFC(values.cardNumber).split(",");
				if(tempfc.length==2) {
					$('#person-edit-cardnum-fc-1').val(tempfc[0]);
					$('#person-edit-cardnum-fc-2').val(tempfc[1]);
				} else {
					$('#person-edit-cardnum-fc-1').val("");
					$('#person-edit-cardnum-fc-2').val("");
				}
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

$('#form-import-input').on('change', function(){
    //FILE VALIDATION PARAMS
    var maxFileSize = 1024 * 1024 * 10; //10mb
    var fileExts = ["csv","txt"];
    var fileType = "text/";

    var file = this.files[0];
    $("#form-import-submit").prop("disabled",true);

    if(file.size > maxFileSize){
	//file size validation
        $('#form-import-error').text("Maximum file size exceeded: "+ Math.floor(maxFileSize/1024/1024) + "MB");
    } else if(!fileExts.includes(file.name.split(".").pop())){
	//file extension validation
	$('#form-import-error').text("File must be of type: "+ fileExts.join(","));
    } else if(file.type.indexOf(fileType)<0){
	//file type validation
	$('#form-import-error').text("Invalid file type: "+ file.type);
    } else {
	//file is valid
	$('#form-import-error').text("");
	$("#form-import-submit").prop("disabled",false);
    }
});

//import csv file action
$("#form-import-submit").click(function(){
	$("#form-import-orgid").val(organizationId);
	$.ajax({
		type: "POST",
		url: "process",
		data: new FormData($('#form-import')[0]),
		//skip the following processing of cache, content type and process data
		cache: false,
		contentType: false,
		processData: false,
		beforeSend: function(){
			$('#form-import-error').text("");
			$("#form-import-submit").hide();
			$('#form-import-progress').show();
		},
		complete: function(){
			$('#form-import-progress').hide();
			$("#form-import-submit").show();
		},
		//Custom XMLHttpRequest
		xhr: function(){
			var myXhr = $.ajaxSettings.xhr();
			if(myXhr.upload){
				// For handling the progress of the upload
				myXhr.upload.addEventListener('progress', function(e){
					if (e.lengthComputable){
						$('#form-import-progress').attr({
							value: e.loaded,
							max: e.total,
						});
					}
				}, false);
			}
			return myXhr;
		},
		success: function(resp){
			if(resp[0]=='1'){
				//close modal
				$("#modal-import").modal("hide");
				//show error modal showing the number of imported contacts
				if(resp[1]==0) var zero_imported = "<br><?=get_text("Make sure the csv file has the correct format, and preferably UTF-8 encoding.",$lang);?>";
				else var zero_imported = "";
				$('#modal-error .modal-body').html("<?=get_text("Total persons imported",$lang);?>: "+resp[1]+zero_imported);
				$("#modal-error").modal("show");
				//repopulate select box
				populateList("persons-select","persons",organizationId);
			} else {
				//show error
				$('#form-import-error').text(resp[1]);
			}
		},
		failure: function(){
			//show modal error
			$('#form-import-error').text("<?=get_text("Operation failed, please try again",$lang);?>");
		}
	});
});

//new action
$("#person-new-form").submit(function(){
	var personNames = $("#person-new-names").val();
	var personLastName = $("#person-new-lastname").val();
	var personIdNum = $("#person-new-idnum").val();
	var personCardNum = $("#person-new-cardnum").val();

	if(personNames!="" && personNames!='undefined' && personLastName!="" && personLastName!='undefined'){
		$.ajax({
			type: "POST",
			url: "process",
			data: "action=add_person&orgid=" + organizationId + "&names=" + personNames + "&lastname=" + personLastName + "&idnum=" + personIdNum + "&cardnum=" + personCardNum,
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
$("#person-edit-form").submit(function(){
	var personId = $("#person-edit-id").val();
	var personNames = $("#person-edit-names").val();
	var personLastName = $("#person-edit-lastname").val();
	var personIdNum = $("#person-edit-idnum").val();
	var personCardNum = $("#person-edit-cardnum").val();

	if(!isNaN(personId) && personNames!="" && personNames!='undefined' && personLastName!="" && personLastName!='undefined'){
		$.ajax({
			type: "POST",
			url: "process",
			data: "action=edit_person&id=" + personId+"&orgid=" + organizationId + "&names=" + personNames + "&lastname=" + personLastName + "&idnum=" + personIdNum + "&cardnum=" + personCardNum,
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
	$("#person-delete-form .btn-success").focus();
});
</script>

</body>
</html>