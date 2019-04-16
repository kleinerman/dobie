//returns true if str is a valid url (by Devshed)
function ValidURL(s) {
var regexp = /(ftp|http|https):\/\/(\w+:{0,1}\w*@)?(\S+)(:[0-9]+)?(\/|\/([\w#!:.?+=&%@!\-\/]))?/
return regexp.test(s);
}

function myTrim(x) {
    return x.replace(/^\s+|\s+$/gm,'');
}

function truncate_str(str, length=15, ending="..."){
	if(str.length > length) return str.substring(0, length - ending.length) + ending;
	else return str;
}

function custom_dump(arr,level) {
	var dumped_text = "";
	if(!level) level = 0;
	
	//The padding given at the beginning of the line.
	var level_padding = "";
	for(var j=0;j<level+1;j++) level_padding += "    ";
	
	if(typeof(arr) == 'object') { //Array/Hashes/Objects 
		for(var item in arr) {
			var value = arr[item];
			
			if(typeof(value) == 'object') { //If it is an array,
				dumped_text += level_padding + "'" + item + "' ...\n";
				dumped_text += dump(value,level+1);
			} else {
				dumped_text += level_padding + "'" + item + "' => \"" + value + "\"\n";
			}
		}
	} else { //Stings/Chars/Numbers etc.
		dumped_text = "===>"+arr+"<===("+typeof(arr)+")";
	}
	return dumped_text;
}

/*dobie funcs*/

//set filtering action to filter on select options
function setFilterAction(){
	$(".data-filter").keyup(function(){
		var options=$("#"+$(this).data("filter") + " option");
		var filterValue=$(this).val().toLowerCase();
		options.each(function(){
			if($(this).text().toLowerCase().includes(filterValue)) $(this).show();
			else $(this).hide();
		})
	});
}

//toggle disabled on buttons
function updateButtons(objId){
	if($("#"+objId).val()!="undefined" && $("#"+objId).val()!="") $("#"+objId+"-edit, #"+objId+"-del, #"+objId+"-pick").prop("disabled",0);
	else $("#"+objId+"-edit, #"+objId+"-del, #"+objId+"-pick").prop("disabled",1);
}

//populateSelect
function populateList(selectId,entity,id=0,actionstr="",hlvalue="",newcontroller=0,orgsGetVisitors=0){

	if(actionstr!=""){
		var completeActionStr=actionstr;
	} else {
		if(id!=0) var extraActionStr="&id="+id;
		else var extraActionStr="";
		completeActionStr = "action=get_"+entity + extraActionStr;
	}

	$.ajax({
		type: "POST",
		url: "process",
		data: completeActionStr,
		success: function(resp){
			$("#"+selectId).empty();
			var qValidItems=0;
			if(resp[0]=='1'){
				var values = resp[1];
				var itemClass="";
				values.forEach(function(item,index){
					//for organizations, dont show item.id==1 Visitors unless specified
					if(entity!="organizations" || orgsGetVisitors || item.id!=1){
						if(item.resStateId!=5){
							itemClass="";
							if(item.resStateId==1) itemClass=" class='toadd' disabled ";
							else if(item.resStateId==2) itemClass=" class='toupd' disabled ";
							else if(item.resStateId==4) itemClass=" class='todel' disabled ";
							if(hlvalue!="" && item.id==hlvalue) itemClass +=" selected";
							//check for disabling controllers without available doors
							if(newcontroller && item.availDoors.length==0) itemClass +=" disabled";
							//join person names if present
							if(typeof item.names!=="undefined" && typeof item.lastName!=="undefined") item.name = item.names + " " + item.lastName;
							//show note if visitor and note exists
							if(entity=="visitors" && item.note!="") item.name += " ("+truncate_str(item.note,8)+")";
							//show
							$("#"+selectId).append("<option value='"+item.id+"'"+itemClass+">"+ item.name +"</option>");
							qValidItems++;
						}
					}
				});
			} else {
				//show error option
				$("#"+selectId).append("<option value='' disabled>"+ resp[1] +"</option>");
			}
			//toggle visibility of -all button if exists
			if($("#"+selectId+"-all").length>0){
					//if more than one valid option > show
				if(qValidItems>1) $("#"+selectId+"-all").show();
				else $("#"+selectId+"-all").hide();
			}
		},
		failure: function(){
				//show error option
				$("#"+selectId).append("<option value=''>Operation failed, please try again</option>");
		}
	});
}


//events for access table rows
function tableClickEvents(){
	//clickable rows for access tables
	$("#access-table tr td:nth-child(n+2)").click(function(){
		$(this).parent().find("input[type=checkbox]").click();
	})

	//unclick All checkbox on row click
	$("#access-table tr td input[type=checkbox]").click(function(){
		if($("#accessesAll").prop("checked")) $("#accessesAll").prop("checked",false);
	})

	//click All event
	$("#accessesAll").click(function(){
		if($(this).prop("checked")) {
			$("#access-table td input[type=checkbox]").prop("checked",true);
			$("#access-del").prop("disabled",false);
			if($('#access-table tr td input[type=checkbox]:checked').length == 1) $("#access-edit").prop("disabled",false);
		} else {
			$("#access-table td input[type=checkbox]").prop("checked",false);
			//no rows selected > disable both
			$("#access-edit,#access-del").prop("disabled",true);
		}
	})
	
	//edit / delete  button toggle
	$('#access-table tr td input:checkbox').change(function(){
		if($('#access-table tr td input[type=checkbox]:checked').length > 0) {
			//if at least 1 row selected > enable delete
			$("#access-del").prop("disabled",false);
			//enable edit only if 1 row is selected
			if($('#access-table tr td input[type=checkbox]:checked').length > 1) $("#access-edit").prop("disabled",true);
			else $("#access-edit").prop("disabled",false);
		} else {
			//no rows selected > disable both
			$("#access-edit,#access-del").prop("disabled",true);
		}
	});
}

//event for access table row filter and checkboxes actions
function setFilterActionTable(){
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
	
	//checkbox click events
	$("input[name=days]").click(function(){
		if($(this).val()==""){
			//if All button
			if($(this).prop("checked")){
				//check all days
				$("input[name=days]").prop("checked",true);
				$(".dayrow").hide();
				$(".everyday_cell").show();
			} else {
				//uncheck all days
				$("input[name=days]").prop("checked",false);
				$(".dayrow").show();
				$(".everyday_cell").hide();
			}
		} else {
			//rest of buttons
			$("input[name=days]:first").prop("checked",false);
		}
	});
}

//adds zero padding to hour string
function addZeroPadding(str){
	str_parts=str.split(":");
	if(str_parts.length>1 && str_parts[0].length==1) str_parts[0]="0"+str_parts[0];
	if(str_parts.length>1 && str_parts[1].length==1) str_parts[1]="0"+str_parts[1];
	return str_parts.join(":");
}

//adds zero padding to single number
function addZeroPaddingSingle(number){
	var result=number;
	if(number<10 && number>-1) result="0"+number;
	return result;
}

//localize datepicker
function datepicker_localize(lang){
	if($.datepicker){
		if(lang=="es"){
			$.datepicker.regional['es'] = {
			closeText: 'Cerrar',
			prevText: '<Ant',
			nextText: 'Sig>',
			currentText: 'Hoy',
			monthNames: ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'],
			monthNamesShort: ['Ene','Feb','Mar','Abr', 'May','Jun','Jul','Ago','Sep', 'Oct','Nov','Dic'],
			dayNames: ['Domingo', 'Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado'],
			dayNamesShort: ['Dom','Lun','Mar','Mié','Juv','Vie','Sáb'],
			dayNamesMin: ['Do','Lu','Ma','Mi','Ju','Vi','Sá'],
			weekHeader: 'Sm',
			dateFormat: 'dd/mm/yy',
			firstDay: 1,
			isRTL: false,
			showMonthAfterYear: false,
			yearSuffix: ''
			};
			$.datepicker.setDefaults($.datepicker.regional['es']);
		}
	}
}

//Used in events
//outputs html for the fa icon for all events
function get_icon(id,mode){
	if(id===null) return "";
	else {
		var iconstr="";
		switch(mode){
			case "type":
				if(id==1) iconstr="fa fa-address-card";
				else if(id==2) iconstr="fa fa-circle";
				else if(id==3) iconstr="fa fa-unlink";
				else if(id==4) iconstr="fa fa-bolt";
			break;
			case "doorlock":
				if(id==1) iconstr="fa fa-rss";
				else if(id==2) iconstr="fa fa-thumbs-up";
				else if(id==3) iconstr="fa fa-circle";
			break;
			case "denialcause":
				if(id==1) iconstr="fa fa-ban";
				else if(id==2) iconstr="far fa-calendar-times";
				else if(id==3) iconstr="far fa-clock";
			break;
			case "side":
				if(id==0) iconstr="fa fa-sign-out-alt";
				else if(id==1) iconstr="fa fa-sign-in-alt";
			break;
			case "allowed":
				if(id==0) iconstr="fa fa-times";
				else if(id==1) iconstr="fa fa-check";
			break;
			default: break;
		}
		if(iconstr!="") return "<span class='"+ iconstr +"'></span>";
		else return "";
	}
}

//display string of mac from format aaaaaaaa to AA:AA:AA:AA
function buildMacFromString(macstring){
	return macstring.replace(/(.{2})/g, "$1:").slice(0,-1).toUpperCase();
}

//funcs for live FC / Raw card number conversion
function bin2dec(bin){
  return parseInt(bin, 2).toString(10);
}

function dec2bin(dec){
  return (dec >>> 0).toString(2);
}

function zerofill_left(number, length){
    var my_string = '' + number;
    while (my_string.length < length){
        my_string = '0' + my_string;
    }
    return my_string;
}

function rawToFC(inputv){
 var tempv=zerofill_left(dec2bin(inputv),24)
 return bin2dec(tempv.substring(0,8)) + ", " +
 bin2dec(tempv.substring(8))
}

function FCToRaw(inputv){
 var inputParts = inputv.split(",");
 var ret = "";
 if(inputParts.length==2){
  ret=bin2dec(zerofill_left(dec2bin(inputParts[0]),8) + zerofill_left(dec2bin(inputParts[1]),16));
 }
 return ret;
}

//events to live update card number fields
//idprefix examples: person-edit and person-new
function addCardnumEvents(idprefix){

	//on cardnum raw change, calculate FC and split into 2 fields
	$("#"+idprefix+"-cardnum").on('input', function(){
		var numparts = rawToFC($(this).val()).split(",");
		if(numparts.length==2){
			$("#"+idprefix+"-cardnum-fc-1").val(numparts[0]);
			$("#"+idprefix+"-cardnum-fc-2").val(numparts[1]);
		} else {
			$("#"+idprefix+"-cardnum-fc-1").val("");
			$("#"+idprefix+"-cardnum-fc-2").val("");
		}
	});

	//on input on any FC field, calculate Raw and join into a single field
	$("#"+idprefix+"-cardnum-fc-1, #"+idprefix+"-cardnum-fc-2").on('input', function(){
		$("#"+idprefix+"-cardnum").val(FCToRaw($("#"+idprefix+"-cardnum-fc-1").val() + ", " + $("#"+idprefix+"-cardnum-fc-2").val()));
	});

	//jump to fc2 on length=3 nums fc1
	$("#"+idprefix+"-cardnum-fc-1").on('input', function(){
		if($(this).val().length>2) $("#"+idprefix+"-cardnum-fc-2").focus();
	});
	//jump to fc1 on length=0 nums fc2
	$("#"+idprefix+"-cardnum-fc-2").on('input', function(){
		if($(this).val().length==0) $("#"+idprefix+"-cardnum-fc-1").focus();
	});

}
