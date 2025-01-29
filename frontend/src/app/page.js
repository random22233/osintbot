"use client";

import Footer from "@/components/Footer";
import Navbar from "@/components/Navbar";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { useState } from "react";
import { FiEye, FiEyeOff } from "react-icons/fi";

const SignInPage = () => {
  const [showPassword, setShowPassword] = useState(false);

  const router = useRouter();

  return (
    <>
      <Navbar />
      <div className="min-h-screen flex items-center justify-center bg-gray-900">
        <div className="bg-gray-800 p-8 rounded-lg shadow-lg w-full max-w-md text-gray-300">
          <h2 className="text-2xl font-bold mb-2">Sign in</h2>
          <p className="text-sm mb-6">
            Hey, new here?{" "}
            <Link href="/signup" className="text-teal-400 hover:underline">
              Create an account
            </Link>
          </p>

          <form>
            {/* Email Input */}
            <div className="mb-4">
              <label htmlFor="email" className="block text-sm mb-1">
                Email
              </label>
              <input
                type="email"
                id="email"
                placeholder="your@email.com"
                className="w-full p-3 bg-gray-700 rounded-md focus:outline-none focus:ring-2 focus:ring-teal-500 text-gray-300 placeholder-gray-500"
              />
            </div>

            {/* Password Input */}
            <div className="mb-6 relative">
              <label htmlFor="password" className="block text-sm mb-1">
                Password
                <a
                  href="#"
                  className="text-teal-400 text-sm float-right hover:underline"
                >
                  Forgot password?
                </a>
              </label>
              <div className="relative">
                <input
                  type={showPassword ? "text" : "password"}
                  id="password"
                  placeholder="Password"
                  className="w-full p-3 bg-gray-700 rounded-md focus:outline-none focus:ring-2 focus:ring-teal-500 text-gray-300 placeholder-gray-500"
                />
                <button
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                  className="absolute inset-y-0 right-3 flex items-center text-gray-400 hover:text-gray-300"
                >
                  {showPassword ? <FiEyeOff /> : <FiEye />}
                </button>
              </div>
            </div>

            {/* Submit Button */}
            <button
              type="button"
              className="w-full bg-gradient-to-r from-teal-400 to-blue-600 text-white p-3 rounded-md font-bold hover:opacity-90"
              onClick={() => router.push("/graph-list")}
            >
              Sign in
            </button>
          </form>
        </div>
      </div>
      <Footer />
    </>
  );
};

export default SignInPage;
