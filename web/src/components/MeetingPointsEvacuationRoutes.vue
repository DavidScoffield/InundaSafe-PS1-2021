<template>

  <div style="height: 500px; width: 70%; margin: auto">

    <h1> Puntos de encuentro y recorridos de evacuación </h1><br>

    <l-map
      :zoom="zoom"
      :center="center"
      style="height: 100%"
    >

      <l-tile-layer :url="url"/>

      <!-- Se dibujan los puntos de encuentro -->
      <l-marker v-for="(meetingPoint, index) in meetingPoints.puntos_encuentro" :key="index"
                :lat-lng="[meetingPoint.coordenada.lat, meetingPoint.coordenada.long]">

        <l-popup :options="{ maxHeight: 300 }">
          <strong>Nombre:</strong> {{meetingPoint.nombre}}<br>
          <strong>Teléfono:</strong> {{meetingPoint.telefono}}<br>
          <strong>Dirección</strong> {{meetingPoint.direccion}}<br>
        </l-popup>
        
      </l-marker>

      <!-- Se dibujan los recorridos de evacuación -->
      <l-polyline v-for="(evacuationRoute, index) in evacuationRoutes.recorridos" :key="index"
                  :lat-lngs="getCoordinateList(evacuationRoute.coordenadas)" :color="randomColor()">
        
        <!-- Marcador de inicio del recorrido -->
        <l-marker :lat-lng="[evacuationRoute.coordenadas[0].lat, evacuationRoute.coordenadas[0].long]">

          <l-icon 
            :icon-size="50"
            icon-url="https://cdn.icon-icons.com/icons2/1854/PNG/512/8_116658.png"/>

          <l-popup :options="{ maxHeight: 300 }">
              <strong>Nombre:</strong> {{evacuationRoute.nombre}}<br>
              <p style="display:inline-block" v-show="showDescription"><strong> Descripcion: </strong> {{evacuationRoute.descripcion}}</p><br>
              <strong>
                <i @click="innerClick">
                  Haga click para 
                  <div style="display: inline" v-if="!showDescription">ver</div>
                  <div style="display: inline" v-else>ocultar</div>
                  la descripción
                </i>
              </strong>
          </l-popup>

        </l-marker>

        <!-- Marcador de fin del recorrido -->
        <l-marker :lat-lng="getEvacuationRouteEndPoint(evacuationRoute.coordenadas)">
          <l-icon 
            :icon-size="30"
            icon-url="http://cdn.onlinewebfonts.com/svg/img_467043.png"/>
        </l-marker>

      </l-polyline>

    </l-map><br><br>    

    <div class="container">

        <div class="row">

            <div class="col-sm">

                <h3>Puntos de encuentro</h3><br>

                <!-- Tabla de puntos de encuentro -->
                <table class="table table-striped">
                    <thead>
                        <tr>
                            <th>Nombre</th>
                            <th>Dirección</th>
                        </tr>
                    </thead>

                    <tbody>
                        <tr v-for="(meetingPoint, index) in meetingPoints.puntos_encuentro" :key="index">
                            <th scope="row">{{ meetingPoint.nombre }}</th>  
                            <td>{{ meetingPoint.direccion }}</td> 
                        </tr>
                    </tbody>
                </table><br>

                <!-- Barra de navegación para puntos de encuentro -->
                <nav aria-label="Meeting points page navigation">
                    <ul class="pagination justify-content-center">
                        <li v-if="meetingPoints.pagina > 1" class="page-item">
                            <a class="page-link" tabindex="-1" @click="fetchMeetingPointPage(meetingPoints.pagina - 1)">Anterior</a>
                        </li>
                        <li v-else class="page-item disabled">
                            <a class="page-link" tabindex="-1">Anterior</a>
                        </li>
                        <li v-for="page in [...Array(meetingPoints.paginas).keys()]" :key="`page-${page}`" class="page-item"
                            v-bind:class="{ 'active' : meetingPoints.pagina == page + 1 }">
                            <a class="page-link" @click="fetchMeetingPointPage(page + 1)">{{ page + 1 }}</a>
                        </li>
                        <li v-if="meetingPoints.pagina < meetingPoints.paginas" class="page-item">
                            <a class="page-link" @click="fetchMeetingPointPage(meetingPoints.pagina + 1)">Siguiente</a>
                        </li>
                        <li v-else class="page-item disabled">
                            <a class="page-link" href="#">Siguiente</a>
                        </li>
                    </ul>
                </nav>

            </div>

            <div class="col-sm">

                <h3>Recorridos de evacuación</h3><br>

                <!-- Tabla de recorridos de evacuación -->
                <table class="table table-striped">
                    <thead>
                        <tr>
                            <th>Nombre</th>
                        </tr>
                    </thead>

                    <tbody>
                        <tr v-for="(evacuationRoute, index) in evacuationRoutes.recorridos" :key="index">
                            <th scope="row">{{ evacuationRoute.nombre }}</th>  
                        </tr>
                    </tbody>
                </table><br>

                <!-- Barra de navegación para recorridos de evacuación -->
                <nav aria-label="Evacuation route page navigation">
                    <ul class="pagination justify-content-center">
                        <li v-if="evacuationRoutes.pagina > 1" class="page-item">
                            <a class="page-link" tabindex="-1" @click="fetchEvacuationRoutePage(evacuationRoutes.pagina - 1)">Anterior</a>
                        </li>
                        <li v-else class="page-item disabled">
                            <a class="page-link" tabindex="-1">Anterior</a>
                        </li>
                        <li v-for="page in [...Array(evacuationRoutes.paginas).keys()]" :key="`page-${page}`" class="page-item"
                            v-bind:class="{ 'active' : evacuationRoutes.pagina == page + 1 }">
                            <a class="page-link active" active="{{evacuationRoutes.pagina == page}}" @click="fetchEvacuationRoutePage(page + 1)">{{ page + 1 }}</a>
                        </li>
                        <li v-if="evacuationRoutes.pagina < evacuationRoutes.paginas" class="page-item">
                            <a class="page-link" @click="fetchEvacuationRoutePage(evacuationRoutes.pagina + 1)">Siguiente</a>
                        </li>
                        <li v-else class="page-item disabled">
                            <a class="page-link" href="#">Siguiente</a>
                        </li>
                    </ul>
                </nav>

            </div>

        </div>

    </div>

  </div>

</template>

<script>

  import { latLng } from "leaflet";
  import { LMap, LTileLayer, LMarker, LPopup, LPolyline, LIcon } from "@vue-leaflet/vue-leaflet";
  
  export default {
  
    name: "MeetingPointsEvacuationRoutes",
  
    components: {
      LMap,
      LTileLayer,
      LMarker,
      LPopup,
      LPolyline,
      LIcon
    },
  
    data() {
      return {
        zoom: 12.5,
        center: latLng(-34.9187, -57.956),
        url: 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
        showDescription: false,
        meetingPoints: [],
        evacuationRoutes: [],
        currentMeetinpointPage: 0,
        currentEvacuationRoutePage: 0,
      };
    },
  
    methods: {
      innerClick() {
        // oculta o muestra la descripción del recorrido de evacuación

        this.showDescription = !this.showDescription;
      },
  
      fetchMeetingPointPage(page=1) {
        // consulta a la api de puntos de encuentro para obtener la página solicitada

        fetch(`https://admin-grupo24.proyecto2021.linti.unlp.edu.ar/api/puntos-encuentro?pagina=${page}`)
          .then((response) => {
              return response.json();
          })
              .then((json) => {
                  this.meetingPoints = json.puntos_encuentro
              })
                  .catch((e) => {
                      console.log(e)
                  })
      },
  
      fetchEvacuationRoutePage(page=1) {
        // consulta a la api de recorridos de evacuación para obtener la página solicitada

        fetch(`https://admin-grupo24.proyecto2021.linti.unlp.edu.ar/api/recorridos-evacuacion?pagina=${page}`)
          .then((response) => {
              return response.json();
          })
              .then((json) => {
                  this.evacuationRoutes = json.recorridos
              })
                  .catch((e) => {
                      console.log(e)
                  })
      },
  
      getCoordinateList(coordinates) {
          // retorna un listado con las coordenadas (lat, long) del recorrido de evacuación

          var coordinateList = []
          for (var latLong of coordinates) {
              coordinateList.push([latLong.lat, latLong.long])
          }
          return coordinateList
      },
  
      randomColor() {
          // retorna un color aleatorio para marcar el recorrido de evacuación

          var colors = [ "#8B008B", "#3221a5", "#7B68EE", 
                         "#FF4500", "#5F9EA0", "#8B4513", 
                         "#32CD32", "#8A2BE2", "#2160d3" ]

          return colors[Math.floor(Math.random()*colors.length)]
      },

      getEvacuationRouteEndPoint(coordinates) {
          // retorna el último punto del recorrido de evacuación

          return [coordinates[coordinates.length - 1].lat, coordinates[coordinates.length - 1].long]
      },
  
    },
  
    created() {
      // hook created donde se cargan los puntos de encuentro y recorridos de evacuación
      // con la información de la primer página de los listados

      this.fetchMeetingPointPage(1)
      this.fetchEvacuationRoutePage(1)
    }
  
  };
  
</script>