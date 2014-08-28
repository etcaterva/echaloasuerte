<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta name="title" content="EchaloASuerte.com" />
<meta name="keywords" content="echaloasuerte, suerte, dados, cara, cruz, aleatorio, distribuido, a distancia, azar, echalo, pick, ban, cara o cruz, loteria, mario corchero" />
<meta name="description" content="EchaloASuerte.com, echalo a suerte desde uno o varios ordenadores, cada uno desde su casas!!" />
<meta http-equiv="Content-Language" content="es">
<meta http-equiv="content-type" content="text/html; charset=utf-8" />
<title>EchaloASuerte</title>
<meta name="keywords" content="" />
<meta name="description" content="" />
<link href="styles.css" rel="stylesheet" type="text/css" media="screen" />
<style type="text/css">
#apDiv1 {
	position:absolute;
	width:200px;
	height:115px;
	z-index:1;
	left: 459px;
	top: 95px;
}
</style>
</head>

<script>
function swapon1()
 {
      document.imgAleatorio.src="img/buttonAleatorio_1.png";
 }
function swapoff1()
 {
      document.imgAleatorio.src="img/buttonAleatorio.png";
 }
function swapon2()
 {
      document.imgEleccion.src="img/buttonEleccion_1.png";
 }
function swapoff2()
 {
      document.imgEleccion.src="img/buttonEleccion.png";
 }
function swapon3()
 {
      document.imgAsociacion.src="img/buttonAsociacion_1.png";
 }
function swapoff3()
 {
      document.imgAsociacion.src="img/buttonAsociacion.png";
 }  
</script>
<body>
<div id="content">
<div id="header">
	<div id="menu">
		<ul>
			<li id="button1"><a href="index.php"  title="">Inicio</a></li>
			<li id="button2"><a href="Individual.php" title="">Individual</a></li>
			<li id="button3"><a href="Compartida.php" title="">Compartida</a></li>
			<li id="button4"><a href="Contacto.php" title="">Contacto</a></li>
			<li id="button5"><a href="Informacion.php" title="">Información</a></li>
		</ul>
	</div>
	<div id="logo">
                <?php
                	require_once("php/data.php");
                    getFraseDia("");
                ?>
    </div>
	</div>
<div id="main">
	<div id="right">
<h4>Unir</h4>
    <p>
    
<?php
		  require_once("php/data.php");
			
			if(isset($_REQUEST["Id"]))
			{
				$resquery = mysql_query("SELECT id,pass,fecha,restantes,participantes,resultado FROM tirada where id = ".$_REQUEST["Id"].";",$conn);
				$restantes = 1;			
				if(mysql_num_rows($resquery) >= 1)
				{
					$row = mysql_fetch_array($resquery);	
					$restantes = $row[3];	
					$participantes = explode(",",$row[4]);	
				}
			}
		  if(!isset($_REQUEST["Id"])&& !isset($_REQUEST["nombre"]))//inicio
		  {
echo "<form action=\"Unir.php\" method=\"post\" name=\"acceder\" id=\"acceder\">
              <p><strong>Id de la tirada </strong>&nbsp;&nbsp;
                <input name=\"Id\" type=\"text\" id=\"Id\" size=\"10\">
              </p>
              <p><strong> Contrase&ntilde;a </strong>
                <input name=\"pass\" type=\"text\" id=\"pass\" size=\"10\">
              </p>
              <p>
                <input type=\"submit\" name=\"Go\" id=\"Go\" value=\"Acceder\">
              </p>
          </form>";	
		  botonAyuda("
		  	Esta pagina sirve para unirte o consultar una tirada que ya haya sido creada (por ti u otra persona). Hay dos formas de acceder, a traves del correo que se te debe haver enviado(si el creador lo indico) o a traves de esta página. Para acceder a traves de esta página sera necesario que indiques el id y la contraseña con la que se creo la tirada, consultaló con el creador de esta. Si no introdujo contraseña, dejala en blanco.  
		  ");
		  }
		  elseif(isset($_REQUEST["Id"]) && !isset($_REQUEST["nombre"]) && $restantes > 0)
		  //confirmar un usuario
		  {
			if(mysql_num_rows($resquery) < 1 || $row[1] != $_REQUEST["pass"])
			{
				echo "<p><font color=\"#FF0000\" >Error: No existe la id indicada o la contraseña es incorrecta.</font>";
		  botonAyuda("
		  	Parece que has intentado acceder a una tirada y no has introducido la id o la contraseña de forma correcta, vuelva atras e intentalo de nuevo.  
		  ");				
			}
			else{
			MostarTirada($_REQUEST["Id"]);
         echo "	<form action=\"Unir.php\" method=\"post\" name=\"unir\" id=\"unir\">
			  <p><strong>Id</strong>&nbsp;&nbsp;..............
                <input name=\"Id\" type=\"text\" id=\"Id\" size=\"10\" readonly=\"true\" value=\"".$_REQUEST["Id"]."\"><br>
				<strong>Participantes restantes: ".$restantes."  <br>
				Participantes confirmados: <br></strong>";
				for($i=1;$i < count($participantes); $i++)
					echo $participantes[$i]."<br>";
			  echo "</strong>  </p>
			  <p><strong>Nombre </strong>
				<input name=\"nombre\" type=\"text\" id=\"nombre\" size=\"20\">
				<input type=\"submit\" name=\"confirmar\" id=\"confirmar\" value=\"Confirmar\">
			  </p>
			</form>";
			botonAyuda("
		  	Has ingresado correctamente en una tirada, ahora, indica tu nombre para confirmar la tirada, si tu nombre ya aparece, no lo hagas de nuevo, ya que entonces uno de los participantes no confirmará la tirada y no la dará por válida entonces.  Comprueba que los campos son correctos 
		  ");
			}
		  }
		  else {//ha introducido un nombre
			MostarTirada($_REQUEST["Id"]);		  
			echo"
			<p><strong>Participantes confirmados:</strong><br>";
			for($i=1;$i < count($participantes); $i++)
				echo $participantes[$i]."<br>";	 
			if($restantes <= 1)
			{
				if($restantes == 1)
				{
					avisarFinalizada($_REQUEST["Id"]);
					echo $_REQUEST["nombre"]."<br>";
					$aux =  $restantes-1;
					$query = "update tirada set restantes = ". $aux .", participantes = '".$row[4].",".$_REQUEST["nombre"]."' where id = ".$_REQUEST["Id"].";";
					mysql_query($query,$conn);
				}
				echo "<p><strong>Resultado</strong>:";
				echo "<br>".$row["resultado"]."</p>";
				botonAyuda("
							Estos son los resultados de la tirada creada y confirmada por todos los usuarios, si has llegado a esta pagina sin pasar por la página de confirmación en algun momento y eres uno de los participantes, es que han intentado engañarte :), comprueba los nombres que aparecen como participantes confirmados.  
						  ");				
			}
			else
			{
				echo $_REQUEST["nombre"]."<br>";
				$aux = $restantes-1;
				echo "<strong>Participantes restantes: <font color=\"red\">".$aux."</font>  <br>";
				$query = "update tirada set restantes = ". $aux .", participantes = '".$row[4].",".$_REQUEST["nombre"]."' where id = ".$_REQUEST["Id"].";";
				mysql_query($query,$conn);
				botonAyuda("
				Has confirmado tu participación en la tirada, podras ver los resultados cuando el resto de participantes realicen la misma acción. Si se indico correo electronico al crear la tirada, te llegará un aviso. <br /> ¡Recuerda que puede estar en correo no deseado!
						  ");
			}			
		  }
	?>    
    </p>
    <center>
    <p><br />
        </p>
      </center>
    </p>
    <p>&nbsp;</p>
	</div>
<script>
function hide(id)
{
	if(document.getElementById(id).style.display=='block')
	{
		document.getElementById(id).style.display='none';
	}else
	{
		document.getElementById(id).style.display='block';
	}
}
</script>

<div id="left">		  <h3 onclick="hide('chat')">
          Chat</h3>
		<div id="chat" class="comnews">     <iframe src="http://www.echaloasuerte.com/yshout5/example/" width="100%" height="100%"><p>Your browser does not support iframes.</p>
        </iframe>
        
        </div>       <h3 onclick="hide('moneda')">
          Cara o Cruz</h3>
		<div id="moneda" class="comnews">
        <center>
<script>
function swaponMoneda()
 {
      document.imgMoneda.src="img/cara.png";
 }
function swapoffMoneda()
 {
      document.imgMoneda.src="img/cruz.png";
 }  
 </script>
        
        <p>
        ¿Cara o Cruz? Haz click
        </p>
		<a href="http://www.echaloasuerte.com/individual/Eleccion.php?num=1&Values=Cara,Cruz"><img  name="imgMoneda" src="img/cruz.png" alt="Moneda" onmouseover="swaponMoneda()" onmouseout="swapoffMoneda()" title="¿Cara o Cruz?" /></a>
        </center>
        </div> 		  <h3 onclick="hide('rrss')">
          Redes Sociales</h3>
		<div id="rrss" class="comnews">
        <center>        <a href="http://www.tuenti.com/#m=Page&func=index&page_key=1_1769_59547535" target="_blank"><img  name="imgTuenti" src="img/tuenti.png" alt="Tuenti" title="Sigenos en Tuenti" /></a>		<iframe src="http://www.facebook.com/plugins/likebox.php?href=http%3A%2F%2Fwww.facebook.com%2Fpages%2FEchaloASuerte%2F202874843092116&amp;width=200&amp;colorscheme=light&amp;show_faces=false&amp;border_color=3A6BAD&amp;stream=false&amp;header=true&amp;height=62" scrolling="no" frameborder="0" style="border:none; overflow:hidden; width:250px; height:62px;" allowTransparency="true"></iframe>  <br />
        
<a href="http://twitter.com/share" class="twitter-share-button" data-url="http://www.echaloasuerte.com" data-text="Usando #EchaloASuerte :D" data-count="horizontal" data-lang="es">Tweet</a><script type="text/javascript" src="http://platform.twitter.com/widgets.js"></script>         
       

<script type="text/javascript" src="http://platform.linkedin.com/in.js"></script><script type="in/share" data-url="http://www.echaloasuerte.com" data-counter="right"></script><br /><br />


<a href="http://www.delicious.com/save" onclick="window.open('http://www.delicious.com/save?v=5&noui&jump=close&url='+encodeURIComponent(location.href)+'&title='+encodeURIComponent(document.title), 'delicious','toolbar=no,width=550,height=550'); return false;"> 
<img src="http://www.videojuegosonline.net/images/share/Share-delicius.png" height="50" width="50" alt="Delicious" />
</a><font color="#FFFFFF" >____</font>
<script type="text/javascript" src="https://apis.google.com/js/plusone.js"></script><!-- Añade esta etiqueta donde quieras colocar el botón +1 -->
<g:plusone></g:plusone></div><br />  </div>     
              <h3>Publicidad</h3> <div style="display:block ;" class="comnews"><center>
<script type="text/javascript"><!--
google_ad_client = "ca-pub-1409219619115807";
/* Publicidad */
google_ad_slot = "5937113309";
google_ad_width = 250;
google_ad_height = 250;
//-->
</script>
<script type="text/javascript"
src="http://pagead2.googlesyndication.com/pagead/show_ads.js">
</script>  </center>
      
       </div>		
					

	</div><div style="clear:both;">
	</div>
<div id="footer">
 
<p><abbrev>EchaloASuerte.com</abbrev>	</p>
</div>
</div>
</div>
<!-- footer ends-->
<div style="text-align: center; font-size: 0.75em;"></div></body>
 
</html>
