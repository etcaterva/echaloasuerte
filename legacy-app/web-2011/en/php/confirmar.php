<?php
	$usuario = isset($_GET['usuario']) ? $_GET['usuario'] : $_POST['usuario'];

	header('Content-Type: text/html; charset=utf-8');
	$conn = mysql_connect("db372506665.db.1and1.com","dbo372506665","1234abcd");
	mysql_select_db("db372506665", $conn);

	mysql_query("UPDATE USUARIO SET checked = 1 where id = ".$usuario);
  ?>