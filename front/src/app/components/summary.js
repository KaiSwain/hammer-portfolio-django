"use client";

import React from "react";
import { useRouter } from "next/navigation";

export default function StudentSummary({ student }) {
  const router = useRouter();

  // Group fields into logical sections for better organization
  const personalInfo = [
    { label: "Full Name", value: student.full_name, icon: "👤" },
    { label: "Gender Identity", value: student.gender_identity?.gender ?? "Not specified", icon: "🏷️" },
    { label: "Class Start Date", value: student.start_date ? new Date(student.start_date).toLocaleDateString() : "Not set", icon: "📅" },
    { label: "Class End Date", value: student.end_date ? new Date(student.end_date).toLocaleDateString() : "Not set", icon: "📅" },
    { label: "Created At", value: new Date(student.created_at).toLocaleDateString(), icon: "📝" },
  ];

  const trainingProgress = [
    { label: "50-Hour Training", value: student.complete_50_hour_training, icon: "🎓" },
    { label: "HammerMath", value: student.hammer_math, icon: "🔨" },
    { label: "Employability Skills", value: student.employability_skills, icon: "💼" },
    { label: "Reading Ruler Assessment", value: student.passed_ruler_assessment, icon: "📏" },
  ];

  const oshaInfo = [
    { label: "OSHA 10 Passed", value: student.passed_osha_10_exam, icon: "🦺" },
    { label: "OSHA Type", value: student.osha_type?.name ?? "Not specified", icon: "🏗️" },
    { label: "OSHA Completion", value: student.osha_completion_date ? new Date(student.osha_completion_date).toLocaleDateString() : "Not completed", icon: "📋" },
  ];

  const assessmentResults = [
    { label: "DISC Assessment", value: student.disc_assessment_type?.type_name ?? "Not taken", icon: "🔵", color: "blue" },
    { label: "16 Types Assessment", value: student.sixteen_types_assessment?.type_name ?? "Not taken", icon: "🟣", color: "purple" },
    { label: "Enneagram Result", value: student.enneagram_result?.result_name ?? "Not taken", icon: "🟢", color: "green" },
  ];

  const testScores = [
    { label: "Pre-test Score", value: student.pretest_score ?? "Not recorded", icon: "📝", type: "score" },
    { label: "Post-test Score", value: student.posttest_score ?? "Not recorded", icon: "📊", type: "score" },
  ];

  // Calculate score improvement if both scores exist
  const scoreImprovement = student.pretest_score && student.posttest_score 
    ? student.posttest_score - student.pretest_score 
    : null;

  const renderStatusBadge = (value) => {
    if (typeof value === 'boolean') {
      return (
        <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
          value 
            ? 'bg-green-100 text-green-800' 
            : 'bg-gray-100 text-gray-800'
        }`}>
          {value ? '✅ Complete' : '⏳ Pending'}
        </span>
      );
    }
    return <span className="text-gray-900">{value}</span>;
  };

  const renderSection = (title, fields, bgColor = "bg-white") => (
    <div className={`${bgColor} rounded-xl border border-gray-200 p-6 shadow-sm`}>
      <h3 className="text-lg font-semibold text-gray-800 mb-4 flex items-center">
        {title}
      </h3>
      <div className="space-y-3">
        {fields.map(({ label, value, icon, color, type }) => (
          <div key={label} className="flex items-center justify-between py-2 border-b border-gray-100 last:border-b-0">
            <div className="flex items-center">
              <span className="text-lg mr-3">{icon}</span>
              <span className="font-medium text-gray-700 text-sm">{label}</span>
            </div>
            <div className="text-right">
              {type === 'score' ? (
                <span className={`text-lg font-bold ${
                  value === "Not recorded" ? 'text-gray-500' : 'text-blue-600'
                }`}>
                  {value}
                </span>
              ) : color ? (
                <span className={`inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-${color}-100 text-${color}-800`}>
                  {value}
                </span>
              ) : (
                renderStatusBadge(value)
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  );

  return (
    <div className="space-y-6">
      {/* Header Card with Student Name */}
      <div className="bg-gradient-to-r from-blue-600 to-blue-700 rounded-xl text-white p-8 shadow-lg">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-3xl font-bold mb-2">{student.full_name}</h2>
            <p className="text-blue-100 text-lg">Construction Pre-Apprentice</p>
            <div className="flex items-center mt-4 space-x-4">
              <div className="flex items-center">
                <span className="text-2xl mr-2">📅</span>
                <span className="text-sm">
                  {student.start_date ? `Started ${new Date(student.start_date).toLocaleDateString()}` : 'Start date not set'}
                </span>
              </div>
              {student.end_date && (
                <div className="flex items-center">
                  <span className="text-2xl mr-2">🎯</span>
                  <span className="text-sm">Ends {new Date(student.end_date).toLocaleDateString()}</span>
                </div>
              )}
            </div>
          </div>
          <div className="text-right">
            <div className="text-6xl mb-2">🎓</div>
            <p className="text-blue-100 text-sm">Student ID: {student.id}</p>
          </div>
        </div>
      </div>

      {/* Personal Information */}
      {renderSection("📋 Personal Information", personalInfo)}

      {/* Training Progress */}
      {renderSection("🎯 Training Progress", trainingProgress, "bg-gradient-to-br from-green-50 to-emerald-50")}

      {/* OSHA Information */}
      {renderSection("🦺 OSHA Certification", oshaInfo, "bg-gradient-to-br from-orange-50 to-amber-50")}

      {/* Assessment Results */}
      {renderSection("🧠 Personality Assessments", assessmentResults, "bg-gradient-to-br from-purple-50 to-indigo-50")}

      {/* Test Scores */}
      <div className="bg-gradient-to-br from-yellow-50 to-orange-50 rounded-xl border border-gray-200 p-6 shadow-sm">
        <h3 className="text-lg font-semibold text-gray-800 mb-4 flex items-center">
          📊 Test Performance
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
          {testScores.map(({ label, value, icon }) => (
            <div key={label} className="bg-white rounded-lg p-4 border border-yellow-200">
              <div className="flex items-center justify-between">
                <div className="flex items-center">
                  <span className="text-2xl mr-3">{icon}</span>
                  <span className="font-medium text-gray-700">{label}</span>
                </div>
                <span className={`text-2xl font-bold ${
                  value === "Not recorded" ? 'text-gray-500' : 'text-yellow-600'
                }`}>
                  {value}
                </span>
              </div>
            </div>
          ))}
        </div>
        
        {/* Score Improvement Indicator */}
        {scoreImprovement !== null && (
          <div className={`p-4 rounded-lg border-2 ${
            scoreImprovement > 0 ? 'bg-green-50 border-green-200' :
            scoreImprovement === 0 ? 'bg-blue-50 border-blue-200' :
            'bg-red-50 border-red-200'
          }`}>
            <div className="flex items-center justify-center">
              <span className="text-3xl mr-3">
                {scoreImprovement > 0 ? '📈' : scoreImprovement === 0 ? '➡️' : '📉'}
              </span>
              <div className="text-center">
                <div className={`text-xl font-bold ${
                  scoreImprovement > 0 ? 'text-green-700' :
                  scoreImprovement === 0 ? 'text-blue-700' :
                  'text-red-700'
                }`}>
                  {scoreImprovement > 0 ? '+' : ''}{scoreImprovement} points
                </div>
                <div className={`text-sm ${
                  scoreImprovement > 0 ? 'text-green-600' :
                  scoreImprovement === 0 ? 'text-blue-600' :
                  'text-red-600'
                }`}>
                  {scoreImprovement > 0 ? 'Excellent improvement!' :
                   scoreImprovement === 0 ? 'Maintained score' :
                   'Needs attention and support'}
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
