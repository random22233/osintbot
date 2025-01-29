import { CiViewTable } from "react-icons/ci";
import { FiMapPin } from "react-icons/fi";
import { SlGraph } from "react-icons/sl";

const NavbarGraph = () => {
  return (
    <nav className="bg-black text-gray-400 flex items-center justify-between px-4 py-2 shadow-md">
      <div className="flex items-center space-x-8">
        <span className="text-sm cursor-pointer">File</span>
        <span className="text-sm cursor-pointer">Import</span>
        <span className="text-sm cursor-pointer">Export</span>
        <span className="text-sm cursor-pointer">Share</span>
        <span className="text-sm cursor-pointer">Settings</span>
        <span className="text-sm cursor-pointer">Help</span>
      </div>
      <div className="text-sm flex items-center justify-center gap-7 bg-gray-800 px-5 py-1 rounded-xl">
        <div className="flex items-center gap-1 cursor-pointer">
          <SlGraph />
          <p>Graph</p>
        </div>
        <div className="flex items-center gap-1 cursor-pointer">
          <CiViewTable />
          <p>Table</p>
        </div>
        <div className="flex items-center gap-1 cursor-pointer">
          <FiMapPin />
          <p>Map</p>
        </div>
      </div>
      <div className="text-sm pr-4">Last save: 11/23/2024, 4:57:38 PM</div>
    </nav>
  );
};

export default NavbarGraph;
