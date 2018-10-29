//returns true if str is a valid url (by Devshed)
function ValidURL(s) {
var regexp = /(ftp|http|https):\/\/(\w+:{0,1}\w*@)?(\S+)(:[0-9]+)?(\/|\/([\w#!:.?+=&%@!\-\/]))?/
return regexp.test(s);
}

function myTrim(x) {
    return x.replace(/^\s+|\s+$/gm,'');
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