import React from "react";
import { Graph } from "react-graph-vis";

const GraphComponent = ({ graphData }) => {
  const options = {
    layout: {
      hierarchical: true,
      direction: 'UD', // 'UD' (Up-Down), 'LR' (Left-Right)
    },
    edges: {
      color: "#000000",
      arrows: {
        to: { enabled: true, scaleFactor: 0.5 },
      },
    },
    height: "500px",
  };

  return (
    <div>
      <Graph
        graph={graphData}
        options={options}
        style={{ height: "100%" }}
      />
    </div>
  );
};

export default GraphComponent;
