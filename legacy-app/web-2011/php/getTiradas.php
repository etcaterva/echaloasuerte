<?php
	header('Content-Type: text/html; charset=utf-8');
	$conn = mysql_connect("db372506665.db.1and1.com","dbo372506665","1234abcd");
	mysql_select_db("db372506665", $conn);
	
	$result = mysql_query("SELECT * FROM TIRADA ORDER BY fecha DESC");
	
	$total = mysql_num_rows($result);
	$json= array();
	while($row = mysql_fetch_array($result))
	{
		$password=$row["password"] != ''? 'Yes' : 'No';
		array_push($json,array($row["id"],$row["nombre"],  $row["fecha"],  $row["participantes"],   $password));
	}

	echo json_encode(array("sEcho"=>2,"iTotalRecords"=>$total,"iTotalDisplayRecords"=>$total,"aaData" => $json));
  ?>