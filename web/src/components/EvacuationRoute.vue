<template>

    <!-- Se dibuja el recorrido de evacuación -->
    <l-polyline :lat-lngs="getCoordinateList(evacuationRoute.coordenadas)" :color="randomColor()">
    
    <!-- Marcador de inicio del recorrido -->
    <l-marker :lat-lng="[evacuationRoute.coordenadas[0].lat, evacuationRoute.coordenadas[0].long]">

        <l-icon :icon-url="require('../assets/icons/evacuation_route_start.png')"
                :icon-size="[35, 45]"/>

        <l-popup :options="{ maxHeight: 350 }">
            <p style="color:green; text-align:center">Recorrido de evacuación</p>
            <strong>Nombre:</strong> {{evacuationRoute.nombre}}<br>
            <p style="display:inline-block" v-show="showDescription">
            <strong> Descripción: </strong> {{evacuationRoute.descripcion}}
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

</template>

<script>

    import { LPopup, LMarker, LIcon, LPolyline } from "@vue-leaflet/vue-leaflet";

    export default {
        name: "EvacuationRoute",

        components: {
            LPopup,
            LMarker,
            LIcon,
            LPolyline
        },

        props: ["evacuationRoute"],

        data() {
            return {
                showDescription: false
            }
        },

        methods: {
            randomColor() {
                // retorna un color aleatorio para marcar el recorrido de evacuación
                var colors = [ "#8B008B", "#3221a5", "#7B68EE", 
                                "#FF4500", "#5F9EA0", "#8B4513", 
                                "#32CD32", "#8A2BE2", "#2160d3" ]

                return colors[Math.floor(Math.random()*colors.length)]
            },

            getCoordinateList(coordinates) {
                // retorna un listado con las coordenadas (lat, long) del recorrido de evacuación

                var coordinateList = []
                for (var latLong of coordinates) {
                    coordinateList.push([latLong.lat, latLong.long])
                }
                return coordinateList
            },

            
            getEvacuationRouteEndPoint(coordinates) {
                // retorna el último punto del recorrido de evacuación

                return [coordinates[coordinates.length - 1].lat, coordinates[coordinates.length - 1].long]
            },

            innerClick() {
                // oculta o muestra la descripción del recorrido de evacuación

                this.showDescription = !this.showDescription;
            },
        }
    }
    
</script>