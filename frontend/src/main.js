import 'bootstrap'
import 'bootstrap/dist/css/bootstrap.min.css'
import './assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'

const app = createApp(App)

app.use(createPinia())
app.use(router)

app.mount('#app')

function compare(a, b) {
  if (a > b) {
      return 1
  } else if (a < b) {
      return -1
  } else {
      return 0
  }
}

// JS defaults to converting arrays to strings when comparing
function compareArrays(a, b) {
  for (let i = 0; i < a.length; i++) {
    const result = compare(a[i], b[i]);
    if (result !== 0) {
      return result;
    }
  }

  return 0;
}

export function sortByKey(arr, key, sortAsc = true) {
  let result = arr.sort((a, b) => Array.isArray(key(a)) ? compareArrays(key(a), key(b)) : compare(key(a), key(b)));
  return sortAsc ? result : result.reverse();
}