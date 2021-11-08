const initialLat = -34.9187 // latitud inicial
const initialLng = -57.956 // longitud inicial
const mapLayerUrl = 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png' // url de la capa del mapa

export class ZoneMap {
  #drawnItems
  /**
   * Definición de la clase que representará a un mapa con
   * la capacidad de mostrar y marcar una zona inundable
   */

  constructor({ selector }) {
    /**
     * Constructor de la clase. Parámetros:
     *
     * selector: es el selector donde se colocará el mapa
     * addSearch: booleano que indica si desea agregar un botón para realizar búsquedas por dirección
     * initialMarker: es el conjunto de coordenadas inicial que se desea mostrar en el mapa
     * enableMarker: booleano que indica si se desea habilitar que el usuario pueda marcar un punto en el mapa
     *
     * Inicializa el mapa a partir del selector y marcador inicial recibido por parámetro
     *
     * Si enableMarker es verdadero, se agrega un manejador al evento clcick para agregar el punto en el mapa
     */

    this.#drawnItems = new L.FeatureGroup()

    this.#initializeMap(selector)

    this.map.on(L.Draw.Event.CREATED, (e) => {
      this.#eventHandler(e, this.map, this.#drawnItems, this.editControls, this.createControls)
    })

    this.map.on('draw:deleted', () => {
      this.#deleteHandler(this.map, this.editControls, this.createControls)
    })
  }

  #initializeMap(selector) {
    /**
     * Método que inicializa el mapa
     *
     * Renderiza el mapa en el selector indicado, y en caso de que exista un marcador inicial, lo colocará en el mapa
     */

    this.map = L.map(selector).setView([initialLat, initialLng], 13)
    L.tileLayer(mapLayerUrl).addTo(this.map)

    this.map.addLayer(this.#drawnItems)

    this.map.addControl(this.createControls)
  }

  #eventHandler(e, map, drawnItems, editControls, createControls) {
    const exisitingZones = Object.values(drawnItems._layers)

    if (exisitingZones.length == 0) {
      const { layerType, layer } = e

      if (layerType == 'marker') {
      }

      layer.editing.enable()
      drawnItems.addLayer(layer)
      editControls.addTo(map)
      createControls.remove()
    }
  }

  #deleteHandler() {
    createControls.addTo(map)
    editControls.remove()
  }

  hasValidZone() {
    return this.drawnLayers.length === 1
  }

  get drawnLayers() {
    return Object.values(this.#drawnItems._layers)
  }

  get editControls() {
    return (this.createControlsToolbar ||= new L.Control.Draw({
      draw: false,
      edit: {
        featureGroup: this.#drawnItems,
      },
    }))
  }

  get createControls() {
    return (this.createControlsToolbar ||= new L.Control.Draw({
      draw: {
        circle: false,
        marker: false,
        polyline: false,
      },
    }))
  }
}
