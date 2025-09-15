// app/services/pdf.js

const API_URL = "https://hammer-production-173f.up.railway.app";

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
    
    // Use the new AI summary endpoint
    const res = await fetch(`${API_URL}/api/ai/summary/`, {
      method: "POST",
      headers: { 
        Authorization: `Token ${token}`,
        'Content-Type': 'application/json',
      },
      credentials: 'include',
      body: JSON.stringify({ student_id: id }),
    });

    console.log('AI summary response status:', res.status);
    console.log('AI summary response headers:', [...res.headers.entries()]);

    if (!res.ok) {
      // Try to get error as JSON first, fallback to text
      let errorMessage;
      try {
        const errorData = await res.json();
        errorMessage = errorData.error || `HTTP ${res.status}: Failed to generate AI summary`;
      } catch {
        errorMessage = `HTTP ${res.status}: Failed to generate AI summary`;
      }
      
      console.error('AI summary error:', errorMessage);
      if (res.status === 401) throw new Error("Unauthorized (check Token).");
      throw new Error(errorMessage);
    }

    // Check if response is PDF (our new backend returns PDF directly)
    const contentType = res.headers.get('Content-Type') || res.headers.get('content-type');
    console.log('Response Content-Type:', contentType);
    console.log('All response headers:', Object.fromEntries(res.headers.entries()));
    
    // Handle PDF response (prioritize PDF detection)
    if (contentType && (contentType.includes('application/pdf') || contentType.includes('pdf'))) {
      console.log('Detected PDF response, handling as blob...');
      // Handle PDF response
      try {
        const pdfBlob = await res.blob();
        console.log('PDF blob size:', pdfBlob.size);
        const url = URL.createObjectURL(pdfBlob);
        const a = document.createElement("a");
        a.href = url;
        a.download = `${studentName.replace(/\s+/g, "_")}_AI_Personality_Summary.pdf`;
        document.body.appendChild(a);
        a.click();
        a.remove();
        URL.revokeObjectURL(url);
        console.log('PDF download triggered successfully');
        return; // Exit early for PDF handling
      } catch (blobError) {
        console.error('Error handling PDF blob:', blobError);
        throw new Error(`PDF download failed: ${blobError.message}`);
      }
    } else {
      // Fallback: handle as JSON response (for backward compatibility)
      console.log('Response is not PDF, attempting to parse as JSON...');
      try {
        const responseData = await res.json();
        console.log('JSON response data:', responseData);
        
        if (!responseData.success) {
          throw new Error(responseData.error || "AI summary generation failed");
        }

        // Create a simple HTML page for the summary and convert to downloadable format
        const htmlContent = `
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>AI Personality Summary - ${studentName}</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; line-height: 1.6; }
        h1 { color: #2563eb; border-bottom: 2px solid #2563eb; padding-bottom: 10px; }
        h2 { color: #1f2937; margin-top: 30px; }
        p { margin: 15px 0; }
        ul { margin: 10px 0; }
        li { margin: 5px 0; }
        .header { text-align: center; margin-bottom: 40px; }
        .content { max-width: 800px; margin: 0 auto; }
    </style>
</head>
<body>
    <div class="content">
        <div class="header">
            <h1>Personality Summary</h1>
            <h2>${studentName}</h2>
            <p><em>Generated on ${new Date().toLocaleDateString()}</em></p>
        </div>
        ${responseData.html_content || responseData.html || 'No content available'}
    </div>
</body>
</html>`;

        // Create a blob and download
        const blob = new Blob([htmlContent], { type: 'text/html' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.href = url;
        a.download = `${studentName.replace(/\s+/g, "_")}_AI_Summary.html`;
        document.body.appendChild(a);
        a.click();
        a.remove();
        URL.revokeObjectURL(url);
        console.log('HTML download triggered successfully');
      } catch (jsonError) {
        console.error('Error parsing JSON response:', jsonError);
        // If JSON parsing also fails, it might be a PDF with wrong content type
        console.log('JSON parsing failed, trying to handle as blob anyway...');
        try {
          const pdfBlob = await res.blob();
          console.log('Fallback blob size:', pdfBlob.size);
          const url = URL.createObjectURL(pdfBlob);
          const a = document.createElement("a");
          a.href = url;
          a.download = `${studentName.replace(/\s+/g, "_")}_AI_Summary.pdf`;
          document.body.appendChild(a);
          a.click();
          a.remove();
          URL.revokeObjectURL(url);
          console.log('Fallback PDF download triggered');
        } catch (blobError) {
          console.error('Both JSON and blob parsing failed:', blobError);
          throw new Error(`Response parsing failed. Response may be corrupted.`);
        }
      }
    }

    alert(`AI Summary generated successfully for ${studentName}!`);
    
  } catch (err) {
    console.error(err);
    alert(err.message || "Error generating AI summary");
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
