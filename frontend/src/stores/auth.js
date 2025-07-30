import { ref, computed } from 'vue'
import { defineStore } from 'pinia'

export const useAuthStore = defineStore('auth', () => {
  const secret = ref(localStorage.getItem('secret'));
  const authenticated = computed(() => {
    let correctSecret = import.meta.env.VITE_SECRET_WORD;
    return secret.value == correctSecret;
  });

  function authenticate(value) {
    if (value == import.meta.env.VITE_SECRET_WORD) {
      localStorage.setItem('secret', value);
      secret.value = value;

      return true;
    }

    return false;
  }

  return { authenticated, authenticate };
})
