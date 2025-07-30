<script setup>
import DataTable from '@/components/DataTable.vue';
import VegaChart from '@/components/VegaChart.vue';
import { computed, ref, watch } from 'vue'
import { absoluteGrowth } from '@/vegaSpecs/absoluteGrowth';
import { stdDev, sum } from '@/main';

const loading = ref(false);
const kingdom = ref('79');
const errorMessage = ref(null);
const growthData = ref([]);
const growthChartData = ref([]);
const allianceGrowthData = ref([]);
const selectedPlayers = ref([]);

const prettyAllianceGrowth = computed(() => {
  return allianceGrowthData.value.map(x => {
    return {
      Alliance: x.Alliance,
      Players: x.PlayerCount,
      Power: `${Math.round(x.LastPower / 10000)/100} M`,
      Growth: `${Math.round(x.Growth / 10000)/100} M`,
      'Growth %': `${Math.round(x.GrowthPercent * 1000) / 10}%`,
    }
  });
});

const prettyGrowth = computed(() => {
  return growthData.value.map(x => {
    return {
      Alliance: x.Alliance,
      Player: nameKey(x),
      Power: `${Math.round(x.Power / 10000)/100} M`,
      Growth: `${Math.round(x.Growth / 10000)/100} M`,
      'Growth %': `${Math.round(x.GrowthPercent * 1000) / 10}%`,
    }
  });
});

const prettyGrowthChartData = computed(() => {
  return growthChartData.value
    .filter(x => selectedPlayers.value.includes(nameKey(x)))
    .map(x => {
    return {
      Date: new Date(x.Date).setHours(0, 0, 0),
      Power: x.Power,
      PlayerId: x.PlayerId,
      Name: x.Name,
      Rank: x.Rank,
      Alliance: x.Alliance,
    }
  });
});

const averageGrowthPercent = computed(() => sum(growthData.value, 'GrowthPercent') / growthData.value.length);
const stdDevGrowthPercent = computed(() => stdDev(growthData.value.map(x => x.GrowthPercent)));

async function fetchApiUrl(url, parameters) {
    let response = await fetch(`${import.meta.env.VITE_API_URL}${url}?${new URLSearchParams(parameters).toString()}`);
    if (response.ok) {
      return await response.json();
    }
    else {
        errorMessage.value = await response.text();
        return [];
    }
}

async function fetchData() {
    loading.value = true;

    let params = { kingdom: kingdom.value };

    fetchApiUrl('/rankings', params)
      .then(resp => growthChartData.value = resp);

    fetchApiUrl('/growth', params)
      .then(resp => growthData.value = resp);
      
    fetchApiUrl('/allianceGrowth', params)
      .then(resp => allianceGrowthData.value = resp);

    loading.value = false;
}

function nameKey(obj) {
  return `${obj.Name} (${obj.PlayerId})`;
}

watch(growthData, (data) => {
  selectedPlayers.value = data
    .filter(x => x.GrowthPercent > averageGrowthPercent.value + stdDevGrowthPercent.value)
    .map(nameKey);
});

fetchData();

</script>

<template>

<div class="header">
  <img class="header-image" src="/shitshot.png" />
  <h1>ShotHole</h1>
</div>

<div class="row">
  <div class="col">
    <div v-if="loading" class="d-flex align-items-center justify-content-center">
      Loading
      <div class="spinner-border text-primary ms-2" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
    </div>
  </div>
</div>

<div class="row">
  <div class="graph-row">
    <div class="pt-2">
      <h4>Player Growth ({{ Math.round(averageGrowthPercent * 1000) / 10 }}% Avg {{ Math.round(stdDevGrowthPercent * 1000) / 10 }}% Std Dev)</h4>
      <div class="data-table">
        <DataTable v-model="selectedPlayers" :data="prettyGrowth" default-sort="Growth %" :numeric-columns="['Growth %', 'Growth', 'Power']" key-name="Player" />
      </div>
    </div>

    <div class="pt-2">
      <h4>Alliance Growth</h4>
      <div class="col-auto data-table">
        <DataTable :data="prettyAllianceGrowth" default-sort="Growth %" :numeric-columns="['Growth %', 'Growth', 'Power']" key-name="Alliance" />
      </div>
    </div>
  </div>
</div>

<div class="row pt-4">
  <div class="col">
    <h4>Player Growth Over Time</h4>
    <VegaChart :data="prettyGrowthChartData" :spec="absoluteGrowth" height="1000px" />
  </div>
</div>

</template>

<style scoped>

h1 {
  margin-bottom: 0px;
}

.header-image {
  height: 48px;
}

.graph-row {
  display: flex;
  justify-content: space-around;
  flex-wrap: wrap;
}

.data-table {
  max-height: 512px;
  overflow: scroll;
  border-radius: 5px;
}

.header {
  display: flex;
  justify-content: center;
  padding-top: 8px;
}

</style>
