<template>
  <button
    class="button-installer btn"
    :style="{ display: installBtn }"
    @click="installer()"
  >
    Instalar!
  </button>
</template>

<script>
export default {
  data() {
    return {
      installBtn: "block",
      installer: undefined,
    };
  },
  created() {
    let installPrompt = null;

    window.addEventListener("beforeinstallprompt", (e) => {
      e.preventDefault();
      installPrompt = e;
      this.installBtn = "block";
    });

    this.installBtn = installPrompt ? "block" : "none";

    this.installer = () => {
      installPrompt.prompt();
      installPrompt.userChoice.then((result) => {
        if (result.outcome === "accepted") {
          this.installBtn = "none";
          console.log("Install accepted!");
        } else {
          this.installBtn = "block";
          console.log("Install denied!");
        }
      });
    };
  },
};
</script>


<style>
.button-installer {
  margin: 0 auto;
  width: 150px;
  background: white !important;
  outline: 3px solid var(--color-2) !important;
  box-shadow: 4px 4px 23px rgba(0, 0, 0, 0.25) !important;
  border-radius: 6px !important;
  border: none !important;
  color: var(--color-2) !important;
}
</style>
