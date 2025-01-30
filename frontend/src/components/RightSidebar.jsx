"use client";

import Image from "next/image";
import { useState } from "react";
import { FaCirclePlus } from "react-icons/fa6";
import { IoMdCloseCircle } from "react-icons/io";

const RightSidebar = ({ isRightSidebar, info, setInfo }) => {
  const [image, setImage] = useState("");
  const [count, setCount] = useState(0);
  const [array, setArray] = useState([]);
  const [status, setStatus] = useState("");

  const goToElement = () => {
    setStatus("");
  };

  const goToHistogram = () => {
    setStatus("histogram");
  };

  const goToNotes = () => {
    setStatus("notes");
  };

  const handleChangeImage = (e) => {
    setImage(URL.createObjectURL(e.target.files[0]));
  };

  const addJob = () => {
    setCount((prev) => prev + 1);
    setArray((prev) => [...prev, { id: Math.random() }]);
  };

  const deleteJob = (id) => {
    setArray((prev) => prev.filter((itm) => itm?.id !== id));
  };

  return (
    <div className="fixed overflow-y-auto h-[100vh] top-0 right-0 bg-[#1b1f20] w-[320px] z-[9999]">
      <div style={{ borderBottom: "1px solid lightgray" }}>
        <ul className="flex justify-between items-center py-3 px-7 text-[13px] text-white border-b-orange-50">
          <li className="cursor-pointer" onClick={goToElement}>
            Element data
          </li>
          <li className="cursor-pointer" onClick={goToHistogram}>
            Histogram
          </li>
          <li className="cursor-pointer" onClick={goToNotes}>
            Notes
          </li>
        </ul>
      </div>

      {status === "" && (
        <>
          <div className="flex flex-col justify-center overflow-hidden w-[320px] h-[250px] relative mt-3">
            <input
              type="file"
              onChange={(e) => handleChangeImage(e)}
              style={{
                position: "absolute",
                opacity: 0,
                width: "100%",
                height: "100%",
                zIndex: 9999,
                top: 0,
                left: 0,
              }}
            />
            <Image
              src={
                image
                  ? image
                  : "https://png.pngtree.com/png-vector/20190820/ourmid/pngtree-no-image-vector-illustration-isolated-png-image_1694547.jpg"
              }
              alt={"image"}
              className="w-[210px] h-[230px] text-center cursor-pointer"
              style={{
                objectFit: "cover",
                borderRadius: "6px",
                alignSelf: "center",
                cursor: "pointer",
              }}
            />
          </div>

          <div className="relative flex flex-col mt-3 px-4">
            <div
              style={{ borderBottom: "1px solid #5D9E92" }}
              className="mt-3"
            ></div>
            <p
              className="text-center font-bold bg-[#1b1f20]"
              style={{
                color: "#5D9E92",
                marginTop: "-11px",
                width: "max-content",
                alignSelf: "center",
              }}
            >
              {info?.type?.toUpperCase()}
            </p>
          </div>

          <div className="px-4 py-2">
            <label className="text-[#4ba58a] text-[14px]">LABEL</label>
            <input
              type="text"
              defaultValue={info?.inputVal}
              className="w-[100%] px-[5px] py-[2px] rounded-md mt-3 bg-[#343b3d] text-gray-300"
            />
          </div>

          <div className="px-4 py-2">
            <div className="flex justify-between items-center">
              <label className="text-[#4ba58a] text-[14px]">
                {info?.type?.toUpperCase()}
              </label>
              <FaCirclePlus
                className="text-[#4ba58a] cursor-pointer"
                onClick={() => addJob()}
              />
            </div>
            {array.map((itm, index) => {
              return (
                <div key={itm?.id} className="relative">
                  <input
                    type="text"
                    className="w-[100%] px-[5px] py-[2px] rounded-md mt-3 bg-[#343b3d] text-gray-300"
                  />
                  <IoMdCloseCircle
                    className="text-[#bc3434] absolute top-[45%] right-2 cursor-pointer"
                    onClick={() => deleteJob(itm?.id)}
                  />
                </div>
              );
            })}
          </div>
        </>
      )}

      {status === "histogram" && (
        <div className="flex justify-center items-center min-h-[90vh] text-gray-300 text-xl px-8 text-center">
          <p>You need to be a PRO user to see this content</p>
        </div>
      )}

      {status === "notes" && (
        <div className="flex justify-center items-center min-h-[90vh] text-gray-300 text-xl px-8 text-center">
          <p>No Notes</p>
        </div>
      )}
    </div>
  );
};

export default RightSidebar;
