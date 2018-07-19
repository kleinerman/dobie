<?
$leavebodyopen=1;
$requirerole=1;
include("header.php");
?>

<div id="page-wrapper">

<div class="row">
<div class="col-lg-12">
<h1 class="page-header">System Users</h1>
</div>
</div>

<div class="row">
<div class="col-lg-12">

<div class="table-container" id="rows-table-container">
<input type="text" name="filter" placeholder="Filter names..." class="form-control data-filter-table" data-filter="rows-table">
<table id="rows-table" class="table-bordered table-hover table-condensed table-responsive table-striped left">
</table>
</div>

<br><br>
<div class="row" id="buttons-row">
<div class="col-sm-4"><button id="rows-new" class="btn btn-success" type="button" data-toggle="modal" data-target="#modal-new">Add</button></div>
<div class="col-sm-4"><button id="rows-edit" class="btn btn-primary" type="button" data-toggle="modal" data-target="#modal-new" disabled>Edit</button></div>
<div class="col-sm-4"><button id="rows-del" class="btn btn-danger" type="button" data-toggle="modal" data-target="#modal-delete" disabled>Delete</button></div>
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
<h4 class="modal-title" id="modal-new-label">New System User</h4>
</div>
<form class="form-horizontal" id="user-new-form" action="#">
<div class="modal-body">

<div class="form-group">
 <label class="control-label col-sm-2">Full Name:</label>
 <div class="col-sm-10">
      <input type="text" class="form-control" id="user-new-fullname" name="fullname" value="" required maxlength="64">
 </div>
</div>
<div class="form-group">
 <label class="control-label col-sm-2">Username:</label>
 <div class="col-sm-10">
      <input type="text" class="form-control" id="user-new-name" name="name" value="" required maxlength="64">
 </div>
</div>
<div class="form-group">
 <label class="control-label col-sm-2">Password:</label>
 <div class="col-sm-10">
      <input type="password" class="form-control" id="user-new-password" name="password" value="">
 </div>
</div>
<div class="form-group">
 <label class="control-label col-sm-2">Confirm Password:</label>
 <div class="col-sm-10">
      <input type="password" class="form-control" id="user-new-cpassword" name="cpassword" value="">
 </div>
</div>
<div class="form-group">
 <label class="control-label col-sm-2">Role:</label>
 <div class="col-sm-10">
      <select id="user-new-role" name="role" required></select>
 </div>
</div>
<div class="form-group">
 <label class="control-label col-sm-2">Active:</label>
 <div class="col-sm-10">
      <input type="checkbox" id="user-new-active" name="active" value="1">
 </div>
</div>

</div>
<div class="modal-footer">
<button class="btn btn-success" id="user-new-submit">Save</button>
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
<form class="form-horizontal" id="user-delete-form" action="#">
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
var roleText=[];

//populate role text array
$(function(){
	$.ajax({
		type: "POST",
		url: "process",
		data: "action=get_roles",
		success: function(resp){
			if(resp[0]=='1'){
				var values = resp[1];
				//copy values into roleText array
				values.forEach(function(item,index){roleText[item.id]=item.description;});
			} else {
				//assign default values
				roleText[1]="Administrator";
				roleText[2]="Operator";
				roleText[3]="Viewer";
			}
			populateTable("rows-table");
		},
		failure: function(){
			//show modal error
			$('#modal-error .modal-body').text("Could not load roles");
			$("#modal-error").modal("show");
		}
	});
});

function tableClickEvents2(){
	//clickable rows for editable tables
	$("#rows-table tr td:nth-child(n+2)").click(function(){
		$(this).parent().find("input[type=checkbox]").click();
	})

	//unclick All checkbox on row click
	$("#rows-table tr td input[type=checkbox]").click(function(){
		if($("#rowsAll").prop("checked")) $("#rowsAll").prop("checked",false);
	})

	//click All event
	$("#rowsAll").click(function(){
		if($(this).prop("checked")) {
			$("#rows-table td input[type=checkbox]").prop("checked",true);
			//$("#rows-del").prop("disabled",false);
			if($('#rows-table tr td input[type=checkbox]:checked').length == 1) $("#rows-edit,#rows-del").prop("disabled",false);
		} else {
			$("#rows-table td input[type=checkbox]").prop("checked",false);
			//no rows selected > disable both
			$("#rows-edit,#rows-del").prop("disabled",true);
		}
	})
	
	//edit / delete  button toggle
	$('#rows-table tr td input:checkbox').change(function(){
		if($('#rows-table tr td input[type=checkbox]:checked').length > 0) {
			//if at least 1 row selected > enable delete
			//$("#rows-del").prop("disabled",false);
			//enable edit only if 1 row is selected
			if($('#rows-table tr td input[type=checkbox]:checked').length > 1) $("#rows-edit,#rows-del").prop("disabled",true);
			else $("#rows-edit,#rows-del").prop("disabled",false);
		} else {
			//no rows selected > disable both
			$("#rows-edit,#rows-del").prop("disabled",true);
		}
	});
}

//populate editable table
function populateTable(tableId){
	//clear table
	$('#'+tableId).empty();
	$.ajax({
		type: "POST",
		url: "process",
		data: "action=get_users",
		success: function(resp){
			if(resp[0]=='1'){
				var values = resp[1];
				//set table headers
				$('#'+tableId).append("<tr><th class=\"smallcol\"><input type=\"checkbox\" id=\"rowsAll\" name=\"rowsAll\" value=\"1\"></th><th>Username</th><th>Description</th><th>Role</th><th class=\"center\">Active</th></tr>");
				//populate fields with rec info
				for(i=0;i<values.length;i++){
					//show row
					if(values[i].active=="1") activeStr="<span class=\"fa fa-check\"></span>";
					else activeStr= "";
					$('#'+tableId).append("<tr><td><input type=\"checkbox\" name=\"users[]\" value="+values[i].id+"></td><td>"+values[i].username+"</td><td>"+values[i].fullName+"</td><td>"+roleText[values[i].roleId]+"</td><td class=\"center\">"+activeStr+"</td></tr>");
				}
				//add trigger events for rows
				tableClickEvents2();
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

function resetForm(){
	//clear text fields
	$("#user-new-name,#user-new-fullname,#user-new-password,#user-new-cpassword").val("");
	//unselect options in fixed selects
	$('#user-new-role').empty();
	//populate role select
	roleText.forEach(function(item,index){$('#user-new-role').append("<option value='"+index+"'>"+item+"</option>");});
	//clear checkboxes
	$('#user-new-active').prop("checked",true);
	//clear id value if edit
	editId=0;
	//enable fields in case admin has been editing
	$('#user-new-name,#user-new-fullname,#user-new-role,#user-new-active').prop("disabled",false);
	//clear placeholder on passw fields
	$('#user-new-password,#user-new-cpassword').prop("placeholder","");
	//set passw fields to required
	$('#user-new-password,#user-new-cpassword').prop("required",true);
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

$('#modal-new').on('show.bs.modal', function (event){
	//clear all previous values
	resetForm();
});

$("#rows-new").click(function(){
	$("#modal-new-label").text("New System User");
});

//fetch info for edit
$("#rows-edit").click(function(){
	var userId = $('#rows-table tr td input[type=checkbox]:checked')[0].value;
	$("#modal-new-label").text("Edit User");
	$.ajax({
		type: "POST",
		url: "process",
		data: "action=get_user&id=" + userId,
		success: function(resp){
			if(resp[0]=='1'){
				//populate fields with rec info
				var values = resp[1];
				editId=userId;
				$('#user-new-name').val(values.username);
				$('#user-new-fullname').val(values.fullName);
				//select role id option >populate the box with the option selected
				$('#user-new-role').empty();
				roleText.forEach(function(v,k){
					if(k==values.roleId) $('#user-new-role').append("<option value='"+k+"' selected>"+v+"</option>");
					else $('#user-new-role').append("<option value='"+k+"'>"+v+"</option>");
				});
				//check active value
				if(values.active==1) $('#user-new-active').prop("checked",true);
				else $('#user-new-active').prop("checked",false);
				
				//disable fields if editing admin
				if(userId==1){
					$('#user-new-name,#user-new-fullname,#user-new-role,#user-new-active').prop("disabled",true);
				}
				//set placeholder on passw fields
				$('#user-new-password,#user-new-cpassword').prop("placeholder","****");
				//disabled required on passw fields
				$('#user-new-password,#user-new-cpassword').prop("required",false);
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

//submit action
$("#user-new-form").submit(function(){

	var userFullName = $("#user-new-fullname").val();
	var userName = $("#user-new-name").val();
	var userPassword = $("#user-new-password").val();
	var userCPassword = $("#user-new-cpassword").val();
	var userRole = $('#user-new-role').val();
	if(typeof($('#user-new-active:checked').val())=="undefined") {var userActive = 0} else {var userActive = 1}
	var errorTxt="";

	if(editId!=0 && !isNaN(editId)) action_str="action=edit_user&id=" + editId;
	else action_str="action=add_user";

	action_str+= "&fullname=" + userFullName + "&username=" + userName + "&password=" + userPassword + "&roleid=" + userRole + "&active=" + userActive;

	if(userPassword!=userCPassword){
		errorTxt="Password and confirmation don't match";
	} else if(isNaN(userRole)){
		errorTxt="Invalid role sent";
	} else if(userFullName=="" || userName=="" || (userPassword=="" && editId==0)){
		errorTxt="Please fill all required fields";
	} else {
		$.ajax({
			type: "POST",
			url: "process",
			data: action_str,
			success: function(resp){
				if(resp[0]=='1'){
					//close modal
					$("#modal-new").modal("hide");
					//repopulate table
					populateTable("rows-table");
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
	}
	
	if(errorTxt!=""){
		//invalid values sent
		$('#modal-error .modal-body').text(errorTxt);
		$("#modal-error").modal("show");
	}
	return false;
});

//delete action
$("#user-delete-form").submit(function(){
	var userId = $('#rows-table tr td input[type=checkbox]:checked').val();

	if(!isNaN(userId)){
		if(userId==1){
			//admin user cant be deleted
			$('#modal-error .modal-body').text("Admin user cannot be deleted");
			$("#modal-error").modal("show");
		} else {
			$.ajax({
				type: "POST",
				url: "process",
				data: "action=delete_user&id=" + userId,
				success: function(resp){
					if(resp[0]=='1'){
						//close modal
						$("#modal-delete").modal("hide");
						//repopulate table
						populateTable("rows-table");
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
		}
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