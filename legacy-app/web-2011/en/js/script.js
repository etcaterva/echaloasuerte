/**Script para las funciones de echaloasuerte**/
function rand(inferior,superior){
    numPosibilidades = superior - inferior;
    aleat = Math.random() * numPosibilidades;
    aleat = Math.round(aleat);
    return parseInt(inferior) + aleat;
} 

function numAleatorio(num, from, to, repe){
	var lista = new Array();
	var i;
	for(i=0;i< num; i++)
	{
		var elem = rand(from,to);
		if(repe || $.inArray(elem, lista) == -1)
			lista[i] = elem;
		else
			i=i-1;
	}	
	return lista;
}

function eleccion(num, values, repe)
{
	var lista = new Array();
	var i;
	for(i=0;i< num; i++)
	{
		var elem = rand(0,values.length-1);
		if(repe || $.inArray(values[elem], lista) == -1)
			lista[i]=values[elem];
		else
			i=i-1;					
	}
	return lista;
}

function asociacion(from, to,repe)
{
	lista = new Array();
	res = new Array();
	for(i=0;i< from.length; i++)
	{
		elem = rand(0,to.length-1);
		if(repe ||$.inArray(elem, lista) == -1)
			{
				lista[i] = elem;
				res[i] = new Array();
				res[i][0] = from[i];
				res[i][1] = to[elem];
			}
		else
			i=i-1;					
	}
	return res;
}

function compare_objects(obj1, obj2){
 
    var parameter_name;
 
    var compare = function(objA, objB, param){
 
        var param_objA = objA[param],
            param_objB = (typeof objB[param] === "undefined") ? false : objB[param];
 
        switch(typeof objA[param]){
            case "object": return (compare_objects(param_objA, param_objB));
            case "function": return (param_objA.toString() === param_objB.toString());
            default: return (param_objA === param_objB);
        }
 
    };
 
    for(parameter_name in obj1){
        if(typeof obj2[parameter_name] === "undefined" || !compare(obj1, obj2, parameter_name)){
            return false;
        }
    }
 
    for(parameter_name in obj2){
        if(typeof obj1[parameter_name] === "undefined" || !compare(obj1, obj2, parameter_name)){
            return false;
        }        
    }
 
    return true;
 
};

function LinksExternos() {
	var Externo;
	var dominio = "pickforme.net";
	if (document.getElementsByTagName('a')) {
		for (var i = 0; (Externo = document.getElementsByTagName('a')[i]); i++) {
			if (Externo.href.indexOf(dominio) == -1) {
				Externo.setAttribute('target', '_blank');
			}
		}
	}
}