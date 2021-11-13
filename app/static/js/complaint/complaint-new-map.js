import { SingleMarkerMap } from '../SingleMarkerMap.js';

const submitHandler = (event, map) => {

	/**
	 * Función para manejar el evento cuando se quiere enviar el formulario
	 * 
	 * Si no se marcaron al menos dos puntos en el mapa, se solicita que se seleccionen
	 * 
	 * Si se marcaron al menos dos puntos, se envían las coordenadas de los mismos al servidor
 	*/
	
	if (!map.validMap()) {
		event.preventDefault();
		alert('Por favor, seleccione un punto en el mapa');
	} else {
		let coordinate = map.marker.getLatLng();
		coordinate = JSON.stringify([coordinate.lat, coordinate.lng]);
		document.getElementById("coordinate").value = coordinate;
	}
}

window.onload = () => {
	let coordinates = document.getElementById('coordinate').value

	if (coordinates) { 
		coordinates = [ JSON.parse(coordinates) ]
	 } else { 
		coordinates = []
	}

	const map = new SingleMarkerMap ({
		selector: 'mapid',
		addSearch: true,
		initialCoordinates: coordinates,
		enableMarker: true
	});
	const form = document.getElementById('complaint_form');
	form.addEventListener('submit', (event) => submitHandler(event, map));
}