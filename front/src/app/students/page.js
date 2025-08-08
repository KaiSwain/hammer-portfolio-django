"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { getStudents } from "../services/students";
import { useRouter } from "next/navigation";

export default function StudentPage() {
  const [students, setStudents] = useState([]);
  const [filteredStudents, setFilteredStudents] = useState([]);
  const [searchTerm, setSearchTerm] = useState("");
  const [sortBy, setSortBy] = useState("");
  const router = useRouter();

  useEffect(() => {
    getStudents().then((data) => {
      setStudents(data);
      setFilteredStudents(data);
    });
  }, []);

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
    <div className="min-h-screen bg-gray-50 p-6">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-bold">Student List</h1>
        <div className="flex space-x-4">
          <button
            onClick={() => router.push("/students/add")}
            className="px-4 py-2 bg-green-600 text-white rounded hover:bg-green-700"
          >
            ➕ Add Student
          </button>
          <button
            onClick={handleLogout}
            className="px-4 py-2 bg-red-600 text-white rounded hover:bg-red-700"
          >
            Logout
          </button>
        </div>
      </div>

      <div className="flex justify-between items-center mb-4">
        <input
          type="text"
          placeholder="Search by name"
          value={searchTerm}
          onChange={handleSearch}
          className="border border-gray-300 rounded px-3 py-2 w-1/3"
        />
        <select
          value={sortBy}
          onChange={handleSort}
          className="border border-gray-300 rounded px-3 py-2"
        >
          <option value="">Sort By</option>
          <option value="start_date">Start Date</option>
          <option value="recent">Recently Added</option>
        </select>
      </div>

      <div className="overflow-x-auto">
        <table className="w-full border border-gray-200 text-left bg-white shadow-sm rounded text-sm">
          <thead className="bg-gray-100 text-gray-700">
            <tr>
              <th className="p-3 border-b">Name</th>
              <th className="p-3 border-b">Gender</th>
              <th className="p-3 border-b">Start</th>
              <th className="p-3 border-b">End</th>
              <th className="p-3 border-b">50hr</th>
              <th className="p-3 border-b">OSHA</th>
              <th className="p-3 border-b">OSHA Type</th>
              <th className="p-3 border-b">Hammer Math</th>
              <th className="p-3 border-b">Employability</th>
              <th className="p-3 border-b">Ruler?</th>
              <th className="p-3 border-b">Pre</th>
              <th className="p-3 border-b">Post</th>
              <th className="p-3 border-b">Disc</th>
              <th className="p-3 border-b">16 Type</th>
              <th className="p-3 border-b">Enneagram</th>
              <th className="p-3 border-b">Created</th>
            </tr>
          </thead>
          <tbody>
            {filteredStudents.map((student) => (
              <tr
                key={student.id}
                onClick={() => router.push(`/students/${student.id}`)}
                className="cursor-pointer hover:bg-gray-50"
              >
                <td className="p-2 border-b">{student.full_name}</td>
                <td className="p-2 border-b">{student.gender_identity?.gender ?? "-"}</td>
                <td className="p-2 border-b">{student.start_date ?? "-"}</td>
                <td className="p-2 border-b">{student.end_date ?? "-"}</td>
                <td className="p-2 border-b">{student.complete_50_hour_training ? "✅" : "❌"}</td>
                <td className="p-2 border-b">{student.passed_osha_10_exam ? "✅" : "❌"}</td>
                <td className="p-2 border-b">{student.osha_type?.name ?? "-"}</td>
                <td className="p-2 border-b">{student.hammer_math ? "✅" : "❌"}</td>
                <td className="p-2 border-b">{student.employability_skills ? "✅" : "❌"}</td>
                <td className="p-2 border-b">{student.passed_ruler_assessment ? "✅" : "❌"}</td>
                <td className="p-2 border-b">{student.pretest_score ?? "-"}</td>
                <td className="p-2 border-b">{student.posttest_score ?? "-"}</td>
                <td className="p-2 border-b">{student.disc_assessment_type?.type_name ?? "-"}</td>
                <td className="p-2 border-b">{student.sixteen_types_assessment?.type_name ?? "-"}</td>
                <td className="p-2 border-b">{student.enneagram_result?.result_name ?? "-"}</td>
                <td className="p-2 border-b">{new Date(student.created_at).toLocaleDateString()}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

