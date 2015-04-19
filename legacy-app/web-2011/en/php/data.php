<?php

/**
**	APERTURA DE LA CONEXION A LA BASE DE DATOS
**/
    $conn = mysql_connect("localhost","root","toor");
    mysql_select_db("echaloasuerte", $conn);

if (!$conn)
{
	die('Error with the database: ' . mysql_error());
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
	$frases = array("<p>Who has to take away today? <br />Let us choose for you!. </p>",
					"<p>Don't know what to answer on your personality test?<br />Let us choose for you!.</p>",
					"<p>Do not end up deciding the name of your dog?<br />Let us choose for you!.</p>",
					"<p>Not sure about inviting him t the weeding?<br />Let us choose for you!.</p>",
					"<p>Ten seconds left, What cable should you cut?<br/>Let us choose for you!.</p>",					"<p>¿Quien invita esta ronda?<br/>Let us choose for you!.</p>",
					"<p>What are you gonna cook today?<br/>Let us choose for you!.</p>",
					"<p>Who will take the big bed?<br/>Let us choose for you!.</p>",
					"<p>Not enaugh cake for all?<br/>Let us choose for you!.</p>",
					"<p>Who are you meeting up this night?<br/>Let us choose for you!.</p>",
					"<p>What game are you playing today?<br/>Let us choose for you!.</p>",
					"<p>Who will you get angry with?<br/>Let us choose for you!.</p>",
					"<p>What subject will you fail?<br/>Let us choose for you!.</p>",
					"<p>How many cigarette will you smoke today?<br/>Let us choose for you!.</p>",
					"<p>Who drinks?<br/>Let us choose for you!.</p>"	,
					"<p>Charmander, Bulbasaur or Squirtle?<br/>Let us choose for you!.</p>",
					"<p>Puff..Where can I start?<br/>Let us choose for you!.</p>"
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
