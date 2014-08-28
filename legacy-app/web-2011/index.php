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
		if(Math.random() < .5) alert('Cara');
		else alert('Cruz');
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
<a href="http://www.pickforme.net/index.php">
<img src="img/eng.png" class="language" style="position:absolute;top:15px;right:15px;" title="English"/>
</a>
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
<h4>Inicio</h4>
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
						  Dame 
							<input type="text" size="3" value="1" name="AleatorioNum" class="digits required" id="AleatorioNum" />
						  numeros(s) desde 
						  <input type="text" size="10" value="0" name="AleatorioFrom" class="digits required" id="AleatorioFrom"/> 
						  hasta 
						  <input type="text" size="10" value="10" name="AleatorioTo" class="digits required" id="AleatorioTo"/>
							<br/><input type="checkbox" name="AleatorioRepe" id="AleatorioRepe"/>
			Los numeros pueden repetirse
			<br/><input type="submit" value="EchaloAsuerte" id="aleatorioBut" class="button"/>
					   </form>			
			<div class="resultados">
				<h4>Resultado</h4>
				<ul>
					<!-- Sera rellenado con los resultados -->
				</ul>
			</div>
		</div>
		
		<div class="menuContent" id="eleccion">
			<form action="" method="post" id="formEleccion">
				Elige 
			  <input type="text" size="5" value="1" name="EleccionNum" class="required digits" id="EleccionNum"/> 
			  uno de los siguientes valores: <br/>
			  <input type="text" size="20" name="EleccionValues[]" class="EleccionValues"/>
			  <input type="text" size="20" name="EleccionValues[]" class="EleccionValues"/>
			  <img id="addBut" src="img/add.png" class="add"/>
				<br/><br/><input type="checkbox" id="EleccionRepe" name="EleccionRepe"/>
				Los valores pueden repetirse
				<br/><input type="submit" value="EchaloASuerte" id="eleccionBut"/>
					   </form>	
			<div class="resultados">
				<h4>Resultado</h4>
				<ul>
					<!-- Sera rellenado con los resultados -->
				</ul>
			</div>					   
		</div>	
		<div class="menuContent" id="asociacion">

			<form action="" method="post" id="formAsociacion">
			Relaciona<br/>
			  <input type="text" size="20" name="SeleccionValues1[]" class="SeleccionValues1"/>
			  <input type="text" size="20" name="SeleccionValues1[]" class="SeleccionValues1"/>
			  <img id="elecAddBut1" src="img/add.png" class="add"/>
				<br/>con<br/>
			  <input type="text" size="20" name="SeleccionValues2[]" class="SeleccionValues2"/>
			  <input type="text" size="20" name="SeleccionValues2[]" class="SeleccionValues2"/>
			  <img id="elecAddBut2" src="img/add.png" class="add"/>
				<br/><input type="checkbox" id="AsociacionRepe" name="AsociacionRepe"/> 
				Los valores del segundo conjunto pueden repetirse.
				<br/><input type="submit" value="EchaloASuerte" id="asociacionBut" />
			</form>
			<div class="resultados">
				<h4>Resultado</h4>
				<TABLE border="0">
					<!-- Sera rellenado con los resultados -->
				</table>
			</div>		
		</div>

		<div class="menuContent menuDatosMultiplicidad" id="compartida"> 
			<form action="" method="post" id="formCompartida">
				Numero de participantes (tú incluido):
				<input type="text" size="7" id="numParticipantes" name="numParticipantes" class="required digits"/>
				<br/>Tu nombre:
				<input type="text" size="20" id="nombreUsuario" name="nombreUsuario" class="required"/>				
				<br/>Nombre de la sala(opcional):
				<input type="text" size="20" id="nombre" name="nombre"/>								
				<br/>Contraseña de la sala(opcional):
				<input type="text" size="20" id="contrasenia" name="contrasenia"/>
				<br/>Direcciones de correos:  (opcional):
				<br/><input type="text" size="20" name="correo[]" class="correo email"/>
				<img id="correoAddBut2" src="img/add.png" class="add"/>
				<br/><input type="submit" value="Crear" id="compartidaBut" />
			</form>
		</div>
	</div>
      
	<dl class="faqs">
        <dt>¿Para que sirve esta pagina?</dt>
        <dd>Esta página te permite realizar decisiones de una forma aleatoria. La pagina ofrece diferentes formas que se adaptan a diferentes necesidades.</dd>
        <dt>¿Que tipo de decisiones?</dt>
        <dd>Puede pedir una serie de numero aleatorios (para echar la loteria, elegir entre una serie de valores (el color de tu traje o el nombre de tu futuro perro) o relacionar dos conjuntos de valores (repartir habitaciones, tareas de limpieza...).</dd>
        <dt>Numeros Aleatorios</dt>
        <dd>Primera opcion a la izquierda.<br/>Este tipo de tirada devuelve una serie de numeros aleatorio dentro dentro de un rango, ambos numeros inclusives. Si deseas que los numeros se puedan repetir activa la casilla indicada para ello. <br/>Puedes utilizar este tipo para decidir un dia del mes para hacer algo o echar la loteria.</dd>
        <dt>Eleccion de valores</dt>
        <dd>Segunda a la izquierda.<br/>Obtiene uno o mas valores de un conjunto dado. Debes indicar si deseas que se puedan repetir los valores en la seleccion. Si no se pueden repetir los elementos, el numero de opciones debe ser mayor al el numero de elementos en el conjunto. 
			<br/>Utiliza esta opcion para elegir el color de tus zapatos, quien saca la basura o a quien le toca beber.</dd>
        <dt>Asociacion de Valores</dt>
        <dd>Último a la izquierda.<br/>Este tipo de tirada te permite asociar valores de dos conjuntos. Debes introducir los dos conjuntos a relacionar al igual que si deseas que los valores del segundo conjunto se puedan repetir. Si no se pueden repetir, el primer conjunto debe ser igual o mayor en numero de elementos al primero. 
		<br/>Utiliza este tipo para repartir las tareas de la casa, los cuartos de un piso, etc...</dd>		
		<dt>Individual</dt>
        <dd>Primer boton arriba. Usa esta tirada para ver los resultados en un solo ordenador.</dd>
		<dt>Distribuida/Multiple</dt>
        <dd>Secundo boton arriba del panel. Utiliza este tipo para que mas de una persona participe, debes indicar tu nombre, y el numero de participantes. Si lo deseas puede indicar tambien un nombre de la sala que vas a crear, asi como una contraseña y una lista de direciones de correo que recibiran un mail invitandoles a unirse.</dd>		
		<dt>¿Como se unen mis amigos?</dt>
        <dd>Una vez creada la sala deben dirigirse al apartado sala y buscar la sala que acabes de crear.</dd>				
    </dl>
      
    <?php
	//uncoment	botonAyuda("En esta pagina debes pulsar uno de los 2 botones.<br />El primero sirve para echar a suerte algo cuando TODOS los participantes se encuentran delante de esta pantalla.<br />El segundo boton se usa para echar a suerte algo que necesite la participacion de almenos 2 personas que no estan en el mismo lugar. Es decir, uno puede estar en Caceres y otro en Madrid.<br />");    
    ?>
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
        ¿Cara o Cruz?  Pincha en la moneda!
        </p>
		<a href="#" id="CaraOCruz"><img  name="imgMoneda" src="img/cruz.png" alt="Moneda" onmouseover="swaponMoneda()" onmouseout="swapoffMoneda()" title="Heads or Tails?" /></a>
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
        ¿Por qué no donar un par de euros a tu pagina favorita?.<a href="acerca.php">Click para más información.</a>
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
<p><abbrev>EchaloASuerte.com</abbrev> | | Un proyecto de <a href="http://www.etcaterva.com">EtCaterva</a></p>
</div>
</div>
</div>
<!-- footer ends-->
<div style="text-align: center; font-size: 0.75em;"></div></body>
</html>
