<?php
	header('Content-Type: text/html; charset=utf-8');
	$conn = mysql_connect("localhost","root","toor");
	mysql_select_db("echaloasuerte", $conn);

	$idTirada = mysql_real_escape_string(isset($_GET['idTirada']) ? $_GET['idTirada'] : $_POST['idTirada']);
	$usuario = mysql_real_escape_string(isset($_GET['usuario']) ? $_GET['usuario'] : $_POST['usuario']);
	$mensaje = mysql_real_escape_string(isset($_GET['mensaje']) ? $_GET['mensaje'] : $_POST['mensaje']);

	mysql_query("INSERT INTO MENSAJE(contenido,usuario,tirada) VALUES('".$mensaje."',".$usuario.",".$idTirada.");");
  ?>
