<?php
	$idTirada = isset($_GET['idTirada']) ? $_GET['idTirada'] : $_POST['idTirada'];
	$usuario = isset($_GET['usuario']) ? $_GET['usuario'] : $_POST['usuario'];
	$mensaje = isset($_GET['mensaje']) ? $_GET['mensaje'] : $_POST['mensaje'];

	header('Content-Type: text/html; charset=utf-8');
	$conn = mysql_connect("db372506665.db.1and1.com","dbo372506665","1234abcd");
	mysql_select_db("db372506665", $conn);

	mysql_query("INSERT INTO MENSAJE(contenido,usuario,tirada) VALUES('".$mensaje."',".$usuario.",".$idTirada.");");
  ?>