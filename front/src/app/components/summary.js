"use client";

import React from "react";
import { useRouter } from "next/navigation";

export default function StudentSummary({ student }) {
  const router = useRouter();

  const fields = [
    { label: "Full Name", value: student.full_name },
    { label: "Gender Identity", value: student.gender_identity?.gender ?? "-" },
    { label: "Class Start Date", value: student.start_date ?? "-" },
    { label: "Class End Date", value: student.end_date ?? "-" },
    { label: "Completed 50-Hour Training", value: student.complete_50_hour_training ? "Yes" : "No" },
    { label: "Passed OSHA 10", value: student.passed_osha_10_exam ? "Yes" : "No" },
    { label: "OSHA 10 Completion Date", value: student.osha_completion_date ?? "-" },
    { label: "OSHA 10 Type", value: student.osha_type?.name ?? "-" },
    { label: "HammerMath Completed", value: student.hammer_math ? "Yes" : "No" },
    { label: "Employability Skills Completed", value: student.employability_skills ? "Yes" : "No" },
    { label: "Passed Reading a Ruler Assessment", value: student.passed_ruler_assessment ? "Yes" : "No" },
    { label: "Ruler Pre-test Score", value: student.pretest_score ?? "-" },
    { label: "Ruler Post-test Score", value: student.posttest_score ?? "-" },
    { label: "Disc Assessment Type", value: student.disc_assessment_type?.type_name ?? "-" },
    { label: "16 Types Assessment", value: student.sixteen_types_assessment?.type_name ?? "-" },
    { label: "Enneagram Result", value: student.enneagram_result?.result_name ?? "-" },
    { label: "Created At", value: new Date(student.created_at).toLocaleDateString() },
  ];

  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      <h2 className="text-xl font-bold mb-4 text-gray-800">Student Info</h2>

      <div className="space-y-3 text-gray-700">
        {fields.map(({ label, value }) => (
          <div key={label} className="flex justify-between border-b border-gray-200 py-2 text-sm">
            <span className="font-medium">{label}:</span>
            <span>{value}</span>
          </div>
        ))}
      </div>

      <button
        onClick={() => router.push(`/students/${student.id}/edit`)}
        className="mt-6 px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
      >
        Edit Student
      </button>
    </div>
  );
}
