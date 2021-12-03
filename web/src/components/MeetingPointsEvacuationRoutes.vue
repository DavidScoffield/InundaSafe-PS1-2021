<template >

  <div style="height: auto; width: 85%; margin: 0 auto">

    <br><h1> Puntos de encuentro y recorridos de evacuación </h1><br>

    <p v-if="!fetchedMeetingPoints || !fetchedEvacuationRoutes">Cargando mapa...
       <img style='height: 50px; width: 70px' src='../assets/icons/loading.gif'> </p>

    <l-map v-if="center" :zoom="zoom" :center="center" style="height: 500px">

      <l-tile-layer :url="url"/>

      <!-- Marcador de la ubicación del usuario o ubicación por defecto -->
      <l-marker :lat-lng="this.userLatLong ? [this.userLatLong.lat, this.userLatLong.long] : this.center">

          <l-icon :icon-url="require('../assets/icons/initial_location.png')"
                  :icon-size="[20, 30]"/>

          <l-popup :options="{ maxHeight: 350 }">
            <strong>Mi ubicación</strong> {{this.userLatLong ? "(GPS)" : "(default)"}}
          </l-popup>
          
      </l-marker>

      <!-- Se dibujan los puntos de encuentro -->
      <l-marker v-for="(meetingPoint, index) in meetingPoints.puntos_encuentro" :key="index"
                :lat-lng="[meetingPoint.coordenada.lat, meetingPoint.coordenada.long]">

        <l-icon :icon-url="require('../assets/icons/meeting_point.png')"
                :icon-size="[30, 40]"/>

        <l-popup :options="{ maxHeight: 350 }">
          <p style="color:green; text-align:center">Punto de encuentro</p>
          <strong>Nombre:</strong> {{meetingPoint.nombre}}<br>
          <strong>Teléfono:</strong> {{meetingPoint.telefono}}<br>
          <strong>Dirección:</strong> {{meetingPoint.direccion}}<br>
          <strong>Email:</strong> {{meetingPoint.email}}<br>
        </l-popup>
        
      </l-marker>

      <!-- Se dibujan los recorridos de evacuación -->
      <l-polyline v-for="(evacuationRoute, index) in evacuationRoutes.recorridos" :key="index"
                  :lat-lngs="getCoordinateList(evacuationRoute.coordenadas)" :color="randomColor()">
        
        <!-- Marcador de inicio del recorrido -->
        <l-marker :lat-lng="[evacuationRoute.coordenadas[0].lat, evacuationRoute.coordenadas[0].long]">

          <l-icon :icon-url="require('../assets/icons/evacuation_route_start.png')"
                  :icon-size="[35, 45]"/>

          <l-popup :options="{ maxHeight: 350 }">
              <p style="color:green; text-align:center">Recorrido de evacuación</p>
              <strong>Nombre:</strong> {{evacuationRoute.nombre}}<br>
              <p style="display:inline-block" v-show="showDescription">
                <strong> Descripcion: </strong> {{evacuationRoute.descripcion}}
              </p><br>
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
          <l-icon :icon-url="require('../assets/icons/evacuation_route_end.png')"
                  :icon-size="[20, 30]"/>
        </l-marker>

      </l-polyline>

    </l-map><br><br>    

    <div class="container">

        <div class="row">

            <div class="col-sm">

                <h3> <img style='height: 40px; width: 35px' src='../assets/icons/meeting_point.png'>
                      Puntos de encuentro {{userLatLong ? "cercanos al usuario" : ""}}</h3><br>

                <!-- Tabla de puntos de encuentro -->
                <table v-if="fetchedMeetingPoints" class="table table-striped">
                    <thead>
                        <tr v-if="meetingPoints.puntos_encuentro.length">
                            <th>Nombre</th>
                            <th>Dirección</th>
                        </tr>
                        <tr v-else>
                          <th>No se encontraron puntos de encuentro</th>
                        </tr>
                    </thead>

                    <tbody>
                        <tr v-for="(meetingPoint, index) in meetingPoints.puntos_encuentro" :key="index">
                            <th scope="row">{{ meetingPoint.nombre }}</th>  
                            <td>{{ meetingPoint.direccion }}</td> 
                        </tr>
                    </tbody>
                </table><br>

                <p v-if="!fetchedMeetingPoints">Buscando puntos de encuentro...<img style='height:50px; width:70px' src='../assets/icons/loading.gif'> </p>

                <!-- Barra de navegación para puntos de encuentro -->
                <nav v-if="meetingPoints.puntos_encuentro.length" aria-label="Meeting points page navigation">
                    <ul class="pagination justify-content-center">
                        <li v-if="meetingPoints.pagina > 1" class="page-item">
                            <a class="page-link" tabindex="-1" @click="fetchMeetingPointPage(meetingPoints.pagina - 1)">Anterior</a>
                        </li>
                        <li v-else class="page-item disabled">
                            <a class="page-link" tabindex="-1">Anterior</a>
                        </li>
                        <li v-for="page in [...Array(meetingPoints.paginas).keys()]" :key="page" class="page-item"
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

                <h3><img style='height: 40px; width: 35px' src='../assets/icons/evacuation_route_start.png'>
                    Recorridos de evacuación</h3><br>

                <!-- Tabla de recorridos de evacuación -->
                <table v-if="fetchedEvacuationRoutes" class="table table-striped">
                    <thead>
                        <tr>
                            <th>{{evacuationRoutes.recorridos.length ? "Nombre" : "No se encontraron recorridos de evacuación"}}</th>
                            <th v-if="evacuationRoutes.recorridos.length">Descripción</th>
                        </tr>
                    </thead>

                    <tbody>
                        <tr v-for="(evacuationRoute, index) in evacuationRoutes.recorridos" :key="index">
                            <th scope="row">{{ evacuationRoute.nombre }}</th>  
                            <th scope="row">{{ evacuationRoute.descripcion }}</th>
                        </tr>
                    </tbody>
                </table><br>

                <p v-if="!fetchedEvacuationRoutes">Buscando recorridos de evacuación...<img style='height:50px; width:70px' src='../assets/icons/loading.gif'> </p>

                <!-- Barra de navegación para recorridos de evacuación -->
                <nav v-if="evacuationRoutes.recorridos.length" aria-label="Evacuation route page navigation">
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
        center: null,
        url: 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
        showDescription: false,
        meetingPoints: { puntos_encuentro : [] },
        evacuationRoutes: { recorridos : [] },
        currentMeetinpointPage: 0,
        currentEvacuationRoutePage: 0,
        fetchedMeetingPoints: false,
        fetchedEvacuationRoutes: false,
        userLatLong: null
      };
    },
  
    methods: {
      innerClick() {
        // oculta o muestra la descripción del recorrido de evacuación

        this.showDescription = !this.showDescription;
      },
  
      fetchMeetingPointPage(page=1) {
        // consulta a la api de puntos de encuentro para obtener la página solicitada

        var url = `${process.env.VUE_APP_BASE_URL}/puntos-encuentro?pagina=${page}`

        if (this.userLatLong) {
          url += `&lat=${this.userLatLong.lat}&long=${this.userLatLong.long}`
        }

        this.fetchedMeetingPoints = false

        fetch(url)
          .then((response) => {
              return response.json();
          })
              .then((json) => {
                  if (json.error_name) {
                    throw json
                  }
                  this.meetingPoints = json.puntos_encuentro
              })
                  .catch((e) => {
                      console.log(e)
                  })
                      .finally(() => {
                        this.fetchedMeetingPoints = true
                      })                  
      },
  
      fetchEvacuationRoutePage(page=1) {
        // consulta a la api de recorridos de evacuación para obtener la página solicitada

        this.fetchedEvacuationRoutes = false

        fetch(`${process.env.VUE_APP_BASE_URL}/recorridos-evacuacion?pagina=${page}`)
          .then((response) => {
              return response.json();
          })
              .then((json) => {
                  if (json.error_name) {
                    throw json
                  }
                  this.evacuationRoutes = json.recorridos
              })
                  .catch((e) => {
                      console.log(e)
                  })
                      .finally(() => {
                        this.fetchedEvacuationRoutes = true
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

      setUserCoordinates(position) {
        // función que setea las coordenadas del usuario en caso de que 
        // se las haya podido obtener de forma correcta
        this.userLatLong = { lat : position.coords.latitude,
                             long : position.coords.longitude }

        this.center = latLng(position.coords.latitude, 
                             position.coords.longitude)

        this.fetchInitialPages()
      },

      geoLocationError(error) {
        // función que se ejecuta en caso de que el usuario no haya aceptado
        // proveer su ubicación o haya ocurrido algún error al tratar de accederla

        this.center = latLng(-34.9213, -57.9545)
        this.fetchInitialPages()
        console.log(error)
      },

      fetchInitialPages(){
        // consulta por las primeras páginas de puntos de encuentro
        // y recorridos de evacuación

        this.fetchMeetingPointPage(1)
        this.fetchEvacuationRoutePage(1)
        
      }
  
    },
  
    created() {
      // hook created donde se consulta por la ubicación del usuario
      // y se cargan los puntos de encuentro y recorridos de evacuación
      // con la información de la primer página de los listados

      navigator.geolocation.getCurrentPosition(this.setUserCoordinates, 
                                               this.geoLocationError, 
                                               {enableHighAccuracy : true})
    }
  
  };
  
</script>