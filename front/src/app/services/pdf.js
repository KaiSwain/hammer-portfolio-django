const API_URL = "http://localhost:8000";



/**
 * pdfService.js
 * ---------------------
 * Handles API requests for generating certificates
 * and triggers file downloads in the browser.
*/

/**
 * Generates selected certificates by calling individual backend endpoints
 * @param {Object} student - Student data
 * @param {Object} selectedCerts - Object with cert names as keys and boolean values
*/
export async function generateCertificates(student, selectedCerts) {
  // Loop through selected certificates
  for (const cert in selectedCerts) {
    if (selectedCerts[cert]) {
      // If certificate is selected, download it
      await downloadCertificate(student, cert.toLowerCase());
    }
  }
}

/**
 * Sends a POST request to backend for one certificate
 * and downloads the PDF file.
 * @param {Object} student - Student data
 * @param {string} cert - Certificate type (e.g., "osha")
*/
async function downloadCertificate(student, cert) {
  const tokenString = localStorage.getItem("token");
  const tokenObj = JSON.parse(tokenString);
  const token = tokenObj.token;
  try {
    // API endpoint follows pattern: /generate-<cert>/
    const response = await fetch(`${API_URL}/generate/${cert}/`, {
      method: "POST",
      headers: { "Content-Type": "application/json",
        "Authorization": `Token ${token}`
       },
      body: JSON.stringify({ student }),
    });

    // Handle failure
    if (!response.ok) {
      throw new Error(`Failed to generate ${cert} certificate`);
    }

    // Convert response to Blob (binary data)
    const blob = await response.blob();

    // Create a temporary URL for download
    const url = window.URL.createObjectURL(blob);

    // Create an <a> tag programmatically for download
    const link = document.createElement("a");
    link.href = url;
    link.download = `${student.full_name}_${cert}.pdf`; // File name
    link.click();

    // Clean up memory
    window.URL.revokeObjectURL(url);
  } catch (error) {
    console.error(`Error generating ${cert}:`, error);
    alert(`Error generating ${cert}`);
  }
}
