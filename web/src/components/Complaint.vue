<template>
  <div class="complaint container d-flex" style="flex-direction:column">
    
    <Title>Denuncias</Title>
    <div class="new-complaint <style.complaint > scoped </style.complaint { position: absolute; rigth: 0; }>">
      <router-link class="button-gradient btn" to="/newComplaint">
        Nueva denuncia
      </router-link>
    </div>
    
    <l-map :zoom="zoom" :center="center" style="height: 500px">
      <l-tile-layer :url="url" />
      <div
        v-for="(complaint, index) in complaints.items"
        :key="`complaints-${index}`"
      >
        <l-marker :lat-lng="complaint.coordenadas">
          <l-popup :options="{ maxHeight: 300 }">
            <div @click="innerClick">
              <ul class="list-unstyled">
                <li style="overflow-wrap: break-word"><strong>Titulo:</strong> {{ complaint.titulo }}</li>
                <li><strong>Categoría:</strong> {{ complaint.categoria }}</li>
                <li>
                  <strong>Estado:</strong>
                  <span class="text-capitalize"> {{ complaint.estado }}</span>
                </li>
                <li style="overflow-wrap: break-word">
                  <strong>Email del denunciante:</strong>
                  {{ complaint.email_denunciante }}
                </li>
                <li>
                  <strong>Teléfono del denunciante:</strong>
                  {{ complaint.telcel_denunciante }}
                </li>
              </ul>
              <p v-show="showDescription" style="overflow-wrap: break-word">
                {{ complaint.descripcion }}
              </p>
              <strong>
                <i style="cursor: pointer">
                  Haga click para
                  <div
                    style="display: inline; cursor: pointer"
                    v-if="!showDescription"
                  >
                    ver
                  </div>
                  <div style="display: inline; cursor: pointer" v-else>
                    ocultar
                  </div>
                  la descripción
                </i>
              </strong>
            </div>
          </l-popup>
        </l-marker>
      </div>
    </l-map>

    <!-- Listado -->
    <table v-if="complaints.items" class="table table-striped mt-1" style="table-layout:fixed;">
      <thead>
        <tr>
          <th>Titulo</th>
          <th>Categoría</th>
          <th>Estado</th>
        </tr>
      </thead>

      <tbody>
        <tr v-for="(complaint, index) in complaints.items" :key="index">
          <td style="overflow-wrap: break-word" scope="row">{{ complaint.titulo }}</td>  
          <td scope="row">{{ complaint.categoria }}</td>
          <td scope="row">{{ complaint.estado }}</td>
        </tr>
      </tbody>
    </table>

    <div v-if="emptyComplaints" class="w-100 mt-2">
      <p> Aún no hay denuncias cargadas. </p>
    </div>

    <!-- Barra de navegación para denuncias -->
    <NavigationBar v-if="complaints.total"
                   :items="complaints" 
                   :fetchPage="fetchNextPage"/>
  </div>
</template>

<script>
import { latLng } from "leaflet";
import { LMap, LTileLayer, LMarker, LPopup } from "@vue-leaflet/vue-leaflet";
import Title from "./Title.vue";
import NavigationBar from "./NavigationBar.vue";

export default {
  name: "Complaint",
  components: {
    LMap,
    LTileLayer,
    LMarker,
    LPopup,
    Title,
    NavigationBar
  },
  data() {
    return {
      zoom: 12.5,
      center: latLng(-34.9187, -57.956),
      url: "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
      showDescription: false,
      complaints: [],
      currentPage: 0,
      emptyComplaints: false
    };
  },
  methods: {
    innerClick() {
      this.showDescription = !this.showDescription;
    },
    fetchNextPage(page = 1) {
      fetch(`${process.env.VUE_APP_BASE_URL}/denuncias?pagina=${page}`)
        .then((response) => {
          return response.json();
        })
        .then((json) => {
          this.complaints = json;

          //Si no hay denuncias seteo a True y muestra el mensaje de vacio
          this.complaints.items.length ? this.emptyComplaints = false : this.emptyComplaints = true
        })
        .catch((e) => {
          console.log("CATCH! complaint index");
          console.log(e);
        });
    },
  },
  created() {
    this.fetchNextPage(1);
  },
};
</script>

<style scoped>
.complaint {
  position: relative;
}
.new-complaint {
  position: absolute;
  right: 10px;
  top: 30px;
}
</style>
