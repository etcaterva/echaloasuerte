<?php
/******************************************************************************
 *	   BBBB	     AAA    RRRR    BBBB      AAA    ZZZZZZ  U     U  L           *
 *	   B   B	A	A	R	R   B   B	 A   A       ZZ  U     U  L           *
 *	   B   B   A	 A  R	R   B   B	A	  A	    ZZ   U     U  L           *
 *	   BBBB	   A	 A  RRRR    BBBB    A     A     Z    U     U  L           *
 *	   B   B   AAAAAAA  R  R    B   B   AAAAAAA    Z     U     U  L           *
 *     B    B  A     A  R   R   B    B  A     A   ZZ     U     U  L           *
 *     B    B  A     A  R    R  B    B  A     A  ZZ       U   U   L           *
 *     BBBBB   A     A  R    R  BBBBB   A     A  ZZZZZZ    UUU    LLLLLLL     *
 ******************************************************************************/

/**
 * Clase: Nodo
 * Descripción: Implementación de un Nodo Simplemente Enlazado para una Lista
 * Autor: Matías Montes
 * Versión: 1.0
 */


class Nodo{

/******************************************************************************/
/* Propiedades */
/*-------------*/

	var $siguiente; //una referencia al siguiente nodo
	var $dato; 		//el objeto o valor almacenado en el nodo

/******************************************************************************/
/* Interfase */
/*-----------*/

	/**
	 * Constructor del Nodo
	 * (mixed) $dato: El objeto/valor del Nodo
	 */
	function Nodo($dato = NULL){
		$this->dato = &$dato;
	}

	/**
	 * Setea la referencia al siguiente nodo de la Lista.
	 * (Nodo) &$nodo: El siguiente nodo.
	 */
	function setSiguiente(&$nodo){
		$this->siguiente = &$nodo;
	}

	/**
	 * Devuelve una referencia al siguiente noso.
	 */
	function &siguiente(){
		return $this->siguiente;
	}

	/**
	 * Devuelve el dato almacenado en el Nodo.
	 */
	function getDato(){
		return $this->dato;
	}

    /**
     * Coloca el dato indicado en el nodo.
     *
     * (mixed) $dato: Dato a colocar en el Nodo.
     */
    function setDato($dato){
    	$this->dato = $dato;
    }
}
?>