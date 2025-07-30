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

export function sum(items, prop) {
  return items?.reduce((a, b) => {
      return a + b[prop];
  }, 0);
}

export function stdDev(array) {
  if (array.length == 0) { return 0; }

  const n = array.length;
  const mean = array.reduce((a, b) => a + b) / n;

  return Math.sqrt(array.map(x => Math.pow(x - mean, 2)).reduce((a, b) => a + b) / n);
}