import React, { useState } from "react";
import Sidebar from "@/components/sidebar";
import GraphComponent from "@/components/Graph";

const Home = () => {
  const [graphData, setGraphData] = useState({ nodes: [], edges: [] });

  return (
    <div className="flex">
      <Sidebar setGraphData={setGraphData} />
      <GraphComponent graphData={graphData} />
    </div>
  );
};

export default Home;
