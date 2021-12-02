<template>
  <div class="container">
    <h2>Denuncias</h2>
    
    <l-map :zoom="zoom" :center="center" style="height: 80%">
      <l-tile-layer :url="url" />
      <div
        v-for="(complaint, index) in complaints.items"
        :key="`complaints-${index}`"
      >
        <l-marker :lat-lng="complaint.coordenadas">
          <l-popup :options="{ maxHeight: 300 }">
            <div @click="innerClick">
              <ul class="list-unstyled">
                <li><strong>Titulo:</strong> {{ complaint.titulo }}</li>
                <li><strong>Categoría:</strong> {{ complaint.categoria }}</li>
                <li>
                  <strong>Estado:</strong>
                  <span class="text-capitalize"> {{ complaint.estado }}</span>
                </li>
                <li><strong>Email del denunciante:</strong> {{ complaint.email_denunciante }}</li>
                <li><strong>Teléfono del denunciante:</strong> {{ complaint.telcel_denunciante }}</li>
              </ul>
              <p v-show="showDescription" style="overflow-wrap: break-word">
                {{ complaint.descripcion }}
              </p>
              <strong>
                <i style="cursor: pointer">
                  Haga click para
                  <div style="display: inline; cursor: pointer" v-if="!showDescription">ver</div>
                  <div style="display: inline; cursor: pointer" v-else>ocultar</div>
                  la descripción
                </i>
              </strong>
            </div>
          </l-popup>
        </l-marker>
      </div>
    </l-map>

    <!-- Barra de navegación para denuncias -->
    <nav aria-label="Complaints page navigation" class="mt-1">
      <ul class="pagination justify-content-center">
        <li v-if="complaints.pagina > 1" class="page-item">
          <button
            class="page-link"
            tabindex="-1"
            @click="fetchNextPage(complaints.pagina - 1)"
            >Anterior</button
          >
        </li>
        <li v-else class="page-item disabled">
          <a class="page-link" tabindex="-1">Anterior</a>
        </li>
        <li
          v-for="page in [...Array(complaints.paginas).keys()]"
          :key="`page-${page}`"
          class="page-item"
          v-bind:class="{ active: complaints.pagina == page + 1 }"
        >
          <button
            class="page-link"
            @click="fetchNextPage(page + 1)"
            >{{ page + 1 }}</button
          >
        </li>
        <li v-if="complaints.pagina < complaints.paginas" class="page-item">
          <button
            class="page-link"
            @click="fetchNextPage(complaints.pagina + 1)"
            >Siguiente</button
          >
        </li>
        <li v-else class="page-item disabled">
          <a class="page-link" href="#">Siguiente</a>
        </li>
      </ul>
    </nav>
  </div>
</template>

<script>
import { latLng } from 'leaflet'
import { LMap, LTileLayer, LMarker, LPopup } from '@vue-leaflet/vue-leaflet'

export default {
  name: 'Complaint',
  components: {
    LMap,
    LTileLayer,
    LMarker,
    LPopup,
  },
  data() {
    return {
      zoom: 12.5,
      center: latLng(-34.9187, -57.956),
      url: 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
      showDescription: false,
      complaints: [],
      currentPage: 0,
    }
  },
  methods: {
    innerClick() {
      this.showDescription = !this.showDescription
    },
    fetchNextPage(page = 1) {
      fetch(`${process.env.VUE_APP_BASE_URL}/denuncias?pagina=${page}`)
        .then((response) => {
          return response.json()
        })
        .then((json) => {
          this.complaints = json
        })
        .catch((e) => {
          console.log("CATCH! complaint index")
          console.log(e)
        })
    },
  },
  created() {
    this.fetchNextPage(1)
  },
}
</script>
