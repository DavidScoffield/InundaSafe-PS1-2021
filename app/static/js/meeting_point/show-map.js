import { SingleMarkerMap } from '../SingleMarkerMap.js';

window.onload = () => {

	let coordinate = document.getElementById('coordinate').value

	if (coordinate) { 
		coordinate = JSON.parse(coordinate).flat()
	 } else { 
		 coordinate = []
	}

	new SingleMarkerMap ({
		selector: 'mapid',
		addSearch: false,
		initialMarker: {
			lat: coordinate[0],
			lng: coordinate[1]
		},
		enableMarker: false
	});
}