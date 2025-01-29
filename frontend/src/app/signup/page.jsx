"use client";

import Footer from "@/components/Footer";
import Navbar from "@/components/Navbar";
import Link from "next/link";
import { useState } from "react";
import { FiEye, FiEyeOff } from "react-icons/fi";

const SignupPage = () => {
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);

  const togglePasswordVisibility = () => {
    setShowPassword(!showPassword);
  };

  const toggleConfirmPasswordVisibility = () => {
    setShowConfirmPassword(!showConfirmPassword);
  };

  return (
    <>
      <Navbar />
      <br />
      <br />
      <div className="min-h-screen flex items-center justify-center bg-gray-900">
        <div className="bg-gray-800 p-8 rounded-lg shadow-lg w-full max-w-md">
          <h1 className="text-white text-2xl font-bold mb-4">Create account</h1>
          <p className="text-gray-400 mb-6">
            Already have an account?{" "}
            <Link href="/" className="text-teal-400 hover:underline">
              Sign in
            </Link>
          </p>

          {/* Email Input */}
          <div className="mb-4">
            <label
              htmlFor="email"
              className="block text-gray-400 text-sm font-semibold mb-2"
            >
              Email
            </label>
            <input
              type="email"
              id="email"
              placeholder="your@email.com"
              className="w-full p-3 rounded bg-gray-700 text-gray-300 border border-gray-600 focus:outline-none focus:ring-2 focus:ring-teal-500"
            />
          </div>

          {/* Password Input */}
          <div className="mb-4">
            <label
              htmlFor="password"
              className="block text-gray-400 text-sm font-semibold mb-2"
            >
              Password
            </label>
            <p className="text-gray-500 text-xs mb-2">
              Password should have a minimum of twelve characters, a special
              character, at least one number, and a mixture of uppercase and
              lowercase letters.
            </p>
            <div className="relative">
              <input
                type={showPassword ? "text" : "password"}
                id="password"
                placeholder="Your password"
                className="w-full p-3 rounded bg-gray-700 text-gray-300 border border-gray-600 focus:outline-none focus:ring-2 focus:ring-teal-500"
              />
              <button
                type="button"
                onClick={togglePasswordVisibility}
                className="absolute inset-y-0 right-3 text-gray-400 hover:text-gray-200"
              >
                {showPassword ? <FiEyeOff /> : <FiEye />}
              </button>
            </div>
          </div>

          {/* Confirm Password Input */}
          <div className="mb-4">
            <label
              htmlFor="confirm-password"
              className="block text-gray-400 text-sm font-semibold mb-2"
            >
              Confirm password
            </label>
            <div className="relative">
              <input
                type={showConfirmPassword ? "text" : "password"}
                id="confirm-password"
                placeholder="Confirm your password"
                className="w-full p-3 rounded bg-gray-700 text-gray-300 border border-gray-600 focus:outline-none focus:ring-2 focus:ring-teal-500"
              />
              <button
                type="button"
                onClick={toggleConfirmPasswordVisibility}
                className="absolute inset-y-0 right-3 text-gray-400 hover:text-gray-200"
              >
                {showConfirmPassword ? <FiEyeOff /> : <FiEye />}
              </button>
            </div>
          </div>

          {/* Terms and Conditions */}
          <div className="flex items-start mb-6">
            <input
              type="checkbox"
              id="terms"
              className="w-5 h-5 text-teal-500 bg-gray-700 border-gray-600 rounded focus:ring-teal-500"
            />
            <label
              htmlFor="terms"
              className="ml-3 text-gray-400 text-sm leading-5"
            >
              By continuing my registration, I accept the{" "}
              <a
                href="/terms"
                className="text-teal-400 hover:underline font-semibold"
              >
                terms and conditions of use
              </a>{" "}
              of the application.
            </label>
          </div>

          {/* Submit Button */}
          <button
            type="submit"
            className="w-full py-3 bg-gradient-to-r from-teal-400 to-blue-600 text-white font-semibold rounded-lg hover:opacity-90 focus:outline-none focus:ring-2 focus:ring-teal-500"
          >
            Create account
          </button>
        </div>
      </div>
      <Footer />
    </>
  );
};

export default SignupPage;
