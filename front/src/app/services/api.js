// API Configuration
const API_BASE_URL = 'https://hammer-app-hk3st.ondigitalocean.app';
const API_URL = `${API_BASE_URL}/api`;

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
};

// Legacy functions for backward compatibility
export const getdetails = () => apiService.getDetails();

export default apiService;
