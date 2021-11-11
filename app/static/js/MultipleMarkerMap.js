const initialLat = -34.9187;												// latitud inicial
const initialLng = -57.956;													// longitud inicial
const mapLayerUrl = 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png';	// url de la capa del mapa

export class MultipleMarkerMap {

	/*
	* Definición de la clase que representará a un mapa con 
	* la capacidad de dibujar polígonos
 	*/

	constructor({selector, addSearch, addResetButton, initialCoordinates, enableMarker}) {

		/*
		* Constructor de la clase. Parámetros:
		* 
		* selector: es el selector donde se colocará el mapa
		* addSearch: booleano que indica si desea agregar un botón para realizar búsquedas por dirección
		* addResetButton: booleano que indica si se desea agregar un botón para resetear las coordenadas ingresadas en el mapa
		* initialCoordinates: es el conjunto de coordenadas inicial que se desea mostrar en el mapa
		* enableMarker: booleano que indica si se desea habilitar que el usuario pueda marcar puntos en el mapa
		* 
		* Inicializa el mapa a partir del selector y marcador inicial recibido por parámetro
		* 
		* Si enableMarker es verdadero, se agrega un manejador al evento clcick para que el usuario pueda ingresar nuevos puntos en el mapa
		*/
		
		this.initializeMap(selector, initialCoordinates);
		
		if (addSearch) {
			this.addSearchControl();
		}

		if (addResetButton) {
			this.addResetCoordinatesButton()
		}
		
		if (enableMarker) {
			this.map.addEventListener('click', (e) => { this.addMarker(e.latlng) });
		}

	}
	
	initializeMap(selector, initialCoordinates) {

		/*
		* Método que inicializa el mapa
		* 
		* Renderiza el mapa en el selector indicado, y en caso de que exista un conjunto de coordenadas
		* inicial, dibujará el polígono correspondiente
		*/

		this.map = L.map(selector).setView([initialLat, initialLng], 13);
		L.tileLayer(mapLayerUrl).addTo(this.map);
		this.map.polylines = L.layerGroup().addTo(this.map);
		this.map.coordinates = []

		for (var coordinate of initialCoordinates) {
			this.addMarker({lat : coordinate[0], lng : coordinate[1]})
		}
		
	}
	
	addMarker({lat, lng}) {

		/*
		* Método para agregar un marcador al mapa
		*/

		this.map.coordinates.push([lat, lng]);
		L.polyline(this.map.coordinates).addTo(this.map.polylines);

		if (this.map.coordinates.length == 1) {		// si es el primer punto agrega un marcador para tener una referencia
			L.marker([lat, lng]).addTo(this.map.polylines);
		}

	}
	
	addSearchControl() {

		/*
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

	validRoute() {

		/*
		* Método que verifica que el mapa contenga al menos 3 puntos
		*/

		return this.map.coordinates.length >= 3;

	}

	addResetCoordinatesButton() {

		/*
		* Método para agregar al mapa un botón para borrar todas las coordenadas ingresadas
		*/

		L.easyButton('fa-undo', function(btn, mapa, ){
			if (confirm("¿Está seguro que desea borrar todas las coordenadas del recorrido de evacuación?")) {
				mapa.coordinates = []
				mapa.polylines.clearLayers()
			}	
		}).addTo( this.map );

	}
		
}