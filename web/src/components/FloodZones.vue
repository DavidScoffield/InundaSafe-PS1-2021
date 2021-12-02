<template>
  <div style="height: auto; width: 100%; margin: 0 auto">
    <h1>Zonas inundables</h1>
    <br />

    <!-- MAPA -->
    <l-map :zoom="zoom" :center="center" style="height: 500px">
      <l-tile-layer :url="url" />

      <!-- Se dibujan las zonas inundables -->
      <div v-for="zone in floodZones.zonas" :key="zone.id">
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
      </div>
    </l-map>

    <!-- LISTADO -->
    <div class="container">
      <table class="table table-striped">
        <thead>
          <tr>
            <th>Nombre</th>
            <th>Codigo</th>
            <th>Estado</th>
            <th>Acción</th>
          </tr>
        </thead>

        <tbody class="text-center">
          <tr v-for="zone in floodZones.zonas" :key="zone.id">
            <th>{{ zone.nombre }}</th>
            <td>{{ zone.codigo }}</td>
            <td>
              <span class="text-capitalize">{{ zone.estado }}</span>
            </td>
            <td>
              <router-link
                :to="'/zonas-inundables/' + zone.id"
                class="btn button-gradient"
                >Detalle</router-link
              >
            </td>
          </tr>
        </tbody>
      </table>

      <!-- Barra de navegación  -->
      <nav aria-label="Pagina de navegacion para zonas inundables">
        <ul class="pagination justify-content-center">
          <li v-if="floodZones.pagina > 1" class="page-item">
            <button
              class="page-link"
              tabindex="-1"
              @click="fetchFloodZonesPage(floodZones.pagina - 1)"
            >
              Anterior
            </button>
          </li>
          <li v-else class="page-item disabled">
            <button class="page-link" tabindex="-1">Anterior</button>
          </li>
          <li
            v-for="page in [...Array(floodZones.paginas).keys()]"
            :key="`page-${page}`"
            class="page-item"
            v-bind:class="{ active: floodZones.pagina == page + 1 }"
          >
            <button class="page-link" @click="fetchFloodZonesPage(page + 1)">
              {{ page + 1 }}
            </button>
          </li>
          <li v-if="floodZones.pagina < floodZones.paginas" class="page-item">
            <button
              class="page-link"
              @click="fetchFloodZonesPage(floodZones.pagina + 1)"
            >
              Siguiente
            </button>
          </li>
          <li v-else class="page-item disabled">
            <button class="page-link" href="#">Siguiente</button>
          </li>
        </ul>
      </nav>
    </div>
  </div>
</template>

<script>
import { latLng } from "leaflet";
import { LMap, LTileLayer, LPopup, LPolygon } from "@vue-leaflet/vue-leaflet";

export default {
  name: "FloodZones",

  components: {
    LMap,
    LTileLayer,
    LPolygon,
    LPopup,
  },

  data() {
    return {
      zoom: 11.5,
      center: latLng(-34.9187, -57.956),
      url: "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
      floodZones: [],
    };
  },

  methods: {
    fetchFloodZonesPage(page = 1) {
      // consulta a la api de zonas inundables para obtener la página solicitada
      fetch(`${process.env.VUE_APP_BASE_URL}/zonas-inundables?pagina=${page}`)
        .then((response) => {
          return response.json();
        })
        .then(({ zonas }) => {
          console.log(zonas);
          this.floodZones = zonas;
        })
        .catch((e) => {
          console.log(e);
        });
    },

    getCoordinateList(coordinates) {
      // retorna un listado con las coordenadas [lat, long] de la zona inundable
      return coordinates.map((coor) => [coor.lat, coor.long]);
    },
  },

  created() {
    // hook created donde se cargan las zonas inundables
    // con la información de la primer página de los listados
    this.fetchFloodZonesPage(1);
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

tbody {
  vertical-align: middle !important;
}
</style>