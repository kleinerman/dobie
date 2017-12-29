<?
$leavebodyopen=1;
$innerheader=1;
$include_extra_js=array("clockpicker","datepicker");

//get access ID or create mode
$id = (isset($_GET["id"]) & is_numeric($_GET["id"])) ? $_GET["id"] : "0";
$personid = (isset($_GET["personid"]) & is_numeric($_GET["personid"])) ? $_GET["personid"] : "0";

include("header.php");
?>
<div id="wrapper" class="container-fluid">

<div class="row">
<!-- /.col-lg-12 -->
<div class="col-lg-12">
<h3 class="page-header" id="page-header"></h3>
</div>
<!-- /.col-lg-12 -->
</div>

<div class="row">

<?if(!$id){?>
<!-- left column start -->
<div class="col-lg-3">

<div class="select-container">
<form action="javascript:void(0)">
<div class="select-container-title">Zone</div>
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
</form>
</div>

</div>


<div class="col-lg-9 center" id="schedule-container" style="display:none">
<?} else {?>
<div class="col-lg-12 center">
<?}?>
<br>

<div class="row">

<div class="col-lg-12 center">
<div class="select-container-title">Schedule</div>
<div class="schedule-container">
<form id="access-edit-form" action="#">
<table id="schedule-table" class="table-condensed table-responsive left">
<tr><th>Day</th><th>Time interval</th><th class="center">Incoming</th><th class="center">Outgoing</th><th class="center">Both</th></tr>
<tr><td><label><input type="checkbox" id="allWeek_check" name="days" value="" checked> Every day</label></td>
<td>
<div class="input-group clockpicker" data-placement="left" data-align="top" data-autoclose="true" title="From"><input type="text" class="form-control from-input" value="08:00" name="from0"><span class="input-group-addon"><span class="fa fa-clock-o"></span></span></div>
<div class="input-group clockpicker" data-placement="left" data-align="top" data-autoclose="true" title="Until"><input type="text" class="form-control until-input" value="18:00" name="to0"><span class="input-group-addon"><span class="fa fa-clock-o"></span></span></div>
</td><td class="center"><input type="radio" name="way0" value="1">
</td><td class="center"><input type="radio" name="way0" value="2">
</td><td class="center"><input type="radio" name="way0" value="3" checked>
</td>
</tr>

<tr class="dayrow"><td><label><input type="checkbox" name="days" value="1"> Monday</label></td>
<td>
<div class="input-group clockpicker" data-placement="left" data-align="top" data-autoclose="true" title="From"><input type="text" class="form-control from-input" value="08:00" name="from1"><span class="input-group-addon"><span class="fa fa-clock-o"></span></span></div>
<div class="input-group clockpicker" data-placement="left" data-align="top" data-autoclose="true" title="Until"><input type="text" class="form-control until-input" value="18:00" name="to1"><span class="input-group-addon"><span class="fa fa-clock-o"></span></span></div>
</td><td class="center"><input type="radio" name="way1" value="1">
</td><td class="center"><input type="radio" name="way1" value="2">
</td><td class="center"><input type="radio" name="way1" value="3" checked>
</td>
</tr>

<tr class="dayrow"><td><label><input type="checkbox" name="days" value="2"> Tuesday</label></td>
<td>
<div class="input-group clockpicker" data-placement="left" data-align="top" data-autoclose="true" title="From"><input type="text" class="form-control from-input" value="08:00" name="from2"><span class="input-group-addon"><span class="fa fa-clock-o"></span></span></div>
<div class="input-group clockpicker" data-placement="left" data-align="top" data-autoclose="true" title="Until"><input type="text" class="form-control until-input" value="18:00" name="to2"><span class="input-group-addon"><span class="fa fa-clock-o"></span></span></div>
</td><td class="center"><input type="radio" name="way2" value="1">
</td><td class="center"><input type="radio" name="way2" value="2">
</td><td class="center"><input type="radio" name="way2" value="3" checked>
</td>
</tr>

<tr class="dayrow"><td><label><input type="checkbox" name="days" value="3"> Wednesday</label></td>
<td>
<div class="input-group clockpicker" data-placement="left" data-align="top" data-autoclose="true" title="From"><input type="text" class="form-control from-input" value="08:00" name="from3"><span class="input-group-addon"><span class="fa fa-clock-o"></span></span></div>
<div class="input-group clockpicker" data-placement="left" data-align="top" data-autoclose="true" title="Until"><input type="text" class="form-control until-input" value="18:00" name="to3"><span class="input-group-addon"><span class="fa fa-clock-o"></span></span></div>
</td><td class="center"><input type="radio" name="way3" value="1">
</td><td class="center"><input type="radio" name="way3" value="2">
</td><td class="center"><input type="radio" name="way3" value="3" checked>
</td>
</tr>

<tr class="dayrow"><td><label><input type="checkbox" name="days" value="4"> Thursday</label></td>
<td>
<div class="input-group clockpicker" data-placement="left" data-align="top" data-autoclose="true" title="From"><input type="text" class="form-control from-input" value="08:00" name="from4"><span class="input-group-addon"><span class="fa fa-clock-o"></span></span></div>
<div class="input-group clockpicker" data-placement="left" data-align="top" data-autoclose="true" title="Until"><input type="text" class="form-control until-input" value="18:00" name="to4"><span class="input-group-addon"><span class="fa fa-clock-o"></span></span></div>
</td><td class="center"><input type="radio" name="way4" value="1">
</td><td class="center"><input type="radio" name="way4" value="2">
</td><td class="center"><input type="radio" name="way4" value="3" checked>
</td>
</tr>

<tr class="dayrow"><td><label><input type="checkbox" name="days" value="5"> Friday</label></td>
<td>
<div class="input-group clockpicker" data-placement="left" data-align="top" data-autoclose="true" title="From"><input type="text" class="form-control from-input" value="08:00" name="from5"><span class="input-group-addon"><span class="fa fa-clock-o"></span></span></div>
<div class="input-group clockpicker" data-placement="left" data-align="top" data-autoclose="true" title="Until"><input type="text" class="form-control until-input" value="18:00" name="to5"><span class="input-group-addon"><span class="fa fa-clock-o"></span></span></div>
</td><td class="center"><input type="radio" name="way5" value="1">
</td><td class="center"><input type="radio" name="way5" value="2">
</td><td class="center"><input type="radio" name="way5" value="3" checked>
</td>
</tr>

<tr class="dayrow"><td><label><input type="checkbox" name="days" value="6"> Saturday</label></td>
<td>
<div class="input-group clockpicker" data-placement="left" data-align="top" data-autoclose="true" title="From"><input type="text" class="form-control from-input" value="08:00" name="from6"><span class="input-group-addon"><span class="fa fa-clock-o"></span></span></div>
<div class="input-group clockpicker" data-placement="left" data-align="top" data-autoclose="true" title="Until"><input type="text" class="form-control until-input" value="18:00" name="to6"><span class="input-group-addon"><span class="fa fa-clock-o"></span></span></div>
</td><td class="center"><input type="radio" name="way6" value="1">
</td><td class="center"><input type="radio" name="way6" value="2">
</td><td class="center"><input type="radio" name="way6" value="3" checked>
</td>
</tr>

<tr class="dayrow"><td><label><input type="checkbox" name="days" value="7"> Sunday</label></td>
<td>
<div class="input-group clockpicker" data-placement="left" data-align="top" data-autoclose="true" title="From"><input type="text" class="form-control from-input" value="08:00" name="from7"><span class="input-group-addon"><span class="fa fa-clock-o"></span></span></div>
<div class="input-group clockpicker" data-placement="left" data-align="top" data-autoclose="true" title="Until"><input type="text" class="form-control until-input" value="18:00" name="to7"><span class="input-group-addon"><span class="fa fa-clock-o"></span></span></div>
</td><td class="center"><input type="radio" name="way7" value="1">
</td><td class="center"><input type="radio" name="way7" value="2">
</td><td class="center"><input type="radio" name="way7" value="3" checked>
</td>
</tr>
</table>
<br>

<div class="left">
Expiration Date: <label><input type="radio" name="expiration" value="0" checked> No</label> <label><input type="radio" name="expiration" value="1"> Yes</label> &nbsp;&nbsp;<input type="text" class="form-control center" name="expiration_date" id="expiration_date" value="<?=date("Y-m-d",mktime(0,0,0)+(60*60*24*365))?>">
<br><br>
<button class="btn btn-success" type="submit">Save</button>
</div>

</form>
</div>
</div>
</div>
</div>

<br><br><br>
<!--END BODY -->
</div>
<!-- /#page-wrapper -->
</div>
<!-- /#wrapper -->

<? include("footer.php"); ?>


<style type="text/css">
.select-options{
	height:200px !important;
}

.clockpicker{
	display:inline-table;
	width:100px;
}

#expiration_date{
	display:none;
	width: 100px;
}

#schedule-table{
	border: 1px solid #ccc;
	width: 100%;
}

.ui-datepicker{
	z-index:10 !important;
}
</style>

<script type="text/javascript">
//init filters
setFilterAction();

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
		//hide schedule
		$("#schedule-container").hide();
	}
});

$("#doors-select").change(function(){
	//show schedule
	$("#schedule-container").fadeIn();
});

//init input filters
$(".data-filter").keyup(function(){
	var options=$("#"+$(this).data("filter") + " option");
	var filterValue=$(this).val().toLowerCase();
	options.each(function(){
		if($(this).text().toLowerCase().includes(filterValue)) $(this).show();
		else $(this).hide();
	})
});

//init table input filter
$(".data-filter-table").keyup(function(){
	var rows=$("#"+$(this).data("filter") + " tr");
	var filterValue=$(this).val().toLowerCase();
	rows.each(function(){
		if($(this).find("td").text().toLowerCase().includes(filterValue)) $(this).show();
		else $(this).hide();
	})
	//show header row
	$("#"+$(this).data("filter") + " tr:first-child").show();
});

//expiration date toggle
$("input[name=expiration]").change(function(){
	if($(this).prop("checked") && $(this).val()==1) {
		$("#expiration_date").fadeIn();
	} else $("#expiration_date").fadeOut();
});

//initial show/hide
if($("input[name=expiration]:checked").val()!=0) $("#expiration_date").fadeIn();

//init clockpicker
$('.clockpicker').clockpicker();

//init date picker
$(function(){
	$("#expiration_date").datepicker({dateFormat: "yy-mm-dd"});
});

//checkbox click events
$("input[name=days]").click(function(){
	if($(this).val()==""){
		//if All button
		if($(this).prop("checked")){
			//check all days
			$("input[name=days]").prop("checked",true);
			$(".dayrow").hide();
		} else {
			//uncheck all days
			$("input[name=days]").prop("checked",false);
			$(".dayrow").show();
		}
	} else {
		//rest of buttons
		$("input[name=days]:first").prop("checked",false);
	}
});

function addZeroPadding(str){
	str_parts=str.split(":");
	if(str_parts.length>1 && str_parts[0].length==1) str_parts[0]="0"+str_parts[0];
	return str_parts.join(":");
}

//initial check all days
$("input[name=days]").prop("checked",true);
//hide days rows, only leave All Days visible
$(".dayrow").hide();
				
//fetch values if set
var accessId=<?=$id?>;
var personId=<?=$personid?>;
//init array for edit access values
var values;

//populate form if edit or create
if(!accessId){
	//if create
	//populate header with person name
	$("#page-header").text("New access for " + parent.$("#persons-select option:selected").text());
} else {
	//if edit
	//fetch access data
	$.ajax({
	type: "POST",
	url: "process",
	data: "action=get_access&id="+accessId,
	success: function(resp){
		//init values
		if(resp[0]=='1'){
			values = resp[1];
			//console.log(values);
			//populate header as Edit Access for Door/Person
			$("#page-header").text("Editing "+ values.personName + " -> " + values.doorName);
			//mark checkboxes according to days
			if(values.allWeek){
				//check allweek box > is checked by default
				//fill start and end times
				$(".from-input").val(addZeroPadding(values.startTime).split(":").slice(0,2).join(":"));
				$(".until-input").val(addZeroPadding(values.endTime).split(":").slice(0,2).join(":"));
				//check in out both
				if(values.iSide && !values.oSide){
					//check incoming
					$(".dayrow input[type=radio][value=1], input[name=way0][value=1]").prop("checked",true);
				} else if(!values.iSide && values.oSide){
					//check outgoing
					$(".dayrow input[type=radio][value=2], input[name=way0][value=2]").prop("checked",true);
				} else {
					//check both
					$(".dayrow input[type=radio][value=3], input[name=way0][value=3]").prop("checked",true);
				}
			} else {
				//uncheck all days
				$(".dayrow").show();
				$("input[name=days]").prop("checked",false);
				for(i=0;i<values.liAccesses.length;i++){
					currLiAccess=values.liAccesses[i];
					currLiAccessWeekDay=currLiAccess.weekDay;
					//check day
					$("input[name=days][value="+currLiAccessWeekDay+"]").prop("checked",true);
					//fill start and end times
					$("input[name=from"+currLiAccessWeekDay+"]").val(addZeroPadding(currLiAccess.startTime).split(":").slice(0,2).join(":"));
					$("input[name=to"+currLiAccessWeekDay+"]").val(addZeroPadding(currLiAccess.endTime).split(":").slice(0,2).join(":"));

					//check in out both
					if(currLiAccess.iSide && !currLiAccess.oSide){
						//check incoming
						$("input[name=way"+currLiAccessWeekDay+"][value=1]").prop("checked",true);
					} else if(!currLiAccess.iSide && currLiAccess.oSide){
						//check outgoing
						$("input[name=way"+currLiAccessWeekDay+"][value=2]").prop("checked",true);
					} else {
						//check both
						$("input[name=way"+currLiAccessWeekDay+"][value=3]").prop("checked",true);
					}
				}
			}
			//fill expiration date: TODO: remove time when it comes stripped from the API
			if(values.expireDate !== "undefined" && values.expireDate!="9999-12-31 00:00"){
				//check yes
				$("input[name=expiration][value=1]").prop("checked",true);
				//fill date
				$("#expiration_date").val(values.expireDate.split(" ")[0]);
				//show field
				$("#expiration_date").show();
			}
		} else {
			//show error
			alert("Error fetching access data");
		}
	},
	failure: function(){
			//show error
			alert("Error fetching access data");
		}
	});
}

//edit / create action
$("#access-edit-form").submit(function(){
	//init obj for create/edit
	var accessRec={};

	// if expiration date > set value
	var hasExpiration = $("input[name=expiration]:checked").val();
	if(hasExpiration==1) accessRec.expireDate = $("#expiration_date").val();
	else accessRec.expireDate = "9999-12-31";

	// get access ID
	if(!accessId){
		//create
		accessRec.doorId = parseInt($("#doors-select").val());
		accessRec.personId = personId;
		// get allWeek
		var allWeek_check = $("#allWeek_check").prop("checked");
		if(allWeek_check){
			//is allWeek
			accessRec.allWeek=1;
			// get start, end and way
			accessRec.startTime = $("input[name=from0]").val();
			accessRec.endTime = $("input[name=to0]").val();
			var way = $("input[name=way0]:checked").val();
			accessRec.iSide = (way%2);
			accessRec.oSide = Math.floor(way/2);
			//here post ajax to allweek access
			//console.log(JSON.stringify(accessRec));
			$.ajax({
				type: "POST",
				url: "process",
				data: "action=add_access_allweek&doorid=" + accessRec.doorId+"&personid=" + accessRec.personId + "&iside=" + accessRec.iSide + "&oside=" + accessRec.oSide + "&starttime=" + accessRec.startTime + "&endtime=" + accessRec.endTime + "&expiredate=" + accessRec.expireDate,
				success: function(resp){
					if(resp[0]=='1'){
						//populate access table
						parent.populateTable("access-table",accessRec.personId);
						//close modal
						parent.$("#modal-edit").modal("hide");
					} else {
						//show modal error
						alert(resp[1]);
					}
				},
				failure: function(){
					//show modal error
					alert("Operation failed, please try again");
				}
			});
		} else {
			//is liAccesses
			accessRec.allWeek=0;
			//for each day, get start, end and way
			var error=0;
			$("input[name=days]:checked").each(function(){
				if($(this).val()!=""){
					//get week day and parse as int
					accessRec.weekDay=parseInt($(this).val());
					// get start, end and way
// 					accessRec.startTime= $("input[name=from"+accessRec.weekDay+"]").val()+":00";
// 					accessRec.endTime = $("input[name=to"+accessRec.weekDay+"]").val()+":00";
 					accessRec.startTime= $("input[name=from"+accessRec.weekDay+"]").val();
 					accessRec.endTime = $("input[name=to"+accessRec.weekDay+"]").val();
					var way = $("input[name=way"+accessRec.weekDay+"]:checked").val();
					accessRec.iSide= (way%2);
					accessRec.oSide= Math.floor(way/2);
					//here post ajax to liaccess access
					//console.log(JSON.stringify(accessRec));
					$.ajax({
						type: "POST",
						url: "process",
						data: "action=add_access_liaccess&doorid=" + accessRec.doorId +"&personid=" + accessRec.personId + "&weekday=" + accessRec.weekDay + "&iside=" + accessRec.iSide + "&oside=" + accessRec.oSide + "&starttime=" + accessRec.startTime + "&endtime=" + accessRec.endTime + "&expiredate=" + accessRec.expireDate,
						success: function(resp){
							//console.log(resp);
						},
						failure: function(){
							error=1;
						}
					});
				}
			});
			if(!error){
				//populate access table
				parent.populateTable("access-table",accessRec.personId);
				//close modal
				parent.$("#modal-edit").modal("hide");
			} else {
				//show modal error
				alert("Error when trying to create access");
			}
		}
	} else {
		//edit
		// get allWeek
		var allWeek_check= $("#allWeek_check").prop("checked");
		if(allWeek_check){
			//is allWeek
			// get start, end and way
			//accessRec.startTime= $("input[name=from0]").val()+":00";
			//accessRec.endTime = $("input[name=to0]").val()+":00";
			accessRec.startTime= $("input[name=from0]").val();
			accessRec.endTime = $("input[name=to0]").val();
			var way = $("input[name=way0]:checked").val();
			accessRec.iSide= (way%2);
			accessRec.oSide= Math.floor(way/2);
			//here post ajax to allweek access
			//console.log(JSON.stringify(accessRec));
			$.ajax({
				type: "POST",
				url: "process",
				data: "action=edit_access_allweek&id=" + accessId + "&iside=" + accessRec.iSide + "&oside=" + accessRec.oSide + "&starttime=" + accessRec.startTime + "&endtime=" + accessRec.endTime + "&expiredate=" + accessRec.expireDate,
				success: function(resp){
					if(resp[0]=='1'){
						//populate access table
						parent.populateTable("access-table",values.personId);
						//close modal
						parent.$("#modal-edit").modal("hide");
					} else {
						//show modal error
						alert(resp[1]);
					}
				},
				failure: function(){
					//show modal error
					alert("Error when trying to create access");
				}
			});
		} else {
			//is liAccesses
			accessRec.doorId = parseInt($("#doors-select").val());
			accessRec.personId = personId;
			//for each day, get start, end and way. Send each liaccess as payload json to process
			var days_payload=[];
			$("input[name=days]:checked").each(function(){
				if($(this).val()!=""){
					//get week day and parse as int
					accessRec.weekDay=parseInt($(this).val());
					// get start, end and way
					//accessRec.startTime= $("input[name=from"+accessRec.weekDay+"]").val()+":00";
					//accessRec.endTime = $("input[name=to"+accessRec.weekDay+"]").val()+":00";
					accessRec.startTime= $("input[name=from"+accessRec.weekDay+"]").val();
					accessRec.endTime = $("input[name=to"+accessRec.weekDay+"]").val();
					var way = $("input[name=way"+accessRec.weekDay+"]:checked").val();
					accessRec.iSide= (way%2);
					accessRec.oSide= Math.floor(way/2);
					//add liaccess as json to payload array
					//console.log(JSON.stringify(accessRec));
					days_payload.push(JSON.stringify(accessRec));
				}
			});
			$.ajax({
				type: "POST",
				url: "process",
				data: "action=edit_access_liaccess&doorid=" + accessRec.doorId + "&personid=" + accessRec.personId + "&id=" + accessId + "&days_payload="+ days_payload.join("|") + "&expiredate=" + accessRec.expireDate,
				success: function(resp){
					console.log(resp);
					if(resp[0]=='1'){
						//populate access table
						parent.populateTable("access-table",personId);
						//close modal
						parent.$("#modal-edit").modal("hide");
					} else {
						//show modal error
						alert(resp[1]);
					}
				},
				failure: function(){
					//show modal error
					alert("Error when trying to create access");
				}
			});
		}
	}
	return false;
});
</script>

</body>
</html>