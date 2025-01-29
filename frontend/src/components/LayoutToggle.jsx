import {
  FiEyeOff,
  FiGrid,
  FiImage,
  FiMaximize,
  FiRefreshCw,
  FiSun,
} from "react-icons/fi";

const LayoutToggle = () => {
  return (
    <div className="bg-gray-800 text-gray-300 p-4 rounded-lg shadow-md w-fit">
      <div className="flex items-center justify-between space-x-8">
        {/* Layout Section */}
        <div className="flex items-center space-x-2">
          <label className="text-sm">Layout</label>
          <div className="flex items-center bg-gray-700 p-1 rounded-md space-x-2">
            <FiGrid className="text-gray-300" />
            <select
              className="bg-gray-700 text-gray-300 text-sm rounded-md focus:outline-none focus:ring-1 focus:ring-teal-500"
              defaultValue="Horizontal"
            >
              <option>Horizontal</option>
              <option>Vertical</option>
            </select>
          </div>
        </div>
        {/* Toggle Section */}
        <div className="flex items-center space-x-4">
          <label className="text-sm">Toggle</label>
          <div className="flex items-center space-x-2">
            <button className="p-2 bg-gray-700 rounded-md hover:bg-gray-600">
              <FiRefreshCw />
            </button>
            <button className="p-2 bg-gray-700 rounded-md hover:bg-gray-600">
              <FiMaximize />
            </button>
            <button className="p-2 bg-gray-700 rounded-md hover:bg-gray-600">
              <FiEyeOff />
            </button>
            <button className="p-2 bg-gray-700 rounded-md hover:bg-gray-600">
              <FiImage />
            </button>
            <button className="p-2 bg-gray-700 rounded-md hover:bg-gray-600">
              <FiSun />
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default LayoutToggle;
