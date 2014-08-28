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
<script type="text/javascript" src="js/jquery.js"></script>
<link href="css/styles.css" rel="stylesheet" type="text/css" media="screen" />
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
$(document).ready(function(){
	/** Cara o cruz**/
	$('#CaraOCruz').click(function(){
		if(Math.random() < .5) alert('Cara');
		else alert('Cruz');
	});
	LinksExternos();
});
</script>

<body>
<a href="http://www.pickforme.net/acerca.php">
<img src="img/eng.png" class="language" style="position:absolute;top:15px;right:15px;" title="English"/>
</a>
<div id="content">
<div id="header">
	<div id="menu">
		<ul>
			<li id="button1"><a href="index.php"  title="">Inicio</a></li>
			<li id="button2"><a href="elegirSalas.php"  title="">Salas</a></li>
			<li id="button4"><a href="contacto.php" title="">Contacto</a></li>
			<li id="button5"><a href="acerca.php" title="">Acerca de</a></li>
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
<h4>Acerca de la página</h4>
	<p>EchaloASuerte.com es una idea absurda surguida tras buscar una página de este tipo y no encontrarla. No pretende ser tu pagina de inicio ni la más visitada de interenet, solo una de las paginas que pueden serte útil en un momento determinado.</p>
<h4>Acerca de nosotros</h4>
<p>La pagina se encuentra dentro del grupo <a href="http://www.etcaterva.com">EtCaterva</a>, creada por <a href="http://etcaterva.com/user.php?id=1">Mario A. Corchero</a> en 2010 y Actualizada en 2012.</p>
<h4>Donaciones</h4>
<p>Actualmente la página permite realizar donaciones de la cantidad que se desee(desde 1 €), para ello se utiliza PayPal, por su seguridad. Nosotros no recibimos tu numero de tarjeta ni nada, solo el pago(menos 40 centimos de coste de transacción).¡Ayudanos a mantener este sitio y haz una donacion!</p>
<h4>Agradecimientos</h4>
<p>Personas que han realizado aportaciones a la pagina (consejos, publicidad, frases...), ¿a que esperas para unirte?</p>
<p>Melania, Koleta, Enrique Alvarez, David Muñoz, Manuel Cantonero, Changu, Daniel Garcia, David Naranjo, Nacho delayed, Fer, Galin, Alberto, Mercedes Mateos...</p>
<p>Utiliza la sección de contactos y aparece en los agradecimientos!</p>
    </div>

<div id="left" >
       <h3 onclick="$('#moneda').toggle('slow')">
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
		<a href="#" id="CaraOCruz"><img  name="imgMoneda" src="img/cruz.png" alt="Moneda" onmouseover="swaponMoneda()" onmouseout="swapoffMoneda()" title="¿Cara o Cruz?" /></a>
        </center>
        </div>     
        
		  <h3 onclick="$('#rrss').toggle('slow')">
          Redes Sociales</h3>
		<div id="rrss" class="comnews">
        <center>        <a href="http://www.tuenti.com/#m=Page&func=index&page_key=1_1769_59547535" target="_blank"><img  name="imgTuenti" src="img/tuenti.png" alt="Tuenti" title="Sigenos en Tuenti" /></a>        
        
		<iframe src="http://www.facebook.com/plugins/likebox.php?href=http%3A%2F%2Fwww.facebook.com%2Fpages%2FEchaloASuerte%2F202874843092116&amp;width=200&amp;colorscheme=light&amp;show_faces=false&amp;border_color=3A6BAD&amp;stream=false&amp;header=true&amp;height=62" scrolling="no" frameborder="0" style="border:none; overflow:hidden; width:250px; height:62px;" allowTransparency="true"></iframe>  <br />
        
<a href="http://twitter.com/share" class="twitter-share-button" data-url="http://www.echaloasuerte.com" data-text="Usando #EchaloASuerte :D" data-count="horizontal" data-lang="es">Tweet</a><script type="text/javascript" src="http://platform.twitter.com/widgets.js"></script>         
       

<script type="text/javascript" src="http://platform.linkedin.com/in.js"></script><script type="in/share" data-url="http://www.echaloasuerte.com" data-counter="right"></script><br /><br />


<a href="http://www.delicious.com/save" onclick="window.open('http://www.delicious.com/save?v=5&noui&jump=close&url='+encodeURIComponent(location.href)+'&title='+encodeURIComponent(document.title), 'delicious','toolbar=no,width=550,height=550'); return false;"> 
<img src="http://www.videojuegosonline.net/images/share/Share-delicius.png" height="50" width="50" alt="Delicious" />
</a><font color="#FFFFFF" >____</font>
<script type="text/javascript" src="https://apis.google.com/js/plusone.js"></script><!-- Añade esta etiqueta donde quieras colocar el botón +1 -->
<g:plusone></g:plusone><br /><img src="img/logo.png" alt="" width="1" height="1" />  </div> 

<h3 onclick="$('#donar').toggle('slow')">
          Donaciones</h3>
		<div id="donar" class="comnews">
       
        <p>
        ¿Por qué no donar un par de euros a tu pagina favorita? <a href="acerca.php">Click para más información.</a>
        </p>
		<center>
<form action="https://www.paypal.com/cgi-bin/webscr" method="post">
<input type="hidden" name="cmd" value="_s-xclick">
<input type="hidden" name="hosted_button_id" value="D4T7AXE8V225N">
<input type="image" src="https://www.paypalobjects.com/es_ES/ES/i/btn/btn_donateCC_LG.gif" border="0" name="submit" alt="PayPal. La forma rápida y segura de pagar en Internet.">
<img alt="" border="0" src="https://www.paypalobjects.com/es_ES/i/scr/pixel.gif" width="1" height="1">
</form>
		
        </center>
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
<p><abbrev>EchaloASuerte.com</abbrev> | | Un proyecto de <a href="http://www.etcaterva.com">EtCaterva</a> || <a href="https://plus.google.com/u/0/111598032987660443498?rel=author">+Mario Corchero</a></p>
</div>
</div>
</div>
<!-- footer ends-->
<div style="text-align: center; font-size: 0.75em;"></div></body>
</html>