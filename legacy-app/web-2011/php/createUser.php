<?php

	header('Content-Type: text/html; charset=utf-8');
	$idTirada = isset($_GET['idTirada']) ? $_GET['idTirada'] : $_POST['idTirada'];
	$pass = isset($_GET['password']) ? $_GET['password'] : $_POST['password'];
	$usuario =isset($_GET['usuario']) ? $_GET['usuario'] : $_POST['usuario'];
	
	
	$conn = mysql_connect("db372506665.db.1and1.com","dbo372506665","1234abcd");
	mysql_select_db("db372506665", $conn);
	
	$result = mysql_query("SELECT * FROM TIRADA WHERE id=".$idTirada);
	$row = mysql_fetch_array($result);
	
	if($pass != $row["password"])
		echo "Error, la contraseña no coincide.";
	else
	{
	
		$result = mysql_query("SELECT * FROM USUARIO WHERE tirada=".$idTirada." and name='".$usuario."';");
		if(mysql_num_rows($result) > 0)
			echo "Error, existe un usuario con el mismo nombre.";
		else
		{
			$query = "INSERT INTO USUARIO (name,tirada) VALUES ('".$usuario."',".$idTirada.");";
			mysql_query($query);
			$userID = mysql_insert_id();
			echo $userID;
		}		
	}
?>