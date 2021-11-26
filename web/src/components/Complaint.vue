<template>

  <div style="height: 500px; width: 100%">
    Denuncias:
    <l-map
      :zoom="zoom"
      :center="center"
      style="height: 100%"
    >
      <l-tile-layer
        :url="url"
      />
      <div v-for="(complaint, index) in complaints.items" :key="`complaints-${index}`">
        <l-marker :lat-lng="complaint.coordenadas">
          <l-popup>
            <div @click="innerClick">
              <strong>Titulo:</strong> {{complaint.titulo}}<br>
              <strong>Categoría:</strong> {{complaint.categoria}}<br>
              <strong>Estado:</strong> {{complaint.estado}}<br>
              <strong>Email del denunciante:</strong> {{complaint.email_denunciante}}<br>
              <strong>Teléfono del denunciante:</strong> {{complaint.telcel_denunciante}}<br>
              <p v-show="showDescription">
                {{complaint.descripcion}}
              </p>
              <strong>
                <i>
                  Haga click para 
                  <div style="display: inline" v-if="!showDescription">ver</div> 
                  <div style="display: inline" v-else>ocultar</div> 
                  la descripción
                </i>
              </strong>
            </div>
          </l-popup>
        </l-marker>
      </div>
      
    </l-map>

    <div v-if="currentPage < complaints.paginas">
      <button @click="movePage(1)">Siguiente</button>
    </div>
    <div v-if="currentPage > 1">
      <button @click="movePage(-1)">Anterior</button>
    </div>

  </div>
  
</template>

<script>

import { latLng } from "leaflet";
import { LMap, LTileLayer, LMarker, LPopup } from "@vue-leaflet/vue-leaflet";

export default {
  name: "Complaint",
  components: {
    LMap,
    LTileLayer,
    LMarker,
    LPopup
  },
  data() {
    return {
      zoom: 12.5,
      center: latLng(-34.9187, -57.956),
      url: 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
      showDescription: false,
      complaints: [],
      currentPage: 1
    };
  },
  methods: {
    innerClick() {
      this.showDescription = !this.showDescription;
    },
    movePage(next) {
      this.currentPage += next
      this.fetchNextPage()
    },
    fetchNextPage() {
      fetch(`http://localhost:5000/api/denuncias?pagina=${this.currentPage}`)
      .then((response) => {
        return response.json();
      })
      .then((json) => {
        this.complaints = json
        console.log(json)
      })
      .catch((e) => {
        console.log(e)
      })
    }
  },
  created() {
    this.fetchNextPage()
  }
};

</script>


<style>

</style>
