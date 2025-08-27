"use client";

import React, { useEffect, useMemo, useState } from "react";
import { useRouter, useParams } from "next/navigation";
import Link from "next/link";
import Image from "next/image";

// services
import { retrieveStudent, editStudent } from "@/app/services/students";
import { getdetails } from "@/app/services/details";

export default function EditStudentPage() {
  const router = useRouter();
  const { id } = useParams();

  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState(false);
  const [currentStep, setCurrentStep] = useState(1);
  const [showModal, setShowModal] = useState(false);
  const [errors, setErrors] = useState({});

  const [details, setDetails] = useState({});
  const [formData, setFormData] = useState({
    full_name: "",
    email: "",
    nccer_number: "",
    gender_identity: "",
    funding_source: "",
    start_date: "",
    end_date: "",
    complete_50_hour_training: false,
    passed_osha_10_exam: false,
    osha_completion_date: "",
    osha_type: "",
    hammer_math: false,
    employability_skills: false,
    job_interview_skills: false,
    passed_ruler_assessment: false,
    pretest_score: "",
    posttest_score: "",
    disc_assessment_type: "",
    sixteen_types_assessment: "",
    enneagram_result: "",
  });

  // Create lookup maps for dropdowns
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
      fundingById: mapBy(details.funding_sources),
    };
  }, [details]);

  // Check authentication
  useEffect(() => {
    const token = localStorage.getItem("token");
    if (!token) {
      router.push("/login");
      return;
    }
  }, [router]);

  // load reference lists + student
  useEffect(() => {
    let mounted = true;
    async function load() {
      try {
        const [detailsData, studentData] = await Promise.all([
          getdetails(),
          retrieveStudent(id)
        ]);
        
        if (!mounted) return;
        
        setDetails(detailsData);
        
        if (studentData) {
          setFormData({
            full_name: studentData.full_name || "",
            email: studentData.email || "",
            nccer_number: studentData.nccer_number || "",
            gender_identity: studentData.gender_identity?.id || "",
            funding_source: studentData.funding_source?.id || "",
            start_date: studentData.start_date || "",
            end_date: studentData.end_date || "",
            complete_50_hour_training: !!studentData.complete_50_hour_training,
            passed_osha_10_exam: !!studentData.passed_osha_10_exam,
            osha_completion_date: studentData.osha_completion_date || "",
            osha_type: studentData.osha_type?.id || "",
            hammer_math: !!studentData.hammer_math,
            employability_skills: !!studentData.employability_skills,
            job_interview_skills: !!studentData.job_interview_skills,
            passed_ruler_assessment: !!studentData.passed_ruler_assessment,
            pretest_score: studentData.pretest_score ?? "",
            posttest_score: studentData.posttest_score ?? "",
            disc_assessment_type: studentData.disc_assessment_type?.id || "",
            sixteen_types_assessment: studentData.sixteen_types_assessment?.id || "",
            enneagram_result: studentData.enneagram_result?.id || "",
          });
        }
      } catch (e) {
        if (mounted) {
          setError("Failed to load student data.");
        }
      } finally {
        if (mounted) {
          setLoading(false);
        }
      }
    }
    load();
    return () => { mounted = false; };
  }, [id]);

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: type === "checkbox" ? checked : value,
    }));
  };

  const validateForm = () => {
    if (!formData.full_name.trim()) {
      setError("Full name is required.");
      return false;
    }
    
    // Validate test scores if provided
    if (formData.pretest_score) {
      const pretest = parseInt(formData.pretest_score);
      if (pretest < 1 || pretest > 14) {
        setError("Pre-test score must be between 1 and 14.");
        return false;
      }
    }
    
    if (formData.posttest_score) {
      const posttest = parseInt(formData.posttest_score);
      if (posttest < 1 || posttest > 14) {
        setError("Post-test score must be between 1 and 14.");
        return false;
      }
    }
    
    setError("");
    return true;
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    // Only show modal on final step, otherwise just navigate
    if (currentStep === 4) {
      if (validateForm()) setShowModal(true);
    }
  };

  const handleConfirmSave = async () => {
    setSaving(true);
    try {
      const payload = {
        full_name: formData.full_name,
        email: formData.email || null,
        nccer_number: formData.nccer_number || null,
        gender_identity_id: Number(formData.gender_identity) || null,
        funding_source_id: Number(formData.funding_source) || null,
        start_date: formData.start_date || null,
        end_date: formData.end_date || null,
        complete_50_hour_training: !!formData.complete_50_hour_training,
        passed_osha_10_exam: !!formData.passed_osha_10_exam,
        osha_completion_date: formData.osha_completion_date || null,
        osha_type_id: Number(formData.osha_type) || null,
        hammer_math: !!formData.hammer_math,
        employability_skills: !!formData.employability_skills,
        job_interview_skills: !!formData.job_interview_skills,
        passed_ruler_assessment: !!formData.passed_ruler_assessment,
        pretest_score: formData.pretest_score === "" ? null : Number(formData.pretest_score),
        posttest_score: formData.posttest_score === "" ? null : Number(formData.posttest_score),
        disc_assessment_type_id: Number(formData.disc_assessment_type) || null,
        sixteen_types_assessment_id: Number(formData.sixteen_types_assessment) || null,
        enneagram_result_id: Number(formData.enneagram_result) || null,
      };

      await editStudent(payload, id);
      setSuccess(true);
      setShowModal(false);
      setTimeout(() => router.push(`/students/${id}`), 1200);
    } catch (e) {
      console.error("Error updating student:", e);
      
      // Try to extract the actual error message from the response
      let errorMessage = "Failed to update student.";
      
      // Check if we have detailed error data from the API response
      if (e.data) {
        if (e.data.non_field_errors) {
          errorMessage = e.data.non_field_errors.join(', ');
        } else if (e.data.detail) {
          errorMessage = e.data.detail;
        } else {
          // Collect field-specific errors
          const fieldErrors = [];
          Object.keys(e.data).forEach(field => {
            if (Array.isArray(e.data[field])) {
              fieldErrors.push(`${field}: ${e.data[field].join(', ')}`);
            } else {
              fieldErrors.push(`${field}: ${e.data[field]}`);
            }
          });
          if (fieldErrors.length > 0) {
            errorMessage = fieldErrors.join('\n');
          }
        }
      } else if (e.response) {
        // Try to parse the response text
        try {
          const errorData = JSON.parse(e.response);
          if (errorData.non_field_errors) {
            errorMessage = errorData.non_field_errors.join(', ');
          } else if (errorData.detail) {
            errorMessage = errorData.detail;
          } else {
            // Collect field-specific errors
            const fieldErrors = [];
            Object.keys(errorData).forEach(field => {
              if (Array.isArray(errorData[field])) {
                fieldErrors.push(`${field}: ${errorData[field].join(', ')}`);
              } else {
                fieldErrors.push(`${field}: ${errorData[field]}`);
              }
            });
            if (fieldErrors.length > 0) {
              errorMessage = fieldErrors.join('\n');
            }
          }
        } catch (parseError) {
          errorMessage = e.response || e.message || "Failed to update student.";
        }
      } else if (e.message) {
        errorMessage = e.message.includes('HTTP error!') 
          ? "Failed to update student. Please check your input and try again."
          : e.message;
      }
      
      setError(errorMessage);
    } finally {
      setSaving(false);
    }
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

  // Loading state
  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-orange-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-16 w-16 border-4 border-blue-600 border-t-transparent mx-auto mb-4"></div>
          <p className="text-gray-600 text-lg">Loading student data...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-orange-50">
      {/* Header */}
      <div className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center">
              <Link href="/students" className="mr-4">
                <Image
                  src="/Hammer-Primary-Blue-Logo.png"
                  alt="If I Had A Hammer Logo"
                  width={120}
                  height={40}
                  className="h-8 w-auto"
                />
              </Link>
              <div>
                <h1 className="text-2xl font-bold text-gray-900">Edit Student</h1>
                <p className="text-gray-600 text-sm">Update {formData.full_name || "student"} information</p>
              </div>
            </div>
            <div className="flex items-center gap-4">
              <Link
                href={`/students/${id}`}
                className="px-4 py-2 text-gray-600 hover:text-gray-800 border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors"
              >
                ← Back to Profile
              </Link>
              <Link
                href="/students"
                className="px-4 py-2 text-gray-600 hover:text-gray-800 border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors"
              >
                All Students
              </Link>
            </div>
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

        {/* Error Message */}
        {error && (
          <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded-lg">
            <div className="flex items-center">
              <span className="text-2xl mr-3">⚠️</span>
              <div>
                <h3 className="text-red-800 font-semibold">Error</h3>
                <p className="text-red-600 text-sm">{error}</p>
              </div>
            </div>
          </div>
        )}

        {/* Success Message */}
        {success && (
          <div className="mb-6 p-4 bg-green-50 border border-green-200 rounded-lg">
            <div className="flex items-center">
              <span className="text-2xl mr-3">✅</span>
              <div>
                <h3 className="text-green-800 font-semibold">Student Updated Successfully!</h3>
                <p className="text-green-600 text-sm">Redirecting to student profile...</p>
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
                  <p className="text-gray-600 text-sm">Update the student&apos;s personal details</p>
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
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Email Address
                    </label>
                    <input
                      type="email"
                      name="email"
                      value={formData.email}
                      onChange={handleChange}
                      className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                      placeholder="Enter student's email"
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      NCCER Number
                    </label>
                    <input
                      name="nccer_number"
                      value={formData.nccer_number}
                      onChange={handleChange}
                      className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                      placeholder="Enter NCCER credential number"
                    />
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
                      Funding Source
                    </label>
                    <select
                      name="funding_source"
                      value={formData.funding_source}
                      onChange={handleChange}
                      className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    >
                      <option value="">Select funding source</option>
                      {details.funding_sources?.map((item) => (
                        <option key={item.id} value={item.id}>
                          {item.name}
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
                  <p className="text-gray-600 text-sm">Update training completion and certifications</p>
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
                            name="job_interview_skills"
                            checked={formData.job_interview_skills}
                            onChange={handleChange}
                            className="w-4 h-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500"
                          />
                          <span className="ml-2 text-sm text-gray-700">Job Interview Skills Complete</span>
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
                  <p className="text-gray-600 text-sm">Update assessment results</p>
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
                  <p className="text-gray-600 text-sm">Update pre and post assessment scores (1-14 scale)</p>
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
                      min="1"
                      max="14"
                      value={formData.pretest_score}
                      onChange={handleChange}
                      className="w-full px-4 py-3 border border-yellow-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-yellow-500 focus:border-transparent text-center text-xl font-semibold"
                      placeholder="1-14"
                    />
                  </div>

                  <div className="bg-green-50 p-6 rounded-lg">
                    <div className="text-center mb-4">
                      <div className="text-4xl mb-2">📊</div>
                      <h3 className="font-semibold text-green-800">Post-Test Score</h3>
                      <p className="text-green-600 text-sm">*Must have at least 10 to Pass*</p>
                    </div>
                    <input
                      name="posttest_score"
                      type="number"
                      min="1"
                      max="14"
                      value={formData.posttest_score}
                      onChange={handleChange}
                      className="w-full px-4 py-3 border border-green-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent text-center text-xl font-semibold"
                      placeholder="1-14"
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
                  type="button"
                  onClick={() => {
                    if (validateForm()) setShowModal(true);
                  }}
                  className="px-8 py-3 bg-orange-600 hover:bg-orange-700 text-white rounded-lg font-medium transition-colors flex items-center"
                >
                  <span className="mr-2">💾</span>
                  Update Student
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
            <h2 className="text-xl font-semibold mb-4">Confirm Student Update</h2>
            <p className="text-gray-600 mb-4">Please review the updated information before saving:</p>
            
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
                disabled={saving}
              >
                Cancel
              </button>
              <button
                onClick={handleConfirmSave}
                disabled={saving}
                className="flex-1 px-4 py-2 bg-orange-600 hover:bg-orange-700 text-white rounded-lg transition-colors flex items-center justify-center"
              >
                {saving ? (
                  <>
                    <div className="animate-spin rounded-full h-4 w-4 border-2 border-white border-t-transparent mr-2"></div>
                    Updating...
                  </>
                ) : (
                  "Update Student"
                )}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
