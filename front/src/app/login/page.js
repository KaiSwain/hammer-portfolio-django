"use client";


import React, { useState, useRef } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";


export default function Login() {
  const [email, setEmail] = useState("test@test.com");
  const [password, setPassword] = useState("iamtestingthisout");
  const dialogRef = useRef();
  const router = useRouter()

  const handleLogin = (e) => {
    e.preventDefault();
    fetch(`http://localhost:8000/login`, {
      method: "POST",
      body: JSON.stringify({ email, password }),
      headers: {
        "Content-Type": "application/json",
      },
    })
      .then((res) => res.json())
      .then((authInfo) => {
        if (authInfo.valid) {
          localStorage.setItem("token", JSON.stringify(authInfo));
          router.push("/students");
        } else {
          existDialog.current.showModal();
        }
      });
  };

  return (
    <div className="min-h-screen bg-gray-100 flex items-center justify-center px-4">
      {/* Error Dialog */}
      <dialog
        className="bg-white shadow-lg rounded-lg p-6 text-gray-800"
        ref={dialogRef}
      >
        <div className="text-red-500 font-semibold mb-2">
          Invalid credentials or user not found.
        </div>
        <button
          className="px-4 py-2 bg-gray-200 hover:bg-gray-300 rounded"
          onClick={() => dialogRef.current.close()}
        >
          Close
        </button>
      </dialog>

      {/* Login Card */}
      <div className="bg-white p-8 rounded-lg shadow-xl border border-gray-200 w-full max-w-md">
        <h1 className="text-2xl font-bold text-gray-800 text-center mb-6">
          Hammer Portal Login
        </h1>

        <form onSubmit={handleLogin} className="space-y-5 text-black ">
          <Input
            label="Email Address"
            value={email}
            setValue={setEmail}
            type="email"
          />
          <Input
            label="Password"
            value={password}
            setValue={setPassword}
            type="password"
          />

          <button
            type="submit"
            className="w-full py-2 bg-blue-600 hover:bg-blue-700 text-white rounded font-semibold transition"
          >
            Sign In
          </button>

          <p className="text-center text-sm text-gray-500 mt-3">
            <Link
              href="/support"
              className="text-blue-600 hover:underline"
            >
              Report a login issue
            </Link>
          </p>
        </form>
      </div>
    </div>
  );
}

// Input Component
function Input({ label, value, setValue, type = "text" }) {
  return (
    <div>
      <label className="block mb-1 text-sm font-medium text-gray-700">
        {label}
      </label>
      <input
        type={type}
        value={value}
        onChange={(e) => setValue(e.target.value)}
        className="w-full px-3 py-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
        required
      />
    </div>
  );
}
