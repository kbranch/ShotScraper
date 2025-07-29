<script setup>

import { computed, onMounted, ref, watch } from 'vue';
import embed from 'vega-embed'

const props = defineProps({
  spec: {
    default: null,
  },
  data: {
    default: null,
  },
  width: {
    default: '100%',
  },
  height: {
    default: '500px',
  },
});

const graphDiv = ref(null);

const finalSpec = computed(() => {
  let specCopy = structuredClone(props.spec);
  specCopy.data = {
    values: props.data ? props.data : [],
    // "format": {"parse": {"date": "date"}}
  }

  return specCopy;
});

onMounted(() => {
  updateGraph(finalSpec.value);
});

watch(finalSpec, updateGraph);

function updateGraph(newSpec) {
  if (!graphDiv.value || !props.data || props.data.length == 0) return;

  let opts = {
    width: graphDiv.value.clientWidth,
    height: graphDiv.value.clientHeight,
    config: {
      background: "#212529",
      axis: {
        labelColor: "white",
        titleColor: "white",
      },
    },
    actions: false,
  }

  embed(graphDiv.value, newSpec, opts);
}

</script>

<template>

<div v-show="data" ref="graphDiv" class="graph"></div>

</template>

<style scoped>

.graph {
  width: v-bind(width);
  height: v-bind(height);
  border-radius: 5px;
  overflow: hidden;
}

</style>