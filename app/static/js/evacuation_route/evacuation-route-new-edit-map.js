import { MultipleMarkerMap } from '../MultipleMarkerMap.js';

const submitHandler = (event, map) => {

	/**
	 * Función para manejar el evento cuando se quiere enviar el formulario
	 * 
	 * Si no se marcaron al menos dos puntos en el mapa, se solicita que se seleccionen
	 * 
	 * Si se marcaron al menos dos puntos, se envían las coordenadas de los mismos al servidor
 	*/
	
	if (!map.validRoute()) {
		event.preventDefault();
		alert('Por favor, seleccione al menos dos puntos en el mapa');
	} else {
		let coordinates = map.coordinates;
		coordinates = JSON.stringify(coordinates);
		document.getElementById("coordinates").value = coordinates;
	}
}

window.onload = () => {

	let coordinates = document.getElementById('coordinates').value

	if (coordinates) { 
		coordinates = JSON.parse(coordinates)
	 } else { 
		 coordinates = []
	}

	const map = new MultipleMarkerMap ({
		selector: 'mapid',
		addSearch: true,
		initialMarker: coordinates,
		enableMarker: true
	});
	const form = document.getElementById('evacuation_route_form');
	form.addEventListener('submit', (event) => submitHandler(event, map));
}