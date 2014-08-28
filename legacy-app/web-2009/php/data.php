<?php

/**
**	APERTURA DE LA CONEXION A LA BASE DE DATOS
**/
$conn = mysql_connect("db372506665.db.1and1.com","dbo372506665","1234abcd");
mysql_select_db("db372506665", $conn);
/*$conn = mysql_connect("localhost","root","1234");
mysql_select_db("echaloasuerte", $conn);*/

if (!$conn)
{
	die('Error al conectar con la base de datos: ' . mysql_error());
}		

/**
**	CONSTANTES PARA DISTINGUIR LOS SERVICIOS
**/
if (!defined("DISTRIBUIDO")) define("DISTRIBUIDO", 0);
if (!defined("NORMAL")) define("NORMAL", 1);  
if (!defined("INFO")) define("INFO", 2);//mostrar sin permitir introducir(para distribuido)

function MostarTirada($id)
{
	$resquery = mysql_query("SELECT * FROM tirada where id = ".$id.";");	
	if($resquery && mysql_num_rows($resquery) >= 1)
	{
		$row = mysql_fetch_array($resquery);
		switch ($row["tipo"])
		{
			case 0:
			  echo "<p>Dame 
                <input disabled=\"disabled\" name=\"num\" type=\"text\" id=\"num\" value=\"".$row["num"]."\" size=\"3\">
              número(s) desde 
              <input disabled=\"disabled\" name=\"From\" type=\"text\" id=\"From\" value=\"".$row["desde"]."\" size=\"10\"> 
              hasta 
              <input disabled=\"disabled\" name=\"To\" type=\"text\" id=\"To\" value=\"".$row["hasta"]."\" size=\"10\">
              </p>
              <p>
                <input disabled=\"disabled\" name=\"repe\" type=\"checkbox\" id=\"repe\"";
				if($row["repe"]) echo "checked=\"checked\"";
				echo ">
Puede haber números repetidos</p>"; 				
			break;
			case 1:
			echo "<p>Elige 
			  <input disabled=\"disabled\" name=\"num\" type=\"text\" id=\"num\" value=\"".$row["num"]."\" size=\"5\"> 
			  de los siguientes valores separados por comas 
			  </p>
			<p>
			  <input disabled=\"disabled\" name=\"Values\" type=\"text\" id=\"Values\" value=\"".$row["val"]."\" size=\"100\">
			</p>
			<p>
			<input disabled=\"disabled\" name=\"repe\" type=\"checkbox\" id=\"repe\" ";
				if($row["repe"]) echo "checked=\"checked\"";
				echo">
							Puede haber elementos repetidos</p>";				
			break;
			case 2:
				echo "<p>Relacioname
				  <input disabled=\"disabled\" name=\"Values\" type=\"text\" id=\"Values\" value=\"".$row["val"]."\" size=\"100\">
				</p>
				<p>con<strong> </strong>
				  <input disabled=\"disabled\" name=\"ValuesB\" type=\"text\" id=\"ValuesB\" value=\"".$row["valB"]."\" size=\"100\"> 
				</p> <p>
				<input disabled=\"disabled\" name=\"repe\" type=\"checkbox\" id=\"repe\"";
				if($row["repe"]) echo "checked=\"checked\"";								
				echo "> 
					Los elementos del segundo campo pueden repetirse.</p>
				    <p>Nota: En cada campo, deben separarse los elementos por comas</p>";				
			break;
		}
	}	
}

/**
**	FIN DE UN FORMULARIO
**	param $tiposervicio: tipo de servicio que propociona el formulario
**	Crea el boton y los cuadros de dialogo
**/
function EndFormulario($tipoServicio)
{
	if($tipoServicio == "NORMAL")
	{
	 echo "<input type=\"submit\" name=\"Go\" id=\"Go\" value=\"EchaloASuerte\">
		   </p>
		   </form><p>";
	}
	else if ($tipoServicio == "DISTRIBUIDO")
	{
	  echo "<p>Somos 
			  <input name=\"partic\" type=\"text\" id=\"partic\" value=\"2\" size=\"5\"> 
			  participantes y quiero que la contraseña sea 
			  <input name=\"password\" type=\"text\" id=\"password\" size=\"20\">.</p>
			<p>  Envia la información a los siguientes correos separados por comas(opcional)
			</p>
			<p>
			  <input name=\"mails\" type=\"text\" id=\"mails\" size=\"70\">
			</p>
			<p>
			<input type=\"submit\" name=\"Go\" id=\"Go\" value=\"Crear\">
			</p>"; 
	}
}

/**
**	CREA EL FORMULARIO PARA UNA TIRADA ALEATORIA
** 	param $tipoServicio: tipo de servicio para el que se crea la tirada
**/
function FormularioAleatorio($tipoServicio)
{			
			$num = 1; $from = 0; $to = 10; 
			if(isset($_REQUEST["num"]))
			{
				$num = $_REQUEST["num"];
				$from = $_REQUEST["From"];
				$to = $_REQUEST["To"];
			}
		    echo "<form name=\"form1\" method=\"post\" action=\"Aleatorio.php\">
              <p>Dame 
                <input name=\"num\" type=\"text\" id=\"num\" value=\"".$num."\" size=\"3\"  onclick=\"if(this.value==".$num.") this.value=''\">
              número(s) desde 
              <input name=\"From\" type=\"text\" id=\"From\" value=\"".$from."\" size=\"10\" onclick=\"if(this.value==".$from.")this.value=''\"> 
              hasta 
              <input name=\"To\" type=\"text\" id=\"To\" value=\"".$to."\" size=\"10\" onclick=\"if(this.value==".$to.")this.value=''\">
              </p>
              <p>
                <input name=\"repe\" type=\"checkbox\" id=\"repe\"";
			if(isset($_REQUEST["repe"])) echo "checked=\"checked\"";	
			echo ">
Puede haber números repetidos</p>";
			  EndFormulario($tipoServicio);
}

/**
**	CREA EL FORMULARIO PARA UNA TIRADA ALEATORIA
** 	param $tipoServicio: tipo de servicio para el que se crea la tirada
**/
function FormularioEleccion($tipoServicio)
{
	
			$num = 1; $val = "Mario, Juan, Pedro, Raul, Jaime, Manuel";
			if(isset($_REQUEST["num"]))
			{
				$num = $_REQUEST["num"];
				$val = $_REQUEST["Values"];
			}	
	
	echo "<form name=\"form1\" method=\"post\" action=\"Eleccion.php\">
              <p>Elige 
  <input name=\"num\" type=\"text\" id=\"num\" value=\"".$num."\" size=\"5\" onclick=\"if(this.value==".$num.")this.value=''\"> 
  de los siguientes valores separados por comas 
  </p>
<p>
  <input name=\"Values\" type=\"text\" id=\"Values\" value=\"".$val."\" size=\"100\" onclick=\"if(this.value=='".$val."')this.value=''\">
</p>
<p>        <input name=\"repe\" type=\"checkbox\" id=\"repe\"";
			if(isset($_REQUEST["repe"])) echo "checked=\"checked\"";	
			echo ">
Puede haber números repetidos</p>";
	EndFormulario($tipoServicio);
}

/**
**	CREA EL FORMULARIO PARA UNA TIRADA DE ASOCIACION
** 	param $tipoServicio: tipo de servicio para el que se crea la tirada
**/
function FormularioAsociacion($tipoServicio)
{
			$val = "Manu, Mesu, Juanfran, Jonathan"; 
			$valB = "Cocina, Ba&ntilde;o, Pasillo y Basura, Comedor";
			if(isset($_REQUEST["num"]))
			{
				$val = $_REQUEST["Values"];
				$valB = $_REQUEST["ValuesB"];
			}		
	
	echo "<form name=\"form1\" method=\"post\" action=\"Asociacion.php\">
<p>Relacioname
  <input name=\"Values\" type=\"text\" id=\"Values\" value=\"".$val."\" size=\"100\" onclick=\"if(this.value=='".$val."')this.value=''\">
</p>
<p>con<strong> </strong>
  <input name=\"ValuesB\" type=\"text\" id=\"ValuesB\" value=\"".$valB."\" size=\"100\" onclick=\"if(this.value=='".$valB."')this.value=''\"> 
</p>
              <p>
                <input name=\"repe\" type=\"checkbox\" id=\"repe\"";
				if(isset($_REQUEST["repe"])) echo "checked=\"checked\"";					
				echo"> 
                Los elementos del segundo campo pueden repetirse.</p>
              <p>Nota: En cada campo, deben separarse los elementos por comas</p>";
			  	EndFormulario($tipoServicio);
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

function botonAyuda($info)
{
		echo "<p>
	<script>
	function swaphelpon()
	 {
		  document.giveMeHelp.src=\"img/ayuda_1.png\";
	 }
	function swaphelpoff()
	 {
		  document.giveMeHelp.src=\"img/ayuda.png\";
	 }
	</script>
	
	  <script src=\"http://code.jquery.com/jquery-latest.js\"></script>
	  <center>
		<p>Si necesitas ayuda haz click en Maggie</p><br />
		<p><img name=\"giveMeHelp\" title=\"¡Ayuda!\" id=\"giveMeHelp\" src=\"img/ayuda.png\" onmouseover=\"swaphelpon()\" onmouseout=\"swaphelpoff()\" alt=\"\"/> 
		</p>
	  </center>
	  <div class=\"help\">
		  <strong>Ayuda:</strong><br />".$info."</div>
	<script>
		$(\"#giveMeHelp\").click(function () {
		$(\".help\").show(\"slow\");
		$(\"#giveMeHelp\").hide(\"fast\");
		});
		</script></p>";
}
?>