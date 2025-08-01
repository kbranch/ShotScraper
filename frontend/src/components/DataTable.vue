<script setup>

import { computed, ref } from 'vue';
import { sortByKey } from '@/main';

const model = defineModel();
const props = defineProps(['data', 'numericColumns', 'defaultSort', 'keyName']);

const sortCol = ref(props.defaultSort);
const sortAsc = ref(false);

const cursor = computed(() => model.value ? 'pointer' : 'default');

const cols = computed(() => {
  if ((props.data?.length ?? 0) == 0) {
    return [];
  }

  let firstRow = props.data[0]

  return Object.keys(firstRow).filter(col => !props.columns || props.columns.includes(col));
});

const sortedData = computed(() => {
  let result = sortByKey(props.data, sortFunc, sortAsc.value);
  return [...result];
});

function sortFunc(row) {
  let value = row[sortCol.value];

  if (props.numericColumns?.includes(sortCol.value)) {
    value = Number(value.replace(/[^\d-.]/g,''));
  }

  return value;
}

function sortColumn(col) {
  if (sortCol.value == col) {
    sortAsc.value = !sortAsc.value;
  }
  else {
    sortCol.value = col;
    sortAsc.value = false;
  }
}

function toggleSelected(row) {
  if (!model.value) { return; }

  let key = row[props.keyName];
  if (model.value.includes(key)) {
    model.value.splice(model.value.indexOf(key), 1);
  }
  else {
    model.value.push(key);
  }
}

</script>

<template>

<table class="table table-dark">
  <thead>
    <tr>
      <th v-for="col in cols" :key="col" :class="{'sort-pad': col != sortCol}" @click="sortColumn(col)">
        {{ col }}
        <img class="invert" v-if="col == sortCol" :src="sortAsc ? '/caret-up-fill.svg' : '/caret-down-fill.svg'" />
      </th>
    </tr>
  </thead>

  <tbody>
    <tr v-for="row in sortedData" :key="row[keyName]" @click="toggleSelected(row)">
      <td v-for="col in cols" :key="row[col]" :class="{ selected: model?.includes(row[keyName]) }">{{ row[col] }}</td>
    </tr>
  </tbody>
</table>

</template>

<style scoped>

.selected {
  background-color: rgba(180, 180, 255, 0.125);
}

table {
  width: 100%;
  position: relative;
}

table thead th {
  position: sticky;
  top: 0;
}

table th:first-child, table tr td:first-child {
	border-radius: 5px 0px 0px 5px;
}

table th:last-child, table tr td:last-child {
	border-radius: 0px 5px 5px 0px;
}

th {
  background-color: var(--color-background-heading) !important;
  color: var(--color-heading) !important;
  cursor: pointer;
}

tr {
  border-radius: 5px;
  cursor: v-bind(cursor);
}

.sort-pad {
  padding-right: 27.6px;
}

</style>