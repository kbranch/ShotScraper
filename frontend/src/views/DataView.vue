<script setup>
import DataTable from '@/components/DataTable.vue';
import VegaChart from '@/components/VegaChart.vue';
import { computed, ref } from 'vue'

const rawData = ref([]);
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

    rawData.value = rankings;

    growthData.value = await fetchApiUrl('/growth', params);
    allianceGrowthData.value = await fetchApiUrl('/allianceGrowth', params);

    loading.value = false;

    // updateGraph(spec.value);
}

const growthChartData = computed(() => {
  return rawData.value.map(x => {
    return {
      // date: new Date(x.Date),
      Date: new Date(x.Date),
      Power: x.Power,
      PlayerId: x.PlayerId,
      Name: x.Name,
      Rank: x.Rank,
      Alliance: x.Alliance,
    }
  });
});

const spec = computed(() => {
  return {
    $schema: "https://vega.github.io/schema/vega-lite/v6.json",
    description: "Multi-series line chart with labels and interactive highlight on hover.  We also set the selection's initial value to provide a better screenshot",
    width: "container",
    height: "container",
    transform: [],
    encoding: {
      x: {
        field: "Date",
        type: "temporal",
        title: "Date",
        axis: {
          grid: false,
        }
      },
      y: {
        field: "Power",
        type: "quantitative",
        title: "Power",
        axis: {
          labelExpr: "round(datum.value / 100000) / 10 + ' M'",
          grid: false,
        },
        scale: {
          // zero: false,
          nice: false,
          type: "log",
        },
      },
      color: {
        condition: {
          param: "hover",
          field: "PlayerId",
          type: "nominal",
          legend: null,
        },
        value: "transparent",
      },
      opacity: {
        condition: {
          param: "hover",
          value: 1,
        },
        value: 0.2,
      }
    },
    layer: [
      {
        description: "transparent layer to make it easier to trigger selection",
        params: [
          {
            name: "hover",
            select: {
              type: "point",
              fields: ["PlayerId"],
              on: "pointerover",
            }
          }
        ],
        mark: {
          type: "line",
          strokeWidth: 8,
          stroke: "transparent",
        }
      },
      {
        mark: "line",
      },
      {
        encoding: {
          x: {
            aggregate: "max",
            field: "Date",
          },
          y: {
            aggregate: { argmax: "Date" },
            field: "Power",
          }
        },
        layer: [
          {
            mark: {
              type: "text",
              align: "left",
              dx: 4,
            },
            encoding: {
              text: {
                field: "Name",
                type: "nominal",
              },
            },
          },
        ],
      }
    ],
    config: {
      view: {
        stroke: null,
      },
    },
  }
});

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
    <div>
      <h4>Player Growth</h4>
      <div class="data-table">
        <DataTable :data="prettyGrowth" default-sort="Growth %" :numeric-columns="['Growth %', 'Growth']" key-name="Name" />
      </div>
    </div>

    <div>
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
    <VegaChart :data="growthChartData" :spec="spec" height="1000px" />
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
  max-height: 500px;
  overflow: scroll;
  border-radius: 5px;
}

.header {
  display: flex;
  justify-content: center;
}

</style>
