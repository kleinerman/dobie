<?
$leavebodyopen=1;
include("header.php");
?>
<div id="page-wrapper">

<div class="row">
<div class="col-lg-12">
<h1 class="page-header"><?=get_text("Events Live",$lang);?></h1>
</div>
</div>

<div class="row">
<div class="col-lg-12">

<div id="events-container"></div>

</div>
</div>

</div>
<? include("footer.php");?>

<script type="text/javascript">
$.getScript(window.location.protocol + "//" + window.location.hostname+":<?=$nodejs_port?>/socket.io/socket.io.js", function() {
	if(typeof io !== 'undefined'){
		var socketio = io.connect(window.location.hostname+":<?=$nodejs_port?>");
		socketio.on("message_to_client", function(data) {
			$("#events-container").append(data + "<br>");
		});
	}
});
</script>

</body>
</html>