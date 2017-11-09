<?
function imvustylez_connect_db(){

	$dbhost='localhost';
	$dbusername='imvustyl';
	$dbuserpass='booboo221';
	$dbname='imvustyl_imvustylez_product_db';
	$dbcnx = mysqli_connect($dbhost, $dbusername, $dbuserpass,$dbname) or die('We are having a short downtime, gonna be back soon!');
	return $dbcnx;
}
?>