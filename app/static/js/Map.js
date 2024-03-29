const initialLat = -34.9187;												// latitud inicial
const initialLng = -57.956;													// longitud inicial
const mapLayerUrl = 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png';	// url de la capa del mapa

export class Map {

	/*
	* Definición de la clase que representará a un mapa
 	*/

	constructor({selector, addSearch, initialCoordinates, enableMarker}) {

		/*
		* Constructor de la clase. Parámetros:
		* 
		* selector: es el selector donde se colocará el mapa
		* addSearch: booleano que indica si desea agregar un botón para realizar búsquedas por dirección
		* initialMarker: es el conjunto de coordenadas inicial que se desea mostrar en el mapa
		* enableMarker: booleano que indica si se desea habilitar que el usuario pueda marcar un punto en el mapa
		* 
		* Inicializa el mapa a partir del selector y marcador inicial recibido por parámetro
		* 
		* Si enableMarker es verdadero, se agrega un manejador al evento clcick para agregar puntos en el mapa
		*/

		this.initializeMap(selector, initialCoordinates);

		if (addSearch) {
			this.addSearchControl();
		}
		
		if (enableMarker) {
			this.map.addEventListener('click', (e) => { this.addMarker(e.latlng) });
		}

	}
	
	initializeMap(selector, initialCoordinates) {

		/**
		 * Método que inicializa el mapa
		 * 
		 * Renderiza el mapa en el selector indicado, y en caso de que exista un marcador inicial, lo colocará en el mapa
		*/

		this.map = L.map(selector).setView([initialLat, initialLng], 13);
		L.tileLayer(mapLayerUrl).addTo(this.map);
		this.map.polylines = L.layerGroup().addTo(this.map);
		this.map.coordinates = []


		for (var coordinate of initialCoordinates) {
			this.addMarker({lat : coordinate[0], lng : coordinate[1]})
		}

	}
	
	addSearchControl() {

		/**
		 * Método para agregar la opción de buscar una dirección en el mapa
		*/

		L.control.scale().addTo(this.map);
		let searchControl = new L.esri.Controls.Geosearch().addTo(this.map);
		
		let results = new L.LayerGroup().addTo(this.map);
		
		searchControl.on('results', (data) => {
			results.clearLayers();
			
			if (data.results.Length > 0) {
				this.addMarker(data, results[0].lating);
			}
		});
	}	
}