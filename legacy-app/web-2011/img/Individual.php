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
<h4>Individual</h4>
    <p>Qué deseas, ¿<strong>un numero aleatorio, elegir un valor o relacionar varios</strong>?</p>
    <p>
      <center>
            <p><a href="individual/Aleatorio.php"><img  name="imgAleatorio" src="img/buttonAleatorio.png" alt="Numero aleatorio" width="264" height="230" onmouseover="swapon1()" onmouseout="swapoff1()" title="Numero aleatorio" /></a> <a href="individual/Eleccion.php"><img name="imgEleccion" src="img/buttonEleccion.png" alt="Elegir entre valores" width="264" height="230" onmouseover="swapon2()" onmouseout="swapoff2()" title="Elegir entre valores"/></a>
              <br />
      <a href="individual/Asociacion.php"><img src="img/buttonAsociacion.png" alt="Asociar valores" name="imgAsociacion" width="264" height="230" id="imgAsociacion" title="Asociar valores" onmouseover="swapon3()" onmouseout="swapoff3()"/></a> </p>
      </center>
    </p>
    <?php
	botonAyuda("
      Debes elegir un tipo de tirada.<br /><br />
 <strong>Numero Aleatorio.</strong><br />
        Devuelve un numero aleatorio dentro de un rango. Se puede especificar varios,       permitiendo repetidos.<br />
        Usos: Obtener un n&uacute;mero aleatorio, obtener una serie de numeros aleatorios,       echar la bonoloto, etc.
       <br /><br  /><strong>Elecci&oacute;n.</strong><br />
        Introducido un n&uacute;mero de valores el sistema el sistema elegira a uno (o varios       segun se indique).<br />
        Usos: Elegir quien debe recoger un paquete, escoger entre varios articulos con       las mismas prestaciones, etc.
       <br /><br /><strong>Asociaci&oacute;n.<br />
        </strong>Dadas dos columnas de valores el sistema las relaciona, pudiendose       indicar si se desean repetir los valores de la segunda columna.<br />
        Usos: Asignar habitaciones de un piso, asignar tareas de la casa, etc."); ?>
    
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
		<div id="chat" class="comnews">    	
        <iframe src="http://www.echaloasuerte.com/yshout5/example/" width="100%" height="400">
          <p>Your browser does not support iframes.</p>
        </iframe>
        
        </div> 
<h3 onclick="hide('moneda')">
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
        <center>
        
        <a href="http://www.tuenti.com/#m=Page&func=index&page_key=1_1769_59547535"><img  name="imgTuenti" src="img/tuenti.png" alt="Tuenti" title="Sigenos en Tuenti" /></a>        
        
		<iframe src="http://www.facebook.com/plugins/likebox.php?href=http%3A%2F%2Fwww.facebook.com%2Fpages%2FEchaloASuerte%2F202874843092116&amp;width=200&amp;colorscheme=light&amp;show_faces=false&amp;border_color=3A6BAD&amp;stream=false&amp;header=true&amp;height=62" scrolling="no" frameborder="0" style="border:none; overflow:hidden; width:250px; height:62px;" allowTransparency="true"></iframe>  
        
        </div>     
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
