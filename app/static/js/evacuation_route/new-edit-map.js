import { MultipleMarkerMap } from '../MultipleMarkerMap.js';

const submitHandler = (event, multipleMarkerMap) => {

	/*
	* Función para manejar el evento cuando se quiere enviar el formulario
	* 
	* Si no se marcaron al menos tres puntos en el mapa, se solicita que se seleccionen
	* 
	* Si se marcaron al menos tres puntos, se envían las coordenadas de los mismos al servidor
 	*/
	
	if (!multipleMarkerMap.validRoute()) {
		event.preventDefault();
		alert('Por favor, seleccione al menos tres puntos en el mapa');
	} else {
		let coordinates = multipleMarkerMap.map.coordinates;
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
		addResetButton: true,
		initialCoordinates: coordinates,
		enableMarker: true
	});
	const form = document.getElementById('evacuation_route_form');
	form.addEventListener('submit', (event) => submitHandler(event, map));
}