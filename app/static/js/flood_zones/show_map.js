import { ZoneMap } from '../ZoneMap.js'

window.onload = () => {
  let coordinates =
    document.getElementById('coordinates').innerText || document.getElementById('coordinates').value

  coordinates = coordinates ? JSON.parse(coordinates) : []

  const map = new ZoneMap({
    selector: 'mapid',
    initialZone: coordinates,
    enableControls: false,
  })
}
