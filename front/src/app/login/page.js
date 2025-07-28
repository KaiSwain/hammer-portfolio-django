"use client";
import { useRouter } from "next/navigation";
import React, { useRef, useState } from "react";
import Link from "next/link";

export default function Login() {
  const [email, setEmail] = useState("kai@kai.com");
  const [password, setPassword] = useState("kai");
  const existDialog = useRef();
  const router = useRouter();

//   const handleLogin = (e) => {
//     e.preventDefault();
//     fetch(`http://localhost:8000/login`, {
//       method: "POST",
//       body: JSON.stringify({ email, password }),
//       headers: {
//         "Content-Type": "application/json",
//       },
//     })
//       .then((res) => res.json())
//       .then((authInfo) => {
//         if (authInfo.valid) {
//           localStorage.setItem("game_token", JSON.stringify(authInfo));
//           router.push("/");
//           window.dispatchEvent(new Event("logged in"));
//         } else {
//           existDialog.current.showModal();
//         }
//       });
//   };

  return (
    <div className="min-h-screen bg-black flex items-center justify-center px-4 py-10 text-white">
      <dialog
        className="bg-zinc-900 rounded-md p-6 text-white"
        ref={existDialog}
      >
        <div className="text-pink-400 font-semibold">User does not exist.</div>
        <button
          className="mt-4 px-4 py-2 bg-gray-700 hover:bg-gray-600 rounded"
          onClick={() => existDialog.current.close()}
        >
          Close
        </button>
      </dialog>

      <div className="bg-white/5 backdrop-blur-md p-8 rounded-2xl shadow-2xl border border-white/10 w-full max-w-md">
        <h1 className="text-3xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-purple-400 via-pink-500 to-yellow-400 text-center mb-6">
          🔐 Sign In to Flip Quest
        </h1>

        <form onSubmit={handleLogin} className="space-y-4">
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
            className="w-full py-2 bg-blue-700 hover:bg-blue-800 transition rounded font-semibold"
          >
            Sign In
          </button>

          <p className="text-center text-sm text-gray-400 mt-4">
            New here?{" "}
            <Link
              href="/register"
              className="text-pink-400 hover:text-pink-300 underline"
            >
              Create an account
            </Link>
          </p>
        </form>
      </div>
    </div>
  );
}

function Input({ label, value, setValue, type = "text" }) {
  return (
    <div>
      <label className="block mb-1 text-sm font-semibold text-gray-200">
        {label}
      </label>
      <input
        type={type}
        value={value}
        onChange={(e) => setValue(e.target.value)}
        className="w-full px-3 py-2 bg-zinc-800 border border-white/10 rounded focus:outline-none focus:ring-2 focus:ring-pink-500"
        required
      />
    </div>
  );
}