"use client";

import { useEffect, useState } from "react";
import { useParams, useRouter } from "next/navigation";
import Link from "next/link";
import Image from "next/image";

// Import services and components
import { retrieveStudent, deleteStudent } from "@/app/services/students"; // API to fetch student data
import CertificateOptions from "@/app/components/certificateOptions"; // Certificate UI
import { generateCertificates } from "@/app/services/pdf"; // Service to handle PDF generation
import StudentSummary from "@/app/components/summary"; // Component for displaying student details
import { generateAiSummary } from "@/app/services/pdf";
import { generateMasterPortfolio } from "@/app/services/pdf";

/**
 * StudentDetails Page
 * --------------------------
 * Displays full student info (via StudentSummary)
 * and provides UI to generate selected certificates.
 */
export default function StudentDetails() {
  const { id } = useParams(); // Get student ID from URL
  const [student, setStudent] = useState(null); // Holds student data
  const [loading, setLoading] = useState(true); // Loading state for fetching data
  const [showDeleteModal, setShowDeleteModal] = useState(false); // Delete confirmation modal
  const [deleting, setDeleting] = useState(false); // Deleting state
  const router = useRouter();

  // Check authentication
  useEffect(() => {
    const token = localStorage.getItem("token");
    if (!token) {
      router.push("/login");
      return;
    }
  }, [router]);

  // Fetch student details on component mount
  useEffect(() => {
    retrieveStudent(id)
      .then((data) => setStudent(data)) // Save student data
      .finally(() => setLoading(false)); // Stop loading spinner
  }, [id]);

  // Handle student deletion
  const handleDeleteStudent = async () => {
    setDeleting(true);
    try {
      await deleteStudent(id);
      // Redirect to students list after successful deletion
      router.push("/students");
    } catch (error) {
      console.error("Failed to delete student:", error);
      alert("Failed to delete student. Please try again.");
      setDeleting(false);
      setShowDeleteModal(false);
    }
  };

  // Show loading state
  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-orange-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-16 w-16 border-4 border-blue-600 border-t-transparent mx-auto mb-4"></div>
          <p className="text-gray-600 text-lg">Loading student details...</p>
        </div>
      </div>
    );
  }

  // If no student found
  if (!student) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-orange-50 flex items-center justify-center">
        <div className="text-center">
          <div className="text-6xl mb-4">❌</div>
          <h2 className="text-2xl font-bold text-gray-800 mb-2">Student Not Found</h2>
          <p className="text-gray-600 mb-6">The requested student could not be found.</p>
          <Link
            href="/students"
            className="inline-flex items-center px-6 py-3 bg-blue-600 hover:bg-blue-700 text-white rounded-lg font-medium transition-colors"
          >
            ← Back to Students
          </Link>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-orange-50">
      {/* Header */}
      <div className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
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
                <h1 className="text-2xl font-bold text-gray-900">{student.full_name}</h1>
                <p className="text-gray-600 text-sm">Student Profile & Certificate Management</p>
              </div>
            </div>
            <div className="flex items-center gap-4">
              <Link
                href={`/students/${student.id}/edit`}
                className="inline-flex items-center px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg font-medium transition-colors"
              >
                <span className="mr-2">✏️</span>
                Edit Student
              </Link>
              <button
                onClick={() => setShowDeleteModal(true)}
                className="inline-flex items-center px-4 py-2 bg-red-600 hover:bg-red-700 text-white rounded-lg font-medium transition-colors"
              >
                <span className="mr-2">🗑️</span>
                Delete Student
              </button>
              <Link
                href="/students"
                className="px-4 py-2 text-gray-600 hover:text-gray-800 border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors"
              >
                ← Back to Students
              </Link>
            </div>
          </div>
        </div>
      </div>

      {/* Content */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Left Column: Student Summary (2/3 width on large screens) */}
          <div className="lg:col-span-2">
            <StudentSummary student={student} />
          </div>

          {/* Right Column: Certificate Generation (1/3 width on large screens) */}
          <div className="lg:col-span-1">
            <CertificateOptions
              student={student}
              generateAiSummary={generateAiSummary}
              onGenerate={generateCertificates} // Pass the PDF service function
              generateMasterPortfolio={generateMasterPortfolio}
            />
          </div>
        </div>
      </div>

      {/* Delete Confirmation Modal */}
      {showDeleteModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-xl p-6 max-w-md w-full">
            <div className="text-center">
              <div className="text-6xl mb-4">⚠️</div>
              <h2 className="text-2xl font-bold text-gray-900 mb-2">Delete Student</h2>
              <p className="text-gray-600 mb-6">
                Are you sure you want to delete <strong>{student.full_name}</strong>? 
                This action cannot be undone and will permanently remove all student data, including certificates and assessments.
              </p>
              
              <div className="flex gap-3">
                <button
                  onClick={() => setShowDeleteModal(false)}
                  disabled={deleting}
                  className="flex-1 px-4 py-3 bg-gray-200 hover:bg-gray-300 text-gray-800 rounded-lg font-medium transition-colors"
                >
                  Cancel
                </button>
                <button
                  onClick={handleDeleteStudent}
                  disabled={deleting}
                  className="flex-1 px-4 py-3 bg-red-600 hover:bg-red-700 text-white rounded-lg font-medium transition-colors flex items-center justify-center"
                >
                  {deleting ? (
                    <>
                      <div className="animate-spin rounded-full h-4 w-4 border-2 border-white border-t-transparent mr-2"></div>
                      Deleting...
                    </>
                  ) : (
                    <>
                      <span className="mr-2">🗑️</span>
                      Delete Student
                    </>
                  )}
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
