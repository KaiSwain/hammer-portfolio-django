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
  // 1) map labels -> endpoint keys with enhanced icons and colors
  const CERT_OPTIONS = useMemo(
    () => [
      { 
        label: "OSHA 10 Certificate", 
        key: "osha", 
        icon: "🦺", 
        color: "orange",
        description: "Safety certification for construction workers"
      },
      { 
        label: "NCCER-HammerMath Credential", 
        key: "nccer", 
        icon: "🏗️", 
        color: "blue",
        description: "Construction industry recognized credential"
      },
      { 
        label: "HammerMath Certificate", 
        key: "hammermath", 
        icon: "🔨", 
        color: "yellow",
        description: "Mathematics for construction trades"
      },
      { 
        label: "Employability Skills", 
        key: "employability", 
        icon: "💼", 
        color: "green",
        description: "Workplace readiness and soft skills"
      },
      { 
        label: "50-Hour Training Certificate", 
        key: "workforce", 
        icon: "🎓", 
        color: "purple",
        description: "Comprehensive pre-apprenticeship training"
      },
      { 
        label: "Portfolio Overview 1-Pager", 
        key: "portfolio", 
        icon: "📁", 
        color: "indigo",
        description: "Complete student achievement portfolio"
      },
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
  const [generating, setGenerating] = useState(false);

  const handleToggle = (endpointKey) => {
    setSelected((prev) => ({ ...prev, [endpointKey]: !prev[endpointKey] }));
  };

  const handleGenerate = async () => {
    if (generating) return;
    try {
      setGenerating(true);
      // selected is already keyed by endpoint keys (e.g., { osha: true, nccer: false, ... })
      await onGenerate(student, selected);
    } catch (error) {
      console.error("Error generating certificates:", error);
      alert("Failed to generate certificates. Please try again.");
    } finally {
      setGenerating(false);
    }
  };

  const handleAiSummary = async () => {
    if (aiBusy || !generateAiSummary) return;
    try {
      setAiBusy(true);
      await generateAiSummary(student);
    } catch (e) {
      console.error(e);
      alert("Failed to generate AI summary. Please try again.");
    } finally {
      setAiBusy(false);
    }
  };

  const handleMasterPortfolio = async () => {
    if (generating || !generateMasterPortfolio) return;
    try {
      setGenerating(true);
      await generateMasterPortfolio(student);
    } catch (e) {
      console.error(e);
      alert("Failed to generate master portfolio. Please try again.");
    } finally {
      setGenerating(false);
    }
  };

  const aiDisabled = aiBusy || !generateAiSummary;
  const selectedCount = Object.values(selected).filter(Boolean).length;

  return (
    <div className="space-y-6">
      {/* Certificate Selection Card */}
      <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
        <div className="flex items-center mb-6">
          <span className="text-2xl mr-3">📄</span>
          <div>
            <h2 className="text-xl font-bold text-gray-800">Generate Certificates</h2>
            <p className="text-gray-600 text-sm">Select certificates to generate for {student.full_name}</p>
          </div>
        </div>

        <div className="space-y-3 mb-6">
          {CERT_OPTIONS.map(({ label, key, icon, color, description }) => (
            <div key={key} className="group">
              <label className={`flex items-center p-4 rounded-lg border-2 cursor-pointer transition-all ${
                selected[key] 
                  ? `border-${color}-300 bg-${color}-50` 
                  : 'border-gray-200 bg-gray-50 hover:bg-gray-100'
              }`}>
                <input
                  type="checkbox"
                  checked={!!selected[key]}
                  onChange={() => handleToggle(key)}
                  className={`w-5 h-5 text-${color}-600 border-gray-300 rounded focus:ring-${color}-500 mr-4`}
                />
                <div className="flex items-center flex-1">
                  <span className="text-2xl mr-3">{icon}</span>
                  <div>
                    <div className="font-medium text-gray-800">{label}</div>
                    <div className="text-sm text-gray-600">{description}</div>
                  </div>
                </div>
                {selected[key] && (
                  <span className={`text-${color}-600 text-xl`}>✓</span>
                )}
              </label>
            </div>
          ))}
        </div>

        {selectedCount > 0 && (
          <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 mb-4">
            <div className="flex items-center">
              <span className="text-blue-600 text-xl mr-2">ℹ️</span>
              <span className="text-blue-800 text-sm">
                {selectedCount} certificate{selectedCount !== 1 ? 's' : ''} selected for generation
              </span>
            </div>
          </div>
        )}

        <button
          onClick={handleGenerate}
          disabled={generating || selectedCount === 0}
          className={`w-full py-3 px-4 rounded-lg font-medium transition-colors flex items-center justify-center ${
            generating || selectedCount === 0
              ? 'bg-gray-300 text-gray-500 cursor-not-allowed'
              : 'bg-green-600 hover:bg-green-700 text-white'
          }`}
        >
          {generating ? (
            <>
              <div className="animate-spin rounded-full h-5 w-5 border-2 border-white border-t-transparent mr-3"></div>
              Generating Certificates...
            </>
          ) : (
            <>
              <span className="mr-2">📥</span>
              Generate Selected Certificates {selectedCount > 0 && `(${selectedCount})`}
            </>
          )}
        </button>
      </div>

      {/* AI Summary Card */}
      <div className="bg-gradient-to-br from-purple-50 to-indigo-50 rounded-xl border border-purple-200 p-6">
        <div className="flex items-center mb-4">
          <span className="text-2xl mr-3">🤖</span>
          <div>
            <h3 className="text-lg font-semibold text-purple-800">AI Personality Summary</h3>
            <p className="text-purple-600 text-sm">Generate an employer-focused personality assessment</p>
          </div>
        </div>

        <div className="bg-white rounded-lg p-4 mb-4">
          <p className="text-gray-700 text-sm">
            Create a comprehensive personality summary based on DISC, 16 Types, and Enneagram assessments 
            to help employers understand {student.full_name}&apos;s working style and strengths.
          </p>
        </div>

        <button
          onClick={handleAiSummary}
          disabled={aiDisabled}
          className={`w-full py-3 px-4 rounded-lg font-medium transition-colors flex items-center justify-center ${
            aiDisabled
              ? "bg-gray-300 text-gray-500 cursor-not-allowed"
              : "bg-purple-600 hover:bg-purple-700 text-white"
          }`}
          title={!generateAiSummary ? "AI summary action not configured" : ""}
        >
          {aiBusy ? (
            <>
              <div className="animate-spin rounded-full h-5 w-5 border-2 border-white border-t-transparent mr-3"></div>
              Generating AI Summary...
            </>
          ) : (
            <>
              <span className="mr-2">✨</span>
              Generate Personality Summary
            </>
          )}
        </button>
      </div>

      {/* Master Portfolio Card */}
      <div className="bg-gradient-to-br from-indigo-50 to-blue-50 rounded-xl border border-indigo-200 p-6">
        <div className="flex items-center mb-4">
          <span className="text-2xl mr-3">📚</span>
          <div>
            <h3 className="text-lg font-semibold text-indigo-800">Complete Portfolio</h3>
            <p className="text-indigo-600 text-sm">Generate a comprehensive portfolio document</p>
          </div>
        </div>

        <div className="bg-white rounded-lg p-4 mb-4">
          <p className="text-gray-700 text-sm">
            Create a complete portfolio PDF containing all student information, achievements, 
            certificates, and personality assessments in one professional document.
          </p>
        </div>

        <button
          onClick={handleMasterPortfolio}
          disabled={generating || !generateMasterPortfolio}
          className={`w-full py-3 px-4 rounded-lg font-medium transition-colors flex items-center justify-center ${
            generating || !generateMasterPortfolio
              ? "bg-gray-300 text-gray-500 cursor-not-allowed"
              : "bg-indigo-600 hover:bg-indigo-700 text-white"
          }`}
        >
          {generating ? (
            <>
              <div className="animate-spin rounded-full h-5 w-5 border-2 border-white border-t-transparent mr-3"></div>
              Generating Portfolio...
            </>
          ) : (
            <>
              <span className="mr-2">📋</span>
              Generate Full Portfolio PDF
            </>
          )}
        </button>
      </div>

      {/* Download Notice */}
      <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
        <div className="flex items-center">
          <span className="text-yellow-600 text-xl mr-2">⏳</span>
          <div>
            <p className="text-yellow-800 text-sm font-medium">Download Notice</p>
            <p className="text-yellow-700 text-xs">
              PDF generation may take a few moments. Your download will start automatically when ready.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
