<?php
$leavebodyopen=1;
$requirerole=array(2,4);
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

<?php if($logged->roleid!=4){ //Operator mode
?>
<div class="select-container valigntop">
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
<?php } else { //Org operator mode: populate orgid
?>
<input type="hidden" id="organizations-select" value="<?=$logged->orgid?>">
<?php } ?>

<div class="select-container valigntop" id="select-container-persons">
<form action="javascript:void(0)">
<div class="select-container-title"><nobr><?=get_text("Persons",$lang);?> <button class="btn btn-primary btn-xs" id="import-csv-button" data-toggle="modal" data-target="#modal-import"><span class="fa fa-plus"></span> <?=get_text("Import CSV",$lang);?></button> <button class="btn btn-success btn-xs" id="export-csv-button" data-toggle="tooltip" title="Export persons to Excel"><span class="fa fa-download"></span> <?=get_text("Export",$lang);?></button> <span class="fa fa-spinner fa-spin download-throbber-container" style="display:none"></span></nobr></div>
<div class="select-container-body">
<input type="text" name="filter" placeholder="<?=get_text("Filter options",$lang);?>..." class="form-control data-filter" data-filter="persons-select">
<select id="persons-select" class="select-options form-control" name="persons-select" size="2" onchange="updateButtons(this.id)"></select>
</div>
<div class="select-container-footer">
<button id="persons-select-add" class="btn btn-success" type="button" data-toggle="modal" data-target="#modal-new"><span class="fa fa-plus"></span><span class="hidden-xs"> <?=get_text("Add",$lang);?></button>
<button id="persons-select-edit" class="btn btn-primary" type="button" data-toggle="modal" data-target="#modal-edit" disabled><span class="fa fa-pen"></span><span class="hidden-xs"> <?=get_text("Edit",$lang);?></span></button>
<button id="persons-select-del" class="btn btn-danger" type="button" data-toggle="modal" data-target="#modal-delete" disabled><span class="fa fa-times"></span><span class="hidden-xs"> <?=get_text("Delete",$lang);?></span></button>
<button id="persons-refresh" class="btn btn-warning" type="button"><span class="fa fa-sync-alt"></span> <span class="hidden-xs"><?=get_text("Refresh",$lang);?></span></button>
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
      <input type="text" class="form-control" id="person-new-names" name="names" value="" maxlength="64" required>
 </div>
</div>
<div class="form-group">
 <label class="control-label col-sm-2"><?=get_text("Last Name",$lang);?>:</label>
 <div class="col-sm-10">
      <input type="text" class="form-control" id="person-new-lastname" name="lastname" value="" maxlength="64" required>
 </div>
</div>
<div class="form-group">
 <label class="control-label col-sm-2"><?=get_text("Identification Number",$lang);?>:</label>
 <div class="col-sm-10">
      <input type="text" class="form-control" id="person-new-idnum" name="idnum" value="" maxlength="64" required>
 </div>
</div>
<div class="form-group">
 <label class="control-label col-sm-2"><?=get_text("Card Number",$lang);?> (Raw):</label>
 <div class="col-sm-10">
      <input type="number" class="form-control" id="person-new-cardnum" name="cardnum" value="" min="0" max="2147483646" required>
 </div>
</div>
<div class="form-group">
 <label class="control-label col-sm-2"><?=get_text("Card Number",$lang);?> (FC):</label>
 <div class="col-sm-10">
      <input type="text" class="form-control small_input" id="person-new-cardnum-fc-1" name="cardnumfc1" value="" maxlength="3">
       , <input type="text" class="form-control" id="person-new-cardnum-fc-2" name="cardnumfc2" value="" maxlength="32">
 </div>
</div>
<div class="form-group">
 <label class="control-label col-sm-2"><?=get_text("Note",$lang);?>:</label>
 <div class="col-sm-10">
      <input type="text" class="form-control" id="person-new-note" name="note" value="" maxlength="256">
 </div>
</div>

<div class="form-group">
 <label class="control-label col-sm-2"><?=get_text("Photo",$lang);?>:</label>
 <div class="col-sm-10">
<div id="person-new-video-container" class="video-container"><video autoplay="true" id="person-new-video-elem" class="video-elem"></video></div>
<div id="person-new-screenshot-container" class="hidden screenshot-container"><img src="blank" alt="output image"><canvas id="person-new-video-canvas"></canvas></div>
<div><button id="person-new-screenshot-button" class="btn btn-success" type="button"><span class="fa fa-camera"></span> <?=get_text("Capture",$lang);?></button>
<button id="person-new-add-screenshot-button" class="btn btn-default" type="button"><span class="fa fa-camera"></span> <?=get_text("Add Photo",$lang);?></button>
<button id="person-new-change-screenshot-button" class="btn btn-warning" type="button"><span class="fa fa-redo-alt"></span> <?=get_text("Change Photo",$lang);?></button>
</div>
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
      <input type="text" class="form-control" id="person-edit-idnum" name="idnum" value="" maxlength="64" required>
 </div>
</div>
<div class="form-group">
 <label class="control-label col-sm-2"><?=get_text("Card Number",$lang);?> (Raw):</label>
 <div class="col-sm-10">
      <input type="number" class="form-control" id="person-edit-cardnum" name="cardnum" value="" min="0" max="2147483646" required>
 </div>
</div>
<div class="form-group">
 <label class="control-label col-sm-2"><?=get_text("Card Number",$lang);?> (FC):</label>
 <div class="col-sm-10">
      <input type="text" class="form-control small_input" id="person-edit-cardnum-fc-1" name="cardnumfc1" value="" maxlength="3">
       , <input type="text" class="form-control" id="person-edit-cardnum-fc-2" name="cardnumfc2" value="" maxlength="32">
 </div>
</div>
<div class="form-group">
 <label class="control-label col-sm-2"><?=get_text("Note",$lang);?>:</label>
 <div class="col-sm-10">
      <input type="text" class="form-control" id="person-edit-note" name="note" value="" maxlength="256">
 </div>
</div>

<div class="form-group">
 <label class="control-label col-sm-2"><?=get_text("Photo",$lang);?>:</label>
 <div class="col-sm-10">
<div id="person-edit-video-container" class="video-container"><video autoplay="true" id="person-edit-video-elem" class="video-elem"></video></div>
<div id="person-edit-screenshot-container" class="hidden screenshot-container"><img src="blank" alt="output image"><canvas id="person-edit-video-canvas" class="hidden"></canvas></div>
<div><button id="person-edit-screenshot-button" class="btn btn-success" type="button"><span class="fa fa-camera"></span> <?=get_text("Capture",$lang);?></button>
<button id="person-edit-add-screenshot-button" class="btn btn-default" type="button"><span class="fa fa-camera"></span> <?=get_text("Add Photo",$lang);?></button>
<button id="person-edit-change-screenshot-button" class="btn btn-warning" type="button"><span class="fa fa-redo-alt"></span> <?=get_text("Change Photo",$lang);?></button>
</div>
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
</style>

<script type="text/javascript">

//init filters
setFilterAction();

var organizationId;

//video vars
var doChangePhoto=0;
var localStream="";

<?php if($logged->roleid!=4){?>
//populate select list
populateList("organizations-select","organizations");

//hide persons select
$("#select-container-persons").hide();

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
		$('#select-container-persons-details').hide();
	}
});

<?php } else { ?>
//populate persons select
populateList("persons-select","persons",<?=$logged->orgid?>);
organizationId=<?=$logged->orgid?>;
//show persons select
$("#select-container-persons").show();
<?php }?>

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
					$('#select-container-persons-details').html("<?=get_text("Identification Number",$lang);?>: "+ values.identNumber +
					"<br><?=get_text("Card Number",$lang);?>: " + values.cardNumber + " - " + rawToFC(values.cardNumber));
					if(values.note && values.note!="") $('#select-container-persons-details').append("<br><?=get_text("Note",$lang);?>: " + values.note);
					//add photo if exists
					$.ajax({
						type: "POST",
						url: "process",
						data: "action=person_has_image&id="+personId,
						success: function(resp){
							if(resp[0]=="1"){
								//person has photo
								var editDate = new Date();
								$('#select-container-persons-details').append("<br><br><img class='details-img' src='persons-image?id="+personId+"&"+editDate.getTime().toString(10)+"'>");
							} //else person does not have photo
						}
					});
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

//init events for cardnum fields (update and live calculation on input)
addCardnumEvents("person-edit");
addCardnumEvents("person-new");

//clear form for new and edit
$('#modal-new,#modal-edit').on('show.bs.modal', function (event){
	//reset form
	$('#person-new-names, #person-new-lastname, #person-new-idnum, #person-new-cardnum, #person-new-cardnum-fc-1, #person-new-cardnum-fc-2,#person-new-note').val("");

	//photo buttons
	$("#person-new-video-container,#person-new-screenshot-button,#person-new-change-screenshot-button").hide();
	$("#person-new-add-screenshot-button").show();
	//clear snapshot img
	$('#person-new-screenshot-container img,#person-edit-screenshot-container img').attr("src","blank");
	$('#person-edit-screenshot-container').hide();
});

//init webcam button events
initCamEvents("person","new");
initCamEvents("person","edit");

//stop streaming on modal close for both modes
$('#modal-new,#modal-edit').on('hidden.bs.modal', function (event){
	stopStream(localStream);
});

//fetch info for edit
$('#modal-edit').on('show.bs.modal', function (event){
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
				$('#person-edit-note').val(values.note);
				var tempfc=rawToFC(values.cardNumber).split(",");
				if(tempfc.length==2) {
					$('#person-edit-cardnum-fc-1').val(myTrim(tempfc[0]));
					$('#person-edit-cardnum-fc-2').val(myTrim(tempfc[1]));
				} else {
					$('#person-edit-cardnum-fc-1').val("");
					$('#person-edit-cardnum-fc-2').val("");
				}
				//photo buttons
				$("#person-edit-video-container,#person-edit-screenshot-button,#person-edit-change-screenshot-button").hide();
				$("#person-edit-add-screenshot-button").show();
				//clear snapshot img
				$('#person-edit-screenshot-container img').attr("src","blank");
				//reset changed photo flag
				doChangePhoto=0;
				//check if user has photo
				$.ajax({
					type: "POST",
					url: "process",
					data: "action=person_has_image&id="+personId,
					success: function(resp){
						if(resp[0]=="1"){
							//show photo and hide buttons accordingly
							//show snapshot img
							var editDate = new Date();
							$('#person-edit-screenshot-container img').attr("src","persons-image?id="+personId+"&"+editDate.getTime().toString(10));
							$('#person-edit-screenshot-container').removeClass("hidden").show();
							//show change button
							$("#person-edit-change-screenshot-button").show();
							//hide add button
							$("#person-edit-add-screenshot-button").hide();
						} // else show add button
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

//import csv validation
$('#form-import-input').on('change', function(){
    //file validation params
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
				//hide details
				$('#select-container-persons-details').hide();
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

//export to excel action
$("#export-csv-button").click(function(){
	organizationId=$("#organizations-select").val();
	//download csv
	$.ajax({
		type: "POST",
		url: "process",
		data: "action=get_persons&id=" + organizationId,
		beforeSend: function(){$(".download-throbber-container").show();$(this).hide()},
		complete: function(resp){$(".download-throbber-container").hide();$(this).show()},
		success: function(resp){
			if(resp[0]=='1'){
				//console.log(resp[1]);
				<?php if($logged->roleid!=4){?>
				organizationName=$("#organizations-select option:selected").html();
				<?php } else { ?>
				organizationName="my-organization";
				<?php }?>
				//trigger csv
				downloadCSV(resp[1],organizationName+".csv");
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
})

function downloadCSV(resultsArr,csvFileName){
	// Each column is separated by ";" and new line "\n" for next row
	var separator = ";";
	var linebreak = '\n';
	//add column names in header
	var csvContent = '<?=get_text("First Name",$lang);?>'+separator+'<?=get_text("Last Name",$lang);?>'+separator+'<?=get_text("Identification Number",$lang);?>'+separator+'<?=get_text("Card Number",$lang);?> (Raw)'+separator+'<?=get_text("Card Number",$lang);?> (FC)'+separator+'<?=get_text("Note",$lang);?>'+linebreak;
	resultsArr.forEach(function(data){
		if(data.resStateId!=5){
			//set no value for null values
			if(data.names === null) data.names="";
			if(data.lastName === null) data.lastName="";
			if(data.note === null) data.note="";

			csvContent += data.names +separator+ data.lastName +separator+ data.identNumber +separator+ data.cardNumber +separator+ rawToFC(data.cardNumber) +separator+ data.note +linebreak;
		}
	});

	// The download function takes a CSV string, the filename and mimeType as parameters
	var download = function(content, fileName, mimeType){
		var a = document.createElement('a');
		mimeType = mimeType || 'application/octet-stream';

		if (navigator.msSaveBlob) { // IE10
			navigator.msSaveBlob(new Blob([content], {
				type: mimeType
			}), fileName);
		} else if (URL && 'download' in a) { //html5 A[download]
			a.href = URL.createObjectURL(new Blob([content], {
				type: mimeType
			}));
			a.setAttribute('download', fileName);
			document.body.appendChild(a);
			a.click();
			document.body.removeChild(a);
		} else {
			location.href = 'data:application/octet-stream,' + encodeURIComponent(content); // only this mime type is supported
		}
	}

	download(csvContent, csvFileName, 'text/csv;encoding:utf-8');
}


//new action
$("#person-new-form").submit(function(){
	var personNames = $("#person-new-names").val();
	var personLastName = $("#person-new-lastname").val();
	var personIdNum = $("#person-new-idnum").val();
	var personCardNum = $("#person-new-cardnum").val();
	var personNote = $("#person-new-note").val();

	if(personNames!="" && personNames!='undefined' && personLastName!="" && personLastName!='undefined'){
		$.ajax({
			type: "POST",
			url: "process",
			data: "action=add_person&orgid=" + organizationId + "&names=" + personNames + "&lastname=" + personLastName + "&idnum=" + personIdNum + "&cardnum=" + personCardNum  + "&note=" + personNote,
			success: function(resp){
				if(resp[0]=='1'){
					//submit photo if set
					if(($("#person-new-screenshot-container img").attr("src") != "blank") && resp[2]>0){
						var new_person_id = resp[2];
						var canvas = document.querySelector("#person-new-video-canvas");
						saveCanvas(canvas,new_person_id);
					}
					//close modal
					$("#modal-new").modal("hide");
					//repopulate select box
					populateList("persons-select","persons",organizationId);
					//hide details
					$('#select-container-persons-details').hide();
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
	var personNote = $("#person-edit-note").val();

	if(!isNaN(personId) && personNames!="" && personNames!='undefined' && personLastName!="" && personLastName!='undefined'){
		$.ajax({
			type: "POST",
			url: "process",
			data: "action=edit_person&id=" + personId +"&orgid=" + organizationId + "&names=" + personNames + "&lastname=" + personLastName + "&idnum=" + personIdNum + "&cardnum=" + personCardNum + "&note=" + personNote,
			success: function(resp){
				if(resp[0]=='1'){
					//submit photo edit if set
					if(doChangePhoto){
						var canvas = document.querySelector("#person-edit-video-canvas");
						saveCanvas(canvas,personId);
					}
					//close modal
					$("#modal-edit").modal("hide");
					//repopulate select box
					populateList("persons-select","persons",organizationId);
					//hide details
					$('#select-container-persons-details').hide();
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
					//hide details
					$('#select-container-persons-details').hide();
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

//Refresh button > repopulate list
$("#persons-refresh").click(function(){
	if(!isNaN(organizationId) && organizationId!="undefined") populateList("persons-select","persons",organizationId);
	//hide details
	$('#select-container-persons-details').hide();
	//disable edit and del buttons
	$("#persons-select-del,#persons-select-edit").prop("disabled",1);
});
</script>

</body>
</html>