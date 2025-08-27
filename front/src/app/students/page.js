"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import Image from "next/image";
import { getStudents } from "../services/students";
import { useRouter } from "next/navigation";

export default function StudentPage() {
  const [students, setStudents] = useState([]);
  const [filteredStudents, setFilteredStudents] = useState([]);
  const [searchTerm, setSearchTerm] = useState("");
  const [sortBy, setSortBy] = useState("");
  const [isLoading, setIsLoading] = useState(true);
  const router = useRouter();

  useEffect(() => {
    // Check authentication
    const token = localStorage.getItem("token");
    if (!token) {
      router.push("/login");
      return;
    }

    setIsLoading(true);
    getStudents()
      .then((data) => {
        console.log('Students data received:', data);
        // Handle both paginated and non-paginated responses
        const studentsArray = data.results ? data.results : (Array.isArray(data) ? data : []);
        setStudents(studentsArray);
        setFilteredStudents(studentsArray);
      })
      .catch((error) => {
        console.error('Error fetching students:', error);
        // If unauthorized, redirect to login
        if (error.message?.includes('401') || error.message?.includes('unauthorized')) {
          localStorage.removeItem("token");
          router.push("/login");
          return;
        }
        // Set empty array on other errors
        setStudents([]);
        setFilteredStudents([]);
      })
      .finally(() => {
        setIsLoading(false);
      });
  }, [router]);

  const handleSearch = (e) => {
    const value = e.target.value.toLowerCase();
    setSearchTerm(value);
    filterStudents(value, sortBy);
  };

  const handleSort = (e) => {
    const sortType = e.target.value;
    setSortBy(sortType);
    filterStudents(searchTerm, sortType);
  };

  const filterStudents = (search, sortType) => {
    let data = [...students];
    if (search) {
      data = data.filter((s) => s.full_name.toLowerCase().includes(search));
    }
    if (sortType === "start_date") {
      data.sort((a, b) => new Date(a.start_date) - new Date(b.start_date));
    } else if (sortType === "recent") {
      data.sort((a, b) => new Date(b.created_at) - new Date(a.created_at));
    }
    setFilteredStudents(data);
  };

  const handleLogout = () => {
    localStorage.removeItem("token");
    router.push("/login");
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-orange-50">
      {/* Header */}
      <div className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex justify-between items-center">
            <div className="flex items-center">
              <Link href="/" className="mr-4">
                <Image
                  src="/Hammer-Primary-Blue-Logo.png"
                  alt="If I Had A Hammer Logo"
                  width={120}
                  height={40}
                  className="h-8 w-auto"
                />
              </Link>
              <div>
                <h1 className="text-2xl font-bold text-gray-900">Student Portfolio</h1>
                <p className="text-gray-600 text-sm">If I Had A Hammer - Teacher Dashboard</p>
              </div>
            </div>
            <div className="flex space-x-3">
              <button
                onClick={() => router.push("/students/add")}
                className="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg font-medium transition-colors flex items-center"
              >
                <span className="mr-2">➕</span>
                Add Student
              </button>
              <button
                onClick={handleLogout}
                className="px-4 py-2 bg-gray-600 hover:bg-gray-700 text-white rounded-lg font-medium transition-colors"
              >
                Logout
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Search and Filters */}
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6 mb-6">
          <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
            <div className="flex-1 max-w-md">
              <label className="block text-sm font-medium text-gray-700 mb-2">Search Students</label>
              <input
                type="text"
                placeholder="Search by student name..."
                value={searchTerm}
                onChange={handleSearch}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>
            <div className="w-full sm:w-auto">
              <label className="block text-sm font-medium text-gray-700 mb-2">Sort By</label>
              <select
                value={sortBy}
                onChange={handleSort}
                className="w-full sm:w-auto px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              >
                <option value="">Default Order</option>
                <option value="start_date">Start Date</option>
                <option value="recent">Recently Added</option>
              </select>
            </div>
          </div>
        </div>

        {/* Students Grid/Table */}
        {isLoading ? (
          <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-12 text-center">
            <div className="animate-spin rounded-full h-12 w-12 border-4 border-blue-600 border-t-transparent mx-auto mb-4"></div>
            <p className="text-gray-600">Loading students...</p>
          </div>
        ) : filteredStudents.length === 0 ? (
          <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-12 text-center">
            <div className="text-6xl mb-4">👥</div>
            <h3 className="text-lg font-semibold text-gray-800 mb-2">No Students Found</h3>
            <p className="text-gray-600 mb-6">
              {searchTerm ? "No students match your search criteria." : "Get started by adding your first student."}
            </p>
            {!searchTerm && (
              <button
                onClick={() => router.push("/students/add")}
                className="px-6 py-3 bg-blue-600 hover:bg-blue-700 text-white rounded-lg font-medium transition-colors"
              >
                Add Your First Student
              </button>
            )}
          </div>
        ) : (
          <div className="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead className="bg-gray-50 border-b border-gray-200">
                  <tr>
                    <th className="px-6 py-4 text-left text-sm font-semibold text-gray-900">Student</th>
                    <th className="px-6 py-4 text-left text-sm font-semibold text-gray-900">Program Progress</th>
                    <th className="px-6 py-4 text-left text-sm font-semibold text-gray-900">Assessments</th>
                    <th className="px-6 py-4 text-left text-sm font-semibold text-gray-900">Timeline</th>
                    <th className="px-6 py-4 text-left text-sm font-semibold text-gray-900">Actions</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-200">
                  {filteredStudents.map((student) => (
                    <tr
                      key={student.id}
                      className="hover:bg-gray-50 transition-colors"
                    >
                      <td className="px-6 py-4">
                        <div className="flex items-center">
                          <div className="flex-shrink-0 w-10 h-10 bg-blue-100 rounded-full flex items-center justify-center">
                            <span className="text-blue-600 font-semibold">
                              {student.full_name?.charAt(0)?.toUpperCase() || "?"}
                            </span>
                          </div>
                          <div className="ml-4">
                            <div className="text-sm font-semibold text-gray-900">{student.full_name}</div>
                            <div className="text-sm text-gray-500">
                              {student.gender_identity?.gender || "Not specified"}
                            </div>
                          </div>
                        </div>
                      </td>
                      <td className="px-6 py-4">
                        <div className="space-y-1">
                          <div className="flex items-center text-xs">
                            <span className={`w-2 h-2 rounded-full mr-2 ${student.complete_50_hour_training ? 'bg-green-500' : 'bg-gray-300'}`}></span>
                            50hr Training
                          </div>
                          <div className="flex items-center text-xs">
                            <span className={`w-2 h-2 rounded-full mr-2 ${student.passed_osha_10_exam ? 'bg-green-500' : 'bg-gray-300'}`}></span>
                            OSHA 10
                          </div>
                          <div className="flex items-center text-xs">
                            <span className={`w-2 h-2 rounded-full mr-2 ${student.hammer_math ? 'bg-green-500' : 'bg-gray-300'}`}></span>
                            Hammer Math
                          </div>
                          <div className="flex items-center text-xs">
                            <span className={`w-2 h-2 rounded-full mr-2 ${student.employability_skills ? 'bg-green-500' : 'bg-gray-300'}`}></span>
                            Employability Skills
                          </div>
                          <div className="flex items-center text-xs">
                            <span className={`w-2 h-2 rounded-full mr-2 ${student.job_interview_skills ? 'bg-green-500' : 'bg-gray-300'}`}></span>
                            Job Interview Skills
                          </div>
                          <div className="flex items-center text-xs">
                            <span className={`w-2 h-2 rounded-full mr-2 ${student.passed_ruler_assessment ? 'bg-green-500' : 'bg-gray-300'}`}></span>
                            Reading Ruler Assessment
                          </div>
                        </div>
                      </td>
                      <td className="px-6 py-4">
                        <div className="space-y-1 text-xs">
                          <div className={`px-2 py-1 rounded-full text-center ${student.disc_assessment_type ? 'bg-blue-100 text-blue-800' : 'bg-gray-100 text-gray-500'}`}>
                            DISC: {student.disc_assessment_type?.type_name || "Pending"}
                          </div>
                          <div className={`px-2 py-1 rounded-full text-center ${student.sixteen_types_assessment ? 'bg-purple-100 text-purple-800' : 'bg-gray-100 text-gray-500'}`}>
                            16T: {student.sixteen_types_assessment?.type_name || "Pending"}
                          </div>
                          <div className={`px-2 py-1 rounded-full text-center ${student.enneagram_result ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-500'}`}>
                            Enneagram: {student.enneagram_result?.result_name || "Pending"}
                          </div>
                        </div>
                      </td>
                      <td className="px-6 py-4 text-sm text-gray-500">
                        <div>Start: {student.start_date || "Not set"}</div>
                        <div>End: {student.end_date || "Not set"}</div>
                      </td>
                      <td className="px-6 py-4">
                        <button
                          onClick={() => router.push(`/students/${student.id}`)}
                          className="px-4 py-2 text-blue-600 hover:text-blue-800 hover:bg-blue-50 rounded-lg transition-colors text-sm font-medium"
                        >
                          View Details →
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

