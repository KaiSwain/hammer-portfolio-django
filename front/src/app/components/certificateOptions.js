"use client";

import React, { useState } from "react";

/**
 * CertificateOptions Component
 * -----------------------------
 * Displays a list of certificate options as checkboxes
 * and a button to trigger PDF generation.
 * 
 * Props:
 * - student: object (student data)
 * - onGenerate: function (called when "Generate PDFs" is clicked)
 */
export default function CertificateOptions({ student, onGenerate }) {
  const [selected, setSelected] = useState({
    Osha: true,
    HammerMath: true,
    Portfolio: false,
    Employability: false,
    NCCER: false,
    Workforce: false,
  });

  const handleToggle = (cert) => {
    setSelected((prev) => ({ ...prev, [cert]: !prev[cert] }));
  };

  const handleGenerate = () => {
    onGenerate(student, selected);
  };

  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      <h2 className="text-xl font-bold mb-4 text-gray-800">Generate Certificates</h2>

      <div className="space-y-3">
        {Object.keys(selected).map((cert) => (
          <label key={cert} className="flex items-center gap-2">
            <input
              type="checkbox"
              checked={selected[cert]}
              onChange={() => handleToggle(cert)}
            />
            <span>{cert}</span>
          </label>
        ))}
      </div>

      <button
        onClick={handleGenerate}
        className="mt-6 w-full py-2 bg-green-600 text-white rounded hover:bg-green-700"
      >
        Generate PDFs
      </button>
    </div>
  );
}
