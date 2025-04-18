<script setup>
    import Header_1 from './Components/Header.vue';
    import Footer_1 from './Components/Footer.vue'
</script>

<template>
<div class="app"></div>
<Header_1 />
<main>
      <router-view></router-view>
</main>
<Footer_1 />
</template>

<style>
.app {
  display: flex;
  flex-direction: column;
}
main {
  flex: 1; /* Растягивает main на всё доступное пространство */
}
</style>
