import { ZoneMap } from '../../ZoneMap.js'

window.onload = () => {
  let coordinates = document.getElementById('coordinates').innerText

  coordinates = coordinates ? JSON.parse(coordinates) : []

  const map = new ZoneMap({
    selector: 'mapid',
    addSearch: true,
    initialZone: coordinates,
  })
}
