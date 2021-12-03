<template>

    <!-- Tabla de puntos de encuentro -->
    <table class="table table-striped">
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
                <th scope="row" style="cursor: pointer"
                    @click="placeMarker([meetingPoint.coordenada.lat, 
                                         meetingPoint.coordenada.long])">
                    {{ meetingPoint.nombre }}
                </th>  
                <td scope="row">{{ meetingPoint.direccion }}</td> 
            </tr>
        </tbody>
    </table>

</template>

<script>

    export default {
        name: "MeetingPointTable",

        props: ["meetingPoints", "placeMarker"]
    }
    
</script>