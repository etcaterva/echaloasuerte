<?php

/**
**	APERTURA DE LA CONEXION A LA BASE DE DATOS
**/
$conn = mysql_connect("localhost","root","toor");
mysql_select_db("echaloasuerte", $conn);

if (!$conn)
{
	die('Error al conectar con la base de datos: ' . mysql_error());
}

/**
**	ENVIA UN MAIL A LOS PARTICIPANTES DE LA TIRADA
**/
function sendJoinMail($mails, $id, $password)
{
	$cuerpo = "Atencion, te han invitado a unirte a una tirada en http://www.EchaloASuerte.com. La id de la tirada es: ".$id." Y la contraseña: ".$password." Puedes unirte en el Menu: Compartida -> Unir o a traves del siguiente link:  http://www.echaloasuerte.com/Unir.php?Id=".$id."&pass=".$password;
	for($i = 1;$i <= count($mails); $i++)
		mail($mails[$i-1],"Tirada en EchaloASuerte.com",$cuerpo,"From: EchaloASuerte.com");
}

function avisarFinalizada($id)
{
	$resquery = mysql_query("SELECT * FROM tirada where id = ".$id.";");
	if($resquery && mysql_num_rows($resquery) >= 1)
	{
		$row = mysql_fetch_array($resquery);
		$mails = explode(",",$row["mails"]);
		$cuerpo = "Atencion, ya estan disponibles los resultados de una tirada con id ".$id.".
Accede a traves del siguiente link: http://www.echaloasuerte.com/Unir.php?Id=".$id."&pass=".$row["pass"];
		for($i = 1;$i <= count($mails); $i++)
			mail($mails[$i-1],"Tirada en EchaloASuerte.com",$cuerpo,"From: EchaloASuerte.com");
	}
}

/**
**	CODIGO PARA MOSTRAR UNA FRASE DIFERENTE CADA VEZ
**/
//predir es la cadena a poner si la pagina no se enceuntra en el directorio raiz. poner ../

function getFraseDia($preDir)
{
	//Array de frases
	$frases = array("<p>¿Quién tiene que sacar hoy la basura? <br />EchaloASuerte elige por tí. </p>",
					"<p>¿No sabes que responder en tu test de personalidad?<br />EchaloASuerte elige por tí.</p>",
					"<p>¿No terminas de decidir el nombre de tu perro?<br />EchaloASuerte elige por tí.</p>",
					"<p>¿No estas seguro de invitarlo a tu boda?<br />EchaloASuerte elige por tí.</p>",
					"<p>Quedan 10 segundos ¿y no sabes qué cable cortar?<br/>EchaloASuerte elige por tí.</p>",					"<p>¿Quien invita esta ronda?<br/>EchaloASuerte elige por tí.</p>",
					"<p>¿No decides que cocinar hoy?<br/>EchaloASuerte elige por tí.</p>",
					"<p>¿Quien se queda con la cama grande?<br/>EchaloASuerte elige por tí.</p>",
					"<p>¿No queda tarta para todos?<br/>EchaloASuerte elige por tí.</p>",
					"<p>¿Con quien toca esta noche?<br/>EchaloASuerte elige por tí.</p>",
					"<p>¿Que Mario Bros vas a bajar hoy?<br/>EchaloASuerte elige por tí.</p>",
					"<p>¿Con quién toca pagarla hoy?<br/>EchaloASuerte elige por tí.</p>",
					"<p>¿Que asignatura vas a dejar este junio?<br/>EchaloASuerte elige por tí.</p>",
					"<p>¿Cuántos paquetes tocan?<br/>EchaloASuerte elige por tí.</p>",
					"<p>¿Quien bebe?<br/>EchaloASuerte elige por tí.</p>"	,
					"<p>¿Charmander, Bulbasaur o Squirtle?<br/>EchaloASuerte elige por tí.</p>",
					"<p>Puff..¿Con que casilla empiezo?<br/>EchaloASuerte elige por tí.</p>"
					);

	$imagenes = array("img/frases/basura.gif",
					"img/frases/personalidad.gif",
					"img/frases/perro.gif",
					"img/frases/boda.gif",
					"img/frases/bomba.gif",
					"img/frases/cerveza.gif",
					"img/frases/cocinero.gif",
					"img/frases/cama.gif",
					"img/frases/tarta.gif",
					"img/frases/beso.gif",
					"img/frases/juego.gif",
					"img/frases/enfado.gif",
					"img/frases/asignatura.gif",
					"img/frases/cigarrillo.gif",
					"img/frases/tequila.gif",
					"img/frases/pokemon.gif",
					"img/frases/buscaminas.gif"
					);

	$r = rand(0,count($frases)-1);
	echo "<table width=\"100%\" border=\"0\">";
	echo "<td width=\"79%\"><center><font color=\"white\">".$frases[$r];
	echo "</font></center></td><td width=\"21%\"><img src=\"".$preDir.$imagenes[$r];
    echo "\"/></td>	";
	echo "</table>";
}
