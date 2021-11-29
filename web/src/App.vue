<template>
  <div>
    Main:
    <div id="nav" style="display: inline">
      <router-link to="/complaints">Denuncias</router-link>
    </div>
    <router-view />
  </div>
</template>

<script>

export default {
  name: 'App',
  data() { 
    return {
      colors: []
    }
  },
  created() {
    fetch("http://localhost:5000/api/colors")
      .then((response) => {
        //let myRules = document.styleSheets[4].cssRules; //nuestra hoja de estilos personalizada (button-gradient, ...)
        //console.log(myRules);
        return response.json();
      })
      .then((json) => {
        this.colors = json
      
        document.documentElement.style.setProperty('--color-1', this.colors.color_1);
        document.documentElement.style.setProperty('--color-2', this.colors.color_2);
        document.documentElement.style.setProperty('--color-3', this.colors.color_3);
        document.documentElement.style.setProperty('--color-4', this.colors.color_4);
        document.documentElement.style.setProperty('--color-5', this.colors.color_5);
      })
      .catch((e) => {
        console.log("CATCH!")
        console.log(e)
        console.log(this.colors)
      })
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
