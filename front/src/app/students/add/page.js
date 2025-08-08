"use client";

import React, { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { createStudent } from "@/app/services/students";
import { getdetails } from "@/app/services/details";

export default function AddStudent() {
  const router = useRouter();

  const [formData, setFormData] = useState({
    full_name: "",
    gender_identity: "",
    start_date: "",
    end_date: "",
    complete_50_hour_training: false,
    passed_osha_10_exam: false,
    osha_completion_date: "",
    osha_type: "",
    hammer_math: false,
    employability_skills: false,
    passed_ruler_assessment: false,
    pretest_score: "",
    posttest_score: "",
    disc_assessment_type: "",
    enneagram_result: "",
    sixteen_types_assessment: ""
  });

  const [errors, setErrors] = useState({});
  const [showModal, setShowModal] = useState(false);
  const [isSaving, setIsSaving] = useState(false);
  const [success, setSuccess] = useState(false);
  const [details, setDetails] = useState({});

  useEffect(() => {
    getdetails().then((data) => setDetails(data));
  }, []);

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: type === "checkbox" ? checked : value,
    }));
  };

  const validateForm = () => {
    let newErrors = {};
    if (!formData.full_name.trim()) {
      newErrors.full_name = "Full name is required.";
    }
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleConfirmSave = async () => {
    setIsSaving(true);
    const payload = {
      ...formData,
      gender_identity: formData.gender_identity || null,
      disc_assessment_type: formData.disc_assessment_type || null,
      enneagram_result: formData.enneagram_result || null,
      osha_type: formData.osha_type || null,
      sixteen_types_assessment: formData.sixteen_types_assessment || null,
      start_date: formData.start_date || null,
      end_date: formData.end_date || null,
      osha_completion_date: formData.osha_completion_date || null,
      pretest_score: formData.pretest_score ? parseInt(formData.pretest_score) : null,
      posttest_score: formData.posttest_score ? parseInt(formData.posttest_score) : null,
    };

    try {
      const response = await createStudent(payload);
      if (response.ok) {
        setSuccess(true);
        setShowModal(false);
        setTimeout(() => router.push("/students"), 2000);
      } else {
        alert("Error saving student.");
      }
    } catch {
      alert("Something went wrong.");
    } finally {
      setIsSaving(false);
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (validateForm()) setShowModal(true);
  };

  return (
    <div className="min-h-screen bg-gray-50 p-6">
      <div className="max-w-3xl mx-auto bg-white rounded-lg shadow-lg p-6">
        <div className="flex justify-between items-center mb-6">
          <button onClick={() => router.back()} className="text-blue-600 hover:underline">
            ← Back
          </button>
          <h1 className="text-2xl font-bold text-gray-700">Add Student</h1>
        </div>

        {success && (
          <div className="mb-4 p-3 bg-green-100 text-green-700 rounded">
            ✅ Student saved successfully!
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-6">
          {/* Basic Info */}
          <div>
            <h2 className="text-lg font-bold text-gray-800 mb-2 uppercase">Student Info</h2>
            <label className="block font-medium text-gray-700">Full Name *</label>
            <input
              name="full_name"
              value={formData.full_name}
              onChange={handleChange}
              className="w-full border border-gray-300 rounded p-2 mt-1"
            />
            {errors.full_name && <p className="text-red-500 text-sm">{errors.full_name}</p>}

            <label className="block font-medium text-gray-700 mt-4">Gender Identity</label>
            <select
              name="gender_identity"
              value={formData.gender_identity}
              onChange={handleChange}
              className="w-full border border-gray-300 rounded p-2 mt-1"
            >
              <option value="">Select</option>
              {details.gender_identities?.map((g) => (
                <option key={g.id} value={g.id}>{g.gender}</option>
              ))}
            </select>
          </div>

          {/* Dates */}
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block font-medium text-gray-700">Start Date</label>
              <input
                type="date"
                name="start_date"
                value={formData.start_date}
                onChange={handleChange}
                className="w-full border border-gray-300 rounded p-2 mt-1"
              />
            </div>
            <div>
              <label className="block font-medium text-gray-700">End Date</label>
              <input
                type="date"
                name="end_date"
                value={formData.end_date}
                onChange={handleChange}
                className="w-full border border-gray-300 rounded p-2 mt-1"
              />
            </div>
          </div>

          {/* OSHA */}
          <h2 className="text-lg font-bold text-gray-800 mt-4 mb-2 uppercase">OSHA Details</h2>
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block font-medium text-gray-700">OSHA Type</label>
              <select
                name="osha_type"
                value={formData.osha_type}
                onChange={handleChange}
                className="w-full border border-gray-300 rounded p-2 mt-1"
              >
                <option value="">Select</option>
                {details.osha_types?.map((type) => (
                  <option key={type.id} value={type.id}>{type.name}</option>
                ))}
              </select>
            </div>
            <div>
              <label className="block font-medium text-gray-700">OSHA Completion Date</label>
              <input
                type="date"
                name="osha_completion_date"
                value={formData.osha_completion_date}
                onChange={handleChange}
                className="w-full border border-gray-300 rounded p-2 mt-1"
              />
            </div>
          </div>

          {/* Certifications */}
          <h2 className="text-lg font-bold text-gray-800 mt-4 mb-2 uppercase">Certifications</h2>
          <div className="grid grid-cols-1 gap-2">
            {["complete_50_hour_training", "passed_osha_10_exam", "hammer_math", "employability_skills", "passed_ruler_assessment"].map((field) => (
              <label key={field} className="flex items-center gap-2">
                <input type="checkbox" name={field} checked={formData[field]} onChange={handleChange} />
                {field.replace(/_/g, " ").toUpperCase()}
              </label>
            ))}
          </div>

          {/* Scores */}
          <h2 className="text-lg font-bold text-gray-800 mt-4 mb-2 uppercase">Ruler Assessment</h2>
          <div className="grid grid-cols-1 gap-4">
            {["pretest_score", "posttest_score"].map((field) => (
              <div key={field}>
                <label className="block font-medium text-gray-700">
                  {field.includes("pre") ? "Pre-test Score" : "Post-test Score"}
                </label>
                <select
                  name={field}
                  value={formData[field]}
                  onChange={handleChange}
                  className="w-full border border-gray-300 rounded p-2"
                >
                  <option value="">Select</option>
                  {[...Array(10)].map((_, i) => (
                    <option key={i + 1} value={i + 1}>{i + 1}</option>
                  ))}
                </select>
              </div>
            ))}
          </div>

          {/* Assessments */}
          <h2 className="text-lg font-bold text-gray-800 mt-4 mb-2 uppercase">Assessments</h2>
          <div className="grid grid-cols-1 gap-4">
            <div>
              <label className="block font-medium text-gray-700">DISC Assessment Type</label>
              <select
                name="disc_assessment_type"
                value={formData.disc_assessment_type}
                onChange={handleChange}
                className="w-full border border-gray-300 rounded p-2 mt-1"
              >
                <option value="">Select</option>
                {details.disc_assessments?.map((d) => (
                  <option key={d.id} value={d.id}>{d.type_name}</option>
                ))}
              </select>
            </div>
            <div>
              <label className="block font-medium text-gray-700">Sixteen Type Assessment</label>
              <select
                name="sixteen_types_assessment"
                value={formData.sixteen_types_assessment}
                onChange={handleChange}
                className="w-full border border-gray-300 rounded p-2 mt-1"
              >
                <option value="">Select</option>
                {details.sixteen_type_assessments?.map((type) => (
                  <option key={type.id} value={type.id}>{type.type_name}</option>
                ))}
              </select>
            </div>
            <div>
              <label className="block font-medium text-gray-700">Enneagram Result</label>
              <select
                name="enneagram_result"
                value={formData.enneagram_result}
                onChange={handleChange}
                className="w-full border border-gray-300 rounded p-2 mt-1"
              >
                <option value="">Select</option>
                {details.enneagram_results?.map((e) => (
                  <option key={e.id} value={e.id}>{e.result_name}</option>
                ))}
              </select>
            </div>
          </div>

          <button
            type="submit"
            className="w-full py-2 bg-blue-600 text-white rounded hover:bg-blue-700 mt-6"
          >
            Save Student
          </button>
        </form>
      </div>

      {/* Confirmation Modal */}
      {showModal && (
        <div className="fixed inset-0 flex items-center justify-center bg-gray-800 bg-opacity-50 z-50">
          <div className="bg-white p-6 rounded shadow-lg max-w-2xl w-full">
            <h2 className="text-xl font-bold mb-4">Confirm Student Details</h2>
            <p className="text-sm text-gray-600 mb-2">
              Please make sure this information is correct and the name is spelled right before saving.
            </p>

            <div className="space-y-2 text-gray-700 text-sm max-h-96 overflow-y-auto">
              {Object.entries(formData).map(([key, value]) => (
                <div key={key} className="flex justify-between border-b py-1">
                  <span className="capitalize">{key.replace(/_/g, " ")}:</span>
                  <span>{typeof value === "boolean" ? (value ? "Yes" : "No") : value || "-"}</span>
                </div>
              ))}
            </div>

            <div className="flex justify-end gap-3 mt-4">
              <button
                onClick={() => setShowModal(false)}
                className="px-4 py-2 bg-gray-200 rounded hover:bg-gray-300"
              >
                Cancel
              </button>
              <button
                onClick={handleConfirmSave}
                className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
                disabled={isSaving}
              >
                {isSaving ? "Saving..." : "Confirm"}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
