<script setup>

import { computed, ref } from 'vue';
import { sortByKey } from '@/main';

const props = defineProps(['data', 'numericColumns', 'defaultSort']);

const sortCol = ref(props.defaultSort);
const sortAsc = ref(false);

const cols = computed(() => {
  if ((props.data?.length ?? 0) == 0) {
    return [];
  }

  let firstRow = props.data[0]

  return Object.keys(firstRow).filter(col => !props.columns || props.columns.includes(col));
});

const sortedData = computed(() => {
  return sortByKey(props.data, sortFunc, sortAsc.value);
});

function sortFunc(row) {
  let value = row[sortCol.value];

  if (props.numericColumns?.includes(sortCol.value)) {
    value = Number(value.replace(/\D/g,''));
  }

  return value;
}

</script>

<template>

<table class="table">
  <thead>
    <tr>
      <th  v-for="col in cols" :key="col" scope="col">{{ col }}</th>
    </tr>
  </thead>

  <tbody>
    <tr v-for="row in sortedData" :key="row">
      <td v-for="col in cols" :key="col">{{ row[col] }}</td>
    </tr>
  </tbody>
</table>

</template>

<style scoped>
</style>