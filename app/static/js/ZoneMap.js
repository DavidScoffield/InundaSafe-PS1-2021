const initialLat = -34.9187 // latitud inicial
const initialLng = -57.956 // longitud inicial
const mapLayerUrl = 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png' // url de la capa del mapa

export class ZoneMap {
  #drawnItems
  #color
  /**
   * Definición de la clase que representará a un mapa con
   * la capacidad de mostrar y marcar una zona inundable
   */

  constructor({ selector, initialZone = null, color = null, enableControls = true }) {
    /**
     * Constructor de la clase. Parámetros:
     
     * selector: es el selector donde se colocará el mapa
     * initialZone: es el conjunto de coordenadas inicial para mostrar
     una zona inundable el mapa
     * enableControls: booleano que indica si se desea habilitar los controles en el mapa
     
     * Inicializa el mapa a partir del selector y initialZone en caso de recibirlo 
     por parámetros
     */
    this.#color = color || '#3388FF'
    this.#drawnItems = new L.FeatureGroup()

    this.#initializeMap(selector, initialZone, enableControls)

    if (enableControls) {
      this.map.on(L.Draw.Event.CREATED, (e) => {
        this.#eventHandler(e, this.map, this.#drawnItems, this.editControls, this.createControls)
      })
      this.map.on('draw:deleted', () => {
        this.#deleteHandler(this.map, this.editControls, this.createControls)
      })
    }
  }

  #initializeMap(selector, initialZone, enableControls) {
    /**
     * Método que inicializa el mapa
     
     * Renderiza el mapa en el selector indicado, y en caso de que exista 
    una zona inicial, la colocará en el mapa
     */

    this.map = L.map(selector).setView([initialLat, initialLng], 13)
    L.tileLayer(mapLayerUrl).addTo(this.map)

    this.map.addLayer(this.#drawnItems)

    if (initialZone) {
      this.#addZone(initialZone, this.#drawnItems, this.map)
    }

    if (enableControls) {
      this.map.addControl(this.createControls)
    }
  }

  #addZone(initialZone, drawnItems, map) {
    const polygon = new L.Polygon(initialZone, { color: this.#color })

    drawnItems.addLayer(polygon)

    map.setView(polygon.getBounds().getCenter(), 13)
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

  #deleteHandler(map, editControls, createControls) {
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
    return (this.editControlsToolbar ||= new L.Control.Draw({
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

  get coordinates() {
    return this.drawnLayers[0]
      .getLatLngs()
      .flat()
      .map((coor) => {
        return { lat: coor.lat, lng: coor.lng }
      })
  }
}
