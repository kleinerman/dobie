<?
$leavebodyopen=1;
$include_extra_js=array("clockpicker","datepicker");
$requirerole=2;
include("header.php");
?>
<div id="page-wrapper">

<div class="row">
<div class="col-lg-12">
<h1 class="page-header"><?=get_text("Events Purge",$lang);?></h1>
</div>
</div>

<div class="row">
<div class="col-lg-12 center">
<?=get_text("Events before selected date and time will be erased",$lang);?>:<br><br>
<form class="form-horizontal" id="events-prepurge-form" action="#">
<div class="input-group input_date_container" data-placement="left" data-align="top" data-autoclose="true" title="<?=get_text("Purge Until",$lang);?>"><input type="text" class="form-control input_date center" id="endDate" value="<?=date("Y-m-d",mktime(0,0,0)-(60*60*24*7))?>" required><span class="input-group-addon"><span class="fa fa-calendar"></span></span></div>

<div class="input-group clockpicker" data-placement="right" data-align="top" data-autoclose="true" title="<?=get_text("Purge Until Time",$lang);?>"><input type="text" class="form-control from-input" value="00:00" id="endTime" name="endTime" required><span class="input-group-addon"><span class="fa fa-clock-o"></span></span></div>
<br><br>
<button class="btn btn-success"><?=get_text("Delete Events",$lang);?></button>
</form>
</div>
</div>

</div>

<?
include("footer.php");
?>
<!-- MODALS -->
<!-- confirm modal -->
<div class="modal fade" id="modal-purge" tabindex="-1" role="dialog" aria-hidden="true">
<div class="modal-dialog">
<div class="modal-content">
<div class="modal-body center">
<?=get_text("Are you sure you want to remove all events before",$lang);?> <span id="purge-selected-datetime"></span> ? 
</div>
<div class="modal-footer center">
<form class="form-horizontal" id="events-purge-form" action="#">
<button class="btn btn-success"><?=get_text("Yes",$lang);?></button>
<button type="button" class="btn btn-danger" onclick="$('#modal-purge').modal('hide');"><?=get_text("Cancel",$lang);?></button>
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
//init clockpicker
$('.clockpicker').clockpicker();
//init date picker
$(".input_date").datepicker({dateFormat: "yy-mm-dd"});

//set the date when the confirm modal is shown
$('#modal-purge').on('show.bs.modal', function (event){
	$("#purge-selected-datetime").text($("#endDate").val() + " " + $("#endTime").val());
});

$("#events-prepurge-form").submit(function(){
	$('#modal-purge').modal('show');
	return false;
});

//purge action
$("#events-purge-form").submit(function(){
	//get date and time values
	var endDate = $("#endDate").val();
	var endTime = $("#endTime").val();
	if(endDate!="" && endTime!=""){
		$.ajax({
			type: "POST",
			url: "process",
			data: "action=purge_events&untildatetime=" + endDate+"+"+endTime,
			success: function(resp){
				if(resp[0]=='1'){
					//show purged totals
					$('#modal-error .modal-body').text(resp[1].delEvents + " <?=get_text("events were deleted successfully",$lang);?>");
					$("#modal-error").modal("show");
				} else {
					//show modal error
					$('#modal-error .modal-body').text(resp[1]);
					$("#modal-error").modal("show");
				}
			},
			complete: function(resp){
				$("#modal-purge").modal("hide");
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