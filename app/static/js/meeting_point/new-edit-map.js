import { SingleMarkerMap } from '../SingleMarkerMap.js';

const submitHandler = (event, map) => {

	/*
	* Función para manejar el evento cuando se quiere enviar el formulario
	* 
	* Si no se marcó ningún punto en el mapa, se solicita que se seleccione alguno
	* 
	* Si se marcó un punto, se envían las coordenadas del mismo al servidor
 	*/

	if (!map.validMap()) {
		event.preventDefault();
		alert('Por favor, seleccione una ubicación en el mapa');
	} else {
		let coordinate = map.marker.getLatLng();
		coordinate = JSON.stringify([[coordinate.lat, coordinate.lng]]);
		document.getElementById("coordinate").value = coordinate;
	}
}

window.onload = () => {

	let coordinates = document.getElementById('coordinate').value

	if (coordinates) { 
		coordinates = [ JSON.parse(coordinates).flat() ]
	 } else { 
		 coordinates = []
	}

	const map = new SingleMarkerMap ({
		selector: 'mapid',
		addSearch: true,
		initialCoordinates: coordinates,
		enableMarker: true
	});
	const form = document.getElementById('meeting_point_form');
	form.addEventListener('submit', (event) => submitHandler(event, map));
	
}