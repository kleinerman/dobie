<?if(!isset($innerheader)){?>
</div>
<!-- /#wrapper -->
<?}?>
<script type="text/javascript" src="dist/js/jquery.min.js"></script>
<?if(in_array("jqueryui",$include_extra_js) or in_array("datepicker",$include_extra_js)){?>
<script type="text/javascript" src="dist/js/jquery-ui.js"></script>
<?}?>
<script type="text/javascript" src="dist/js/bootstrap.min.js"></script>
<?if($islogged){
if(!isset($innerheader)){?>
<!-- Metis Menu Plugin JavaScript -->
<script type="text/javascript" src="bower_components/metisMenu/dist/metisMenu.min.js"></script>
<!-- Custom Theme JavaScript -->
<script type="text/javascript" src="dist/js/sb-admin-2.js"></script>
<?}?>
<?if(in_array("graphics",$include_extra_js)){?>
<!-- graphics js -->
<script type="text/javascript" src="bower_components/raphael/raphael-min.js"></script>
<script type="text/javascript" src="bower_components/morrisjs/morris.min.js"></script>
<?}?>
<?if(in_array("clockpicker",$include_extra_js)){?>
<script type="text/javascript" src="dist/js/bootstrap-clockpicker.min.js"></script>
<?}?>
<script type="text/javascript" src="lib/jslib.js"></script>
<script type="text/javascript">
// tooltip init
$('body').tooltip({
selector: "[data-toggle=tooltip]",
container: "body"
})
</script>
<?
}
if(!isset($leavebodyopen)){
?>
</body>
</html>
<?}?>