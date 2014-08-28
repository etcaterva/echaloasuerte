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
<script type="text/javascript" src="js/jquery.dataTables.min.js"></script>
<script type="text/javascript" src="js/jquery.validate.js"></script>
<link href="css/styles.css" rel="stylesheet" type="text/css" media="screen" />
<link href="css/demo_table.css" rel="stylesheet" type="text/css" media="screen" />

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
	
	
	$('#salasTable tbody tr').click(function()
	{
		if($('#dataToJoin').valid())
		{
			var tiradaID = $(this).attr('id');
			var pass =$('#contrasenia').val();
			$.get("php/createUser.php",{"idTirada" : tiradaID,"password": pass, "usuario" : $('#nameUsuario').val()},function(data){
				if(data.length > 10)
					alert(data);
				else
					window.location.replace("sala.php?idTirada="+tiradaID+"&usuario="+data+"&password="+encodeURI(pass));
			});
		}
	});

	alert('oucj');
	$('#salasTable').dataTable();
	alert('oucj');
	var tiradas = 0;
	function refresh(){
		$.getJSON('php/getTiradaS.php',function(data){
			if(tiradas == 0 || tiradas != data)
			{
				tiradas = data;
				$table = $('#salasTable tbody tr');
				$table.empty();		
				var	htmlToAdd;
				$.each(data,function(key,value)
				{
					htmlToAdd+= "<tr id='"+key+"'>";
					htmlToAdd+= "	<td>"+key+"</td><td>"+value.nombre+"</td><td>"+value.fecha+"</td><td>"+value.participantes+"</td><td>"+value.contrasenia+"</td>";
					htmlToAdd+= "</tr>";
				});
				$table.append(htmlToAdd);
			}
		});
	}//end refresh
	refresh();
	
	$('#dataToJoin').validate();
	
	//refreshcar cada 10 segundos:
	//var t = setInterval(function(){refresh();},10000);
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
                	/*UNCOMENT	require_once("php/data.php");
                    getFraseDia("");*/
                ?>
    </div>
	</div>
<div id="main">
	<div id="right">
<h4 id="titulo">Salas</h4>
    <div id='panel'>
		<div id="participantes">	
			<form action="" method="post" id="dataToJoin">
				<img src="img/user.png"/>Nombre de Usuario: <input type="text" size="15" id="nameUsuario" name="nameUsuario" class="required"/>
				<img src="img/llave.png"/>Contraseña: <input type="text" size="15" id="contrasenia" name="contrasenia" class=""/>
			</form>
		</div>
		<div id="salas">
			<form>
			<table cellpadding="0" cellspacing="0" border="0" class="display" id="salasTable">
				<thead>
				  <tr>
					<th>ID</th>
					<th>Nombre</th>
					<th>Fecha</th>
					<th>Participantes</th>
					<th>¿Contraseña?</th>
				  </tr>
				</thead>
				<tbody>	
				</tbody>
			</table>
		</div>
	</div>
      
	<dl class="faqs">
        <dt>¿Para que vale esta página?</dt>
        <dd>La principal idea de esta página es ayudarte a decidir elecciones de forma aleatoria. La página include diferente tipos de modalidades según qué quieres echar a suerte.</dd>
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
<g:plusone></g:plusone><br /><img src="img/logo.png" alt="" width="1" height="1" />  </div> <h3>Publicidad</h3> <div style="display:block ;" class="comnews"><center>
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
<div style="text-align: center; font-size: 0.75em;"></div></body>
</html>
