<?php if(!isset($innerheader)){?>
</div>
<!-- /#wrapper -->
<?php }?>
<script src="dist/js/jquery.min.js"></script>
<?php if(in_array("jqueryui",$include_extra_js) or in_array("datepicker",$include_extra_js)){?>
<script src="dist/js/jquery-ui.js"></script>
<?php }?>
<script src="dist/js/bootstrap.min.js"></script>
<?php if($islogged){
if(!isset($innerheader)){?>
<!-- Metis Menu Plugin JavaScript -->
<script src="bower_components/metisMenu/dist/metisMenu.min.js"></script>
<!-- Custom Theme JavaScript -->
<script src="dist/js/sb-admin-2.js"></script>
<?php }?>
<?php if(in_array("graphics",$include_extra_js)){?>
<!-- graphics js -->
<script src="bower_components/raphael/raphael-min.js"></script>
<script src="bower_components/morrisjs/morris.min.js"></script>
<?php }?>
<?php if(in_array("clockpicker",$include_extra_js)){?>
<script src="dist/js/bootstrap-clockpicker.min.js"></script>
<?php }?>
<script src="lib/jslib.js?v=1"></script>
<script>
// tooltip init
$('body').tooltip({
selector: "[data-toggle=tooltip]",
container: "body"
})
<?php if((in_array("jqueryui",$include_extra_js) or in_array("datepicker",$include_extra_js)) and $lang!="en"){?>
$(function(){datepicker_localize("<?=$lang?>")});
<?php }?>
</script>
<?php
}
if(!isset($leavebodyopen)){
?>
</body>
</html>
<?php }?>
