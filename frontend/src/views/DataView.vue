<script setup>
import DataTable from '@/components/DataTable.vue';
import embed from 'vega-embed'
import { computed, watch, ref, onMounted } from 'vue'

const graphDiv = ref(null);
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

function updateGraph(spec) {
  if (!graphDiv.value) return;

  let opts = {
    width: graphDiv.value.clientWidth,
    height: graphDiv.value.clientHeight,
  }

  embed('#graph', spec, opts);
}

const data = computed(() => {
  return rawData.value.map(x => {
    return {
      // date: new Date(x.Date),
      date: x.date,
      price: x.Power,
      symbol: x.PlayerId,
      // PlayerId: x.PlayerId,
      // Rank: x.Rank,
      // Alliance: x.Alliance,
    }
  });
});

const spec = computed(() => {
  return {
    $schema: "https://vega.github.io/schema/vega-lite/v6.json",
    description: "Multi-series line chart with labels and interactive highlight on hover.  We also set the selection's initial value to provide a better screenshot",
  //   "data": {
  //   "url": "data/stocks.csv",
  //   "format": {"parse": {"date": "date"}}
  // },
    data: {
      values: rawData.value ? rawData.value : [],
      // "format": {"parse": {"date": "date"}}
    },
    width: "container",
    height: "container",
  //   "layer": [
  //   {
  //     "params": [{
  //       "name": "index",
  //       "value": [{"x": {"year": 2005, "month": 1, "date": 1}}],
  //       "select": {
  //         "type": "point",
  //         "encodings": ["x"],
  //         "on": "pointerover",
  //         "nearest": true
  //       }
  //     }],
  //     "mark": "point",
  //     "encoding": {
  //       "x": {"field": "date", "type": "temporal", "axis": null},
  //       "opacity": {"value": 0}
  //     }
  //   },
  //   {
  //     "transform": [
  //       {
  //         "lookup": "symbol",
  //         "from": {"param": "index", "key": "symbol"}
  //       },
  //       {
  //         "calculate": "datum.index && datum.index.price > 0 ? (datum.price - datum.index.price)/datum.index.price : 0",
  //         "as": "indexed_price"
  //       }
  //     ],
  //     "mark": "line",
  //     "encoding": {
  //       "x": {"field": "date", "type": "temporal", "axis": null},
  //       "y": {
  //         "field": "indexed_price", "type": "quantitative",
  //         "axis": {"format": "%"}
  //       },
  //       "color": {"field": "symbol", "type": "nominal"}
  //     }
  //   },
  //   {
  //     "transform": [{"filter": {"param": "index"}}],
  //     "encoding": {
  //       "x": {"field": "date", "type": "temporal", "axis": null},
  //       "color": {"value": "firebrick"}
  //     },
  //     "layer": [
  //       {"mark": {"type": "rule", "strokeWidth": 0.5}},
  //       {
  //         "mark": {"type": "text", "align": "center", "fontWeight": 100},
  //         "encoding": {
  //           "text": {"field": "date", "timeUnit": "yearmonth"},
  //           "y": {"value": 310}
  //         }
  //       }
  //     ]
  //   }
  // ]

  //   layer: [
  //   {
  //     params: [{
  //       name: "index",
  //       // value: [{x: {year: 2005, month: 1, date: 1}}],
  //       select: {
  //         type: "point",
  //         encodings: ["x"],
  //         on: "pointerover",
  //         nearest: true
  //       }
  //     }],
  //     mark: "point",
  //     encoding: {
  //       x: {field: "Date", type: "temporal", axis: null},
  //       opacity: {value: 0}
  //     }
  //   },
  //   {
  //     transform: [
  //       {
  //         lookup: "Name",
  //         from: {param: "index", key: "Name"}
  //       },
  //       {
  //         calculate: "datum.index && datum.index.Power > 0 ? (datum.Power - datum.index.Power) / datum.index.Power : 0",
  //         as: "indexed_power"
  //       }
  //     ],
  //     mark: "line",
  //     encoding: {
  //       x: {field: "Date", type: "temporal", axis: null},
  //       y: {
  //         field: "indexed_power", type: "quantitative",
  //         axis: {format: "%"}
  //       },
  //       color: {field: "Name", type: "nominal"}
  //     }
  //   },
  //   {
  //     transform: [{filter: {param: "index"}}],
  //     encoding: {
  //       x: {field: "Date", type: "temporal", axis: null},
  //       color: {value: "firebrick"}
  //     },
  //     layer: [
  //       {mark: {type: "rule", strokeWidth: 0.5}},
  //       {
  //         mark: {type: "text", align: "center", fontWeight: 100},
  //         encoding: {
  //           text: {field: "Date", timeUnit: "day"},
  //           y: {value: 310}
  //         }
  //       }
  //     ]
  //   }
  // ]
    transform: [],
    encoding: {
      x: {
        field: "Date",
        type: "temporal",
        title: "Date",
      },
      y: {
        field: "Power",
        type: "quantitative",
        title: "Power",
        scale: {
          zero: false,
          nice: false,
          // type: "log",
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

onMounted(() => {
  embed('#graph', spec.value)
});

watch(spec, updateGraph);

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
    <div class="graph-wrapper pe-2">
      <h4>Player Growth</h4>
      <div class="data-table">
        <DataTable :data="prettyGrowth" default-sort="Growth %" :numeric-columns="['Growth %', 'Growth']" key-name="Name" />
      </div>
    </div>

    <div class="graph-wrapper">
      <h4>Alliance Growth</h4>
      <div class="col-auto data-table">
        <DataTable :data="prettyAllianceGrowth" default-sort="Growth %" :numeric-columns="['Growth %', 'Growth']" key-name="Alliance" />
      </div>
    </div>
  </div>
</div>

<div class="row">
  <div class="col">
    <div v-show="data" ref="graphDiv" id="graph"></div>
  </div>
</div>

</template>

<style scoped>

#graph {
  width: 100%;
  height: 1800px;
}

.graph-row {
  display: flex;
  justify-content: space-around;
  flex-wrap: wrap;
}

.data-table {
  max-height: 500px;
  overflow: scroll;
}

.header {
  display: flex;
  justify-content: center;
}

</style>
