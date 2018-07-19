<?
$leavebodyopen=1;
$requirerole=2;
include("header.php");
?>
<div id="page-wrapper">

<div class="row">
<div class="col-lg-12">
<h1 class="page-header">Access - Person -> Door</h1>
</div>
</div>

<div class="row">
<!-- left column start -->
<div class="col-lg-12 center">
<br>

<div class="row">

<div class="col-lg-3">

<div class="select-container">
<div class="select-container-title">Organizations</div>
<div class="select-container-body">
<input type="text" name="filter" placeholder="Filter options..." class="form-control data-filter" data-filter="organizations-select">
<select id="organizations-select" class="select-options select-options-small form-control" name="organizations-select" size="2"></select>
</div>
</div>

<br><br>

<div class="select-container" id="select-container-persons" style="display:none">
<div class="select-container-title">Person</div>
<div class="select-container-body">
<input type="text" name="filter" placeholder="Filter options..." class="form-control data-filter" data-filter="person-select">
<select id="persons-select" class="select-options select-options-small form-control" name="persons-select" size="2" onchange="updateButtons(this.id)"></select>
</div>
<div class="select-container-footer">
<div class="left">
<button id="persons-select-all" class="btn btn-success" type="button" data-toggle="modal" data-target="#modal-edit">Add to all...</button>
</div>
</div>
</div>

</div>

<div class="col-lg-9 center">

<div class="table-container" id="accesses-table-container" style="display:none">
<input type="text" name="filter" placeholder="Filter names..." class="form-control data-filter-table" data-filter="access-table">
<table id="access-table" class="table-bordered table-hover table-condensed table-responsive table-striped left">
</table>
</div>

</div>

</div>

<br><br>
<div class="row" id="buttons-row" style="display:none">
<div class="col-sm-4"><button id="access-new" class="btn btn-success" type="button" data-toggle="modal" data-target="#modal-edit">Add</button></div>
<div class="col-sm-4"><button id="access-edit" class="btn btn-primary" type="button" data-toggle="modal" data-target="#modal-edit">Edit</button></div>
<div class="col-sm-4"><button id="access-del" class="btn btn-danger" type="button" data-toggle="modal" data-target="#modal-delete">Delete</button></div>
</div>

</div>

</div>

</div>

<?
include("footer.php");
?>

<!-- MODALS -->
<!-- add modal -->
<div class="modal fade" id="modal-add" tabindex="-1" role="dialog" aria-hidden="true">
<div class="modal-dialog">
<div class="modal-content">
<div class="modal-header">
<button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>
<h4 class="modal-title" id="modal-add-label">&nbsp;</h4>
</div>
<div class="modal-body center">
<iframe class="iframe iframe-big" src="blank"></iframe>
</div>
</div>
</div>
<!-- /.modal -->
</div>

<!-- edit modal -->
<div class="modal fade modal-full" id="modal-edit" tabindex="-1" role="dialog" aria-hidden="true">
<div class="modal-dialog">
<div class="modal-content">
<div class="modal-header">
<button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>
<h4 class="modal-title" id="modal-edit-label">&nbsp;</h4>
</div>
<div class="modal-body center">
<iframe class="iframe iframe-big" src="blank"></iframe>
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
<form class="form-horizontal" id="access-delete-form" action="#">
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

//populate accesses table
function populateTable(tableId,personId){
	//clear table
	$('#'+tableId).empty();
	$.ajax({
		type: "POST",
		url: "process",
		data: "action=get_person_accesses&id=" + personId,
		success: function(resp){
			if(resp[0]=='1'){
				var values = resp[1];
				//set table headers
				$('#'+tableId).append("<tr><th class=\"smallcol\"><input type=\"checkbox\" id=\"accessesAll\" name=\"accessesAll\" value=\"1\"></th><th>Door</th><th>Zone</th><th class=\"center\">All Week</th></tr>");
				//populate fields with rec info
				for(i=0;i<values.length;i++){
					//set row class
					itemClass="";
					if(values[i].resStateId==1) itemClass=" class='toadd' ";
					else if(values[i].resStateId==2) itemClass=" class='toupd' ";
					else if(values[i].resStateId==4) itemClass=" class='todel' ";
					//show row
					if(values[i].allWeek=="1") allWeekStr="<span class=\"fa fa-check\"></span>";
					else allWeekStr = "";
					if(values[i].resStateId==3) $('#'+tableId).append("<tr"+itemClass+"><td><input type=\"checkbox\" name=\"accesses[]\" value="+values[i].id+"></td><td>"+values[i].doorName+"</td><td>"+values[i].zoneName+"</td><td class=\"center\">"+allWeekStr+"</td></tr>");
					else $('#'+tableId).append("<tr"+itemClass+"><td></td><td>"+values[i].doorName+"</td><td>"+values[i].zoneName+"</td><td class=\"center\">"+allWeekStr+"</td></tr>");
				}
				//add trigger events for rows
				tableClickEvents();
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

$("#organizations-select").change(function(){
	organizationId=$("#organizations-select").val();
	if(!isNaN(organizationId) && organizationId!="undefined"){
		//populate list
		populateList("persons-select","persons",organizationId);
		//hide accesses table
		$("#accesses-table-container").hide();
		//show list
		$("#select-container-persons").fadeIn();
	}
});

$("#persons-select").change(function(){
	personId=$("#persons-select").val();
	if(!isNaN(personId) && personId!="undefined"){
		//populate access list
		populateTable("access-table",personId);
		//show list
		$("#accesses-table-container").fadeIn();
		//show buttons
		$("#buttons-row").fadeIn();
		//disable buttons
		$("#access-edit,#access-del").prop("disabled",true);
	}
});

//Add to all button > open iframe modal
$("#persons-select-all").click(function(){
	var orgId= $("#organizations-select").val();
	$("#modal-edit").find('iframe').prop('src','access-edit-person?personid=all&orgid='+orgId);
});

//Add button > open iframe modal
$("#access-new").click(function(){
	var personId= $("#persons-select").val();
	$("#modal-edit").find('iframe').prop('src','access-edit-person?personid='+personId);
});

//Edit button > open iframe modal
$("#access-edit").click(function(){
	var accessId= $("input[name='accesses[]']:checked").val();
	$("#modal-edit").find('iframe').prop('src','access-edit-person?id='+accessId);
});

//Delete button action
$("#access-delete-form").submit(function(){
	var selectedItems = [];
	$("input[name='accesses[]']:checked").each(function() {selectedItems.push($(this).val())});

	if(selectedItems.length>0){
		$.ajax({
			type: "POST",
			url: "process",
			data: "action=delete_access_bulk&ids=" + selectedItems.join("|"),
			success: function(resp){
				if(resp[0]=='1'){
					//close modal
					$("#modal-delete").modal("hide");
					//repopulate table
					populateTable("access-table",$("#persons-select").val());
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
		//no rows selected
		$('#modal-error .modal-body').text("Make sure to select at least 1 row");
		$("#modal-error").modal("show");
	}
	return false;
});
</script>

</body>
</html>