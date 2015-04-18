<?php
	$idTirada = isset($_GET['idTirada']) ? $_GET['idTirada'] : $_POST['idTirada'];
	$pass = isset($_GET['password']) ? $_GET['password'] : $_POST['password'];

	header('Content-Type: text/html; charset=utf-8');
    $conn = mysql_connect("localhost","root","toor");
    mysql_select_db("echaloasuerte", $conn);

	$result = mysql_query("SELECT * FROM TIRADA WHERE id=".$idTirada);



	$row = mysql_fetch_array($result);
	if($row['password'] != '' && $row['password'] != $pass) exit("pass incorrecta");

	$jsonTirada = array("id" => $row['id'], "nombre" => $row['nombre'], "password" => $row['password'], "participantes" => $row['participantes']);

	$result = mysql_query("SELECT * FROM USUARIO WHERE tirada=".$idTirada);
	$jsonUsuarios = array();
	while($row = mysql_fetch_array($result))
	{
		$jsonUsuarios[$row['id']] = array("id" => $row['id'], "name" => $row['name'], "checked" => $row['checked']);
	}

	$result = mysql_query("SELECT * FROM MENSAJE WHERE tirada=".$idTirada);
	$jsonMensajes = array();
	while($row = mysql_fetch_array($result))
	{
		$jsonMensajes[$row['id']] = array("id" => $row['id'], "contenido" => $row['contenido'], "fecha" => $row['fecha'], "usuario" => $row['usuario'], "tirada" => $row['tirada']);
	}

	$result = mysql_query("SELECT * FROM ALEATORIO WHERE ID=".$idTirada);
	if(mysql_num_rows($result) != 0)
	{//Tirada aleatoria
		$row = mysql_fetch_array($result);
		$jsonTipoTirada = array("tipo" => "aleatorio", "id" => $row['id'], "num" => $row['num'], "desde" => $row['desde'], "hasta" => $row['hasta'], "repetir" => $row['repetir']);
	}else{
		$result = mysql_query("SELECT * FROM ELECCION WHERE ID=".$idTirada);
		if(mysql_num_rows($result) != 0)
		{//Tirada eleccion
			$row = mysql_fetch_array($result);
			$jsonTipoTirada = array("tipo" => "eleccion", "id" => $row['id'], "num" => $row['num'], "repetir" => $row['repetir']);
			$result = mysql_query("SELECT * FROM OPCION WHERE eleccion=".$idTirada);
			$aux = array();
			while($row = mysql_fetch_array($result))
			{
				$aux[$row['id']] = array("id" => $row['id'], "contenido" => $row['contenido']);
			}
			$jsonTipoTirada["values"] =$aux;
		}else{
			$result = mysql_query("SELECT * FROM ASOCIACION WHERE id=".$idTirada);
			if(mysql_num_rows($result) != 0)
			{//Tirada asociacion
				$row = mysql_fetch_array($result);
				$jsonTipoTirada = array("tipo" => "asociacion", "id" => $row['id'], "repetir" => $row['repetir']);
				$result = mysql_query("SELECT * FROM OPCION WHERE asociacion_desde=".$idTirada);
				$aux = array();
				while($row = mysql_fetch_array($result))
				{
					$aux[$row['id']] = array("id" => $row['id'], "contenido" => $row['contenido']);
				}
				$jsonTipoTirada["valuesA"]=$aux;
				$result = mysql_query("SELECT * FROM OPCION WHERE asociacion_hasta=".$idTirada);
				$aux = array();
				while($row = mysql_fetch_array($result))
				{
					$aux[$row['id']] = array("id" => $row['id'], "contenido" => $row['contenido']);
				}
				$jsonTipoTirada["valuesB"]=$aux;
			}
		}
	}

	//soluciones
	$result = mysql_query("SELECT * FROM ITEM_SOLUCION WHERE tirada=".$idTirada);
	$jsonSolucion = array();
	while($row = mysql_fetch_array($result))
	{
		$jsonSolucion[$row['id']] = $row["contenido"];
	}

	$jsonFinal= array("tirada" => $jsonTirada,"tipo" => $jsonTipoTirada,  "usuarios" => $jsonUsuarios, "chat" => $jsonMensajes, "solucion" => $jsonSolucion);
	echo json_encode($jsonFinal);
  ?>
