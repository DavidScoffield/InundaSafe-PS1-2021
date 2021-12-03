<template>

    <!-- Se dibuja el punto de encuentro -->
    <l-marker :lat-lng="[meetingPoint.coordenada.lat, meetingPoint.coordenada.long]">

        <l-icon :icon-url="require('../../assets/icons/meeting_point.png')"
                :icon-size="[30, 40]"/>

        <l-popup :options="{ maxHeight: 350 }">
            <p style="color:green; text-align:center">Punto de encuentro</p>
            <strong>Nombre:</strong> {{meetingPoint.nombre}}<br>
            <strong>Teléfono:</strong> {{meetingPoint.telefono}}<br>
            <strong>Dirección:</strong> {{meetingPoint.direccion}}<br>
            <strong>Email:</strong> {{meetingPoint.email}}<br>
        </l-popup>
    
    </l-marker>

</template>

<script>

    import { LPopup, LMarker, LIcon } from "@vue-leaflet/vue-leaflet";

    export default {
        name: "MeetingPoint",

        components: {
            LPopup,
            LMarker,
            LIcon
        },

        props: ["meetingPoint"]
    }
    
</script>