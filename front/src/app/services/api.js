// API Configuration - Uses environment variables for different environments
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'https://hammer-production-173f.up.railway.app';
const API_URL = `${API_BASE_URL}/api`;

console.log('🔧 API Configuration:', { API_BASE_URL, NODE_ENV: process.env.NODE_ENV });

// Get token from localStorage
const getToken = () => {
  if (typeof window !== 'undefined') {
    const tokenString = localStorage.getItem("token");
    if (tokenString) {
      try {
        const tokenObj = JSON.parse(tokenString);
        return tokenObj.token;
      } catch (error) {
        console.error('Error parsing token:', error);
        return null;
      }
    }
  }
  return null;
};

// Common headers
const getHeaders = () => {
  const token = getToken();
  const headers = {
    'Content-Type': 'application/json',
  };
  
  if (token) {
    headers.Authorization = `Token ${token}`;
  }
  
  return headers;
};

// API service functions
export const apiService = {
  // Health check
  async healthCheck() {
    const response = await fetch(`${API_URL}/health/`, {
      method: 'GET',
      headers: getHeaders(),
    });
    return response.json();
  },

  // Authentication
  async login(credentials) {
    const response = await fetch(`${API_URL}/login/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(credentials),
    });
    return response.json();
  },

  // Students
  async getStudents() {
    try {
      console.log('Fetching students from:', `${API_URL}/students/`);
      const response = await fetch(`${API_URL}/students/`, {
        method: 'GET',
        headers: getHeaders(),
        credentials: 'include',
      });
      
      console.log('Students response status:', response.status);
      console.log('Students response headers:', response.headers);
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const data = await response.json();
      console.log('Students data received:', data);
      return data;
    } catch (error) {
      console.error('Error fetching students:', error);
      throw error;
    }
  },

  async createStudent(studentData) {
    try {
      console.log('Creating student with data:', studentData);
      const response = await fetch(`${API_URL}/students/`, {
        method: 'POST',
        headers: getHeaders(),
        credentials: 'include',
        body: JSON.stringify(studentData),
      });
      
      if (!response.ok) {
        const errorText = await response.text();
        console.error('Create student error:', errorText);
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      return response.json();
    } catch (error) {
      console.error('Error creating student:', error);
      throw error;
    }
  },

  async getStudent(id) {
    try {
      const response = await fetch(`${API_URL}/students/${id}/`, {
        method: 'GET',
        headers: getHeaders(),
        credentials: 'include',
      });
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      return response.json();
    } catch (error) {
      console.error('Error fetching student:', error);
      throw error;
    }
  },

  async updateStudent(id, studentData) {
    try {
      const response = await fetch(`${API_URL}/students/${id}/`, {
        method: 'PUT',
        headers: getHeaders(),
        credentials: 'include',
        body: JSON.stringify(studentData),
      });
      
      if (!response.ok) {
        const errorText = await response.text();
        console.error('Update student error:', errorText);
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      return response.json();
    } catch (error) {
      console.error('Error updating student:', error);
      throw error;
    }
  },

  async deleteStudent(id) {
    const response = await fetch(`${API_URL}/students/${id}/`, {
      method: 'DELETE',
      headers: getHeaders(),
    });
    return response.ok;
  },

  // Details/Options
  async getDetails() {
    const response = await fetch(`${API_URL}/details/`, {
      headers: getHeaders(),
    });
    return response.json();
  },

  // Certificate Generation
  async generateAllCertificates(studentData) {
    const response = await fetch(`${API_URL}/generate/all/`, {
      method: 'POST',
      headers: getHeaders(),
      body: JSON.stringify({ student: studentData }),
    });
    return response;
  },

  async generatePortfolioCertificate(studentData) {
    const response = await fetch(`${API_URL}/generate/portfolio/`, {
      method: 'POST',
      headers: getHeaders(),
      body: JSON.stringify({ student: studentData }),
    });
    return response;
  },

  async generateNCCERCertificate(studentData) {
    const response = await fetch(`${API_URL}/generate/nccer/`, {
      method: 'POST',
      headers: getHeaders(),
      body: JSON.stringify({ student: studentData }),
    });
    return response;
  },

  async generateOSHACertificate(studentData) {
    const response = await fetch(`${API_URL}/generate/osha/`, {
      method: 'POST',
      headers: getHeaders(),
      body: JSON.stringify({ student: studentData }),
    });
    return response;
  },

  async generateHammerMathCertificate(studentData) {
    const response = await fetch(`${API_URL}/generate/hammermath/`, {
      method: 'POST',
      headers: getHeaders(),
      body: JSON.stringify({ student: studentData }),
    });
    return response;
  },

  async generateEmployabilityCertificate(studentData) {
    const response = await fetch(`${API_URL}/generate/employability/`, {
      method: 'POST',
      headers: getHeaders(),
      body: JSON.stringify({ student: studentData }),
    });
    return response;
  },

  async generateWorkforceCertificate(studentData) {
    const response = await fetch(`${API_URL}/generate/workforce/`, {
      method: 'POST',
      headers: getHeaders(),
      body: JSON.stringify({ student: studentData }),
    });
    return response;
  },

  // AI Summary
  async generateAiSummary(studentId) {
    const response = await fetch(`${API_URL}/api/ai/summary/`, {
      method: 'POST',
      headers: getHeaders(),
      body: JSON.stringify({ student_id: studentId }),
    });
    return response;
  },

  // Student Files API
  async getStudentFiles(studentId) {
    try {
      const response = await fetch(`${API_URL}/students/${studentId}/files/`, {
        method: 'GET',
        headers: getHeaders(),
      });
      
      if (!response.ok) {
        if (response.status === 401) {
          throw new Error('Authentication required');
        }
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const data = await response.json();
      console.log('Student files API response:', data);
      
      // The API now returns an array directly
      if (Array.isArray(data)) {
        return data;
      } else if (data && Array.isArray(data.files)) {
        // Handle old format if still returned
        return data.files;
      } else if (data && Array.isArray(data.results)) {
        // Handle paginated response
        return data.results;
      } else {
        console.warn('API returned unexpected data structure:', data);
        return [];
      }
    } catch (error) {
      console.error('Error fetching student files:', error);
      throw error;
    }
  },

  async uploadStudentFile(studentId, file, originalFilename) {
    try {
      const formData = new FormData();
      formData.append('file', file);
      formData.append('original_filename', originalFilename);
      
      const token = getToken();
      const headers = {};
      if (token) {
        headers.Authorization = `Token ${token}`;
      }
      
      const response = await fetch(`${API_URL}/students/${studentId}/files/upload/`, {
        method: 'POST',
        headers: headers, // Don't set Content-Type for FormData
        body: formData,
      });
      
      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || `HTTP error! status: ${response.status}`);
      }
      
      return response.json();
    } catch (error) {
      console.error('Error uploading student file:', error);
      throw error;
    }
  },

  async deleteStudentFile(fileId) {
    try {
      const response = await fetch(`${API_URL}/student-files/${fileId}/`, {
        method: 'DELETE',
        headers: getHeaders(),
      });
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      return true;
    } catch (error) {
      console.error('Error deleting student file:', error);
      throw error;
    }
  },

  async downloadStudentFile(fileId) {
    try {
      const token = getToken();
      const headers = {};
      if (token) {
        headers.Authorization = `Token ${token}`;
      }
      
      // First, get the download information
      const response = await fetch(`${API_URL}/student-files/${fileId}/download/`, {
        method: 'GET',
        headers: headers,
      });
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const downloadInfo = await response.json();
      console.log('Download info:', downloadInfo);
      
      // Now fetch the actual file using the download_url
      const fileUrl = `${API_BASE_URL}${downloadInfo.download_url}`;
      const fileResponse = await fetch(fileUrl);
      
      if (!fileResponse.ok) {
        throw new Error(`File fetch error! status: ${fileResponse.status}`);
      }
      
      return {
        response: fileResponse,
        filename: downloadInfo.filename,
        contentType: downloadInfo.content_type
      };
    } catch (error) {
      console.error('Error downloading student file:', error);
      throw error;
    }
  },

  async testAiConnection() {
    const response = await fetch(`${API_URL}/ai/test/`, {
      method: 'GET',
      headers: getHeaders(),
    });
    return response;
  },
};

// Legacy functions for backward compatibility
export const getdetails = () => apiService.getDetails();

export default apiService;
