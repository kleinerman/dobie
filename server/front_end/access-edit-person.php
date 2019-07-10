<?
$leavebodyopen=1;
$innerheader=1;
$requirerole=2;
$include_extra_js=array("clockpicker","datepicker");

//get access ID or create mode
$id = (isset($_GET["id"]) and is_numeric($_GET["id"])) ? $_GET["id"] : "0";
$personid = (isset($_GET["personid"]) and $_GET["personid"]!="") ? $_GET["personid"] : "0";
$orgid = (isset($_GET["orgid"]) and is_numeric($_GET["orgid"])) ? $_GET["orgid"] : "0";

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

<div>
<?=get_text("Create access to",$lang);?>:<br>
<div class="btn-group" data-toggle="buttons">
  <label class="btn btn-primary input-mode-label" data-value="zone">
    <input type="radio" class="input-mode-radio" name="input-mode" value="zone"> <?=get_text("Zone",$lang);?>
  </label>
  <label class="btn btn-primary input-mode-label" data-value="door-group">
    <input type="radio" class="input-mode-radio" name="input-mode" value="door-group"> <?=get_text("Door Group",$lang);?>
  </label>
</div>

<br><br>

<div id="input-mode-zone" style="display:none">
<div class="select-container">
<form action="javascript:void(0)">
<div class="select-container-title"><?=get_text("Zone",$lang);?></div>
<div class="select-container-body">
<input type="text" name="filter" placeholder="<?=get_text("Filter options",$lang);?>..." class="form-control data-filter" data-filter="zones-select">
<select id="zones-select" class="select-options select-options-small form-control" name="zones-select" size="2"></select>
</div>
<div class="select-container-footer">
&nbsp;
</div>
</form>
</div>

<div class="select-container" id="select-container-doors" style="display:none">
<form action="javascript:void(0)">
<div class="select-container-title"><?=get_text("Doors",$lang);?> <button id="doors-select-all" class="btn btn-primary btn-xs" type="button"><?=get_text("Select all",$lang);?></button></div>
<div class="select-container-body">
<input type="text" name="filter" placeholder="<?=get_text("Filter options",$lang);?>..." class="form-control data-filter" data-filter="doors-select">
<select id="doors-select" class="select-options select-options-small form-control" name="doors-select" size="2" onchange="updateButtons(this.id)" multiple></select>
</div>
<div class="select-container-footer"></div>
</form>
</div>
</div>

<div id="input-mode-door-group" style="display:none">
<div class="select-container">
<form action="javascript:void(0)">
<div class="select-container-title"><?=get_text("Door Groups",$lang);?></div>
<div class="select-container-body">
<input type="text" name="filter" placeholder="<?=get_text("Filter options",$lang);?>..." class="form-control data-filter" data-filter="door-groups-select">
<select id="door-groups-select" class="select-options select-options-small form-control" name="door-groups-select" size="2"></select>
</div>
<div class="select-container-footer">
<div class="legend left"><span class="vdg-row">&nbsp;&nbsp;&nbsp;&nbsp;</span> = <?=get_text("Visit Door Groups",$lang);?></div>
<br>
</div>
</form>
</div>

<div class="select-container" id="select-container-door-group-doors" style="display:none">
<form action="javascript:void(0)">
<div class="select-container-title"><?=get_text("Doors",$lang);?></div>
<div class="select-container-body">
<select id="door-group-doors-select" class="select-options select-options-small form-control" name="door-group-doors-select" size="2" disabled></select>
</div>
<div class="select-container-footer"></div>
</form>
</div>
</div>

</div>
</div>


<div class="col-lg-9 center" id="schedule-container" style="display:none">
<?} else {?>
<div class="col-lg-12 center">
<?}?>
<br>

<div class="row">

<div class="col-lg-12 center">
<div class="select-container-title"><?=get_text("Schedule",$lang);?></div>
<div class="schedule-container">
<form id="access-edit-form" action="#">
<table id="schedule-table" class="table-condensed table-responsive left">
<tr><th><?=get_text("Day",$lang);?></th><th><?=get_text("Time interval",$lang);?></th><th class="center"><?=get_text("Incoming",$lang);?></th><th class="center"><?=get_text("Outgoing",$lang);?></th><th class="center"><?=get_text("Both",$lang);?></th></tr>
<tr><td><label><input type="checkbox" id="allWeek_check" name="days" value="" checked> <?=get_text("Every day",$lang);?></label></td>
<td class="everyday_cell">
<div class="input-group clockpicker" data-placement="left" data-align="top" data-autoclose="true" title="<?=get_text("From",$lang);?>"><input type="text" class="form-control from-input" value="00:00" name="from0"><span class="input-group-addon"><span class="far fa-clock"></span></span></div>
<div class="input-group clockpicker" data-placement="left" data-align="top" data-autoclose="true" title="<?=get_text("Until",$lang);?>"><input type="text" class="form-control until-input" value="23:59" name="to0"><span class="input-group-addon"><span class="far fa-clock"></span></span></div>
</td><td class="center everyday_cell"><input type="radio" name="way0" value="1">
</td><td class="center everyday_cell"><input type="radio" name="way0" value="2">
</td><td class="center everyday_cell"><input type="radio" name="way0" value="3" checked>
</td>
</tr>

<tr class="dayrow"><td><label><input type="checkbox" name="days" value="1"> <?=get_text("Monday",$lang);?></label></td>
<td>
<div class="input-group clockpicker" data-placement="left" data-align="top" data-autoclose="true" title="<?=get_text("From",$lang);?>"><input type="text" class="form-control from-input" value="00:00" name="from1"><span class="input-group-addon"><span class="far fa-clock"></span></span></div>
<div class="input-group clockpicker" data-placement="left" data-align="top" data-autoclose="true" title="<?=get_text("Until",$lang);?>"><input type="text" class="form-control until-input" value="23:59" name="to1"><span class="input-group-addon"><span class="far fa-clock"></span></span></div>
</td><td class="center"><input type="radio" name="way1" value="1">
</td><td class="center"><input type="radio" name="way1" value="2">
</td><td class="center"><input type="radio" name="way1" value="3" checked>
</td>
</tr>

<tr class="dayrow"><td><label><input type="checkbox" name="days" value="2"> <?=get_text("Tuesday",$lang);?></label></td>
<td>
<div class="input-group clockpicker" data-placement="left" data-align="top" data-autoclose="true" title="<?=get_text("From",$lang);?>"><input type="text" class="form-control from-input" value="00:00" name="from2"><span class="input-group-addon"><span class="far fa-clock"></span></span></div>
<div class="input-group clockpicker" data-placement="left" data-align="top" data-autoclose="true" title="<?=get_text("Until",$lang);?>"><input type="text" class="form-control until-input" value="23:59" name="to2"><span class="input-group-addon"><span class="far fa-clock"></span></span></div>
</td><td class="center"><input type="radio" name="way2" value="1">
</td><td class="center"><input type="radio" name="way2" value="2">
</td><td class="center"><input type="radio" name="way2" value="3" checked>
</td>
</tr>

<tr class="dayrow"><td><label><input type="checkbox" name="days" value="3"> <?=get_text("Wednesday",$lang);?></label></td>
<td>
<div class="input-group clockpicker" data-placement="left" data-align="top" data-autoclose="true" title="<?=get_text("From",$lang);?>"><input type="text" class="form-control from-input" value="00:00" name="from3"><span class="input-group-addon"><span class="far fa-clock"></span></span></div>
<div class="input-group clockpicker" data-placement="left" data-align="top" data-autoclose="true" title="<?=get_text("Until",$lang);?>"><input type="text" class="form-control until-input" value="23:59" name="to3"><span class="input-group-addon"><span class="far fa-clock"></span></span></div>
</td><td class="center"><input type="radio" name="way3" value="1">
</td><td class="center"><input type="radio" name="way3" value="2">
</td><td class="center"><input type="radio" name="way3" value="3" checked>
</td>
</tr>

<tr class="dayrow"><td><label><input type="checkbox" name="days" value="4"> <?=get_text("Thursday",$lang);?></label></td>
<td>
<div class="input-group clockpicker" data-placement="left" data-align="top" data-autoclose="true" title="<?=get_text("From",$lang);?>"><input type="text" class="form-control from-input" value="00:00" name="from4"><span class="input-group-addon"><span class="far fa-clock"></span></span></div>
<div class="input-group clockpicker" data-placement="left" data-align="top" data-autoclose="true" title="<?=get_text("Until",$lang);?>"><input type="text" class="form-control until-input" value="23:59" name="to4"><span class="input-group-addon"><span class="far fa-clock"></span></span></div>
</td><td class="center"><input type="radio" name="way4" value="1">
</td><td class="center"><input type="radio" name="way4" value="2">
</td><td class="center"><input type="radio" name="way4" value="3" checked>
</td>
</tr>

<tr class="dayrow"><td><label><input type="checkbox" name="days" value="5"> <?=get_text("Friday",$lang);?></label></td>
<td>
<div class="input-group clockpicker" data-placement="left" data-align="top" data-autoclose="true" title="<?=get_text("From",$lang);?>"><input type="text" class="form-control from-input" value="00:00" name="from5"><span class="input-group-addon"><span class="far fa-clock"></span></span></div>
<div class="input-group clockpicker" data-placement="left" data-align="top" data-autoclose="true" title="<?=get_text("Until",$lang);?>"><input type="text" class="form-control until-input" value="23:59" name="to5"><span class="input-group-addon"><span class="far fa-clock"></span></span></div>
</td><td class="center"><input type="radio" name="way5" value="1">
</td><td class="center"><input type="radio" name="way5" value="2">
</td><td class="center"><input type="radio" name="way5" value="3" checked>
</td>
</tr>

<tr class="dayrow"><td><label><input type="checkbox" name="days" value="6"> <?=get_text("Saturday",$lang);?></label></td>
<td>
<div class="input-group clockpicker" data-placement="left" data-align="top" data-autoclose="true" title="<?=get_text("From",$lang);?>"><input type="text" class="form-control from-input" value="00:00" name="from6"><span class="input-group-addon"><span class="far fa-clock"></span></span></div>
<div class="input-group clockpicker" data-placement="left" data-align="top" data-autoclose="true" title="<?=get_text("Until",$lang);?>"><input type="text" class="form-control until-input" value="23:59" name="to6"><span class="input-group-addon"><span class="far fa-clock"></span></span></div>
</td><td class="center"><input type="radio" name="way6" value="1">
</td><td class="center"><input type="radio" name="way6" value="2">
</td><td class="center"><input type="radio" name="way6" value="3" checked>
</td>
</tr>

<tr class="dayrow"><td><label><input type="checkbox" name="days" value="7"> <?=get_text("Sunday",$lang);?></label></td>
<td>
<div class="input-group clockpicker" data-placement="left" data-align="top" data-autoclose="true" title="<?=get_text("From",$lang);?>"><input type="text" class="form-control from-input" value="00:00" name="from7"><span class="input-group-addon"><span class="far fa-clock"></span></span></div>
<div class="input-group clockpicker" data-placement="left" data-align="top" data-autoclose="true" title="<?=get_text("Until",$lang);?>"><input type="text" class="form-control until-input" value="23:59" name="to7"><span class="input-group-addon"><span class="far fa-clock"></span></span></div>
</td><td class="center"><input type="radio" name="way7" value="1">
</td><td class="center"><input type="radio" name="way7" value="2">
</td><td class="center"><input type="radio" name="way7" value="3" checked>
</td>
</tr>
</table>
<br>

<div class="left">
<?=get_text("Expiration Date",$lang);?>: <label><input type="radio" name="expiration" value="0" checked> <?=get_text("No",$lang);?></label> <label><input type="radio" name="expiration" value="1"> <?=get_text("Yes",$lang);?></label> &nbsp;&nbsp;<input type="text" class="form-control center" name="expiration_date" id="expiration_date" value="<?=date("Y-m-d",mktime(0,0,0)+(60*60*24*365))?>">
<br><br>
<button class="btn btn-success" id="form-submit-button" type="submit"><?=get_text("Save",$lang);?></button> <button id="form-spinner" class="btn btn-default" type="button" disabled style="display:none"><span class="fas fa-spinner fa-pulse"></span></button>
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

<script type="text/javascript">
//init filters
setFilterAction();
setFilterActionTable();

var zoneId;

//populate select list
populateList("zones-select","zones");
populateList("door-groups-select","door_groups");

//on click event for input mode toggle
$(".input-mode-label").click(function(){
	if($(this).data("value")=="zone"){
		$("#input-mode-zone").show();
		$("#input-mode-door-group").hide();
	} else {
		$("#input-mode-zone").hide();
		$("#input-mode-door-group").show();
	}
	//hide schedule
	$("#schedule-container").hide();
});

//select on change events for zones, doors and door groups
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
	//enable all doors
	doorAll=0;
	//show schedule
	$("#schedule-container").fadeIn();
});

$("#door-groups-select").change(function(){
	doorGroupId=$("#door-groups-select").val();
	if(!isNaN(doorGroupId) && doorGroupId!="undefined"){
		//populate list
		populateList("door-group-doors-select","door_group_doors",doorGroupId);
		//show list
		$("#select-container-door-group-doors").fadeIn();
		//show schedule
		$("#schedule-container").fadeIn();
	}
});

$("#doors-select-all").click(function(){
	//unselect values if existent
	//if($("#doors-select option:selected").length>0) $("#doors-select option:selected").prop("selected", false);
	//instead, select them all
	$("#doors-select option").prop("selected", true);
	//show schedule
	$("#schedule-container").fadeIn();
	//enable all doors
	doorAll=1;
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
$("#expiration_date").datepicker({dateFormat: "yy-mm-dd"});

//initial check all days
$("input[name=days]").prop("checked",true);

//hide days rows, only leave All Days visible
$(".dayrow").hide();

//fetch values if set
var accessId=<?=$id?>;
var personId='<?=$personid?>';
var orgId=<?=$orgid?>;
if(personId!="" && personId!="all" && (personId.indexOf(',')<0)) personId = parseInt(personId);
//init array for edit access values
var values;
var doorAll=0;

//populate form if edit or create
if(!accessId){
	//if create
	//populate header with person name
	if(!isNaN(personId)) $("#page-header").text("<?=get_text("New access for",$lang);?> " + parent.$("#persons-select option:selected").text());
	else $("#page-header").text("<?=get_text("New access for",$lang);?> " + parent.$("#organizations-select option:selected").text());
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
			$("#page-header").html("<?=get_text("Editing",$lang);?> "+ values.personName + " <span class=\"fa fa-arrow-right\"></span> " + values.doorName);
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
				$(".everyday_cell").hide();
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
			//fill expiration date
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
			alert("<?=get_text("Error fetching access data",$lang);?>");
		}
	},
	failure: function(){
			//show error
			alert("<?=get_text("Error fetching access data",$lang);?>");
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

	// check if create or edit
	if(!accessId){
		//create
		//if(doorAll)
		//check if door group input mode was used > send door group id and not door
		if($("input[name=input-mode]:checked").val()=="door-group"){
			accessRec.doorGroupId=$("#door-groups-select").val();
			accessRec.doorId="";
		} else {
			//send door group id empty and get door value
			accessRec.doorGroupId="";
			if($.isArray($("#doors-select").val())) accessRec.doorId = $("#doors-select").val().join(","); //accessRec.zoneId = parseInt($("#zones-select").val());
			else accessRec.doorId = parseInt($("#doors-select").val());
		}
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

			//check if add access to all persons
			//if(accessRec.personId=="all" || (personId.indexOf(',')>=0)){
			if(isNaN(accessRec.personId)){
				//all persons or specific persons
				//if all doors > add access to organization for a zone
				if(accessRec.doorId=="" || isNaN(accessRec.doorId)) var datastring = "action=add_access_allweek_organization_zone&zoneid=" + accessRec.zoneId+ "&orgid=" + orgId + "&iside=" + accessRec.iSide + "&oside=" + accessRec.oSide + "&starttime=" + accessRec.startTime + "&endtime=" + accessRec.endTime + "&expiredate=" + accessRec.expireDate + "&personid=" + accessRec.personId + "&doorid=" + accessRec.doorId + "&doorgroupid=" + accessRec.doorGroupId;
				//else > add access to organizations for a single door
				else var datastring = "action=add_access_allweek_organization&doorid=" + accessRec.doorId+ "&orgid=" + orgId + "&iside=" + accessRec.iSide + "&oside=" + accessRec.oSide + "&starttime=" + accessRec.startTime + "&endtime=" + accessRec.endTime + "&expiredate=" + accessRec.expireDate + "&personid=" + accessRec.personId;
			} else {
				//single person
				//if all doors > add access to a single person for a zone
				//if(doorAll) 
				if(accessRec.doorId=="" || isNaN(accessRec.doorId)) var datastring = "action=add_access_allweek_zone&zoneid=" + accessRec.zoneId+"&personid=" + accessRec.personId + "&iside=" + accessRec.iSide + "&oside=" + accessRec.oSide + "&starttime=" + accessRec.startTime + "&endtime=" + accessRec.endTime + "&expiredate=" + accessRec.expireDate + "&doorid=" + accessRec.doorId + "&doorgroupid=" + accessRec.doorGroupId;
				//else > add access to a single person for a single door
				else var datastring = "action=add_access_allweek&doorid=" + accessRec.doorId+"&personid=" + accessRec.personId + "&iside=" + accessRec.iSide + "&oside=" + accessRec.oSide + "&starttime=" + accessRec.startTime + "&endtime=" + accessRec.endTime + "&expiredate=" + accessRec.expireDate;
			}

			$.ajax({
				type: "POST",
				url: "process",
				data: datastring,
				beforeSend:function(){$("#form-submit-button").hide();$("#form-spinner").show()},
				complete:function(){$("#form-submit-button").show();$("#form-spinner").hide()},
				success: function(resp){
					if(resp[0]=='1'){
						//populate access table
						//if all, hide accesses table
						//if(accessRec.personId=="all" || (personId.indexOf(',')>=0)){
						if(isNaN(accessRec.personId)){
							parent.$("#accesses-table-container").hide();
							//unselect person if any
							parent.$("#persons-select option:selected").prop("selected", false);
							//hide buttons
							parent.$("#buttons-row").hide();
						} else parent.populateTable("access-table",accessRec.personId);
						//close modal
						parent.$("#modal-edit").modal("hide");
					} else {
						//show modal error
						alert(resp[1]);
					}
				},
				failure: function(){
					//show modal error
					alert("<?=get_text("Operation failed, please try again",$lang);?>");
				}
			});
		} else {
			//is liAccesses
			accessRec.allWeek=0;
			//for each day, get start, end and way
			var error=0;
			
			if($("input[name=days]:checked").length<1){
				error="<?=get_text("You must select at least 1 day of the week or check 'Every day'",$lang);?>";
			} else {
				$("input[name=days]:checked").each(function(){
					if($(this).val()!=""){
						//get week day and parse as int
						accessRec.weekDay=parseInt($(this).val());
						// get start, end and way
						accessRec.startTime= $("input[name=from"+accessRec.weekDay+"]").val();
						accessRec.endTime = $("input[name=to"+accessRec.weekDay+"]").val();
						var way = $("input[name=way"+accessRec.weekDay+"]:checked").val();
						accessRec.iSide= (way%2);
						accessRec.oSide= Math.floor(way/2);

						//check if add access to all persons
						//if(accessRec.personId=="all" || (personId.indexOf(',')>=0)){
						if(isNaN(accessRec.personId)){
							//all persons
							//if all doors > add liaccess to organization for a zone
							//if(doorAll) 
							if(accessRec.doorId=="" || isNaN(accessRec.doorId)) var datastring = "action=add_access_liaccess_organization_zone&zoneid=" + accessRec.zoneId +"&orgid=" + orgId + "&weekday=" + accessRec.weekDay + "&iside=" + accessRec.iSide + "&oside=" + accessRec.oSide + "&starttime=" + accessRec.startTime + "&endtime=" + accessRec.endTime + "&expiredate=" + accessRec.expireDate + "&personid=" + accessRec.personId + "&doorid=" + accessRec.doorId + "&doorgroupid=" + accessRec.doorGroupId;
							//else > add liaccess to organizations for a single door
							else var datastring = "action=add_access_liaccess_organization&doorid=" + accessRec.doorId +"&orgid=" + orgId + "&weekday=" + accessRec.weekDay + "&iside=" + accessRec.iSide + "&oside=" + accessRec.oSide + "&starttime=" + accessRec.startTime + "&endtime=" + accessRec.endTime + "&expiredate=" + accessRec.expireDate + "&personid=" + accessRec.personId;
						} else {
							//single person
							//if all doors > add liaccess to a single person for a zone
							//if(doorAll) 
							if(accessRec.doorId=="" || isNaN(accessRec.doorId)) var datastring = "action=add_access_liaccess_zone&zoneid=" + accessRec.zoneId +"&personid=" + accessRec.personId + "&weekday=" + accessRec.weekDay + "&iside=" + accessRec.iSide + "&oside=" + accessRec.oSide + "&starttime=" + accessRec.startTime + "&endtime=" + accessRec.endTime + "&expiredate=" + accessRec.expireDate + "&doorid=" + accessRec.doorId + "&doorgroupid=" + accessRec.doorGroupId;
							//else > add liaccess to a single person for a single door
							else var datastring = "action=add_access_liaccess&doorid=" + accessRec.doorId +"&personid=" + accessRec.personId + "&weekday=" + accessRec.weekDay + "&iside=" + accessRec.iSide + "&oside=" + accessRec.oSide + "&starttime=" + accessRec.startTime + "&endtime=" + accessRec.endTime + "&expiredate=" + accessRec.expireDate;
						}
						$.ajax({
							type: "POST",
							url: "process",
							data: datastring,
							beforeSend:function(){$("#form-submit-button").hide();$("#form-spinner").show()},
							complete:function(){$("#form-submit-button").show();$("#form-spinner").hide()},
							success: function(resp){
								//console.log(resp);
							},
							failure: function(){
								error="<?=get_text("Error when trying to create access",$lang);?>";
							}
						});
					}
				});
			}
			if(!error){
				//populate access table
				//if all, hide accesses table
				//if(accessRec.personId=="all") {
				if(isNaN(accessRec.personId)){
					parent.$("#accesses-table-container").hide();
					//unselect person if any
					parent.$("#persons-select option:selected").prop("selected", false);
					//hide buttons
					parent.$("#buttons-row").hide();
				} else parent.populateTable("access-table",accessRec.personId);
				//close modal
				parent.$("#modal-edit").modal("hide");
			} else {
				//show modal error
				alert(error);
			}
		}
	} else {
		//edit
		// get allWeek
		var allWeek_check= $("#allWeek_check").prop("checked");
		if(allWeek_check){
			//is allWeek
			// get start, end and way
			accessRec.startTime= $("input[name=from0]").val();
			accessRec.endTime = $("input[name=to0]").val();
			var way = $("input[name=way0]:checked").val();
			accessRec.iSide= (way%2);
			accessRec.oSide= Math.floor(way/2);
			//check if its changing access type from liaccess to allweek
			if(!values.allWeek) var datastring = "action=add_access_allweek&doorid=" + values.doorId+"&personid=" + values.personId + "&iside=" + accessRec.iSide + "&oside=" + accessRec.oSide + "&starttime=" + accessRec.startTime + "&endtime=" + accessRec.endTime + "&expiredate=" + accessRec.expireDate;
			else var datastring = "action=edit_access_allweek&id=" + accessId + "&iside=" + accessRec.iSide + "&oside=" + accessRec.oSide + "&starttime=" + accessRec.startTime + "&endtime=" + accessRec.endTime + "&expiredate=" + accessRec.expireDate;
			//console.log(datastring);

			$.ajax({
				type: "POST",
				url: "process",
				data: datastring,
				beforeSend:function(){$("#form-submit-button").hide();$("#form-spinner").show()},
				complete:function(){$("#form-submit-button").show();$("#form-spinner").hide()},
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
					alert("<?=get_text("Error when trying to create access",$lang);?>");
				}
			});
		} else {
			//is liAccesses
			accessRec.doorId = values.doorId;
			accessRec.personId = values.personId;
			//for each day, get start, end and way. Send each liaccess as payload json to process
			var days_payload=[];

			if($("input[name=days]:checked").length<1){
				alert("<?=get_text("You must select at least 1 day of the week or check 'Every day'",$lang);?>");
			} else {
				$("input[name=days]:checked").each(function(){
					if($(this).val()!=""){
						//get week day and parse as int
						accessRec.weekDay=parseInt($(this).val());
						// get start, end and way
						accessRec.startTime= $("input[name=from"+accessRec.weekDay+"]").val();
						accessRec.endTime = $("input[name=to"+accessRec.weekDay+"]").val();
						var way = $("input[name=way"+accessRec.weekDay+"]:checked").val();
						accessRec.iSide= (way%2);
						accessRec.oSide= Math.floor(way/2);
						//add liaccess as json to payload array
						days_payload.push(JSON.stringify(accessRec));
					}
				});

				$.ajax({
					type: "POST",
					url: "process",
					data: "action=edit_access_liaccess&doorid=" + accessRec.doorId + "&personid=" + accessRec.personId + "&id=" + accessId + "&days_payload="+ days_payload.join("|") + "&expiredate=" + accessRec.expireDate,
					beforeSend:function(){$("#form-submit-button").hide();$("#form-spinner").show()},
					complete:function(){$("#form-submit-button").show();$("#form-spinner").hide();/*console.log(resp)*/},
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
						alert("<?=get_text("Error when trying to edit access",$lang);?>");
					},
					error: function(){alert("<?=get_text("Error when trying to edit access",$lang);?>")}
				});
			}
		}
	}
	return false;
});
</script>

</body>
</html>