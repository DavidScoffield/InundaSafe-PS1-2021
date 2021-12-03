<template>
  <l-polygon
    :lat-lngs="getCoordinateList(zone.coordenadas)"
    :color="zone.color"
    :fill="true"
    :fillColor="zone.color"
    :fillOpacity="0.5"
  >
    <l-popup :options="{ maxHeight: 300 }">
      <ul>
        <li><strong>Nombre:</strong> {{ zone.nombre }}</li>
        <li><strong>Codigo:</strong> {{ zone.codigo }}</li>
        <li>
          <strong>Estado:</strong>
          <span class="text-capitalize"> {{ zone.estado }}</span>
        </li>
        <li>
          <strong>Cantidad de puntos: </strong>
          {{ zone.cantidad_coordenadas }}
        </li>
      </ul>
    </l-popup></l-polygon
  >
</template>

<script>
import { LPopup, LPolygon } from "@vue-leaflet/vue-leaflet";

export default {
  name: "PolygonZone",

  components: {
    LPolygon,
    LPopup,
  },

  props: ["zone"],

  methods: {
    getCoordinateList(coordinates) {
      // retorna un listado con las coordenadas [lat, long] de la zona inundable
      return coordinates.map((coor) => [coor.lat, coor.long]);
    },
  },
};
</script>

<style scoped>
ul {
  list-style: none;
  padding-left: 0;
}

ul > li {
  display: list-item;
}
</style>