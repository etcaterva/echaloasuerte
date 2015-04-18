<?php
	header('Content-Type: text/html; charset=utf-8');
	$conn = mysql_connect("localhost","root","toor");
	mysql_select_db("echaloasuerte", $conn);

	$usuario =  mysql_real_escape_string(isset($_GET['usuario']) ? $_GET['usuario'] : $_POST['usuario']);

	mysql_query("UPDATE USUARIO SET checked = 1 where id = ".$usuario);
  ?>
