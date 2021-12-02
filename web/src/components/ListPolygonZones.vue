<template>
  <div v-for="zone in floodZones.zonas" :key="zone.id">
    <PolygonZone :zone="zone" />
  </div>
</template>

<script>
import PolygonZone from "./PolygonZone.vue";

export default {
  name: "ListPolygonZones",

  components: {
    PolygonZone,
  },

  props: ["floodZones"],
};
</script>

<style>
</style>