<template>
  <div id="app">
    <router-view></router-view>
  </div>
</template>

<script>
export default {
  created() {
    // Asigna el método logout a la instancia de Vue raíz
    this.$root.logout = this.logout; 
  },
  methods: {
    logout() {
      this.$store.dispatch('userLoggedOut');
      this.$router.push({ name: 'login' });
    },
  },
};
</script>