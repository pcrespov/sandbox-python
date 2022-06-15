let schema = {
    additionalProperties: false,
    properties: {
      input: {
        items: {
          oneOf: [
            {
              additionalProperties: false,
              properties: {
                defaultValue: {
                  required: true,
                  type: "number",
                },
                enabled: {
                  type: "string",
                },
                id: {
                  type: "string",
                },
                name: {
                  required: true,
                  type: "string",
                },
                possibleValues: {
                  items: {
                    additionalProperties: false,
                    properties: {
                      name: {
                        required: true,
                        type: "string",
                      },
                      value: {
                        required: true,
                        type: "number",
                      },
                    },
                    type: "object",
                  },
                  minItems: 1,
                  required: true,
                  type: "array",
                },
              },
            },
            {
              additionalProperties: false,
              properties: {
                defaultValue: {
                  required: true,
                  type: "number",
                },
                enabled: {
                  type: "string",
                },
                id: {
                  type: "string",
                },
                maximumValue: {
                  required: true,
                  type: "number",
                },
                minimumValue: {
                  required: true,
                  type: "number",
                },
                name: {
                  required: true,
                  type: "string",
                },
              },
            },
          ],
          type: "object",
        },
        minItems: 1,
        required: true,
        type: "array",
      },
      output: {
        additionalProperties: false,
        minItems: 1,
        properties: {
          data: {
            items: {
              additionalProperties: false,
              properties: {
                id: {
                  required: true,
                  type: "string",
                },
                name: {
                  required: true,
                  type: "string",
                },
              },
              type: "object",
            },
            minItems: 1,
            required: true,
            type: "array",
          },
          plots: {
            items: {
              additionalProperties: false,
              properties: {
                xAxisTitle: {
                  required: true,
                  type: "string",
                },
                xValue: {
                  required: true,
                  type: "string",
                },
                yAxisTitle: {
                  required: true,
                  type: "string",
                },
                yValue: {
                  required: true,
                  type: "string",
                },
              },
              type: "object",
            },
            maxItems: 9,
            minItems: 1,
            required: true,
            type: "array",
          },
        },
        required: true,
        type: "object",
      },
      parameters: {
        items: {
          additionalProperties: false,
          properties: {
            name: {
              required: true,
              type: "string",
            },
            value: {
              required: true,
              type: "string",
            },
          },
          type: "object",
        },
        type: "array",
      },
      simulation: {
        additionalProperties: false,
        properties: {
          endingPoint: {
            required: true,
            type: "number",
          },
          pointInterval: {
            required: true,
            type: "number",
          },
        },
        type: "object",
      },
    },
    type: "object",
  };
