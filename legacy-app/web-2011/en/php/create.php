<?php

	header('Content-Type: text/html; charset=utf-8');

	$numParticipantes=isset($_GET['numParticipantes']) ? $_GET['numParticipantes'] : $_POST['numParticipantes'];
	$nombreUsuario=isset($_GET['nombreUsuario']) ? $_GET['nombreUsuario'] : $_POST['nombreUsuario'];
	$nombre=isset($_GET['nombre']) ? $_GET['nombre'] : $_POST['nombre'];
	$contrasenia=isset($_GET['contrasenia']) ? $_GET['contrasenia'] : $_POST['contrasenia'];
	$correo=isset($_GET['correo']) ? $_GET['correo'] : $_POST['correo'];
	$type=isset($_GET['type']) ? $_GET['type'] : $_POST['type'];
	$solutionItem=isset($_GET['solutionItem']) ? $_GET['solutionItem'] : $_POST['solutionItem'];
	switch($type)
	{
		case "aleatorio": $num=isset($_GET['AleatorioNum']) ? $_GET['AleatorioNum'] : $_POST['AleatorioNum'];
						  $from=isset($_GET['AleatorioFrom']) ? $_GET['AleatorioFrom'] : $_POST['AleatorioFrom'];
						  $to=isset($_GET['AleatorioTo']) ? $_GET['AleatorioTo'] : $_POST['AleatorioTo'];
						  $repe=isset($_GET['AleatorioRepe']) || isset($_POST['AleatorioRepe']);
						  if(empty($repe))
							$repe=0;
						  else
						    $repe=1;
						break;
		case "eleccion":  $num=isset($_GET['EleccionNum']) ? $_GET['EleccionNum'] : $_POST['EleccionNum'];
						  $values=isset($_GET['EleccionValues']) ? $_GET['EleccionValues'] : $_POST['EleccionValues'];
						  $repe=isset($_GET['EleccionRepe']) || isset($_POST['EleccionRepe']);
						  if(empty($repe))
							$repe=0;
						  else
						    $repe=1;
						break;
		case "asociacion":$valuesA=isset($_GET['SeleccionValues1']) ? $_GET['SeleccionValues1'] : $_POST['SeleccionValues1'];
						  $valuesB=isset($_GET['SeleccionValues2']) ? $_GET['SeleccionValues2'] : $_POST['SeleccionValues2'];
						  $repe=isset($_GET['AsociacionRepe']) || isset($_POST['AsociacionRepe']);
						  if(empty($repe))
							$repe=0;
						  else
						    $repe=1;
						break;
	}
    $conn = mysql_connect("localhost","root","toor");
    mysql_select_db("echaloasuerte", $conn);
	if (!$conn)
	{
		die('Error on the database: ' . mysql_error());
	}
	//creamos la tirada
	$query = "INSERT INTO TIRADA (password, participantes, nombre) VALUES ('".$contrasenia."',".$numParticipantes.",'".$nombre."')";
	mysql_query($query);
	$tiradaID = mysql_insert_id();//id de la tirada
	//Creamos usuario
	$query = "INSERT INTO USUARIO (name, tirada) VALUES ('".$nombreUsuario."',".$tiradaID.")";
	mysql_query($query);
	$usuarioID = mysql_insert_id();//id de usuario

	//creamos los item solucion
	for($i = 0;$i < count($solutionItem);$i++)
	{
		$query = "INSERT INTO ITEM_SOLUCION (contenido, tirada) VALUES ('".$solutionItem[$i]."',".$tiradaID.")";
		mysql_query($query);
	}

	//creamos la tirada especificamente
	switch($type)
	{
		case "aleatorio":
			$query = 	"INSERT INTO ALEATORIO (id, num, desde, hasta, repetir) VALUES (".$tiradaID.",".$num.",".$from.",".$to.",".$repe.");";
			mysql_query($query);
			break;
		case "eleccion":
			$query = 	"INSERT INTO ELECCION (id, num, repetir) VALUES (".$tiradaID.",".$num.",".$repe.");";
			mysql_query($query);
			for($i = 0;$i < count($values);$i++)
			{
				$query = "INSERT INTO OPCION (eleccion, contenido) VALUES (".$tiradaID.",'".$values[$i]."');";
				mysql_query($query);
			}
			break;
		case "asociacion":
			$query = 	"INSERT INTO ASOCIACION (id, repetir) VALUES (".$tiradaID.",".$repe.");";
			mysql_query($query);
			for($i = 0;$i < count($valuesA) && $i < count($valuesB);$i++)
			{	if($i < count($valuesA))
				{
					$query = "INSERT INTO OPCION (asociacion_desde, contenido) VALUES (".$tiradaID.",'".$valuesA[$i]."');";
					mysql_query($query);
				}
				if($i < count($valuesB))
				{
					$query = "INSERT INTO OPCION (asociacion_hasta, contenido) VALUES (".$tiradaID.",'".$valuesB[$i]."');";
					mysql_query($query);
				}
			}
			break;
	}

	echo json_encode(array("tirada"=>$tiradaID, "usuario" => $usuarioID));

	//enviar los emails:
	$url = "http://www.pickforme.net/elegirSalas.php";
	$cuerpo = "You have been invited into a room:\n";
	$cuerpo .= "ID: ".$tiradaID."\n";
	$cuerpo .= "Administrator: ".$nombreUsuario."\n";
	$cuerpo .= "Room: ".$nombre."\n";
	$cuerpo .= "Password: ".$contrasenia."\n";
	$cuerpo .= "Go to ".$url." to look for the room.";
	for($i = 0;$i < count($correo);$i++)
	{
		mail($correo[$i],"Invitation for EchaloASuerte.com",$cuerpo,"From: admin@echaloasuerte.com");
	}
?>
