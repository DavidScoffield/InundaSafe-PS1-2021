import { ZoneMap } from '../ZoneMap.js'

window.onload = () => {
  let coordinates =
    document.getElementById('coordinates').innerText || document.getElementById('coordinates').value

  coordinates = coordinates ? JSON.parse(coordinates) : []

  const color = document.getElementById('color').innerText || document.getElementById('color').value

  console.log('Color Mapa: ' + color)

  const map = new ZoneMap({
    selector: 'mapid',
    color: color,
    initialZone: coordinates,
    enableControls: false,
  })
}
