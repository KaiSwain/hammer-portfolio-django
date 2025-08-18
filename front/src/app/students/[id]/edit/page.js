"use client";

import React, { useEffect, useMemo, useState } from "react";
import { useRouter, useParams } from "next/navigation";

// services
import { retrieveStudent, editStudent } from "@/app/services/students";
import { getdetails } from "@/app/services/details";

/**
 * EditStudentPage
 * - Loads a student by id
 * - Pre-fills a form
 * - Lets you edit & save (PATCH)
 * - Uses dropdowns for related fields (IDs)
 */
export default function EditStudentPage() {
  const router = useRouter();
  const { id } = useParams();

  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState(false);

  const [details, setDetails] = useState({});
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
    sixteen_types_assessment: "",
    enneagram_result: "",
  });

  // load reference lists + student
  useEffect(() => {
    let mounted = true;
    async function load() {
      try {
        const [dets, stu] = await Promise.all([getdetails(), retrieveStudent(id)]);
        if (!mounted) return;
        setDetails(dets || {});
        if (stu) {
          // convert nested objects -> IDs or friendly strings for inputs
          setFormData({
            full_name: stu.full_name || "",
            gender_identity: stu.gender_identity?.id ?? "",
            start_date: stu.start_date || "",
            end_date: stu.end_date || "",
            complete_50_hour_training: !!stu.complete_50_hour_training,
            passed_osha_10_exam: !!stu.passed_osha_10_exam,
            osha_completion_date: stu.osha_completion_date || "",
            osha_type: stu.osha_type?.id ?? "",
            hammer_math: !!stu.hammer_math,
            employability_skills: !!stu.employability_skills,
            passed_ruler_assessment: !!stu.passed_ruler_assessment,
            pretest_score: stu.pretest_score ?? "",
            posttest_score: stu.posttest_score ?? "",
            disc_assessment_type: stu.disc_assessment_type?.id ?? "",
            sixteen_types_assessment: stu.sixteen_types_assessment?.id ?? "",
            enneagram_result: stu.enneagram_result?.id ?? "",
          });
        }
      } catch (e) {
        setError("Failed to load student.");
      } finally {
        setLoading(false);
      }
    }
    load();
    return () => {
      mounted = false;
    };
  }, [id]);

  // generic change handler
  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: type === "checkbox" ? checked : value,
    }));
  };

  // simple validate: require name
  const validate = () => {
    if (!formData.full_name.trim()) {
      setError("Full name is required.");
      return false;
    }
    setError("");
    return true;
  };

  const handleSave = async (e) => {
    e.preventDefault();
    if (!validate()) return;
    setSaving(true);
    setSuccess(false);
    try {
      // coerce blanks to null for FKs + numbers
      const payload = {
        full_name: formData.full_name,
        gender_identity_id: Number(formData.gender_identity) || null,
        start_date: formData.start_date || null,
        end_date: formData.end_date || null,
        complete_50_hour_training: !!formData.complete_50_hour_training,
        passed_osha_10_exam: !!formData.passed_osha_10_exam,
        osha_completion_date: formData.osha_completion_date || null,
        osha_type_id: Number(formData.osha_type) || null,
        hammer_math: !!formData.hammer_math,
        employability_skills: !!formData.employability_skills,
        passed_ruler_assessment: !!formData.passed_ruler_assessment,
        pretest_score: formData.pretest_score === "" ? null : Number(formData.pretest_score),
        posttest_score: formData.posttest_score === "" ? null : Number(formData.posttest_score),
        disc_assessment_type_id: Number(formData.disc_assessment_type) || null,
        sixteen_types_assessment_id: Number(formData.sixteen_types_assessment) || null,
        enneagram_result_id: Number(formData.enneagram_result) || null,
      };

      await editStudent(payload, id); // expects PATCH in service for partial, or PUT with partial=True on server
      setSuccess(true);
      // optional: navigate back after short delay
      // setTimeout(() => router.push("/students"), 1200);
    } catch (err) {
      setError("Failed to save changes.");
    } finally {
      setSaving(false);
    }
  };

  if (loading) return <div className="p-6">Loading...</div>;
  if (!formData) return <div className="p-6">Student not found.</div>;

  return (
    <div className="min-h-screen bg-gray-50 p-6">
      <div className="max-w-3xl mx-auto bg-white rounded-lg shadow p-6">
        <div className="flex items-center justify-between mb-6">
          <button onClick={() => router.back()} className="text-blue-600 hover:underline">← Back</button>
          <h1 className="text-2xl font-bold text-gray-800">Edit Student</h1>
        </div>

        {error && <div className="mb-4 p-3 rounded bg-red-100 text-red-700">{error}</div>}
        {success && <div className="mb-4 p-3 rounded bg-green-100 text-green-700">✅ Saved!</div>}

        <form onSubmit={handleSave} className="space-y-6">
          {/* STUDENT INFO */}
          <section>
            <h2 className="text-sm font-bold text-gray-600 tracking-widest mb-2">STUDENT INFO</h2>
            <label className="block text-sm font-medium text-gray-700">Full Name *</label>
            <input
              name="full_name"
              className="w-full border border-gray-300 rounded p-2 mt-1"
              value={formData.full_name}
              onChange={handleChange}
            />

            <label className="block text-sm font-medium text-gray-700 mt-4">Gender Identity</label>
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
          </section>

          {/* DATES */}
          <section>
            <h2 className="text-sm font-bold text-gray-600 tracking-widest mb-2"></h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700">Class Start Date</label>
                <input type="date" name="start_date" className="w-full border border-gray-300 rounded p-2 mt-1" value={formData.start_date || ""} onChange={handleChange} />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700">Class End Date</label>
                <input type="date" name="end_date" className="w-full border border-gray-300 rounded p-2 mt-1" value={formData.end_date || ""} onChange={handleChange} />
              </div>
            </div>
          </section>

          {/* OSHA */}
          <section>
            <h2 className="text-sm font-bold text-gray-600 tracking-widest mb-2"></h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700">OSHA Type</label>
                <select name="osha_type" value={formData.osha_type} onChange={handleChange} className="w-full border border-gray-300 rounded p-2 mt-1">
                  <option value="">Select</option>
                  {details.osha_types?.map((o) => (
                    <option key={o.id} value={o.id}>{o.name}</option>
                  ))}
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700">OSHA Completion Date</label>
                <input type="date" name="osha_completion_date" className="w-full border border-gray-300 rounded p-2 mt-1" value={formData.osha_completion_date || ""} onChange={handleChange} />
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mt-2">
            </div>
          </section>

          {/* CERTIFICATIONS / SKILLS */}
          <section>
            <h2 className="text-sm font-bold text-gray-600 tracking-widest mb-2">CERTIFICATIONS & SKILLS</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <label className="flex items-center gap-2">
                <input type="checkbox" name="passed_osha_10_exam" checked={formData.passed_osha_10_exam} onChange={handleChange} />
                <span className="text-sm">Passed OSHA 10 Exam</span>
              </label>
              <label className="flex items-center gap-2">
                <input type="checkbox" name="complete_50_hour_training" checked={formData.complete_50_hour_training} onChange={handleChange} />
                <span className="text-sm">Completed 50-Hour Training</span>
              </label>
              <label className="flex items-center gap-2">
                <input type="checkbox" name="hammer_math" checked={formData.hammer_math} onChange={handleChange} />
                <span className="text-sm">Completed HammerMath</span>
              </label>
              <label className="flex items-center gap-2">
                <input type="checkbox" name="employability_skills" checked={formData.employability_skills} onChange={handleChange} />
                <span className="text-sm">Completed Employability Skills Training</span>
              </label>
              <label className="flex items-center gap-2">
                <input type="checkbox" name="passed_ruler_assessment" checked={formData.passed_ruler_assessment} onChange={handleChange} />
                <span className="text-sm">Passed Reading a Ruler Assessment</span>
              </label>
            </div>
          </section>

          {/* ASSESSMENTS */}
          <section>
            <h2 className="text-sm font-bold text-gray-600 tracking-widest mb-2">ASSESSMENTS</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mt-4">
              <div>
                <label className="block text-sm font-medium text-gray-700">Reading a Ruler Pre-test Score</label>
                <select name="pretest_score" value={formData.pretest_score} onChange={handleChange} className="w-full border border-gray-300 rounded p-2">
                  <option value="">Select</option>
                  {[...Array(14)].map((_, i) => (
                    <option key={i + 1} value={i + 1}>{i + 1}</option>
                  ))}
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700">Reading a Ruler Post-test Score</label>
                <select name="posttest_score" value={formData.posttest_score} onChange={handleChange} className="w-full border border-gray-300 rounded p-2">
                  <option value="">Select</option>
                  {[...Array(14)].map((_, i) => (
                    <option key={i + 1} value={i + 1}>{i + 1}</option>
                  ))}
                </select>
              </div>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mt-3">
              <div>
                <label className="block text-sm font-medium text-gray-700">DISC Assessment Type</label>
                <select name="disc_assessment_type" value={formData.disc_assessment_type} onChange={handleChange} className="w-full border border-gray-300 rounded p-2 mt-1">
                  <option value="">Select</option>
                  {details.disc_assessments?.map((d) => (
                    <option key={d.id} value={d.id}>{d.type_name}</option>
                  ))}
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700">16 Types Assessment</label>
                <select name="sixteen_types_assessment" value={formData.sixteen_types_assessment} onChange={handleChange} className="w-full border border-gray-300 rounded p-2 mt-1">
                  <option value="">Select</option>
                  {details.sixteen_type_assessments?.map((t) => (
                    <option key={t.id} value={t.id}>{t.type_name}</option>
                  ))}
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700">Enneagram Result</label>
                <select name="enneagram_result" value={formData.enneagram_result} onChange={handleChange} className="w-full border border-gray-300 rounded p-2 mt-1">
                  <option value="">Select</option>
                  {details.enneagram_results?.map((e) => (
                    <option key={e.id} value={e.id}>{e.result_name}</option>
                  ))}
                </select>
              </div>
            </div>

          </section>

          <div className="flex items-center justify-end gap-3 pt-2">
            <button type="button" onClick={() => router.back()} className="px-4 py-2 rounded bg-gray-100 hover:bg-gray-200">Cancel</button>
            <button type="submit" disabled={saving} className="px-4 py-2 rounded bg-blue-600 text-white hover:bg-blue-700 disabled:opacity-60">
              {saving ? "Saving..." : "Save Changes"}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
