"use client";

import { useEffect, useState } from "react";
import { useParams, useRouter } from "next/navigation";

// Import services and components
import { retrieveStudent } from "@/app/services/students"; // API to fetch student data
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

  return (
    <div className="min-h-screen bg-gray-50 p-6">
      <div className="flex items-center justify-center mb-6">
          <button onClick={() => router.back()} className="text-blue-600 hover:underline">← Back</button>
          
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
    </div>
  );
}
