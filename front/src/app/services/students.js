
const API_BASE_URL = 'http://localhost:8000';

// Helper function to get token
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

// Helper function to get headers
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

export const getStudents = async () => {
  try {
    console.log('Fetching students from:', `${API_BASE_URL}/api/students/`);
    const response = await fetch(`${API_BASE_URL}/api/students/`, {
      method: 'GET',
      headers: getHeaders(),
      credentials: 'include',
    });
    
    console.log('Students response status:', response.status);
    
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
};

export const retrieveStudent = async (id) => {
  try {
    const response = await fetch(`${API_BASE_URL}/api/students/${id}/`, {
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
};

export const createStudent = async (studentObj) => {
  try {
    console.log('Creating student with data:', studentObj);
    const response = await fetch(`${API_BASE_URL}/api/students/`, {
      method: 'POST',
      headers: getHeaders(),
      credentials: 'include',
      body: JSON.stringify(studentObj),
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
};

export const editStudent = async (studentObj, id) => {
  try {
    console.log('Editing student with data:', studentObj, 'ID:', id);
    const response = await fetch(`${API_BASE_URL}/api/students/${id}/`, {
      method: 'PUT',
      headers: getHeaders(),
      credentials: 'include',
      body: JSON.stringify(studentObj),
    });
    
    if (!response.ok) {
      const errorText = await response.text();
      console.error('Edit student error:', errorText);
      throw new Error(`HTTP error! status: ${response.status} - ${errorText}`);
    }
    
    return response.json();
  } catch (error) {
    console.error('Error editing student:', error);
    throw error;
  }
};

export const deleteStudent = async (id) => {
  try {
    const response = await fetch(`${API_BASE_URL}/api/students/${id}/`, {
      method: 'DELETE',
      headers: getHeaders(),
      credentials: 'include',
    });
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    // DELETE requests typically return 204 No Content with empty body
    // Only try to parse JSON if there's actually content
    if (response.status === 204 || response.headers.get('content-length') === '0') {
      return { success: true, message: 'Student deleted successfully' };
    }
    
    // Check if response has content before parsing JSON
    const text = await response.text();
    if (!text) {
      return { success: true, message: 'Student deleted successfully' };
    }
    
    return JSON.parse(text);
  } catch (error) {
    console.error('Error deleting student:', error);
    throw error;
  }
};


