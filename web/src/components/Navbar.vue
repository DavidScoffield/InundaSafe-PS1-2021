<template>
  <div id="nav" style="display: inline">
    <nav class="navbar navbar-expand-lg navbar-light navbar-gradient fixed-top">
      <div class="container-fluid">
        <div>
          <router-link
            to="/"
            exact
            class="navbar-brand font-weight-bold d-flex align-items-center"
          >
            <img
              :src="logoApp"
              alt="Logo de la aplicación"
              style="width: 32px; height: 32px; margin-right: 5px"
            />
            <strong> InundaSafe - Pública </strong>
          </router-link>
        </div>
        <button
          class="navbar-toggler"
          type="button"
          data-bs-toggle="collapse"
          data-bs-target="#navbarSupportedContent"
          aria-controls="navbarSupportedContent"
          :aria-expanded="false"
          aria-label="Toggle navigation"
        >
          <span class="navbar-toggler-icon"></span>
        </button>
        <div
          class="collapse navbar-collapse row justify-content-between"
          id="navbarSupportedContent"
        >
          <ul
            class="navbar-nav col-12 col-lg-auto d-flex align-items-start"
            style="margin-left: 15px"
          >
            <li class="nav-item" v-for="url in urls" :key="url.label">
              <NavLink :to="url.to">{{ url.label }}</NavLink>
            </li>
          </ul>
          <div class="btn-group col-auto">
            <a
              type="button"
              href="https://admin-grupo24.proyecto2021.linti.unlp.edu.ar/"
              target="_blank"
              class="btn button-gradient"
            >
              <i class="fa fa-user pr-2"></i> Iniciar Sesión
            </a>
          </div>
        </div>
      </div>
    </nav>
  </div>
</template>

<script>
import logoApp from "../assets/logo.png";
import NavLink from "../components/NavLink.vue";

export default {
  name: "Navbar",

  components: {
    NavLink,
  },

  data() {
    return {
      logoApp: logoApp,
      urls: [
        {
          label: "Denuncias",
          to: "complaints",
        },
        {
          label: "Zonas inundables",
          to: "zonas-inundables",
        },
        {
          label: "Puntos de encuentro y recorridos de evacuación",
          to: "puntos-recorridos",
        },
      ],
    };
  },
};
</script>

<style scoped>
.navbar-gradient {
  background-color: var(--color-3) !important;
  box-shadow: 0px 0px 23px rgba(0, 0, 0, 0.25) !important;
  border-bottom-left-radius: 15px;
  border-bottom-right-radius: 15px;
}
</style>