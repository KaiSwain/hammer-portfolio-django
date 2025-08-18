"use client";
import React, { useMemo, useState } from "react";

/**
 * Props:
 * - student: object
 * - onGenerate: (student, selectedByEndpoint: Record<string, boolean>) => void
 * - generateAiSummary?: (student: any) => Promise<void> | void
 */
export default function CertificateOptions({
  student,
  onGenerate,
  generateAiSummary,
  generateMasterPortfolio
}) {
  // 1) map labels -> endpoint keys
  const CERT_OPTIONS = useMemo(
    () => [
      { label: "OSHA 10", key: "osha" },
      { label: "NCCER-HammerMath Credential", key: "nccer" }, // keep label, key matches /generate/nccer/
      { label: "HammerMath", key: "hammermath" },
      { label: "Employability Skills", key: "employability" },
      { label: "50-Hour Training", key: "workforce" }, // maps to /generate/workforce/
      { label: "Job Portfolio", key: "portfolio" },
    ],
    []
  );

  // 2) initial defaults (previous behavior preserved)
  const initialSelected = useMemo(
    () => ({
      osha: true,
      nccer: false,
      hammermath: true,
      employability: false,
      workforce: false,
      portfolio: false,
    }),
    []
  );

  // state is now keyed by endpoint keys, not labels
  const [selected, setSelected] = useState(initialSelected);
  const [aiBusy, setAiBusy] = useState(false);

  const handleToggle = (endpointKey) => {
    setSelected((prev) => ({ ...prev, [endpointKey]: !prev[endpointKey] }));
  };

  const handleGenerate = () => {
    // selected is already keyed by endpoint keys (e.g., { osha: true, nccer: false, ... })
    onGenerate(student, selected);
  };

  const handleAiSummary = async () => {
    if (aiBusy || !generateAiSummary) return;
    try {
      setAiBusy(true);
      await generateAiSummary(student); // or pass student.id if your fn expects id
    } catch (e) {
      console.error(e);
      alert("Failed to generate AI summary.");
    } finally {
      setAiBusy(false);
    }
  };

  const aiDisabled = aiBusy || !generateAiSummary;

  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      <h2 className="text-xl font-bold mb-4 text-gray-800">
        Generate Certificates
      </h2>

      <div className="space-y-3">
        {CERT_OPTIONS.map(({ label, key }) => (
          <label key={key} className="flex items-center gap-2">
            <input
              type="checkbox"
              checked={!!selected[key]}
              onChange={() => handleToggle(key)}
            />
            <span>{label}</span>
          </label>
        ))}
      </div>

      <div className="mt-6 grid grid-cols-1 gap-3">
        <button
          onClick={handleGenerate}
          className="w-full py-2 bg-green-600 text-white rounded hover:bg-green-700"
        >
          Generate Selected PDFs
        </button>

        <button
          onClick={handleAiSummary}
          disabled={aiDisabled}
          className={`w-full py-2 rounded text-white ${
            aiDisabled
              ? "bg-gray-400 cursor-not-allowed"
              : "bg-blue-600 hover:bg-blue-700"
          }`}
          title={!generateAiSummary ? "AI summary action not wired up" : ""}
        >
          {aiBusy ? "Generating AI Summary..." : "Generate Personality Summary"}
        </button>

        <p className="flex justify-center">
          Please wait a moment to generate download
        </p>
      </div>
      <button
        onClick={() => generateMasterPortfolio(student)}
        className="w-full py-2 bg-indigo-600 text-white rounded hover:bg-indigo-700"
      >
        Generate Full Portfolio PDF
      </button>
    </div>
  );
}
