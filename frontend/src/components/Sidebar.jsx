import React, { useState } from "react";
import { SearchOutlined } from "@ant-design/icons";
import { Col, Form, Input, Row } from "antd";
import { useDnD } from "./DnDContext";

const Sidebar = ({ setGraphData }) => {
  const [query, setQuery] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [_, setType] = useDnD();

  const onDragStart = (event, nodeType) => {
    setType(nodeType);
    event.dataTransfer.effectAllowed = "move";
  };

  const handleSearch = async () => {
    if (!query) {
      setError("Please enter an email or username.");
      return;
    }

    setLoading(true);
    setError(null);

    try {
      // Call the backend API to search using the query
      const response = await fetch(`/api/search?query=${query}`);
      const data = await response.json();

      if (data.error) {
        setError("Failed to fetch data. Please try again.");
        setLoading(false);
        return;
      }

      const parentNode = {
        id: query,
        label: query,
        title: "Search Term",
      };

      let nodes = [parentNode];
      let edges = [];

      // Create child nodes based on the data returned
      Object.entries(data).forEach(([key, value], index) => {
        const childNode = {
          id: `${query}-${index}`,
          label: `${key}: ${JSON.stringify(value)}`,
          title: key,
        };

        nodes.push(childNode);
        edges.push({ from: parentNode.id, to: childNode.id });
      });

      // Set the graph data with nodes and edges
      setGraphData({ nodes, edges });

    } catch (err) {
      setError("An error occurred while searching.");
    }

    setLoading(false);
  };

  return (
    <aside className={`${isSidebar ? "sidebar_open" : "sidebar_close"}`}>
      <Form name="search" className="max-w-[100%]">
        <Row>
          <Col span={24}>
            <Form.Item name="query">
              <div className="flex items-center p-1 rounded-sm space-x-2 absolute top-[2px] z-10">
                <select
                  className="bg-gray-600 text-gray-300 text-sm rounded-md focus:outline-none focus:ring-1 cursor-pointer"
                  defaultValue="Username"
                >
                  <option>Username</option>
                  <option>Phone</option>
                  <option>Image</option>
                  <option>IP</option>
                  <option>Full Name</option>
                  <option>Email</option>
                  <option>Social Media</option>
                  <option>Profile</option>
                  <option>Keyword</option>
                  <option>Address</option>
                  <option>Domain</option>
                </select>
              </div>
              <Input
                prefix={<SearchOutlined />}
                placeholder="Enter search term"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                className="bg-gray-700 graph_filter_input"
                style={{
                  background: "rgb(55 65 81)",
                  color: "gray",
                  paddingLeft: "91px",
                }}
              />
              <div className="text-center">
                <SearchOutlined
                  className="text-center flex items-center justify-center mt-5 text-white bg-orange-400 p-2 rounded-[50%] cursor-pointer"
                  style={{ color: "white" }}
                  onClick={handleSearch}
                />
              </div>
            </Form.Item>
          </Col>
        </Row>
      </Form>

      {error && <p className="error">{error}</p>}
      {loading && <p>Loading...</p>}

      {/* Example Drag and Drop Section (Unchanged) */}
      <div className="description">
        <p className="text-white font-bold text-xl">
          Personal{" "}
          <span className="font-bold text-gray-500 text-[14px]">(10)</span>
        </p>
      </div>
      <div className="flex flex-wrap items-center gap-3">
        {/* Add your draggable nodes here */}
        <div
          className="dndnode input flex flex-col items-center"
          onDragStart={(event) => onDragStart(event, "phone")}
          draggable
        >
          {/* <FaPhoneAlt className="personal_node" /> */}
          <p className="text-gray-200 text-[13px]">Phone</p>
        </div>
        <div
          className="dndnode input flex flex-col items-center"
          onDragStart={(event) => onDragStart(event, "email")}
          draggable
        >
          {/* <MdOutlineMarkEmailUnread className="personal_node" /> */}
          <p className="text-gray-200 text-[13px]">Email</p>
        </div>
        <div
          className="dndnode input flex flex-col items-center"
          onDragStart={(event) => onDragStart(event, "username")}
          draggable
        >
          {/* <MdOutlineAlternateEmail className="personal_node" /> */}
          <p className="text-gray-200 text-[13px]">Username</p>
        </div>
      </div>
    </aside>
  );
};

export default Sidebar;