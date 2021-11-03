import { MultipleMarkerMap } from '../MultipleMarkerMap.js';

window.onload = () => {

	let coordinates = document.getElementById('coordinates').value

	if (coordinates) { 
		coordinates = JSON.parse(coordinates)
	 } else { 
		 coordinates = []
	}

	new MultipleMarkerMap ({
		selector: 'mapid',
		addSearch: false,
		initialMarker: coordinates,
		enableMarker: false
	});
	
}