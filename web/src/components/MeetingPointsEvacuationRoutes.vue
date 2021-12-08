<template >

  <div style="height: auto; width: 85%; margin: auto;">
    
    <div class="d-flex justify-content-between">
      <Title>Puntos de encuentro y recorridos de evacuación</Title>
        <router-link class="button-gradient btn my-auto w-auto" style="white-space: nowrap" to="/newComplaint"
          >Nueva denuncia</router-link
        >
    </div>

    <p v-show="errorMessaje" style="color:red">{{errorMessaje}}</p>

    <p v-show="successMessage" style="color:green">{{successMessage}}</p>

    <p v-if="!fetchedMeetingPoints || !fetchedEvacuationRoutes">Cargando mapa...
       <img style='height: 50px; width: 70px' src='../assets/icons/loading.gif'> </p>

    <l-map style="height: 500px" :zoom="zoom" :key="map" :center="markerCoordinates ? markerCoordinates :
                                      (userLatLong ? [userLatLong.lat, userLatLong.long] : center)" >

      <l-tile-layer :url="url"/>

      <!-- Marcador de la ubicación del usuario o ubicación por defecto -->
      <l-marker :lat-lng="userLatLong ? [userLatLong.lat, userLatLong.long] : center">

          <l-icon :icon-url="require('../assets/icons/initial_location.png')"
                  :icon-size="[20, 30]"/>

          <l-popup :options="{ maxHeight: 350 }">
            <strong>Mi ubicación</strong> {{userLatLong ? "(GPS)" : "(default)"}}
          </l-popup>
          
      </l-marker>

      <l-control position="bottomleft" >
        <button type="button" class="btn btn-success" @click="reCenterMap()">
          Centrar
        </button>
      </l-control>

      <!-- Marcador para referencias  -->
      <l-marker v-if="pendingMarkers > 0" :lat-lng="markerCoordinates">

          <l-icon :icon-url="require('../assets/icons/circle.png')"
                  :icon-size="[40, 60]"/>
          
      </l-marker>


      <!-- Se dibujan los puntos de encuentro -->
      <MeetingPoint v-for="(meetingPoint, index) in meetingPoints.puntos_encuentro"
                    :key="index" :meetingPoint="meetingPoint"/>

      <!-- Se dibujan los recorridos de evacuación -->
      <EvacuationRoute v-for="(evacuationRoute, index) in evacuationRoutes.recorridos"
                       :key="index" :evacuationRoute="evacuationRoute"/>

    </l-map><br><br>    

    <div class="container">

        <div class="row">

            <div class="col-sm">

                <h3> <img style='height: 40px; width: 35px' src='../assets/icons/meeting_point.png'>
                      Puntos de encuentro {{userLatLong ? "cercanos al usuario" : ""}}</h3><br>

                <!-- Tabla de puntos de encuentro -->
                <MeetingPointTable v-if="fetchedMeetingPoints"
                                   :meetingPoints="meetingPoints"
                                   :placeMarker="placeMarker"/><br>

                <p v-if="!fetchedMeetingPoints">Buscando puntos de encuentro...<img style='height:50px; width:70px' src='../assets/icons/loading.gif'> </p>

                <!-- Barra de navegación para puntos de encuentro -->
                <MeetingPointNavigationBar v-if="meetingPoints.puntos_encuentro.length"
                                           :meetingPoints="meetingPoints"
                                           :fetchMeetingPointPage="fetchMeetingPointPage"/>

            </div>

            <div class="col-sm">

                <h3><img style='height: 40px; width: 35px' src='../assets/icons/evacuation_route_start.png'>
                    Recorridos de evacuación</h3><br>

                <!-- Tabla de recorridos de evacuación -->
                <EvacuationRouteTable v-if="fetchedEvacuationRoutes"
                                      :evacuationRoutes="evacuationRoutes"
                                      :placeMarker="placeMarker"/><br>

                <p v-if="!fetchedEvacuationRoutes">Buscando recorridos de evacuación...<img style='height:50px; width:70px' src='../assets/icons/loading.gif'> </p>

                <!-- Barra de navegación para recorridos de evacuación -->
                <EvacuationRouteNavigationBar v-if="evacuationRoutes.recorridos.length"
                                              :evacuationRoutes="evacuationRoutes" 
                                              :fetchEvacuationRoutePage="fetchEvacuationRoutePage"/>

            </div>

        </div>

    </div>

  </div>

</template>

<script>

  import { latLng } from "leaflet";
  import { LMap, LTileLayer, LMarker, LPopup, LIcon, LControl } from "@vue-leaflet/vue-leaflet";
  import Title from "./Title.vue";
  import MeetingPoint from "./meeting-point/MeetingPoint.vue";
  import MeetingPointTable from "./meeting-point/MeetingPointTable.vue";
  import MeetingPointNavigationBar from "./meeting-point/MeetingPointNavigationBar.vue";
  import EvacuationRoute from "./evacuation-route/EvacuationRoute.vue";
  import EvacuationRouteTable from "./evacuation-route/EvacuationRouteTable.vue";
  import EvacuationRouteNavigationBar from "./evacuation-route/EvacuationRouteNavigationBar.vue";

  export default {
  
    name: "MeetingPointsEvacuationRoutes",
  
    components: {
      LMap,
      LTileLayer,
      Title,
      MeetingPoint,
      MeetingPointTable,
      MeetingPointNavigationBar,
      EvacuationRoute,
      EvacuationRouteTable,
      EvacuationRouteNavigationBar,
      LMarker,
      LPopup,
      LIcon,
      LControl
    },
  
    data() {
      return {
        zoom: 12.5,
        center: latLng(-34.9213, -57.9545),
        url: 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
        map: 0,
        meetingPoints: { puntos_encuentro : [] },
        evacuationRoutes: { recorridos : [] },
        fetchedMeetingPoints: false,
        fetchedEvacuationRoutes: false,
        userLatLong: null,
        errorMessaje: "",
        successMessage: "",
        pendingMarkers: 0,
        markerCoordinates: null
      };
    },
  
    methods: {
  
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
  
      setUserCoordinates(position) {
        // función que setea las coordenadas del usuario en caso de que 
        // se las haya podido obtener de forma correcta
        
        this.userLatLong = { lat : position.coords.latitude,
                             long : position.coords.longitude }

        this.fetchMeetingPointPage(1)

        this.successMessage = "Mostrando los puntos de encuentro más cercanos a la ubicación del usuario"
        setTimeout(() => this.successMessage = "", 10000)
      }, 

      geoLocationError(error, message="", timeout=7000) {
        // función que se ejecuta en caso de que el usuario no haya aceptado
        // proveer su ubicación o haya ocurrido algún error al tratar de accederla

        if (message) {
          this.errorMessaje = message
        } else if (error.code == 1) {
          this.errorMessaje = "El usuario no aceptó conocer su ubicación" 
        } else {
          this.errorMessaje = "Ocurrió un error inesperado al tratar de obtener su ubicación, por favor, inténtelo nuevamente"
        }

        setTimeout(() => this.errorMessaje = "", timeout)
      },

      placeMarker(coordinates) {
        // posiciona un marcador de referencia por 5 segundos

        this.markerCoordinates = coordinates
        this.pendingMarkers += 1
        setTimeout(() => this.pendingMarkers -= 1, 5000)
      },

      reCenterMap() {
        // reubica el centro del mapa

        this.markerCoordinates = this.userLatLong ? [this.userLatLong.lat, this.userLatLong.long] : this.center
        this.map += 1
      }
  
    },
  
    created() {
      // hook created donde se consulta por la ubicación del usuario
      // y se cargan los puntos de encuentro y recorridos de evacuación
      // con la información de la primer página de los listados

      this.fetchMeetingPointPage(1)
      this.fetchEvacuationRoutePage(1)

      if ("geolocation" in navigator) {
        /* la geolocalización está disponible */
        navigator.geolocation.getCurrentPosition(this.setUserCoordinates, 
                                                 this.geoLocationError, 
                                                 {enableHighAccuracy: true,
                                                  timeout: 8000, maximumAge: 0})
      } else {
        /* la geolocalización no está disponible */
        this.geoLocationError(4, "Su dispositivo no soporta la geolocalización, la ubicación por defecto es el centro de La Plata", 13000)
      }      
    },
  };
  
</script>
