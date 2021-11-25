<template>
  <div>
    Main:
    <Complaint/>
  </div>
</template>

<script>
import Complaint from './components/Complaint.vue'


export default {
  components: { Complaint },
  name: 'App',
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
