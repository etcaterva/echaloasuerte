<?php
	$idTirada = isset($_GET['idTirada']) ? $_GET['idTirada'] : $_POST['idTirada'];
	$usuario = isset($_GET['usuario']) ? $_GET['usuario'] : $_POST['usuario'];
	$mensaje = isset($_GET['mensaje']) ? $_GET['mensaje'] : $_POST['mensaje'];

	header('Content-Type: text/html; charset=utf-8');
    $conn = mysql_connect("localhost","root","toor");
    mysql_select_db("echaloasuerte", $conn);

	mysql_query("INSERT INTO MENSAJE(contenido,usuario,tirada) VALUES('".$mensaje."',".$usuario.",".$idTirada.");");
  ?>
