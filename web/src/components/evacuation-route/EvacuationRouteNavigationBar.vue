<template>

    <!-- Barra de navegación para recorridos de evacuación -->
    <nav aria-label="Evacuation route page navigation">
        <ul class="pagination justify-content-center">
            <li v-if="evacuationRoutes.pagina > 1" class="page-item">
                <button class="page-link" tabindex="-1" @click="fetchEvacuationRoutePage(evacuationRoutes.pagina - 1)">Anterior</button>
            </li>
            <li v-else class="page-item disabled">
                <button class="page-link" tabindex="-1">Anterior</button>
            </li>
            <li v-for="page in [...Array(evacuationRoutes.paginas).keys()]" :key="page" class="page-item"
                v-bind:class="{ active : evacuationRoutes.pagina == page + 1 }">
                <button class="page-link" @click="fetchEvacuationRoutePage(page + 1)">{{ page + 1 }}</button>
            </li>
            <li v-if="evacuationRoutes.pagina < evacuationRoutes.paginas" class="page-item">
                <button class="page-link" @click="fetchEvacuationRoutePage(evacuationRoutes.pagina + 1)">Siguiente</button>
            </li>
            <li v-else class="page-item disabled">
                <button class="page-link">Siguiente</button>
            </li>
        </ul>
    </nav>

</template>

<script>

    export default {
        name: "EvacuationRouteNavigationBar",

        props: ["evacuationRoutes", 
                "fetchEvacuationRoutePage"],
    }
    
</script>