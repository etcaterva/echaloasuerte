<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta name="title" content="PickForMe.net" />
<meta name="keywords" content="pickforme, random, chose, pickforme.net, lucky, heads or tail, mario corchero" />
<meta name="description" content="PickForMe.net, decide stuff randomly!!" />
<meta http-equiv="Content-Language" content="es">
<meta http-equiv="content-type" content="text/html; charset=utf-8" />
<title>PickForMe</title>
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
		if(Math.random() < .5) alert('Head');
		else alert('Tail');
	});
	LinksExternos();
});
</script>

<body>
<a href="http://www.echaloasuerte.com/contacto.php">
<img src="img/es.png" class="language" style="position:absolute;top:15px;right:15px;" title="Español"/>
</a>
<div id="content">
<div id="header">
	<div id="menu">
		<ul>
			<li id="button1"><a href="index.php"  title="">Home</a></li>
			<li id="button1"><a href="elegirSalas.php"  title="">Rooms</a></li>
			<li id="button4"><a href="contacto.php" title="">Contact Us</a></li>
			<li id="button5"><a href="acerca.php" title="">About</a></li>
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
<h4>Contact Us</h4>
      <p>Have you find any bug on the site?<br/>
	  Do you have an idea to improve the site?<br/>
	  Any question about it?<br/>
	  Do you have a good sentence to apear at the top?<br/>	  
	  Do not hesitate to contact us!</p>
            <p>
              <? 
if (!(isset($_REQUEST["nombre"])&& isset($_REQUEST["email"])&&isset($_REQUEST["coment"]))){ 
?>
            </p>
            <form action="contacto.php" method=post>
              <p>Name:......
  <input type=text name="nombre" size=16>
  <br>
<br>
                Email:...........
                <input type=text name="email" size=16>
                <br>
                <br>
                Coments: 
                <textarea name="coment" cols=32 rows=6></textarea>
                <br>
                <input type=submit value="Enviar">
              </p>
</form>
            <? 
}else{ 
   	//Estoy recibiendo el formulario, compongo el cuerpo 
   	$cuerpo = "Formulario enviado\n"; 
   	$cuerpo .= "Nombre: " . $_REQUEST["nombre"] . "\n"; 
   	$cuerpo .= "Email: " . $_REQUEST["email"] . "\n"; 
   	$cuerpo .= "Comentarios: " . $_REQUEST["coment"] . "\n"; 

   	//mando el correo... 
   	mail("admin@echaloasuerte.com","Comentario en EchaloASuerte.com",$cuerpo,"From:".$_REQUEST["email"]); 


   	//doy las gracias por el env&iacute;o 
   	echo "Thanks so much for helping this web to grow. :)"; 
} 
?>
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

<div id="left" >
       <h3 onclick="$('#moneda').toggle('slow')">
          Heads or Tails</h3>
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
        Heads or Tails?  Click the coin!
        </p>
		<a href="#" id="CaraOCruz"><img  name="imgMoneda" src="img/cruz.png" alt="Moneda" onmouseover="swaponMoneda()" onmouseout="swapoffMoneda()" title="Heads or Tails?" /></a>
        </center>
        </div>     
        
		  <h3 onclick="$('#rrss').toggle('slow')">
          Social Networks</h3>
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
          Donations</h3>
		<div id="donar" class="comnews">
       
        <p>
        Want to help us with the project? You can donate just 2€ if you want.<a href="acerca.php">Click here and get further information.</a>
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
 <h3>Advertising</h3> <div style="display:block ;" class="comnews"><center>
<script type="text/javascript"><!--
google_ad_client = "ca-pub-1409219619115807";
/* Advertising */
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
<p><abbrev>PickForMe.net</abbrev> | | Proyect within <a href="http://www.etcaterva.com">EtCaterva</a> Group</p>
</div>
</div>
</div>
<!-- footer ends-->
<div style="text-align: center; font-size: 0.75em;"></div></body>
</html>
