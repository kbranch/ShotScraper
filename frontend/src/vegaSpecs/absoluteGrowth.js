export const absoluteGrowth = {
  $schema: "https://vega.github.io/schema/vega-lite/v6.json",
  width: "container",
  height: "container",
  encoding: {
    x: {
      field: "Date",
      type: "temporal",
      timeUnit: "yearmonthdate",
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
        zero: false,
        // nice: false,
        // type: "log",
      },
    },
    color: {
      field: "PlayerId",
      type: "nominal",
      legend: null,
    }
  },
  layer: [
    {
      mark: {
        type: "line",
        interpolate: "natural",
      }
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
}