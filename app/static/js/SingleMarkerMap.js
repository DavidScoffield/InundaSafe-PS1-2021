import { Map } from './Map.js';

export class SingleMarkerMap extends Map {

	/**
	 * Definición de la clase que representará a un mapa con 
	 * la capacidad de mostrar y marcar un solo punto
 	*/
	
	addMarker({lat, lng}) {

		/*
		* Método para agregar un marcador al mapa
		* 
		* Si ya había un marcador colocado en el mapa, lo elimina y coloca uno nuevo a partir de la
		* latitud y longitud recibida por parámetro
		*/

		if (this.marker) {
			this.marker.remove()
		}

		this.map.coordinates = [lat, lng];
		this.marker = L.marker([lat, lng]).addTo(this.map);

	}

	validMap() {

		/*
		* Método que verifica que el mapa contenga 1 punto
		*/

		return this.marker
		
	}
	
}