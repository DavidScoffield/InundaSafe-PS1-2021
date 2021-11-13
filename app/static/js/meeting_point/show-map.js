import { SingleMarkerMap } from '../SingleMarkerMap.js';

window.onload = () => {

	let coordinates = document.getElementById('coordinate').value

	if (coordinates) { 
		coordinates = JSON.parse(coordinates)
	 } else { 
		 coordinates = []
	}

	new SingleMarkerMap ({
		selector: 'mapid',
		addSearch: false,
		initialCoordinates: [coordinates],
		enableMarker: false
	});
}