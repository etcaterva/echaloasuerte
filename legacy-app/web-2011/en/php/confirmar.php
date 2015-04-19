<?php
	$usuario = isset($_GET['usuario']) ? $_GET['usuario'] : $_POST['usuario'];

	header('Content-Type: text/html; charset=utf-8');
    $conn = mysql_connect("localhost","root","toor");
    mysql_select_db("echaloasuerte", $conn);

	mysql_query("UPDATE USUARIO SET checked = 1 where id = ".$usuario);
  ?>
