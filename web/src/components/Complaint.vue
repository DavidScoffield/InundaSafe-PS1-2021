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
      <div v-for="(complaint, index) in complaints" :key="`complaints-${index}`">
        <l-marker :lat-lng="complaint.coordinate">
          <l-popup>
            <div @click="innerClick">
              <strong>Titulo:</strong> {{complaint.title}}<br>
              <strong>Categoría:</strong> {{complaint.category}}<br>
              <strong>Estado:</strong> {{complaint.state}}<br>
              <strong>Email del denunciante:</strong> {{complaint.creator_email}}<br>
              <strong>Teléfono del denunciante:</strong> {{complaint.creator_telephone}}<br>
              <p v-show="showDescription">
                {{complaint.description}}
              </p>
              <strong>
                <i>
                  Click para 
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
      complaints : [
        {
          title: "Titulo denuncia 1",
          category: "Categoria 1",
          state: "Estado 1",
          creator_email: "Email del creador de la denuncia 1",
          creator_telephone: "Telefono del creador 1",
          description: "Descripción para la denuncia numero 1",
          coordinate: [-34.91521472314688, -57.97890472516883]
        },
        {
          title: "Titulo denuncia 2",
          category: "Categoria 2",
          state: "Estado 2",
          creator_email: "Email del creador de la denuncia 2",
          creator_telephone: "Telefono del creador 2",
          description: "Descripción para la denuncia numero 2",
          coordinate: [-34.9029674883098, -57.97890472516883]
        }
      ]
    };
  },
  methods: {
    innerClick() {
      this.showDescription = !this.showDescription;
    }
  },
};

</script>


<style>

</style>
