<script setup>

import { useAuthStore } from '@/stores/auth';
import { ref, watch } from 'vue';

const auth = useAuthStore();
const secret = ref(null);

watch(secret, () => auth.authenticate(secret.value));

</script>

<template>

<div id="authbox">
  <div id="inputWrapper">
    <input v-model="secret" type="text" class="form-control" placeholder="Secret phrase?">
  </div>
</div>

</template>

<style scoped>

#authbox {
  display: flex;
  align-items: center;
  justify-content: center;
  padding-top: 32px;
  max-width: 100%;
}

input {
  width: 100%;
}

#inputWrapper {
  width: 100%;
  max-width: 500px;
}

</style>