<template>
  <div class="container-fluid px-0 mb-3 text-center">
    <div class="welcome">
      <div>
        <h1 style="color: black; font-weight: 600">Bienvenido a InundaSafe</h1>
        <p class="mx-5" style="color: black; font-weight: 600">
          En este sitio podras acceder a toda la información necesaria conocer
          las zonas con peligro de inundación y las acciones a llevar a cabo en
          caso de suceder tal evento, como los puntos de encuentro en cada
          sector y los recorridos de evacuación cercanos a tu localidad. Si
          conoces un lugar con problemas escribe una denuncia y la atenderemos
          cuanto antes.
        </p>
      </div>
    </div>

    <hr class="my-4" />

    <div class="container">
      <div class="d-flex flex-wrap gap-4 justify-content-center">
        <div class="d-flex justify-content-center">
          <div class="card" style="width: 23rem">
            <router-link
              to="/complaints"
              style="text-decoration: none; color: inherit"
            >
              <img
                height="230"
                class="card-img-top"
                :src="imagenDenuncias"
                alt="Imagen de denuncias"
              />
              <div class="card-body">
                <h5 class="card-title">Denuncias</h5>
                <p class="card-text">
                  Ayudanos a prevenir emergencias realizando denuncias sobre
                  puntos peligrosos de la ciudad
                </p>
              </div>
            </router-link>
            <router-link class="button-gradient btn w-50 mx-auto my-1" to="/newComplaint"
              >Nueva denuncia</router-link
            >
          </div>
        </div>

        <div class="d-flex justify-content-center">
          <div class="card" style="width: 23rem">
            <router-link
              to="/zonas-inundables"
              style="text-decoration: none; color: inherit"
            >
              <img
                height="230"
                class="card-img-top"
                :src="imagenZonasInundables"
                alt="Imagen de zonas inundables"
              />
              <div class="card-body">
                <h5 class="card-title">Zonas Inundables</h5>
                <p class="card-text">
                  Conoce las zonas peligrosas de la ciudad para estar informado
                  ante una emergencia
                </p>
              </div>
            </router-link>
          </div>
        </div>

        <div class="d-flex justify-content-center">
          <div class="card" style="width: 23rem">
            <router-link
              to="/puntos-recorridos"
              style="text-decoration: none; color: inherit"
            >
              <img
                height="230"
                class="card-img-top"
                :src="imagenRecorridos"
                alt="Imagen de recorridos de evacuación y puntos de encuentro"
              />
              <div class="card-body">
                <h5 class="card-title">
                  Puntos de Encuentro y Recorridos de evacuación
                </h5>
                <p class="card-text">
                  Puntos de encuentro para reunir grupos ante una emergencia y
                  recorridos para evacuar la zona de forma segura
                </p>
              </div>
            </router-link>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>


<script>
import imagenRecorridos from "../assets/icons/recorridos_y_puntos3.png";
import imagenZonasInundables from "../assets/icons/zonas_inundables_sin_texto.png";
import imagenDenuncias from "../assets/icons/Denuncias.png";

export default {
  data() {
    return {
      imagenRecorridos: imagenRecorridos,
      imagenZonasInundables: imagenZonasInundables,
      imagenDenuncias: imagenDenuncias,
    };
  },
};
</script>

<style scoped>

.welcome {
  padding-top: 30px;
  padding-bottom: 30px;
  margin-bottom: 30px;
  background: linear-gradient(
    82.45deg,
    var(--color-2) -44.21%,
    var(--color-1) 94.15%
  );
  opacity: 0.65;
}

.card {
  transition-property: transform, box-shadow;
  transition-duration: 0.3s;
  transition-timing-function: ease-in-out;
  min-width: 100%;
}

.card:hover {
  box-shadow: 0px 0px 13px 7px rgba(175, 175, 175, 0.329);
  transform: scale(1.05);
  z-index: 100;
}
/* } */
</style>