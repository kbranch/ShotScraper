<script setup>

import { RouterView } from 'vue-router'
import { useAuthStore } from './stores/auth';
import AuthView from './views/AuthView.vue';

const auth = useAuthStore();

</script>

<template>
  <AuthView v-if="!auth.authenticated" />
  <RouterView v-else />
</template>

<style>

.invert {
  filter: invert(1);
}

</style>

<style scoped>
</style>
