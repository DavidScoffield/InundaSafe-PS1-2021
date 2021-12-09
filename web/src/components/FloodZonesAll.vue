<template>
  <div style="height: auto; width: 100%; margin: 0 auto" class="container flood_zone">
    <Title>Zonas inundables</Title>
    <div
      class="new-complaint <style.complaint > scoped </style.complaint { position: absolute; rigth: 0; }>"
    >
      <router-link class="button-gradient btn" to="/newComplaint"
        >Nueva denuncia</router-link
      >
    </div>
    <br />

    <!-- MAPA -->
    <l-map :zoom="zoom" :center="center" style="height: 500px">
      <l-tile-layer :url="url" />

      <!-- Se dibujan las zonas inundables -->
      <ListPolygonZones v-if="emptyZones === null" :floodZones="floodZones" />
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

        <template v-if="emptyZones === null">
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
                  exact
                  class="btn button-gradient"
                  >Detalle</router-link
                >
              </td>
            </tr>
          </tbody>
        </template>
      </table>

      <p v-if="emptyZones" class="w-100">
        {{ emptyZones }}
      </p>

      <!-- Barra de navegación  -->
      <NavigationBar v-if="emptyZones === null"
                     :items="floodZones" 
                     :fetchPage="fetchFloodZonesPage"/>
    </div>
  </div>
</template>

<script>
import { latLng } from "leaflet";
import { LMap, LTileLayer } from "@vue-leaflet/vue-leaflet";
import ListPolygonZones from "./ListPolygonZones.vue";
import Title from "./Title.vue";
import NavigationBar from "./NavigationBar.vue";


export default {
  name: "FloodZonesAll",

  components: {
    LMap,
    LTileLayer,
    ListPolygonZones,
    Title,
    NavigationBar
  },

  data() {
    return {
      zoom: 11.5,
      center: latLng(-34.9187, -57.956),
      url: "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
      floodZones: [],
      emptyZones: null,
    };
  },

  methods: {
    fetchFloodZonesPage(page = 1) {
      // consulta a la api de zonas inundables para obtener la página solicitada
      fetch(`${process.env.VUE_APP_BASE_URL}/zonas-inundables?pagina=${page}`)
        .then((response) => {
          if (!response.ok) {
            return response.json().then((r) => {
              throw Error(r.error_description);
            });
          }
          return response.json();
        })
        .then((json) => {
          this.floodZones = json.zonas;
        })
        .catch(({ message }) => {
          // this.emptyZones = message;
          console.log({ message });
          this.emptyZones = "No hay zonas inundables disponibles.";
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
tbody {
  vertical-align: middle !important;
}
.flood_zone {
  position: relative;
}
.new-complaint {
  position: absolute;
  right: 10px;
  top: 35px;
}
</style>