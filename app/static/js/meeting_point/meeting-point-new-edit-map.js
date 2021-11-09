import { SingleMarkerMap } from '../SingleMarkerMap.js';

const submitHandler = (event, map) => {

	/**
	 * Función para manejar el evento cuando se quiere enviar el formulario
	 * 
	 * Si no se marcó ningún punto en el mapa, se solicita que se seleccione alguno
	 * 
	 * Si se marcó un punto, se setean las coordenadas del mismo en los inputs del formulario
 	*/

	if (!map.marker) {
		event.preventDefault();
		alert('Por favor, seleccione una ubicación en el mapa');
	} else {
		let latlng = map.marker.getLatLng();
		document.getElementById('coor_Y').setAttribute('value', latlng.lat);
		document.getElementById('coor_X').setAttribute('value', latlng.lng);
	}
}

window.onload = () => {
	const map = new SingleMarkerMap ({
		selector: 'mapid',
		addSearch: true,
		initialMarker: {
			lat: document.getElementById('coor_Y').value,
			lng: document.getElementById('coor_X').value
		},
		enableMarker: true
	});
	const form = document.getElementById('meeting_point_form');
	form.addEventListener('submit', (event) => submitHandler(event, map));
}