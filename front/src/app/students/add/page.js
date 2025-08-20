"use client";

import React, { useEffect, useMemo, useState } from "react";
import { useRouter } from "next/navigation";
import { createStudent } from "@/app/services/students";
import { getdetails } from "@/app/services/details";
import Link from "next/link";

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
    sixteen_types_assessment: "",
  });

  const [errors, setErrors] = useState({});
  const [showModal, setShowModal] = useState(false);
  const [isSaving, setIsSaving] = useState(false);
  const [success, setSuccess] = useState(false);
  const [details, setDetails] = useState({});
  const [currentStep, setCurrentStep] = useState(1);

  useEffect(() => {
    // Check authentication
    const token = localStorage.getItem("token");
    if (!token) {
      router.push("/login");
      return;
    }
    
    getdetails().then((data) => setDetails(data));
  }, [router]);

  // Build quick lookup maps for IDs -> labels
  const lookups = useMemo(() => {
    const mapBy = (arr = [], key = "id") =>
      arr.reduce((acc, item) => {
        acc[item[key]] = item;
        return acc;
      }, {});
    return {
      genderById: mapBy(details.gender_identities),
      oshaById: mapBy(details.osha_types),
      discById: mapBy(details.disc_assessments),
      sixById: mapBy(details.sixteen_type_assessments),
      enneagramById: mapBy(details.enneagram_results),
    };
  }, [details]);

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
      gender_identity_id: parseInt(formData.gender_identity) || null,
      disc_assessment_type_id: parseInt(formData.disc_assessment_type) || null,
      enneagram_result_id: parseInt(formData.enneagram_result) || null,
      osha_type_id: parseInt(formData.osha_type) || null,
      sixteen_types_assessment_id: parseInt(formData.sixteen_types_assessment) || null,
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
        setTimeout(() => router.push("/students"), 1200);
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

  const nextStep = () => {
    if (currentStep < 4) setCurrentStep(currentStep + 1);
  };

  const prevStep = () => {
    if (currentStep > 1) setCurrentStep(currentStep - 1);
  };

  const steps = [
    { number: 1, title: "Basic Info", icon: "👤" },
    { number: 2, title: "Program Progress", icon: "📚" },
    { number: 3, title: "Assessments", icon: "📋" },
    { number: 4, title: "Test Scores", icon: "📊" }
  ];

  // Friendly labels for the modal
  const modalLabels = {
    full_name: "FULL NAME",
    gender_identity: "GENDER IDENTITY",
    start_date: "Class START DATE",
    end_date: "Class END DATE",
    complete_50_hour_training: "COMPLETED 50-HOUR TRAINING",
    passed_osha_10_exam: "PASSED OSHA 10 EXAM",
    osha_completion_date: "OSHA 10 COMPLETION DATE",
    osha_type: "OSHA 10 TYPE",
    hammer_math: "COMPLETED HAMMERMATH",
    employability_skills: "COMPLETED EMPLOYABILITY SKILLS",
    passed_ruler_assessment: "PASSED READING A RULER ASSESSMENT",
    pretest_score: "PRE-TEST SCORE",
    posttest_score: "POST-TEST SCORE",
    disc_assessment_type: "DISC ASSESSMENT TYPE",
    sixteen_types_assessment: "SIXTEEN TYPES ASSESSMENT",
    enneagram_result: "ENNEAGRAM RESULT",
  };

  // Display order in the modal
  const modalOrder = [
    "full_name",
    "gender_identity",
    "start_date",
    "end_date",
    "osha_type",
    "osha_completion_date",
    "complete_50_hour_training",
    "passed_osha_10_exam",
    "hammer_math",
    "employability_skills",
    "passed_ruler_assessment",
    "pretest_score",
    "posttest_score",
    "disc_assessment_type",
    "sixteen_types_assessment",
    "enneagram_result",
  ];

  // Convert raw values to display strings
  const formatValue = (key, value) => {
    if (typeof value === "boolean") return value ? "Yes" : "No";
    if (value === "" || value == null) return "-";

    switch (key) {
      case "gender_identity":
        return lookups.genderById[value]?.gender ?? String(value);
      case "disc_assessment_type":
        return lookups.discById[value]?.type_name ?? String(value);
      case "sixteen_types_assessment":
        return lookups.sixById[value]?.type_name ?? String(value);
      case "enneagram_result":
        return lookups.enneagramById[value]?.result_name ?? String(value);
      case "osha_type":
        return lookups.oshaById[value]?.name ?? String(value);
      default:
        return String(value);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-orange-50">
      {/* Header */}
      <div className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center">
              <Link href="/students" className="text-2xl mr-4">🔨</Link>
              <div>
                <h1 className="text-2xl font-bold text-gray-900">Add New Student</h1>
                <p className="text-gray-600 text-sm">Create a comprehensive student profile</p>
              </div>
            </div>
            <Link
              href="/students"
              className="px-4 py-2 text-gray-600 hover:text-gray-800 border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors"
            >
              ← Back to Students
            </Link>
          </div>
        </div>
      </div>

      {/* Progress Steps */}
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
        <div className="mb-8">
          <div className="flex justify-between items-center">
            {steps.map((step, index) => (
              <div key={step.number} className="flex items-center">
                <div className={`flex items-center justify-center w-10 h-10 rounded-full ${
                  currentStep >= step.number 
                    ? 'bg-blue-600 text-white' 
                    : 'bg-gray-300 text-gray-600'
                }`}>
                  <span className="text-lg">{step.icon}</span>
                </div>
                <div className="ml-3">
                  <p className={`text-sm font-medium ${
                    currentStep >= step.number ? 'text-blue-600' : 'text-gray-500'
                  }`}>
                    Step {step.number}
                  </p>
                  <p className="text-xs text-gray-500">{step.title}</p>
                </div>
                {index < steps.length - 1 && (
                  <div className={`w-16 h-0.5 mx-4 ${
                    currentStep > step.number ? 'bg-blue-600' : 'bg-gray-300'
                  }`} />
                )}
              </div>
            ))}
          </div>
        </div>

        {/* Success Message */}
        {success && (
          <div className="mb-6 p-4 bg-green-50 border border-green-200 rounded-lg">
            <div className="flex items-center">
              <span className="text-2xl mr-3">✅</span>
              <div>
                <h3 className="text-green-800 font-semibold">Student Added Successfully!</h3>
                <p className="text-green-600 text-sm">Redirecting to student list...</p>
              </div>
            </div>
          </div>
        )}

        {/* Form */}
        <form onSubmit={handleSubmit}>
          <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-8">
            {/* Step 1: Basic Info */}
            {currentStep === 1 && (
              <div className="space-y-6">
                <div className="text-center mb-6">
                  <h2 className="text-xl font-semibold text-gray-800">Basic Information</h2>
                  <p className="text-gray-600 text-sm">Enter the student&apos;s personal details</p>
                </div>

                <div className="grid md:grid-cols-2 gap-6">
                  <div className="md:col-span-2">
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Full Name *
                    </label>
                    <input
                      name="full_name"
                      value={formData.full_name}
                      onChange={handleChange}
                      className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                      placeholder="Enter student's full name"
                    />
                    {errors.full_name && (
                      <p className="text-red-500 text-sm mt-1">{errors.full_name}</p>
                    )}
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Gender Identity
                    </label>
                    <select
                      name="gender_identity"
                      value={formData.gender_identity}
                      onChange={handleChange}
                      className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    >
                      <option value="">Select gender identity</option>
                      {details.gender_identities?.map((item) => (
                        <option key={item.id} value={item.id}>
                          {item.gender}
                        </option>
                      ))}
                    </select>
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Start Date
                    </label>
                    <input
                      name="start_date"
                      type="date"
                      value={formData.start_date}
                      onChange={handleChange}
                      className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      End Date
                    </label>
                    <input
                      name="end_date"
                      type="date"
                      value={formData.end_date}
                      onChange={handleChange}
                      className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    />
                  </div>
                </div>
              </div>
            )}

            {/* Step 2: Program Progress */}
            {currentStep === 2 && (
              <div className="space-y-6">
                <div className="text-center mb-6">
                  <h2 className="text-xl font-semibold text-gray-800">Program Progress</h2>
                  <p className="text-gray-600 text-sm">Track training completion and certifications</p>
                </div>

                <div className="grid md:grid-cols-2 gap-6">
                  <div className="space-y-4">
                    <div className="bg-blue-50 p-4 rounded-lg">
                      <h3 className="font-medium text-gray-800 mb-3">Training Completions</h3>
                      <div className="space-y-3">
                        <label className="flex items-center">
                          <input
                            type="checkbox"
                            name="complete_50_hour_training"
                            checked={formData.complete_50_hour_training}
                            onChange={handleChange}
                            className="w-4 h-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500"
                          />
                          <span className="ml-2 text-sm text-gray-700">50-Hour Training Complete</span>
                        </label>

                        <label className="flex items-center">
                          <input
                            type="checkbox"
                            name="hammer_math"
                            checked={formData.hammer_math}
                            onChange={handleChange}
                            className="w-4 h-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500"
                          />
                          <span className="ml-2 text-sm text-gray-700">Hammer Math Complete</span>
                        </label>

                        <label className="flex items-center">
                          <input
                            type="checkbox"
                            name="employability_skills"
                            checked={formData.employability_skills}
                            onChange={handleChange}
                            className="w-4 h-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500"
                          />
                          <span className="ml-2 text-sm text-gray-700">Employability Skills Complete</span>
                        </label>

                        <label className="flex items-center">
                          <input
                            type="checkbox"
                            name="passed_ruler_assessment"
                            checked={formData.passed_ruler_assessment}
                            onChange={handleChange}
                            className="w-4 h-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500"
                          />
                          <span className="ml-2 text-sm text-gray-700">Ruler Assessment Passed</span>
                        </label>
                      </div>
                    </div>
                  </div>

                  <div className="space-y-4">
                    <div className="bg-orange-50 p-4 rounded-lg">
                      <h3 className="font-medium text-gray-800 mb-3">OSHA Certification</h3>
                      <div className="space-y-3">
                        <label className="flex items-center">
                          <input
                            type="checkbox"
                            name="passed_osha_10_exam"
                            checked={formData.passed_osha_10_exam}
                            onChange={handleChange}
                            className="w-4 h-4 text-orange-600 border-gray-300 rounded focus:ring-orange-500"
                          />
                          <span className="ml-2 text-sm text-gray-700">OSHA 10 Exam Passed</span>
                        </label>

                        <div>
                          <label className="block text-sm font-medium text-gray-700 mb-1">
                            OSHA Type
                          </label>
                          <select
                            name="osha_type"
                            value={formData.osha_type}
                            onChange={handleChange}
                            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent text-sm"
                          >
                            <option value="">Select OSHA type</option>
                            {details.osha_types?.map((item) => (
                              <option key={item.id} value={item.id}>
                                {item.name}
                              </option>
                            ))}
                          </select>
                        </div>

                        <div>
                          <label className="block text-sm font-medium text-gray-700 mb-1">
                            OSHA Completion Date
                          </label>
                          <input
                            name="osha_completion_date"
                            type="date"
                            value={formData.osha_completion_date}
                            onChange={handleChange}
                            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent text-sm"
                          />
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            )}

            {/* Step 3: Assessments */}
            {currentStep === 3 && (
              <div className="space-y-6">
                <div className="text-center mb-6">
                  <h2 className="text-xl font-semibold text-gray-800">Personality Assessments</h2>
                  <p className="text-gray-600 text-sm">Select completed assessment results</p>
                </div>

                <div className="grid md:grid-cols-3 gap-6">
                  <div className="bg-blue-50 p-6 rounded-lg">
                    <div className="text-center mb-4">
                      <div className="text-3xl mb-2">🔵</div>
                      <h3 className="font-semibold text-blue-800">DISC Assessment</h3>
                    </div>
                    <select
                      name="disc_assessment_type"
                      value={formData.disc_assessment_type}
                      onChange={handleChange}
                      className="w-full px-3 py-2 border border-blue-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    >
                      <option value="">Select DISC type</option>
                      {details.disc_assessments?.map((item) => (
                        <option key={item.id} value={item.id}>
                          {item.type_name}
                        </option>
                      ))}
                    </select>
                  </div>

                  <div className="bg-purple-50 p-6 rounded-lg">
                    <div className="text-center mb-4">
                      <div className="text-3xl mb-2">🟣</div>
                      <h3 className="font-semibold text-purple-800">16 Types Assessment</h3>
                    </div>
                    <select
                      name="sixteen_types_assessment"
                      value={formData.sixteen_types_assessment}
                      onChange={handleChange}
                      className="w-full px-3 py-2 border border-purple-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                    >
                      <option value="">Select 16 type</option>
                      {details.sixteen_type_assessments?.map((item) => (
                        <option key={item.id} value={item.id}>
                          {item.type_name}
                        </option>
                      ))}
                    </select>
                  </div>

                  <div className="bg-green-50 p-6 rounded-lg">
                    <div className="text-center mb-4">
                      <div className="text-3xl mb-2">🟢</div>
                      <h3 className="font-semibold text-green-800">Enneagram</h3>
                    </div>
                    <select
                      name="enneagram_result"
                      value={formData.enneagram_result}
                      onChange={handleChange}
                      className="w-full px-3 py-2 border border-green-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent"
                    >
                      <option value="">Select Enneagram type</option>
                      {details.enneagram_results?.map((item) => (
                        <option key={item.id} value={item.id}>
                          {item.result_name}
                        </option>
                      ))}
                    </select>
                  </div>
                </div>
              </div>
            )}

            {/* Step 4: Test Scores */}
            {currentStep === 4 && (
              <div className="space-y-6">
                <div className="text-center mb-6">
                  <h2 className="text-xl font-semibold text-gray-800">Test Scores</h2>
                  <p className="text-gray-600 text-sm">Enter pre and post assessment scores</p>
                </div>

                <div className="grid md:grid-cols-2 gap-8">
                  <div className="bg-yellow-50 p-6 rounded-lg">
                    <div className="text-center mb-4">
                      <div className="text-4xl mb-2">📝</div>
                      <h3 className="font-semibold text-yellow-800">Pre-Test Score</h3>
                      <p className="text-yellow-600 text-sm">Baseline assessment score</p>
                    </div>
                    <input
                      name="pretest_score"
                      type="number"
                      min="0"
                      max="100"
                      value={formData.pretest_score}
                      onChange={handleChange}
                      className="w-full px-4 py-3 border border-yellow-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-yellow-500 focus:border-transparent text-center text-xl font-semibold"
                      placeholder="0-100"
                    />
                  </div>

                  <div className="bg-green-50 p-6 rounded-lg">
                    <div className="text-center mb-4">
                      <div className="text-4xl mb-2">📊</div>
                      <h3 className="font-semibold text-green-800">Post-Test Score</h3>
                      <p className="text-green-600 text-sm">Final assessment score</p>
                    </div>
                    <input
                      name="posttest_score"
                      type="number"
                      min="0"
                      max="100"
                      value={formData.posttest_score}
                      onChange={handleChange}
                      className="w-full px-4 py-3 border border-green-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent text-center text-xl font-semibold"
                      placeholder="0-100"
                    />
                  </div>
                </div>

                {/* Score Improvement Indicator */}
                {formData.pretest_score && formData.posttest_score && (
                  <div className="mt-6 p-4 bg-blue-50 rounded-lg">
                    <div className="text-center">
                      <div className="text-2xl mb-2">
                        {parseInt(formData.posttest_score) > parseInt(formData.pretest_score) ? '📈' : 
                         parseInt(formData.posttest_score) === parseInt(formData.pretest_score) ? '➡️' : '📉'}
                      </div>
                      <h4 className="font-semibold text-blue-800">
                        Score Change: {parseInt(formData.posttest_score) - parseInt(formData.pretest_score)} points
                      </h4>
                      <p className="text-blue-600 text-sm">
                        {parseInt(formData.posttest_score) > parseInt(formData.pretest_score) ? 
                         'Great improvement!' : 
                         parseInt(formData.posttest_score) === parseInt(formData.pretest_score) ? 
                         'Maintained score' : 
                         'Needs attention'}
                      </p>
                    </div>
                  </div>
                )}
              </div>
            )}

            {/* Navigation Buttons */}
            <div className="flex justify-between mt-8 pt-6 border-t border-gray-200">
              <button
                type="button"
                onClick={prevStep}
                disabled={currentStep === 1}
                className={`px-6 py-3 rounded-lg font-medium transition-colors ${
                  currentStep === 1
                    ? 'bg-gray-100 text-gray-400 cursor-not-allowed'
                    : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
                }`}
              >
                ← Previous
              </button>

              {currentStep < 4 ? (
                <button
                  type="button"
                  onClick={nextStep}
                  className="px-6 py-3 bg-blue-600 hover:bg-blue-700 text-white rounded-lg font-medium transition-colors"
                >
                  Next →
                </button>
              ) : (
                <button
                  type="submit"
                  className="px-8 py-3 bg-green-600 hover:bg-green-700 text-white rounded-lg font-medium transition-colors flex items-center"
                >
                  <span className="mr-2">✅</span>
                  Create Student
                </button>
              )}
            </div>
          </div>
        </form>
      </div>

      {/* Confirmation Modal */}
      {showModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-xl p-6 max-w-2xl w-full max-h-96 overflow-y-auto">
            <h2 className="text-xl font-semibold mb-4">Confirm Student Creation</h2>
            <p className="text-gray-600 mb-4">Please review the student information before saving:</p>
            
            <div className="bg-gray-50 rounded-lg p-4 mb-6">
              <h3 className="font-semibold text-lg text-gray-800 mb-2">{formData.full_name || "Unnamed Student"}</h3>
              <div className="grid grid-cols-2 gap-2 text-sm">
                <div><strong>Gender:</strong> {lookups.genderById[formData.gender_identity]?.gender || "Not specified"}</div>
                <div><strong>Start Date:</strong> {formData.start_date || "Not set"}</div>
                <div><strong>DISC:</strong> {lookups.discById[formData.disc_assessment_type]?.type_name || "Not selected"}</div>
                <div><strong>16 Types:</strong> {lookups.sixById[formData.sixteen_types_assessment]?.type_name || "Not selected"}</div>
                <div><strong>Enneagram:</strong> {lookups.enneagramById[formData.enneagram_result]?.result_name || "Not selected"}</div>
                <div><strong>OSHA:</strong> {lookups.oshaById[formData.osha_type]?.name || "Not selected"}</div>
              </div>
            </div>

            <div className="flex gap-3">
              <button
                onClick={() => setShowModal(false)}
                className="flex-1 px-4 py-2 bg-gray-200 hover:bg-gray-300 text-gray-800 rounded-lg transition-colors"
                disabled={isSaving}
              >
                Cancel
              </button>
              <button
                onClick={handleConfirmSave}
                disabled={isSaving}
                className="flex-1 px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg transition-colors flex items-center justify-center"
              >
                {isSaving ? (
                  <>
                    <div className="animate-spin rounded-full h-4 w-4 border-2 border-white border-t-transparent mr-2"></div>
                    Saving...
                  </>
                ) : (
                  "Save Student"
                )}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
