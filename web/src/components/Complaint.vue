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
          titulo: "Titulo denuncia 1",
          categoria: "Categoria 1",
          estado: "Estado 1",
          email_denunciante: "Email del creador de la denuncia 1",
          telcel_denunciante: "Telefono del creador 1",
          descripcion: "Descripción para la denuncia numero 1",
          coordinate: [-34.91521472314688, -57.97890472516883]
        },
        {
          titulo: "Titulo denuncia 2",
          categoria: "Categoria 2",
          estado: "Estado 2",
          email_denunciante: "Email del creador de la denuncia 2",
          telcel_denunciante: "Telefono del creador 2",
          descripcion: "Descripción para la denuncia numero 2",
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
