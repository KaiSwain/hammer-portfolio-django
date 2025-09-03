"use client";

import React, { useState, useRef } from "react";
import Link from "next/link";
import Image from "next/image";
import { useRouter } from "next/navigation";

export default function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [showSupportModal, setShowSupportModal] = useState(false);
  const [supportForm, setSupportForm] = useState({ name: "", email: "", issue: "" });
  const errorDialogRef = useRef();
  const supportDialogRef = useRef();
  const router = useRouter();

  const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'https://hammer-app-hk3st.ondigitalocean.app';

  const handleLogin = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    
    try {
      const response = await fetch(`${API_BASE_URL}/api/login/`, {
        method: "POST",
        body: JSON.stringify({ email, password }),
        headers: {
          "Content-Type": "application/json",
        },
      });
      
      const authInfo = await response.json();
      
      if (authInfo.valid) {
        localStorage.setItem("token", JSON.stringify(authInfo));
        router.push("/students");
      } else {
        errorDialogRef.current.showModal();
      }
    } catch (error) {
      console.error("Login error:", error);
      errorDialogRef.current.showModal();
    } finally {
      setIsLoading(false);
    }
  };

  const handleSupportSubmit = async (e) => {
    e.preventDefault();
    
    try {
      const response = await fetch(`${API_BASE_URL}/api/support/`, {
        method: "POST",
        body: JSON.stringify(supportForm),
        headers: {
          "Content-Type": "application/json",
        },
      });
      
      const result = await response.json();
      
      if (result.success) {
        // Reset form and close modal
        setSupportForm({ name: "", email: "", issue: "" });
        setShowSupportModal(false);
        supportDialogRef.current.close();
        
        // Show success message
        alert("Support request submitted successfully! We'll get back to you soon.");
      } else {
        alert("Error submitting support request. Please try again.");
      }
    } catch (error) {
      console.error("Support request error:", error);
      alert("Error submitting support request. Please try again.");
    }
  };

  const openSupportModal = () => {
    setShowSupportModal(true);
    supportDialogRef.current.showModal();
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-orange-50 flex items-center justify-center px-4">
      {/* Error Dialog */}
      <dialog
        className="bg-white shadow-xl rounded-xl p-6 text-gray-800 border border-gray-200 backdrop:bg-black/50"
        ref={errorDialogRef}
      >
        <div className="text-center">
          <div className="text-red-500 text-4xl mb-4">⚠️</div>
          <h3 className="text-lg font-semibold mb-2 text-gray-800">Login Failed</h3>
          <p className="text-red-600 mb-4">
            Invalid credentials or user not found. Please check your email and password.
          </p>
          <button
            className="px-6 py-2 bg-gray-200 hover:bg-gray-300 rounded-lg transition-colors"
            onClick={() => errorDialogRef.current.close()}
          >
            Try Again
          </button>
        </div>
      </dialog>

      {/* Support Dialog */}
      <dialog
        className="bg-white shadow-xl rounded-xl p-6 text-gray-800 border border-gray-200 backdrop:bg-black/50 max-w-md w-full mx-4"
        ref={supportDialogRef}
      >
        <div className="mb-4">
          <h3 className="text-xl font-semibold text-gray-800 mb-2">Request Login Support</h3>
          <p className="text-gray-600 text-sm">
            Having trouble logging in? Fill out this form and we&apos;ll help you get back on track.
          </p>
        </div>

        <form onSubmit={handleSupportSubmit} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Your Name</label>
            <input
              type="text"
              value={supportForm.name}
              onChange={(e) => setSupportForm({...supportForm, name: e.target.value})}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              required
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Email Address</label>
            <input
              type="email"
              value={supportForm.email}
              onChange={(e) => setSupportForm({...supportForm, email: e.target.value})}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              required
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Describe the Issue</label>
            <textarea
              value={supportForm.issue}
              onChange={(e) => setSupportForm({...supportForm, issue: e.target.value})}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 h-24 resize-none"
              placeholder="Tell us what's happening..."
              required
            ></textarea>
          </div>

          <div className="flex gap-3 pt-2">
            <button
              type="submit"
              className="flex-1 bg-blue-600 hover:bg-blue-700 text-white py-2 rounded-lg font-medium transition-colors"
            >
              Submit Request
            </button>
            <button
              type="button"
              onClick={() => {
                setShowSupportModal(false);
                supportDialogRef.current.close();
              }}
              className="flex-1 bg-gray-200 hover:bg-gray-300 text-gray-800 py-2 rounded-lg font-medium transition-colors"
            >
              Cancel
            </button>
          </div>
        </form>
      </dialog>

      {/* Login Card */}
      <div className="bg-white p-8 rounded-2xl shadow-xl border border-gray-200 w-full max-w-md">
        {/* Header */}
        <div className="text-center mb-8">
          <div className="mb-4 flex justify-center">
            <Image
              src="/Hammer-Primary-Blue-Logo.png"
              alt="If I Had A Hammer Logo"
              width={200}
              height={80}
              className="h-12 w-auto"
            />
          </div>
          <p className="text-gray-600 text-sm">Teacher Portal Access</p>
        </div>

        <form onSubmit={handleLogin} className="space-y-5">
          <Input
            label="Email Address"
            value={email}
            setValue={setEmail}
            type="email"
            placeholder="teacher@example.com"
          />
          <Input
            label="Password"
            value={password}
            setValue={setPassword}
            type="password"
            placeholder="Enter your password"
          />

          <button
            type="submit"
            disabled={isLoading}
            className="w-full py-3 bg-blue-600 hover:bg-blue-700 disabled:bg-blue-400 text-white rounded-lg font-semibold transition-colors flex items-center justify-center"
          >
            {isLoading ? (
              <>
                <div className="animate-spin rounded-full h-4 w-4 border-2 border-white border-t-transparent mr-2"></div>
                Signing In...
              </>
            ) : (
              "Sign In"
            )}
          </button>

          <div className="text-center">
            <button
              type="button"
              onClick={openSupportModal}
              className="text-blue-600 hover:text-blue-800 hover:underline text-sm font-medium transition-colors"
            >
              Having trouble logging in?
            </button>
          </div>
        </form>

        {/* Footer */}
        <div className="mt-8 pt-6 border-t border-gray-200 text-center">
          <p className="text-gray-500 text-xs">
            Need access? Contact your administrator.
          </p>
        </div>
      </div>
    </div>
  );
}

// Input Component
function Input({ label, value, setValue, type = "text", placeholder = "" }) {
  return (
    <div>
      <label className="block mb-2 text-sm font-medium text-gray-700">
        {label}
      </label>
      <input
        type={type}
        value={value}
        onChange={(e) => setValue(e.target.value)}
        placeholder={placeholder}
        className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-colors"
        required
      />
    </div>
  );
}
