<template>
  <router-link
    :to="'/' + to"
    v-slot="{ href, navigate, isActive, isExactActive }"
    custom
  >
    <a
      :href="href"
      @click="navigate"
      :class="[
        'nav-link',
        isActive && 'active',
        isExactActive && 'router-link-exact-active',
      ]"
    >
      <slot></slot
    ></a>
  </router-link>
</template>

<script>
export default {
  name: "NavLink",
  props: ["to"],
};
</script>
