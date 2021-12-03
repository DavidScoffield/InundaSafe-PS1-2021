<template>

    <!-- Barra de navegación para puntos de encuentro -->
    <nav aria-label="Meeting points page navigation">
        <ul class="pagination justify-content-center">
            <li v-if="meetingPoints.pagina > 1" class="page-item">
                <button class="page-link" tabindex="-1" @click="fetchMeetingPointPage(meetingPoints.pagina - 1)">Anterior</button>
            </li>
            <li v-else class="page-item disabled">
                <button class="page-link" tabindex="-1">Anterior</button>
            </li>
            <li v-for="page in [...Array(meetingPoints.paginas).keys()]" :key="page" class="page-item"
                v-bind:class="{ active : meetingPoints.pagina == page + 1 }">
                <button class="page-link" @click="fetchMeetingPointPage(page + 1)">{{ page + 1 }}</button>
            </li>
            <li v-if="meetingPoints.pagina < meetingPoints.paginas" class="page-item">
                <button class="page-link" @click="fetchMeetingPointPage(meetingPoints.pagina + 1)">Siguiente</button>
            </li>
            <li v-else class="page-item disabled">
                <button class="page-link">Siguiente</button>
            </li>
        </ul>
    </nav>

</template>

<script>

    export default {
        name: "MeetingPointNavigationBar",

        props: ["meetingPoints", 
                "fetchMeetingPointPage"],
    }
    
</script>