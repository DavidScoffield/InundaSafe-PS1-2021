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
                <th scope="row">{{ evacuationRoute.nombre }}</th>  
                <th scope="row">{{ evacuationRoute.descripcion }}</th>
            </tr>
        </tbody>
    </table>

</template>

<script>

    export default {
        name: "EvacuationRouteTable",

        props: ["evacuationRoutes"]
    }
    
</script>