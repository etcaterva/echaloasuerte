<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta name="title" content="PickForMe.net" />
<meta name="keywords" content="pickforme, random, chose, pickforme.net, lucky, heads or tail, mario corchero" />
<meta name="description" content="PickForMe.net, decide stuff randomly!!" />
<meta http-equiv="Content-Language" content="en" />
<meta http-equiv="content-type" content="text/html; charset=utf-8" />
<title>PickForMe</title>


<script type="text/javascript" src="js/jquery.js"></script>
<script type="text/javascript" src="js/script.js"></script>
<script type="text/javascript" src="js/jquery.validate.js"></script>
<link href="css/styles.css" rel="stylesheet" type="text/css" media="screen" />
<script> 
$(document).ready(function(){
	/** Variables de control **/
	var tipoEncuesta = 0;//tipo encuesta seleccionada
	var imagenTipoEncuesta = 0;//imagen selecciona(tipo)
	
	var tipoEncuestaUbicacion = 0;//tipo encuesta seleccionada [para multiple/individual]
	var imagenTipoEncuestaUbicacion = 0;//imagen selecciona(tipo)	[para multiple/individual]
	
	$('.menuContent').attr('opacity','50%');
	$('.menuContent').hide();
	
	/** Click en individual/multilpe **/
	$('#imgIndividual').click(
		function()
		{
		var auxx = tipoEncuestaUbicacion;
			if(tipoEncuestaUbicacion != 'individual')
			{
				if(tipoEncuestaUbicacion == 0)//al ser la primera tenemos que controlar esto
				{
					$(this).attr('src', $(this).attr('src').replace(/(\.\w{3,4}$)/,'_1$1'));
				}else
				{
					var str = imagenTipoEncuestaUbicacion.attr('src');
					imagenTipoEncuestaUbicacion.attr('src',str.substring(0, str.length-6)+'.png');	
					if(tipoEncuestaUbicacion == 'compartida')
						$('#compartida').hide(200,0);
					$('#menuTipo .actual').removeClass('actual');
				}
				imagenTipoEncuestaUbicacion = $(this);
				$(this).addClass('actual');				
				tipoEncuestaUbicacion='individual';
			}
		});
		
	$('#imgCompartida').click(
		function()
		{
			if(tipoEncuestaUbicacion != 'compartida')
			{
				$('html, body').animate({
					scrollTop: $('#right').offset().top + 'px'
				}, 'fast');

				
				var str = imagenTipoEncuestaUbicacion.attr('src');
				imagenTipoEncuestaUbicacion.attr('src',str.substring(0, str.length-6)+'.png');
				$('#compartida').show(200);
				$('#menuTipo .actual').removeClass('actual');
				imagenTipoEncuestaUbicacion = $(this);		
				$(this).addClass('actual');	
				tipoEncuestaUbicacion="compartida";
			}
		});		
	
	/** Click en los tipos de tirada **/
	$('#imgAleatorio').click(
		function()
		{
			if(tipoEncuesta == 0 || tipoEncuesta.attr('id') != 'aleatorio')
			{
				if(tipoEncuesta == 0)//al ser la primera tenemos que controlar esto
				{
					$('#aleatorio').show();
					$(this).attr('src', $(this).attr('src').replace(/(\.\w{3,4}$)/,'_1$1'));
				}else
				{
					var aux = tipoEncuesta;
					var str = imagenTipoEncuesta.attr('src');
					imagenTipoEncuesta.attr('src',str.substring(0, str.length-6)+'.png');					
					aux.fadeTo(200,0.1, function()
					{
						$('#aleatorio').fadeTo(200,1);
						aux.hide();
					});
					$('#menuTirada .actual').removeClass('actual');
				}
				imagenTipoEncuesta = $(this);
				tipoEncuesta=$('#aleatorio');
				$(this).addClass('actual');
			}
		});
		
	$('#imgEleccion').click(
		function()
		{
			if(tipoEncuesta.attr('id') != 'eleccion')
			{
				var aux = tipoEncuesta;	
				var str = imagenTipoEncuesta.attr('src');
				imagenTipoEncuesta.attr('src',str.substring(0, str.length-6)+'.png');
				aux.fadeTo(200,0.1, function()
				{
					$('#eleccion').fadeTo(200,1);
					aux.hide();
				});
				$('#menuTirada .actual').removeClass('actual');
				imagenTipoEncuesta = $(this);		
				$(this).addClass('actual');	
				tipoEncuesta=$('#eleccion');				
			}
		});	

	$('#imgAsociacion').click(
		function()
		{
			if(tipoEncuesta.attr('id') != 'asociacion')
			{
				var aux = tipoEncuesta;	
				var str = imagenTipoEncuesta.attr('src');
				imagenTipoEncuesta.attr('src',str.substring(0, str.length-6)+'.png');
				aux.fadeTo(200,0.1, function()
				{
					$('#asociacion').fadeTo(200,1);
					aux.hide();
				});
				$('#menuTirada .actual').removeClass('actual');
				imagenTipoEncuesta = $(this);		
				$(this).addClass('actual');	
				tipoEncuesta=$('#asociacion');				
			}
		});			
	
	/** Raton sobre una imagen **/
	$('#panel #menuTipo img, #panel #menuTirada img').each(function(){
		var imgFile= $(this).attr('src');
		var imgExt = /(\.\w{3,4}$)/;
		var preloadImage = new Image();
		preloadImage.src = imgFile.replace(imgExt,'_1$1');
		
		$(this).hover(
			function()
			{
				if(!$(this).hasClass('actual'))
					$(this).attr('src',preloadImage.src);
			},
			function()
			{
				if(!$(this).hasClass('actual'))
					$(this).attr('src',imgFile);
			});
	});	
	
	//esto tiene que ir despues de hover
	$('#imgAleatorio').click();
	$('#imgIndividual').click();
	
	/**click sobre añadir en formulario**/
	$('#addBut').click(function()
	{
		$(this).before('<input type="text" size="20" name="EleccionValues[]" class="EleccionValues hidden"/>');
		$('#panel .hidden').show('slow').removeClass('hidden');
	});
	$('#elecAddBut1').click(function()
	{
		$(this).before('<input type="text" size="20" name="SeleccionValues1[]" class="SeleccionValues1 hidden"/>');
		$('#panel .hidden').show('slow').removeClass('hidden');		
	});	
	$('#elecAddBut2').click(function()
	{
		$(this).before('<input type="text" size="20" name="SeleccionValues2[]" class="SeleccionValues2 hidden"/>');
		$('#panel .hidden').show('slow').removeClass('hidden');		
	});		
	$('#correoAddBut2').click(function()
	{
		$(this).before('<input type="text" size="20" name="correo[]" class="correo hidden email"/>');
		$('#panel .hidden').show('slow').removeClass('hidden');		
	});			
	
	
	/**FAQS**/
	$('.faqs dd').hide(); // Hide all DDs inside .faqs
	$('.faqs dt').hover(function(){$(this).addClass('hover')},function(){$(this).removeClass('hover')}).click(function(){ // Add class "hover" on dt when hover
		$(this).next().slideToggle('normal'); // Toggle dd when the respective dt is clicked
	});
	
	/**Reaccion a los botones de los formularios**/
	
	
	$('#aleatorioBut').click(function(){
		if(!$('#formAleatorio').valid()) return false;
		if(tipoEncuestaUbicacion=="compartida" && !$('#formCompartida').valid()) return false;
		
		var res = numAleatorio($('#AleatorioNum').val(),$('#AleatorioFrom').val(),$('#AleatorioTo').val(),$('#AleatorioRepe').attr('checked'));	
		if(tipoEncuestaUbicacion!="compartida")
		{
			$('#aleatorio .resultados ul').hide('slow',function(){
				$(this).html('');
				for(var i=0;i<res.length;i++)
					$('#aleatorio .resultados ul').append('<li>'+res[i]+'</li>');
			});
			$('#aleatorio .resultados').show('slow');
			$('#aleatorio .resultados ul').show('slow');			
		}
		else{//serializar y enviar los formularios
			var dataCompartida = $('#formCompartida').serialize();
			var dataAleatorio = $('#formAleatorio').serialize();
			var dataToSend = dataCompartida + "&" + dataAleatorio + "&type=aleatorio";
			for(var i=0;i<res.length;i++)
				dataToSend += "&solutionItem%5B%5D=" + res[i];//%5B%5D para que sea un array
			$.post('php/create.php',dataToSend,function(returnedData)
			{
				window.location.replace("sala.php?idTirada="+returnedData.tirada+"&usuario="+returnedData.usuario+"&password="+encodeURI($('#contrasenia').val()));

			},"json");
		}
		return false;
	});
	
	$('#eleccionBut').click(function(){
		if(!$('#formEleccion').valid()) return false;
		if(tipoEncuestaUbicacion=="compartida" && !$('#formCompartida').valid()) return false;		
	
		var repeticiones = 1;
		var array = new Array();
		$('.EleccionValues').each(function(){
			if($.inArray($(this).val(), array) != -1)
			{
				$(this).val($(this).val()+'('+repeticiones+')');
				repeticiones = repeticiones+1;
			}		
			if($(this).val() != '')
				array[array.length] = $(this).val();
		});
		var res = eleccion($('#EleccionNum').val(),array,$('#EleccionRepe').attr('checked'));
		if(tipoEncuestaUbicacion!="compartida")
		{		
			$('#eleccion .resultados ul').hide('slow',function(){
				$(this).html('');
				for(var i=0;i<res.length;i++)
					$('#eleccion .resultados ul').append('<li>'+res[i]+'</li>');
			});
			$('#eleccion .resultados').show('slow');		
			$('#eleccion .resultados ul').show('slow');		
		}
		else{//serializar y enviar los formularios
			var dataCompartida = $('#formCompartida').serialize();
			var dataEleccion = $('#formEleccion').serialize();
			var dataToSend = dataCompartida + "&" + dataEleccion + "&type=eleccion";
			for(var i=0;i<res.length;i++)
				dataToSend += "&solutionItem%5B%5D=" + res[i];//%5B%5D para que sea un array
			$.post('php/create.php',dataToSend,function(returnedData)
			{
				window.location.replace("sala.php?idTirada="+returnedData.tirada+"&usuario="+returnedData.usuario+"&password="+encodeURI($('#contrasenia').val()));
			},"json");
		}
		return false;
	});	
	
	$('#asociacionBut').click(function(){
		if(!$('#formAsociacion').valid()) return false;	
		if(tipoEncuestaUbicacion=="compartida" && !$('#formCompartida').valid()) return false;		
	
		var arrayFrom = new Array();
		var arrayTo = new Array();
		var repeticiones = 1;
		$('.SeleccionValues1').each(function(){
			if($.inArray($(this).val(), arrayFrom) != -1)
			{
				$(this).val($(this).val()+'('+repeticiones+')');
				repeticiones = repeticiones+1;
			}
			if($(this).val() != '')
				arrayFrom[arrayFrom.length] = $(this).val();
		});
		$('.SeleccionValues2').each(function(){
				arrayTo[arrayTo.length] = $(this).val();
		});	
		if($('#AsociacionRepe').attr('checked') != 'checked' && arrayFrom.length > arrayTo.length) $('#AsociacionRepe').attr('checked','checked');
		var res = asociacion(arrayFrom,arrayTo,$('#AsociacionRepe').attr('checked'));
		if(tipoEncuestaUbicacion!="compartida")
		{				
			$('#asociacion .resultados table').hide('slow',function(){
				$(this).html('');
				var vineta = "<td><img class='auto' src='img/vineta.png'></td>";
				var flecha = "<td><img class='auto' src='img/vinetaFlecha.png'></td>";
				for(var i=0;i<res.length;i++)
				{
					var linea = '<tr>'+vineta+'<td>' + res[i][0]+'</td>'+flecha+'<td>' + res[i][1]+'</td></tr>';
					$('#asociacion .resultados table').append(linea);
				}
			});
			$('#asociacion .resultados').show('slow');
			$('#asociacion .resultados table').show('slow');
		}
		else{//serializar y enviar los formularios
			var dataCompartida = $('#formCompartida').serialize();
			var dataAsociacion = $('#formAsociacion').serialize();
			var dataToSend = dataCompartida + "&" + dataAsociacion + "&type=asociacion";
			for(var i=0;i<res.length;i++)
				dataToSend += "&solutionItem%5B%5D=" + res[i][0] + "][" + res[i][1];//%5B%5D para que sea un array ( ][ es el separador)
			$.post('php/create.php',dataToSend,function(returnedData)
			{
				window.location.replace("sala.php?idTirada="+returnedData.tirada+"&usuario="+returnedData.usuario+"&password="+encodeURI($('#contrasenia').val()));
			},"json");
		}			
		return false;
	});		
	
	
	/** Cara o cruz**/
	$('#CaraOCruz').click(function(){
		if(Math.random() < .5) alert('Head');
		else alert('Tail');
	});
	
	/** Validations **/
	jQuery.validator.addMethod("ToGreaterThanFrom", function(value, element, param) {
		if($('#AleatorioRepe').attr('checked'))
			return parseInt(value) > parseInt($('#AleatorioFrom').val());
		else
			return parseInt(value) - parseInt($('#AleatorioFrom').val()) > parseInt($('#AleatorioNum').val());
	}, "You should specify a wider range");
	
	$('#formAleatorio').validate({
		rules:{
			AleatorioTo: {ToGreaterThanFrom : true}
		}
	});

	jQuery.validator.addMethod("NumOfFields", function(value, element, param) {
		if($('#EleccionRepe').attr('checked') != 'checked')
			return parseInt(value) <= $('.EleccionValues').length;
		else return true;
	}, "Not enaugh values.");
	
	$('#formEleccion').validate({
		rules:{
			EleccionNum: {NumOfFields : true}
		}
	});
	
	jQuery.validator.addMethod("AsociacionFields", function(value, element, param) {
		if($('#AsociacionRepe').attr('checked') != 'checked')
			return $('.SeleccionValues1').length <= $('.SeleccionValues2').length;
		else return true;
	}, "Not enaugh values on the first set.");	
	
	$('#formAsociacion').validate({
		rules:{
			repe: {AsociacionFields : true}
		}
	});	
	
	$('#formCompartida').validate();		
	
	//eventos submit(por si se pulsa intro en lugar del boton
	$('#formAsociacion').submit(function(){$('#asociacionBut').click();return false;});
	$('#formAleatorio').submit(function(){$('#aleatorioBut').click();return false;});
	$('#formEleccion').submit(function(){$('#eleccionBut').click();return false;});	
	$('#formCompartida').submit(function(){
		if(tipoEncuesta.attr('id') == 'aleatorio') $('#aleatorioBut').click();
		else if(tipoEncuesta.attr('id') == 'eleccion') $('#eleccionBut').click();
		else if(tipoEncuesta.attr('id') == 'asociacion') $('#asociacionBut').click();
		return false;
	});
	$('#compartidaBut').click(function(){$('#formCompartida').submit();return false;});
	
	LinksExternos();
});

</script>

<body>
<a href="http://www.echaloasuerte.com">
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
<h4>Home</h4>
    <div id='panel'>
		<div id='menuTipo'>
			<img id="imgIndividual" src="img/buttonIndividual.png" alt="Tirada Individual"  />   
			<img id="imgCompartida" src="img/buttonCompartida.png" alt="Tirada Compartida"  />
		</div>
		
		<div id='menuTirada'>
			<img id="imgAleatorio" src="img/buttonAleatorio.png" alt="Numero aleatorio"/>
			<img id="imgEleccion" src="img/buttonEleccion.png" alt="Elegir entre valores"/>
			<img id="imgAsociacion" src="img/buttonAsociacion.png" alt="Asociar valores" />
		</div>
		
		<div class="menuContent" id="aleatorio">
			<form action="" method="post" id="formAleatorio">
						  Get 
							<input type="text" size="3" value="1" name="AleatorioNum" class="digits required" id="AleatorioNum" />
						  numbers(s) from 
						  <input type="text" size="10" value="0" name="AleatorioFrom" class="digits required" id="AleatorioFrom"/> 
						  to 
						  <input type="text" size="10" value="10" name="AleatorioTo" class="digits required" id="AleatorioTo"/>
							<br/><input type="checkbox" name="AleatorioRepe" id="AleatorioRepe"/>
			Numbers can be repeated
			<br/><input type="submit" value="EchaloAsuerte" id="aleatorioBut" class="button"/>
					   </form>			
			<div class="resultados">
				<h4>Results</h4>
				<ul>
					<!-- Sera rellenado con los resultados -->
				</ul>
			</div>
		</div>
		
		<div class="menuContent" id="eleccion">
			<form action="" method="post" id="formEleccion">
				Chooose 
			  <input type="text" size="5" value="1" name="EleccionNum" class="required digits" id="EleccionNum"/> 
			  of the following values: <br/>
			  <input type="text" size="20" name="EleccionValues[]" class="EleccionValues"/>
			  <input type="text" size="20" name="EleccionValues[]" class="EleccionValues"/>
			  <img id="addBut" src="img/add.png" class="add"/>
				<br/><br/><input type="checkbox" id="EleccionRepe" name="EleccionRepe"/>
				Values can be repeated
				<br/><input type="submit" value="EchaloASuerte" id="eleccionBut"/>
					   </form>	
			<div class="resultados">
				<h4>Results</h4>
				<ul>
					<!-- Sera rellenado con los resultados -->
				</ul>
			</div>					   
		</div>	
		<div class="menuContent" id="asociacion">

			<form action="" method="post" id="formAsociacion">
			Link<br/>
			  <input type="text" size="20" name="SeleccionValues1[]" class="SeleccionValues1"/>
			  <input type="text" size="20" name="SeleccionValues1[]" class="SeleccionValues1"/>
			  <img id="elecAddBut1" src="img/add.png" class="add"/>
				<br/>with<br/>
			  <input type="text" size="20" name="SeleccionValues2[]" class="SeleccionValues2"/>
			  <input type="text" size="20" name="SeleccionValues2[]" class="SeleccionValues2"/>
			  <img id="elecAddBut2" src="img/add.png" class="add"/>
				<br/><input type="checkbox" id="AsociacionRepe" name="AsociacionRepe"/> 
				Values on the second set can be repeated.
				<br/><input type="submit" value="EchaloASuerte" id="asociacionBut" />
			</form>
			<div class="resultados">
				<h4>Results</h4>
				<TABLE border="0">
					<!-- Sera rellenado con los resultados -->
				</table>
			</div>		
		</div>

		<div class="menuContent menuDatosMultiplicidad" id="compartida"> 
			<form action="" method="post" id="formCompartida">
				Number of participants (you included):
				<input type="text" size="7" id="numParticipantes" name="numParticipantes" class="required digits"/>
				<br/>Your name:
				<input type="text" size="20" id="nombreUsuario" name="nombreUsuario" class="required"/>				
				<br/>Room name(optional):
				<input type="text" size="20" id="nombre" name="nombre"/>								
				<br/>Room password(optional):
				<input type="text" size="20" id="contrasenia" name="contrasenia"/>
				<br/>EMail adresses (optional):
				<br/><input type="text" size="20" name="correo[]" class="correo email"/>
				<img id="correoAddBut2" src="img/add.png" class="add"/>
				<br/><input type="submit" value="Crear" id="compartidaBut" />
			</form>
		</div>
	</div>
      
	<dl class="faqs">
        <dt>What is this page for?</dt>
        <dd>The aim of the page is to help you to make random decisions. The page includes different ways to do it that can be helpful.</dd>
        <dt>What kind of decisions the page offers?</dt>
        <dd>You can ask for a set of numbers(to play the lottery), choose between some values(choose the color of your suit) or relate values (distribute the rooms of a house).</dd>
        <dt>Randon Numbers</dt>
        <dd>First button of the left.<br/>This kind of 'roll' it for a number of random numbers. You can choose the number of values ​​to obtain, the range of numbers generated (from and to, inclusive) and if you want that the numbers can be repeated. <br/>This type of roll can be used to get a random number or take lottery.</dd>
        <dt>Value Election</dt>
        <dd>Second at the left.<br/>Gets one or more values ​​between those listed, you can determine the number of values ​​to choose and whether to allow repeated. You must also indicate the set of values ​​from which to choose. The number of values ​​to choose must be equal to or greater than the number of values ​​to choose from. 
			<br/>This type of shot is often used to choose a color, figure out who throws the trash, going today to bar, etc ...</dd>
        <dt>Value Linking</dt>
        <dd>Third on the left.<br/>This type of 'lying' is used to relate two sets of values. You must enter values ​​for the two sets, you should also indicate whether you want a first set value can be related to several of the latter. If you do not allow duplicate values, the first set must be greater than or equal to the second. 
		<br/>Use this type of roll to make groups, spread the floor cleaning, rooms, etc ...</dd>		
		<dt>Indivial</dt>
        <dd>First button at the top. Use this type of roll to get the result on this computer only.</dd>
		<dt>Distributed</dt>
        <dd>Second on the top. Second top menu. Use this spread to take something to luck with people who are not using this computer. In this way, you will create a room you will join the rest and all will see the result at once. You must indicate the number of participants, your name appear in the room, a name and password for the room if you wish and e-mail to be sent a link to enter the room.</dd>		
		<dt>How can my friends join to the room?</dt>
        <dd>Once you've created a room, your friends can look for it on the tab "Rooms", remember that if you have entered a password, you should provide it.</dd>				
    </dl>
      
    <?php
	//uncoment	botonAyuda("En esta pagina debes pulsar uno de los 2 botones.<br />El primero sirve para echar a suerte algo cuando TODOS los participantes se encuentran delante de esta pantalla.<br />El segundo boton se usa para echar a suerte algo que necesite la participacion de almenos 2 personas que no estan en el mismo lugar. Es decir, uno puede estar en Caceres y otro en Madrid.<br />");    
    ?>
	</div>

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
