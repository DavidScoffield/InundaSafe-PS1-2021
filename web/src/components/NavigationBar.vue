<template>

    <!-- Barra de navegación -->
    <nav>
        <ul class="pagination justify-content-center">
            <li v-if="items.pagina > 1" class="page-item">
                <button class="page-link" tabindex="-1" @click="fetchPage(items.pagina - 1)">Anterior</button>
            </li>
            <li v-else class="page-item disabled">
                <button class="page-link" tabindex="-1">Anterior</button>
            </li>
            <li v-for="page in [...Array(items.paginas).keys()]" :key="page" class="page-item"
                v-bind:class="{ active : items.pagina == page + 1 }">
                <button class="page-link" @click="fetchPage(page + 1)">{{ page + 1 }}</button>
            </li>
            <li v-if="items.pagina < items.paginas" class="page-item">
                <button class="page-link" @click="fetchPage(items.pagina + 1)">Siguiente</button>
            </li>
            <li v-else class="page-item disabled">
                <button class="page-link">Siguiente</button>
            </li>
        </ul>
    </nav>

</template>

<script>

    export default {
        name: "NavigationBar",

        props: ["items", 
                "fetchPage"],
    }
    
</script>