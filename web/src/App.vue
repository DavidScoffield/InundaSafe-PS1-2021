<template>
  <!-- NAVBAR -->
  <Navbar />
  <!-- CONTENT -->
  <div class="w-100 content-center">
    <router-view />
  </div>
  <!-- FOOTER -->
  <Footer />
</template>

<script>
import Navbar from "./components/Navbar.vue";
import Footer from "./components/Footer.vue";

export default {
  name: "App",

  components: {
    Navbar,
    Footer,
  },

  data() {
    return {
      colors: [],
    };
  },
  created() {
    console.log(`${process.env.VUE_APP_BASE_URL}/colors`);
    fetch(`${process.env.VUE_APP_BASE_URL}/colors`)
      .then((response) => {
        //let myRules = document.styleSheets[4].cssRules; //nuestra hoja de estilos personalizada (button-gradient, ...)
        //console.log(myRules);
        return response.json();
      })
      .then((json) => {
        this.colors = json;

        document.documentElement.style.setProperty(
          "--color-1",
          this.colors.color_1
        );
        document.documentElement.style.setProperty(
          "--color-2",
          this.colors.color_2
        );
        document.documentElement.style.setProperty(
          "--color-3",
          this.colors.color_3
        );
        document.documentElement.style.setProperty(
          "--color-4",
          this.colors.color_4
        );
        document.documentElement.style.setProperty(
          "--color-5",
          this.colors.color_5
        );
      })
      .catch((e) => {
        console.log("CATCH!");
        console.log(e);
        console.log(this.colors);
      });
  },
};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  display: flex;
  flex-wrap: wrap;
  flex-direction: column;
  min-height: 100vh;
}
</style>
