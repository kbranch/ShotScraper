<script setup>
import DataTable from '@/components/DataTable.vue';
import VegaChart from '@/components/VegaChart.vue';
import { computed, ref } from 'vue'
import { absoluteGrowth } from '@/vegaSpecs/absoluteGrowth';

const growthChartData = ref([]);
const loading = ref(false);
const errorMessage = ref(null);
const kingdom = ref('79');
const growthData = ref([]);
const allianceGrowthData = ref([]);

const prettyAllianceGrowth = computed(() => {
  return allianceGrowthData.value.map(x => {
    return {
      Alliance: x.Alliance,
      Players: x.PlayerCount,
      Growth: `${Math.round(x.Growth / 10000)/100} M`,
      'Growth %': `${Math.round(x.GrowthPercent * 1000) / 10}%`,
    }
  });
});

const prettyGrowth = computed(() => {
  return growthData.value.map(x => {
    return {
      Alliance: x.Alliance,
      Player: `${x.Name} (${x.PlayerId})`,
      Growth: `${Math.round(x.Growth / 10000)/100} M`,
      'Growth %': `${Math.round(x.GrowthPercent * 1000) / 10}%`,
    }
  });
});

const prettyGrowthChartData = computed(() => {
  return growthChartData.value.map(x => {
    return {
      Date: new Date(x.Date).setHours(0, 0, 0, 0),
      Power: x.Power,
      PlayerId: x.PlayerId,
      Name: x.Name,
      Rank: x.Rank,
      Alliance: x.Alliance,
    }
  });
});

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
    let rankings = await fetchApiUrl('/rankings', params);

    growthChartData.value = rankings;

    growthData.value = await fetchApiUrl('/growth', params);
    allianceGrowthData.value = await fetchApiUrl('/allianceGrowth', params);

    loading.value = false;
}

fetchData();

</script>

<template>

<div class="header">
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
      <h4>Player Growth</h4>
      <div class="data-table">
        <DataTable :data="prettyGrowth" default-sort="Growth %" :numeric-columns="['Growth %', 'Growth']" key-name="Name" />
      </div>
    </div>

    <div class="pt-2">
      <h4>Alliance Growth</h4>
      <div class="col-auto data-table">
        <DataTable :data="prettyAllianceGrowth" default-sort="Growth %" :numeric-columns="['Growth %', 'Growth']" key-name="Alliance" />
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
}

</style>
