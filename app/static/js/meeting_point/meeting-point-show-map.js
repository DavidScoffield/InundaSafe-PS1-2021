import { SingleMarkerMap } from '../SingleMarkerMap.js';

window.onload = () => {
	new SingleMarkerMap ({
		selector: 'mapid',
		addSearch: false,
		initialMarker: {
			lat: document.getElementById('coor_Y').innerHTML,
			lng: document.getElementById('coor_X').innerHTML
		},
		enableMarker: false
	});
}