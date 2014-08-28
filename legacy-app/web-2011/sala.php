<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta name="title" content="EchaloASuerte.com" />
<meta name="keywords" content="echaloasuerte, suerte, dados, cara, cruz, aleatorio, distribuido, a distancia, azar, echalo, pick, ban, cara o cruz, loteria, mario corchero" />
<meta name="description" content="Deja que el azar eliga una decision por ti. Olvidate de los papelitos. Esta es tu pagina, y cada uno desde su ordenador!" />
<meta http-equiv="Content-Language" content="es" />
<meta http-equiv="content-type" content="text/html; charset=utf-8" />
<title>EchaloASuerte</title>

<script type="text/javascript" src="js/jquery.js"></script>
<script type="text/javascript" src="js/script.js"></script>
<link href="css/styles.css" rel="stylesheet" type="text/css" media="screen" />
<script> 
$(document).ready(function(){
	
	/**FAQS**/
	$('.faqs dd').hide(); // Hide all DDs inside .faqs
	$('.faqs dt').hover(function(){$(this).addClass('hover')},function(){$(this).removeClass('hover')}).click(function(){ // Add class "hover" on dt when hover
		$(this).next().slideToggle('normal'); // Toggle dd when the respective dt is clicked
	});
	
	/** Cara o cruz**/
	$('#CaraOCruz').click(function(){
		if(Math.random() < .5) alert('Cara');
		else alert('Cruz');
	});
	
	var tiradaID= "<?php echo $_GET["idTirada"];?>";
	var password= "<?php echo $_GET["password"];?>";
	var usuarioID= "<?php echo $_GET["usuario"];?>";
	var dataTirada = 0;//JSON con toda la info
	var resuelto = 0;

	function refresh(){
		$.getJSON('php/getDataTirada.php',{idTirada : tiradaID, password : password, time : new Date().getTime()},function(data){
			//alert(data);
			var nombreSala = data.tirada.nombre;
			nombreSala+= "   (id: "+data.tirada.id+")";
			$('#titulo').text(nombreSala);
			var participantesRestantes;
			
			if(dataTirada == 0 || !compare_objects(dataTirada.usuarios,data.usuarios))
			{
				//numero de participantes y usuarios
				var participantesActuales = 0;
				$('#totales').text(data.tirada.participantes);
				$('#usuarios ul').empty();
				$.each(data.usuarios,function(key,val)
				{
					var usuarioHTML = "<li>"+val.name+"</li>";
					if(val.checked=="1")
					{
						participantesActuales++;
						usuarioHTML = "<li class='checked'>"+val.name+"</li>";
					}
					$('#usuarios ul').append(usuarioHTML);
				});
				$('#actuales').text(participantesActuales);
				participantesRestantes =data.tirada.participantes-participantesActuales;
				$('#restantes').text(participantesRestantes);
			}
			
			//
			
			//chat 
			if(dataTirada == 0 || !compare_objects(dataTirada.chat,data.chat))
			{			
				$('#chat ol').empty();
				$.each(data.chat,function(key,val)
				{
					var userMesage = data.usuarios[val.usuario].name;
					$('#chat ol').append("<li><span>"+userMesage+":</span> "+val.contenido+"</li>");
					var $chat = $('#chat');
					$chat[0].scrollTop = $chat[0].scrollHeight;
				});	
			}
			
			//Activar o desactivar estoy listo
			if(data.usuarios[usuarioID].checked == "1" || participantesRestantes < 1)
			{
				$('#listoBut').hide();
			}
			
			//contenido
			if(dataTirada == 0)
			{
				$contenido = $('#contenido');
				$contenido.empty();
				$contenido.html('<h3>Contenido</h3><br/>');	
				var contenidoHtml;
				switch(data.tipo.tipo)
				{
					case "aleatorio":
						contenidoHtml = "Obtener " + data.tipo.num + " numero(s) entre " + data.tipo.desde + " y "+data.tipo.hasta;
						if(+data.tipo.num > 1)
						{
							contenidoHtml += ",";
							if(data.tipo.repe == 0) contenidoHtml += " no";
							contenidoHtml += " puede haber elementos repetidos";
						}
						contenidoHtml+=".";
						break;
					case "eleccion":
						contenidoHtml = "Obtener " + data.tipo.num + " valores ";
						if(+data.tipo.num > 1)
						{
							contenidoHtml += ",";
							if(data.tipo.repe == 0) contenidoHtml += " no";
							contenidoHtml += " puede haber elementos repetidos";
						}
						contenidoHtml+=".<br/><ul><h5>Valores: </h5>";
						$.each(data.tipo.values, function(key,value)
						{
							contenidoHtml+="<li>"+value.contenido+"</li>";
						});
						contenidoHtml+="</ul>";
						break;
					case "asociacion":
						contenidoHtml = "Relacionar los siguientes valores ";
						contenidoHtml += ", los elementos del segundo conjunto";
						if(data.tipo.repe == 0) contenidoHtml += " no";
						contenidoHtml += " pueden repetirse";
						contenidoHtml+=".<br/><ul><h5>Conjunto1: </h5>";
						$.each(data.tipo.valuesA, function(key,value)
						{
							contenidoHtml+="<li>"+value.contenido+"</li>";
						});
						contenidoHtml+="</ul>";
						contenidoHtml+=".<br/><ul><h5>Conjunto 2: </h5>";
						$.each(data.tipo.valuesB, function(key,value)
						{
							contenidoHtml+="<li>"+value.contenido+"</li>";
						});
						contenidoHtml+="</ul>";	
						break;
				}
				$contenido.append(contenidoHtml);
			}	
				//soluciones?
				if(resuelto == 0 && participantesRestantes == 0){
					resuelto = 1;
					var htmlResult ="<div class='menuContent'>";
					htmlResult +="<div class='resultados'>";
					htmlResult +="<h4>RESULTADOS</h4>";
					if(data.tipo.tipo == "asociacion"){
						var vineta = "<td><img class='auto' src='img/vineta.png'></td>";
						var flecha = "<td><img class='auto' src='img/vinetaFlecha.png'></td>";					
						htmlResult +="<TABLE border='0'>";				
						$.each(data.solucion,function(key, value){
							htmlResult+= '<tr>'+vineta+'<td>' + value.split('][')[0]+'</td>'+flecha+'<td>' + value.split('][')[1]+'</td></tr>';
							});					
						htmlResult +="</table>";							
					}else{
						htmlResult +="<ul>";
						$.each(data.solucion,function(key, value){
							htmlResult+='<li>'+value+'</li>';
							});
						htmlResult +="</ul>";							
					}
					htmlResult +="</div>";
					htmlResult +="</div>";
					$('#chat').before(htmlResult);
					$('.resultados').show('slow');
				}
			
			dataTirada = data;
		});
	}//end refresh
	refresh();
	
	//enviar un mensaje
	$('#chatBut').click(function()
	{
		var mensaje = $('#chatText').val();
		$('#chatText').val('');
		$.post('php/chatMesage.php',{idTirada : tiradaID, usuario : usuarioID, mensaje : mensaje});
		refresh();
		return false;
	});
	
	//cofirmar(estoy listo)
	$('#listoBut').click(function()
	{
		$.post('php/confirmar.php',{usuario : usuarioID});
		refresh();
		return false;
	});
	
	//refreshcar cada 2 segundos:
	var t = setInterval(function(){refresh();},2000);
	
	LinksExternos();
});

</script>

<body>
<div id="content">
<div id="header">
	<div id="menu">
		<ul>
			<li id="button1"><a href="index.php"  title="">Inicio</a></li>
			<li id="button1"><a href="elegirSalas.php"  title="">Salas</a></li>
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
<h4 id="titulo">Salas</h4>
    <div id='panel'>
		<div id="participantes">
			<p>Participantes totales: <span id="totales"></span><img src="img/user.png"/> Confirmados: <span id="actuales"></span><img src="img/user3.png"/> Restantes: <span id="restantes"></span><img src="img/user2.png"/> </p>
		</div>
		<div id="contenido">
			<h3>Contenido</h3>

		</div>
		<div id="usuarios">
			<h3>Usuarios</h3>
			<ul>
			
			</ul>			
		</div>		
	
		<div id="chat">
			<ol>
				
			</ol>
		</div>
		
		<div id="controls">
			<form action="*" method="post" name="formChat">
				<input type="text" size="50" id="chatText" />
				<input type="submit" value="Enviar" id="chatBut"/>
				<input type="submit" value="Estoy Listo!" id="listoBut"/>
			</form>
		</div>
		
	</div>
      
	<dl class="faqs">
        <dt>¿Para que vale esta página?</dt>
        <dd>En esta página deben reunirse todos los participantes de la sala y pinchar en Estoy Listo para que se muestren los resultados.</dd>
        <dt>¿Cuando aparecen los resultados?</dt>
        <dd>Cuando el numero minimo de usuarios indicados por el creador pinchen Estoy listo.</dd>		
        <dt>¿Puden entrar mas usuarios de los indicados?</dt>
        <dd>Por supuesto, todos los usuarios que tengan la contraseña pueden entrar en la sala.</dd>	
        <dt>¿Puedo comunicarme con los usuarios de la sala?</dt>
        <dd>Si, dispones de un chat para ello, se encuentra al final del panel, escribe el mensaje que desees y pulsa "Enviar".</dd>			
        <dt>El resultado no es justo</dt>
        <dd>Lo sentimos pero los resultados salen de forma totalmente aleatoria, asegurate de que "contenido" muestra los parametros tal y como acordasteis.</dd>												
    </dl>
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
<p><abbrev>EchaloASuerte.com</abbrev> | | Un proyecto de <a href="http://www.etcaterva.com">EtCaterva</a></p>
</div>
</div>
</div>
<!-- footer ends-->
<div style="text-align: center; font-size: 0.75em;"></div>

</body>
</html>
