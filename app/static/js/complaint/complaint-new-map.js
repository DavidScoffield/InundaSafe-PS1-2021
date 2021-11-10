import { SingleMarkerMap } from '../SingleMarkerMap.js';

const submitHandler = (event, map) => {

	/**
	 * Función para manejar el evento cuando se quiere enviar el formulario
	 * 
	 * Si no se marcaron al menos dos puntos en el mapa, se solicita que se seleccionen
	 * 
	 * Si se marcaron al menos dos puntos, se envían las coordenadas de los mismos al servidor
 	*/
	
	if (map.coordinate.length == 0) {
		event.preventDefault();
		alert('Por favor, seleccione un punto en el mapa');
	} else {
		let coordinate = map.coordinate;
		coordinate = JSON.stringify(coordinate);
		document.getElementById("coordinate").value = coordinate;
	}
}

window.onload = () => {
	let coordinate = document.getElementById('coordinate').value

	if (coordinate) { 
		coordinate = JSON.parse(coordinate)
		
		//ESTA BIEN? Hago esto porque initializeMap() y addMarker() lo usan asi
		coordinate["lat"] = coordinate[0]
		coordinate["lng"] = coordinate[1]
	 } else { 
		coordinate = []
	}

	const map = new SingleMarkerMap ({
		selector: 'mapid',
		addSearch: true,
		initialMarker: coordinate,
		enableMarker: true
	});
	const form = document.getElementById('complaint_form');
	form.addEventListener('submit', (event) => submitHandler(event, map));
}