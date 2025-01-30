"use client";

import {
  Background,
  ConnectionMode,
  Controls,
  MarkerType,
  Panel,
  ReactFlow,
  ReactFlowProvider,
  addEdge,
  useEdgesState,
  useNodesState,
  useReactFlow,
} from "@xyflow/react";
import { useCallback, useEffect, useRef, useState } from "react";
import { BsCurrencyBitcoin, BsPersonCircle } from "react-icons/bs";
import {
  FaArrowRight,
  FaDiscord,
  FaEthereum,
  FaInstagram,
  FaPhoneAlt,
  FaTelegramPlane,
} from "react-icons/fa";
import { FaSquareFacebook } from "react-icons/fa6";
import { GoGlobe } from "react-icons/go";
import { HiOutlinePhotograph } from "react-icons/hi";
import {
  MdAccountBalanceWallet,
  MdForum,
  MdGroup,
  MdOutlineAccountBalance,
  MdOutlineAlternateEmail,
  MdOutlineMarkEmailUnread,
} from "react-icons/md";
import { RiPagesFill } from "react-icons/ri";
import { SiLitecoin, SiSolana } from "react-icons/si";
import { TiGroup } from "react-icons/ti";

import "@xyflow/react/dist/style.css";

import CustomConnectionLine from "@/components/CustomConnectionLine";
// import CustomNode from "@/components/CustomNode";
import FloatingEdge from "@/components/FloatingEdge";
import LayoutToggle from "@/components/LayoutToggle";
import NavbarGraph from "@/components/NavbarGraph";
import RightSidebar from "@/components/RightSidebar";
import { FaArrowLeft } from "react-icons/fa6";
import { DnDProvider, useDnD } from "../../components/DnDContext";
import Sidebar from "../../components/Sidebar";

const initialNodes = [
  // {
  //   id: "1",
  //   type: "input",
  //   data: { label: "input node" },
  //   position: { x: 250, y: 5 },
  //   type: "bidirectional",
  //   markerEnd: { type: MarkerType.Arrow },
  // },
];

let id = 0;
const getId = () => `dndnode_${id++}`;

const edgeTypes = {
  floating: FloatingEdge,
};

// const nodeTypes = {
//   custom: CustomNode,
// };

const defaultEdgeOptions = {
  type: "floating",
  markerEnd: {
    type: MarkerType.Arrow,
    color: "#b1b1b7",
  },
};

const connectionLineStyle = {
  stroke: "#b1b1b7",
};

const DnDFlow = () => {
  const reactFlowWrapper = useRef(null);
  const [nodes, setNodes, onNodesChange] = useNodesState(initialNodes);
  const [edges, setEdges, onEdgesChange] = useEdgesState([]);
  const { screenToFlowPosition } = useReactFlow();
  const [type] = useDnD();
  const [colorMode, setColorMode] = useState("dark");

  const [nodeBg, setNodeBg] = useState("red");

  const [nodeId, setNodeId] = useState(null);
  const [inputValue, setInputValue] = useState("");

  const [isSidebar, setIsSidebar] = useState(true);
  const [isRightSidebar, setIsRightSidebar] = useState(false);
  const [isInfo, setIsInfo] = useState(false);
  const [isSave, setIsSave] = useState(true);

  const [info, setInfo] = useState({});

  const clickNode = (type, id, inputVal, item) => {
    setInfo({ type, inputVal, item });
    // console.log({ inputVal });
  };

  const onConnect = useCallback(
    (params) => setEdges((eds) => addEdge({ ...params }, eds)),
    [setEdges]
  );

  const onDragOver = useCallback((event) => {
    event.preventDefault();
    event.dataTransfer.dropEffect = "move";
  }, []);

  const onDrop = useCallback(
    (event) => {
      event.preventDefault();

      if (!isSave) {
        alert("Please first enter label");
        return;
      }

      // check if the dropped element is valid
      if (!type) {
        return;
      }

      // console.log(type);

      // project was renamed to screenToFlowPosition
      // and you don't need to subtract the reactFlowBounds.left/top anymore
      // details: https://reactflow.dev/whats-new/2023-11-10
      const position = screenToFlowPosition({
        x: event.clientX,
        y: event.clientY,
      });
      const newNode = {
        id: getId(),
        type: "straight",
        position,
        // markerEnd: {
        //   type: MarkerType.Arrow,
        //   width: 20,
        //   height: 20,
        //   color: "red",
        // },
        data: {
          label: (
            <div
              className="flex items-center gap-1 flex-start"
              // onClick={() => clickNode(type, getId())}
            >
              {type == "phone" && <FaPhoneAlt className={"node_icon"} />}
              {type == "email" && (
                <MdOutlineMarkEmailUnread className={"node_icon"} />
              )}
              {type == "username" && (
                <MdOutlineAlternateEmail className={"node_icon"} />
              )}
              {type == "instagram" && <FaInstagram className={"node_icon"} />}
              {type == "facebook" && (
                <FaSquareFacebook className={"node_icon"} />
              )}
              {type == "telegram" && (
                <FaTelegramPlane className={"node_icon"} />
              )}
              {type == "discord" && <FaDiscord className={"node_icon"} />}
              {type == "person" && <BsPersonCircle className={"node_icon"} />}
              {type == "photo" && (
                <HiOutlinePhotograph className={"node_icon"} />
              )}
              {type == "group" && <TiGroup className={"node_icon"} />}
              {type == "association" && <MdGroup className={"node_icon"} />}
              {type == "forums" && <MdForum className={"node_icon"} />}
              {type == "account" && (
                <MdAccountBalanceWallet className={"node_icon"} />
              )}
              {type == "darkweb" && <RiPagesFill className={"node_icon"} />}
              {type == "waybackmachine" && (
                <MdOutlineAccountBalance className={"node_icon"} />
              )}
              {type == "bitcoin" && (
                <BsCurrencyBitcoin className={"node_icon"} />
              )}
              {type == "ethereum" && <FaEthereum className={"node_icon"} />}
              {type == "solana" && <SiSolana className={"node_icon"} />}
              {type == "litecoin" && <SiLitecoin className={"node_icon"} />}
              {type == "ip" && <GoGlobe className={"node_icon"} />}

              {nodeId !== 1 ? (
                <>
                  <input
                    className="text-gray-500 w-[50px] bg-[black] rounded-[2px] text-[12px] px-2 node_input"
                    type={"text"}
                    placeholder="Enter label"
                    // value={inputValue}
                    onChange={(e) => setInputValue(e.target.value)}
                  />
                  <button
                    className="save_btn"
                    onClick={() => save(getId(), inputValue)}
                  >
                    Save
                  </button>
                </>
              ) : (
                <p className="w-[100px]">{inputValue}</p>
              )}
            </div>
          ),
        },
        style: {
          strokeWidth: 2,
          stroke: "#FF0072",
        },
      };

      setNodes((nds) => nds.concat(newNode));
      setIsSave(false);
    },
    [screenToFlowPosition, type, nodeId, inputValue, isSave, setNodes]
  );

  const save = (id, val) => {
    // console.log(val);
    // if (val) {
    console.log(id);
    setNodeId(id);
    setIsSave(true);
    // } else {
    //   alert("Please enter a label");
    // }
  };

  useEffect(() => {
    console.log({ nodes });
    nodes?.map((itm) => {
      console.log(itm?.id + 1);
      console.log(nodeId);
      if (
        Number(itm?.id?.split("_")[1]) + 1 ===
        Number(nodeId?.split("_")[1])
      ) {
        setNodes((nds) =>
          nds.concat({
            ...itm,
            data: {
              label: (
                <div
                  className="flex items-center gap-1 flex-start"
                  onClick={() =>
                    clickNode(
                      type,
                      Number(itm?.id?.split("_")[1]),
                      inputValue,
                      itm
                    )
                  }
                >
                  {type == "phone" && <FaPhoneAlt className={"node_icon"} />}
                  {type == "email" && (
                    <MdOutlineMarkEmailUnread className={"node_icon"} />
                  )}
                  {type == "username" && (
                    <MdOutlineAlternateEmail className={"node_icon"} />
                  )}
                  {type == "instagram" && (
                    <FaInstagram className={"node_icon"} />
                  )}
                  {type == "facebook" && (
                    <FaSquareFacebook className={"node_icon"} />
                  )}
                  {type == "telegram" && (
                    <FaTelegramPlane className={"node_icon"} />
                  )}
                  {type == "discord" && <FaDiscord className={"node_icon"} />}
                  {type == "person" && (
                    <BsPersonCircle className={"node_icon"} />
                  )}
                  {type == "photo" && (
                    <HiOutlinePhotograph className={"node_icon"} />
                  )}
                  {type == "group" && <TiGroup className={"node_icon"} />}
                  {type == "association" && <MdGroup className={"node_icon"} />}
                  {type == "forums" && <MdForum className={"node_icon"} />}
                  {type == "account" && (
                    <MdAccountBalanceWallet className={"node_icon"} />
                  )}
                  {type == "darkweb" && <RiPagesFill className={"node_icon"} />}
                  {type == "waybackmachine" && (
                    <MdOutlineAccountBalance className={"node_icon"} />
                  )}
                  {type == "bitcoin" && (
                    <BsCurrencyBitcoin className={"node_icon"} />
                  )}
                  {type == "ethereum" && <FaEthereum className={"node_icon"} />}
                  {type == "solana" && <SiSolana className={"node_icon"} />}
                  {type == "litecoin" && <SiLitecoin className={"node_icon"} />}
                  {type == "ip" && <GoGlobe className={"node_icon"} />}

                  <p className="w-[100px] text-left text-[9px]">{inputValue}</p>
                </div>
              ),
            },
          })
        );
      }
    });
    // setNodes((prev) => {
    //   if (nds === nodeId) {
    //     // nodes?.map((itm) => {
    //     //   return { ...itm };
    //     // });
    //   }
    // });
  }, [nodeId, inputValue, nodes, setNodes, type]);

  // useEffect(() => {
  //   setNodes((nds) =>
  //     nds.map((node) => {
  //       if (node.id) {
  //         // it's important that you create a new node object
  //         // in order to notify react flow about the change
  //         return {
  //           ...node,
  //           style: {
  //             ...node.style,
  //             backgroundColor: nodeBg,
  //           },
  //         };
  //       }

  //       return node;
  //     })
  //   );
  // }, [nodeBg, setNodes]);

  const onChange = (evt) => {
    setColorMode(evt.target.value);
  };

  const toggleSidebar = () => {
    setIsSidebar((prev) => !prev);
  };

  const toggleRightSidebar = () => {
    setIsRightSidebar((prev) => !prev);
  };

  return (
    <>
      <NavbarGraph />
      <div className="dndflow">
        <Sidebar isSidebar={isSidebar} />
        {isRightSidebar && (
          <RightSidebar
            isRightSidebar={isRightSidebar}
            info={info}
            setInfo={setInfo}
          />
        )}
        <div className="reactflow-wrapper" ref={reactFlowWrapper}>
          <ReactFlow
            nodes={nodes}
            edges={edges}
            onNodesChange={onNodesChange}
            onEdgesChange={onEdgesChange}
            onConnect={onConnect}
            // snapToGrid={true}
            onDrop={onDrop}
            onDragOver={onDragOver}
            fitView
            colorMode={colorMode}
            connectionMode={ConnectionMode.Loose}
            // style={{ backgroundColor: "#F7F9FB" }}
            defaultEdgeOptions={defaultEdgeOptions}
            connectionLineComponent={CustomConnectionLine}
            connectionLineStyle={connectionLineStyle}
            edgeTypes={edgeTypes}
            // nodeTypes={nodeTypes}
          >
            {/* <LayoutToggle /> */}
            <Panel position="top-left">
              <LayoutToggle />
              {/* <select onChange={onChange} data-testid="colormode-select">
              <option value="dark">dark</option>
              <option value="light">light</option>
              <option value="system">system</option>
            </select> */}
            </Panel>
            <FaArrowLeft
              className="arrow_left"
              onClick={() => toggleSidebar()}
            />
            {!isRightSidebar ? (
              <FaArrowLeft
                className={isRightSidebar ? "arrow_right_open" : "arrow_right"}
                onClick={() => toggleRightSidebar()}
              />
            ) : (
              <FaArrowRight
                className={isRightSidebar ? "arrow_right_open" : "arrow_right"}
                onClick={() => toggleRightSidebar()}
              />
            )}

            <Controls />
            <Background />
          </ReactFlow>
        </div>
      </div>
    </>
  );
};

const Page = () => (
  <ReactFlowProvider>
    <DnDProvider>
      <DnDFlow />
    </DnDProvider>
  </ReactFlowProvider>
);

export default Page;
