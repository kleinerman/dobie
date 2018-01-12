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
function populateList(selectId,entity,id=0){

	if(id!=0) var extraActionStr="&id="+id;
	else var extraActionStr="";

	$.ajax({
	type: "POST",
	url: "process",
	data: "action=get_"+entity + extraActionStr,
	success: function(resp){
		$("#"+selectId).empty();
		if(resp[0]=='1'){
			var values = resp[1];
			var itemClass="";
			values.forEach(function(item,index){
				if(item.resStateId!=5){
					itemClass="";
					if(item.resStateId==1) itemClass=" class='toadd' disabled ";
					else if(item.resStateId==2) itemClass=" class='toupd' disabled ";
					else if(item.resStateId==4) itemClass=" class='todel' disabled ";
					$("#"+selectId).append("<option value='"+item.id+"'"+itemClass+">"+ item.name +"</option>");
				}
			});
		} else {
			//show error option
			$("#"+selectId).append("<option value=''>"+ resp[1] +"</option>");
		}
	},
	failure: function(){
			//show error option
			$("#"+selectId).append("<option value=''>Operation failed, please try again</option>");
		}
	});
}
