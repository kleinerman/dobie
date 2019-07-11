<?
$leavebodyopen=1;
include("header.php");
?>
<div id="page-wrapper">

<div class="row">
<div class="col-lg-12">
<h1 class="page-header"><?=get_text("Search Persons",$lang);?></h1>
</div>
</div>

<div class="row">
<div class="col-md-3">

<form class="form-horizontal" id="person-search-form" action="#">
<div class="form-group">
<label class="control-label"><?=get_text("Names Pattern",$lang);?>:</label><br>
<input type="text" class="form-control" id="person-search-names" name="names" value="" maxlength="64">
</div>
<div class="form-group">
 <label class="control-label"><?=get_text("Last Name Pattern",$lang);?>:</label><br>
      <input type="text" class="form-control" id="person-search-lastname" name="lastname" value="" maxlength="64">
</div>
<div class="form-group">
 <label class="control-label"><?=get_text("Identification Number",$lang);?>:</label><br>
      <input type="text" class="form-control" id="person-search-idnum" name="idnum" value="" maxlength="64">
</div>
<div class="form-group">
 <label class="control-label"><?=get_text("Card Number",$lang);?> (Raw):</label><br>
      <input type="number" class="form-control cardnum-fc" id="person-search-cardnum" name="cardnum" value="" min="0" max="2147483646">
</div>
<div class="form-group">
 <label class="control-label"><?=get_text("Card Number",$lang);?> (FC):</label><br>
      <input type="text" class="form-control small_input cardnum-fc" id="person-search-cardnum-fc-1" name="cardnumfc1" value="" maxlength="3">
       , <input type="text" class="form-control cardnum-fc cardnum-fc-2" id="person-search-cardnum-fc-2" name="cardnumfc2" value="" maxlength="32">
</div>

<br>

<div class="center">
<button class="btn btn-success" id="person-search-submit"><span class="fa fa-search fa-fw"></span> <?=get_text("Search",$lang);?></button> <button type="button" class="btn btn-warning" id="person-reset-filter"><span class="fa fa-power-off fa-fw"></span> <?=get_text("Reset",$lang);?></button>
</div>
<br>
</form>


</div>


<div class="col-md-9">
<div id="persons-search-results-container" class="table-responsive gowide">
</div>
</div>
</div>

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
<?
include("footer.php");
?>

<script>
//init events for cardnum fields (update and live calculation on input)
addCardnumEvents("person-search");

//outputs html for event table based on received data from api
function buildResultTable(data){
	//init headers
	var ret_string='<table id="events-table" class="table-bordered table-hover table-condensed table-striped left"><tr><th><?=get_text("Names",$lang);?></th><th><?=get_text("Last Name",$lang);?></th><th><?=get_text("Organization",$lang);?></th><th class="center"><?=get_text("Ident. #",$lang);?></th><th class="center"><?=get_text("Card #",$lang);?></th><th class="center"><?=get_text("Note",$lang);?></th></tr>';

	for(var i=0;i<data.length;i++){
		//set no value for null values
		if(data[i].orgName === null) data[i].orgName="";
		if(data[i].names === null) data[i].names="";
		if(data[i].lastName === null) data[i].lastName="";
		if(data[i].note === null) data[i].note="";

		if(!isNaN(data[i].cardNumber)) data[i].cardNumberFull = data[i].cardNumber + " ("+rawToFC(data[i].cardNumber)+")";
		else data[i].cardNumberFull = data[i].cardNumber;

		//build row
		ret_string+="<tr><td>"+ data[i].names +"</td><td>"+ data[i].lastName +"</td><td>"+ data[i].orgName +"</td><td class=\"center\">"+ data[i].identNumber +"</td><td class=\"center\">"+ data[i].cardNumberFull +"</td><td class=\"center\">"+ data[i].note +"</td></tr>";
	}

	ret_string+="</table>";
	return ret_string;
}

//new action
$("#person-search-form").submit(function(){
	var personNames = $("#person-search-names").val();
	var personLastName = $("#person-search-lastname").val();
	var personIdNum = $("#person-search-idnum").val();
	var personCardNum = $("#person-search-cardnum").val();

	if(personNames!="" || personLastName!="" || personIdNum!="" || personCardNum!=""){
		$.ajax({
			type: "POST",
			url: "process",
			data: "action=search_person&names=" + personNames + "&lastname=" + personLastName + "&idnum=" + personIdNum + "&cardnum=" + personCardNum,
			success: function(resp){
				if(resp[0]=='1'){
					//populate results
					$("#persons-search-results-container").html(buildResultTable(resp[1]));
				} else {
					//show no results / error on resp[1]
					$("#persons-search-results-container").html("<div class='center'>"+resp[1]+"</div>");
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
		$('#modal-error .modal-body').text("<?=get_text("Please fill at least one field",$lang);?>");
		$("#modal-error").modal("show");
	}
	return false;
});

$("#person-reset-filter").click(function(){
	location.reload();
});
</script>

</body>
</html>