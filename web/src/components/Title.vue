<template>
  <div class="d-flex align-items-center container my-4 mx-auto">
    <!-- @click="hasHistory() ? $router.go(-1) : $router.push('/')" -->
    <button
      type="button"
      @click="$router.push('/')"
      class="btn text-muted p-2 mr-5"
      title="Retroceder"
    >
      <i class="fa fa-arrow-left fa-lg"></i>
    </button>
    <h1>
      <slot></slot>
    </h1>
  </div>
</template>

<script>
export default {
  name: "Title",

  methods: {
    hasHistory() {
      return window.history.length > 2;
    },
  },
};
</script>

<style scoped>
h1 {
  font-weight: 700;
  margin: 0 0 0 15px;
}

/* .title {
  margin: 10px 0;
} */
</style>