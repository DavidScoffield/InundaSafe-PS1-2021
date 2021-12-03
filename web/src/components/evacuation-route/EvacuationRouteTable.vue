<template>

    <!-- Tabla de recorridos de evacuación -->
    <table class="table table-striped">
        <thead>
            <tr>
                <th>{{evacuationRoutes.recorridos.length ? "Nombre" : "No se encontraron recorridos de evacuación"}}</th>
                <th v-if="evacuationRoutes.recorridos.length">Descripción</th>
            </tr>
        </thead>

        <tbody>
            <tr v-for="(evacuationRoute, index) in evacuationRoutes.recorridos" :key="index">
                <th scope="row" style="cursor: pointer"
                    @click="placeMarker([evacuationRoute.coordenadas[0].lat, 
                                         evacuationRoute.coordenadas[0].long])">
                    {{ evacuationRoute.nombre }}
                </th>  
                <td scope="row">{{ evacuationRoute.descripcion }}</td>
            </tr>
        </tbody>
    </table>

</template>

<script>

    export default {
        name: "EvacuationRouteTable",

        props: ["evacuationRoutes", "placeMarker"]
    }
    
</script>