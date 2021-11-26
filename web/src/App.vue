<template>
  <div>
    <FormNewComplaint/>
  </div>
</template>

<script>
import FormNewComplaint from './components/FormNewComplaint.vue'

export default {
  name: 'App',
  components: {
    FormNewComplaint
  }
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
