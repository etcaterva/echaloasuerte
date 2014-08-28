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
      document.imgIndividual.src="img/buttonIndividual_1.png";
 }
function swapoff1()
 {
      document.imgIndividual.src="img/buttonIndividual.png";
 }
function swapon2()
 {
      document.imgCompartida.src="img/buttonCompartida_1.png";
 }
function swapoff2()
 {
      document.imgCompartida.src="img/buttonCompartida.png";
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
<h4>Informacion</h4>
      <p>¿No acabas de enterarte de	como funciona la página? Aqui tienes una &quot;breve&quot; explicación.</p>
      <h2>Introducción</h2>
      <p>EchaloASuerte es una página cuyo objetivo es ayudarte a tomar una decisión, repartir trabajo, comida o cualquier cosa que necesite ser aleatoria, ademas, permite realizarlo desde multiples ordenadores.</p>
      <h2>Tipos de tirada</h2>
      <p>En EchaloASuerte dispones de las siguientes opciones:</p>
      <p>-Numero aleatorio<br />
      -Eleccion<br />
      -Asociacion </p>
      <p> <strong>Numero Aleatorio.</strong><br />
        Devuelve un numero aleatorio dentro de un rango. Se puede especificar varios,       permitiendo repetidos.<br />
        Usos: Obtener un n&uacute;mero aleatorio, obtener una serie de numeros aleatorios,       echar la bonoloto, etc.</p>
      <p> <strong>Elecci&oacute;n.</strong><br />
        Introducido un n&uacute;mero de valores el sistema el sistema elegira a uno (o varios       segun se indique).<br />
        Usos: Elegir quien debe recoger un paquete, escoger entre varios articulos con       las mismas prestaciones, etc.</p>
      <p> <strong>Asociaci&oacute;n.<br />
        </strong>Dadas dos columnas de valores el sistema las relaciona, pudiendose       indicar si se desean repetir los valores de la segunda columna.<br />
        Usos: Asignar habitaciones de un piso, asignar tareas de la casa, etc.</p>
      <p>&nbsp;</p>
      <h2>Modos</h2>
      <p>La web se puede dividir en 2 tipos de &quot;tiradas&quot; (echar a suerte algo).<br />
      -Individual. <br />
      -Compartida.<br />
      En el tipo individual se supone que todos los participantes estan delante del mismo ordenador, mientras que en el modo compartido los participantes pueden estar cada uno en una punta del mundo.<br />
      En el modo individual solo sera necesario indicar los valores para 
      obtener un resultado, mientras que en el modo compartido, habrá que crear una tirada, y una vez creada, el resto de participantes deberan unirse a ella. Una vez se haya unido el número de participantes acordado, se visualizaran los resultados.<br />
      Nota: al crear la tirada, puede indicar el email de los participantes para que reciban un mail con los datos.
      </p>
<p>&nbsp;</p>
<h4>Acerca de</h4>
<p>EchaloASuerte.com es una idea absurda surguida tras buscar una página de este tipo y no encontrarla. No pretende ser tu pagina de inicio ni la mas visitada de interenet, solo una de las paginas chorras que pueden serte util en un momento determinado.</p>
<p>Idea y diseño por Mario Corchero Jimenez.</p>
<p>Gracias a todos por visitar la pagina y por ofrecer frases de inicio :D.</p>
<h4>Agradecimientos</h4>
<p>Personas que han realizado aportaciones a la pagina (consejos, publicidad, frases...)</p>
<p>Koleta, Enrique Alvarez, David Muñoz, Manuel Cantonero, Changu, Dani Garcia, Nacho delayed, Fer, Galin, Alberto, Mercedes Mateos...</p>
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
