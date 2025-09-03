// app/services/pdf.js

const API_URL = "https://hammer-app-hk3st.ondigitalocean.app";

/** Generate selected cert PDFs (unchanged) */
export async function generateCertificates(student, selectedCerts) {
  for (const cert in selectedCerts) {
    if (selectedCerts[cert]) {
      await downloadCertificate(student, cert.toLowerCase());
    }
  }
}

/** Generate AI summary (pass the whole student) */
export async function generateAiSummary(student) {
  return downloadAiSummaryById(student.id, student.full_name);
}

async function downloadCertificate(student, cert) {
  const tokenString = localStorage.getItem("token");
  const token = JSON.parse(tokenString || "null")?.token;
  if (!token) {
    alert("Not authenticated. Please sign in again.");
    return;
  }

  try {
    const response = await fetch(`${API_URL}/api/generate/${cert}/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Token ${token}`,
      },
      credentials: 'include',
      body: JSON.stringify({ student }),
    });

    if (!response.ok) {
      const msg = await response.text().catch(() => "");
      throw new Error(`HTTP ${response.status}: ${msg || `Failed ${cert}`}`);
    }

    const blob = await response.blob();
    const url = window.URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.download = `${(student.full_name || "Student").replace(/\s+/g, "_")}_${cert}.pdf`;
    document.body.appendChild(link);
    link.click();
    link.remove();
    window.URL.revokeObjectURL(url);
  } catch (error) {
    console.error(error);
    alert(error.message || `Error generating ${cert}`);
  }
}

async function downloadAiSummaryById(id, studentName = "Student") {
  try {
    const tokenString = localStorage.getItem("token");
    if (!tokenString) throw new Error("No auth token in localStorage.");
    const token = JSON.parse(tokenString)?.token;
    if (!token) throw new Error("Malformed auth token.");

    console.log('Generating AI summary for student ID:', id);
    const res = await fetch(`${API_URL}/api/students/${id}/personality-summary/`, {
      method: "POST",
      headers: { 
        Authorization: `Token ${token}`,
        'Content-Type': 'application/json',
      },
      credentials: 'include',
    });

    console.log('AI summary response status:', res.status);

    if (!res.ok) {
      const msg = await res.text().catch(() => "");
      console.error('AI summary error:', msg);
      if (res.status === 401) throw new Error("Unauthorized (check Token).");
      throw new Error(`HTTP ${res.status}: ${msg || "Failed to generate PDF"}`);
    }

    const disp = res.headers.get("Content-Disposition") || "";
    const match = /filename="?([^"]+)"?/.exec(disp);
    const suggestedName = match?.[1] || `${studentName.replace(/\s+/g, "_")}_ai_summary.pdf`;

    const blob = await res.blob();
    if (!blob.size) throw new Error("Empty PDF (0 bytes).");

    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = suggestedName;
    document.body.appendChild(a);
    a.click();
    a.remove();
    URL.revokeObjectURL(url);
  } catch (err) {
    console.error(err);
    alert(err.message || "Error generating PDF");
  }
}

export async function generateMasterPortfolio(student) {
  const tokenString = localStorage.getItem("token");
  const token = JSON.parse(tokenString || "null")?.token;
  if (!token) {
    alert("Not authenticated. Please sign in again.");
    return;
  }

  try {
    const res = await fetch(`${API_URL}/api/generate/all/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Token ${token}`,
      },
      credentials: 'include',
      body: JSON.stringify({ student }),
    });

    if (!res.ok) {
      const msg = await res.text().catch(() => "");
      throw new Error(`HTTP ${res.status}: ${msg || "Failed to generate master PDF"}`);
    }

    const blob = await res.blob();
    if (!blob.size) throw new Error("Empty PDF (0 bytes).");

    const safeName =
      (student.full_name || "Student").replace(/\s+/g, "_") + "_Certificates_Master.pdf";

    const url = window.URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = safeName;
    document.body.appendChild(a);
    a.click();
    a.remove();
    window.URL.revokeObjectURL(url);
  } catch (err) {
    console.error(err);
    alert(err.message || "Error generating master PDF");
  }
}
