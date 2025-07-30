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
        interpolate: "natural",
        strokeWidth: 6,
        stroke: "transparent",
      }
    },
    {
      mark: {
        type: "line",
        interpolate: "natural",
      },
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