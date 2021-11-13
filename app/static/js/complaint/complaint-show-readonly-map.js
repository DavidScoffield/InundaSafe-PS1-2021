import { SingleMarkerMap } from '../SingleMarkerMap.js';

window.onload = () => {
	let coordinate_lat = document.getElementById('coordinate_lat').value
    let coordinate_lng = document.getElementById('coordinate_lng').value

    let coordinate = []

    coordinate_lat = JSON.parse(coordinate_lat)
    coordinate_lng = JSON.parse(coordinate_lng)

	const map = new SingleMarkerMap ({
		selector: 'mapid',
		addSearch: true,
		initialCoordinates: [[coordinate_lat, coordinate_lng]],
		enableMarker: false
	});

}