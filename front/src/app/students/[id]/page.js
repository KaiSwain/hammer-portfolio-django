"use client";

import { useEffect, useState } from "react";
import { useParams, useRouter } from "next/navigation";

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
  const [showDeleteModal, setShowDeleteModal] = useState(false);
  const router = useRouter();
  // Fetch student details on component mount
  useEffect(() => {
    retrieveStudent(id)
      .then((data) => setStudent(data)) // Save student data
      .finally(() => setLoading(false)); // Stop loading spinner
  }, [id]);

  // Show loading state
  if (loading) return <p>Loading...</p>;

  // If no student found
  if (!student) return <p>No student found</p>;

  const handleDelete = async () => {
    try {
      await deleteStudent(id);
      router.push('/students');
    } catch (error) {
      console.error('Error deleting student:', error);
      alert('Failed to delete student');
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 p-6">
      <div className="flex items-center justify-between mb-6">
        <button onClick={() => router.back()} className="text-blue-600 hover:underline">← Back</button>
        <div className="flex space-x-4">
          <button 
            onClick={() => router.push(`/students/${id}/edit`)}
            className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
          >
            ✏️ Edit Student
          </button>
          <button 
            onClick={() => setShowDeleteModal(true)}
            className="px-4 py-2 bg-red-600 text-white rounded hover:bg-red-700"
          >
            🗑️ Delete Student
          </button>
        </div>
      </div>
      <div className="max-w-5xl mx-auto grid grid-cols-1 md:grid-cols-2 gap-8">
        
        {/* ✅ Left Column: Student Summary */}
        <StudentSummary student={student} />

        {/* ✅ Right Column: Certificate Generation */}
        <CertificateOptions
          student={student}
          generateAiSummary={generateAiSummary}
          onGenerate={generateCertificates} // Pass the PDF service function
          generateMasterPortfolio={generateMasterPortfolio}
        />
      </div>

      {/* Delete Confirmation Modal */}
      {showDeleteModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white p-6 rounded-lg shadow-lg max-w-md w-full mx-4">
            <h3 className="text-lg font-bold mb-4 text-red-600">⚠️ Confirm Deletion</h3>
            <p className="mb-6">
              Are you sure you want to delete <strong>{student?.full_name}</strong>? 
              This action cannot be undone and will permanently remove all student data.
            </p>
            <div className="flex space-x-4 justify-end">
              <button 
                onClick={() => setShowDeleteModal(false)}
                className="px-4 py-2 bg-gray-300 text-gray-700 rounded hover:bg-gray-400"
              >
                Cancel
              </button>
              <button 
                onClick={handleDelete}
                className="px-4 py-2 bg-red-600 text-white rounded hover:bg-red-700"
              >
                Delete Student
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
