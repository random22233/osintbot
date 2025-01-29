"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import { FaPencil } from "react-icons/fa6";
import { MdDeleteOutline } from "react-icons/md";

function GraphList() {
  const router = useRouter();

  return (
    <div className="min-h-screen bg-gradient-to-b from-gray-900 to-gray-800 text-white font-sans">
      <div className="max-w-4xl mx-auto py-40 px-4 sm:px-6 lg:px-8">
        <h1 className="text-5xl font-bold mb-10">
          Create a <span className="text-teal-400">new graph</span>
        </h1>
        <div className="flex flex-col sm:flex-row gap-4 items-center">
          <input
            type="text"
            placeholder="Graph title..."
            className="flex-1 w-full sm:w-auto px-4 py-2 rounded-md bg-gray-700 text-white focus:outline-none focus:ring-2 focus:ring-teal-500"
          />
          <button
            className="px-6 py-2 rounded-md text-white create_new_graph_btn"
            onClick={() => router.push("/graph")}
          >
            Create a new graph
          </button>
        </div>
        <div className="my-12 text-center text-gray-400 or_text">or</div>
        <h2 className="text-5xl font-bold mb-10">
          Saved <span className="text-teal-400">graphs</span>
        </h2>
        <div className="flex flex-col gap-4">
          <input
            type="text"
            placeholder="Filter by keywords..."
            className="w-full px-4 py-2 rounded-md bg-gray-700 text-white focus:outline-none focus:ring-2 focus:ring-teal-500"
          />
          <div className="bg-gray-800 p-4 rounded-md shadow">
            <div className="flex justify-between items-center">
              <div>
                <Link href={"/graph"} className="text-teal-400">
                  test
                </Link>
              </div>
              <div className="flex gap-5 items-center">
                <div className="text-gray-400 text-sm">
                  11/18/2024, 12:32:19 AM
                </div>
                <div className="flex gap-2">
                  <button className="p-2 rounded-md bg-green-500 hover:bg-green-600 text-white">
                    <FaPencil className="text-sm" />{" "}
                    {/* Replace with an edit icon */}
                  </button>
                  <button className="p-2 rounded-md bg-red-500 hover:bg-red-600 text-white">
                    <MdDeleteOutline className="text-sm" />
                    {/* Replace with a delete icon */}
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default GraphList;
