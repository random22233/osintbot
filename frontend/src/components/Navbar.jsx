"use client";

import { MdKeyboardArrowDown } from "react-icons/md";

const Navbar = () => {
  return (
    <nav
      className="bg-gray-900 px-8 py-4 fixed w-[100%]"
      style={{ borderBottom: "1px solid rgb(51 65 85)" }}
    >
      <div className="max-w-7xl mx-auto flex items-center justify-between">
        {/* Logo Section */}
        <div className="flex items-center space-x-2">
          <div className="bg-white w-8 h-8 rounded-full flex items-center justify-center">
            <span className="text-black font-bold text-xl">P</span>
          </div>
          <div>
            <h1 className="text-white text-sm font-bold leading-4 tracking-wider">
              PREDICTA
            </h1>
            <p className="text-teal-400 font-bold text-sm tracking-wider">
              GRAPH
            </p>
          </div>
        </div>

        <div className="flex items-center justify-between gap-12">
          {/* Menu Items */}
          <div className="hidden md:flex text-gray-300 gap-12">
            <a href="/pricing" className="hover:text-white">
              Pricing
            </a>
            <div className="relative group">
              <button className="hover:text-white flex items-center">
                Contact{" "}
                <span className="ml-1">
                  <MdKeyboardArrowDown />
                </span>
              </button>
              {/* Dropdown (hidden by default) */}
              <div className="absolute hidden group-hover:block bg-gray-800 rounded-md mt-2 p-1 shadow-lg text-sm w-[140px]">
                <a
                  href="#"
                  className="block px-4 py-2 hover:bg-gray-700 rounded-md"
                >
                  Contact Us
                </a>
                <a
                  href="#"
                  className="block px-4 py-2 hover:bg-gray-700 rounded-md"
                >
                  Book a meeting
                </a>
              </div>
            </div>
          </div>

          {/* Sign In Button */}
          <div>
            <a
              href="/signin"
              className="bg-gradient-to-r from-teal-400 to-blue-600 text-white px-7 py-3 rounded-full hover:opacity-90 text-sm font-semibold"
            >
              Sign in
            </a>
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
