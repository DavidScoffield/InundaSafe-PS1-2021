<template>
  <div style="height: auto; width: 100%; margin: 0 auto">
    <Title>Zona inundable: {{ floodZone?.nombre }}</Title>
    <br />
    <!-- MAPA -->
    <l-map :zoom="zoom" :center="center" style="height: 500px">
      <l-tile-layer :url="url" />

      <!-- Se dibuja la zona inundable -->
      <PolygonZone v-if="floodZone !== null" :zone="floodZone" />
    </l-map>

    <!-- INFO -->
    <div class="container">
      <table class="table table-striped">
        <thead>
          <tr>
            <th>Nombre</th>
            <th>Codigo</th>
            <th>Estado</th>
            <th>Color</th>
          </tr>
        </thead>

        <tbody class="text-center">
          <tr>
            <th>{{ floodZone?.nombre }}</th>
            <td>{{ floodZone?.codigo }}</td>
            <td>
              <span class="text-capitalize">{{ floodZone?.estado }}</span>
            </td>
            <td>
              {{ floodZone?.color }}
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
import { latLng } from "leaflet";
import { LMap, LTileLayer } from "@vue-leaflet/vue-leaflet";
import PolygonZone from "./PolygonZone.vue";
import Title from "./Title.vue";

export default {
  name: "FloodZones",

  components: {
    LMap,
    LTileLayer,
    PolygonZone,
    Title,
  },

  data() {
    return {
      zoom: 11.5,
      center: latLng(-34.9187, -57.956),
      url: "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
      floodZone: null,
    };
  },

  methods: {
    fetchFloodZone() {
      // consulta a la api de zonas inundables para obtener la página solicitada
      const fetchedId = this.$route.params.id;

      fetch(`${process.env.VUE_APP_BASE_URL}/zonas-inundables/${fetchedId}`)
        .then((response) => {
          if (!response.ok) {
            return this.$router.push({ name: "Home" });
          }
          return response.json();
        })
        .then(({ atributos }) => {
          this.floodZone = atributos;

          const middledCoor = parseInt(atributos.cantidad_coordenadas / 2);

          this.center = latLng(
            atributos.coordenadas[middledCoor].lat,
            atributos.coordenadas[middledCoor].long
          );
        })
        .catch((e) => {
          console.log(e);
        });
    },
  },

  created() {
    this.fetchFloodZone();
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