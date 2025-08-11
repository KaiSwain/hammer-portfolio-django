
export const getStudents = () => {
  const tokenString = localStorage.getItem("token");
  const tokenObj = JSON.parse(tokenString);
  const token = tokenObj.token;
  const API_URL = "http://localhost:8000";
  return fetch(`${API_URL}/students`, {
    headers: { Authorization: `Token ${token}` },
  }).then((res) => res.json());
};

export const retrieveStudent = (id) => {
  const tokenString = localStorage.getItem("token");
  const tokenObj = JSON.parse(tokenString);
  const token = tokenObj.token;
  const API_URL = "http://localhost:8000";
  return fetch(`${API_URL}/students/${id}`, {
    headers: { Authorization: `Token ${token}` },
  }).then((res) => res.json());
};

export const createStudent = (studentObj) => {
  const tokenString = localStorage.getItem("token");
  const tokenObj = JSON.parse(tokenString);
  const token = tokenObj.token;
  const API_URL = "http://localhost:8000";
  return fetch(`${API_URL}/students`, {
    headers: {
      Authorization: `Token ${token}`,
      "Content-Type": "application/json",
    },
    method: "POST",
    body: JSON.stringify(studentObj),
  });
};

export const editStudent = (studentObj, id) => {
  const tokenString = localStorage.getItem("token");
  const tokenObj = JSON.parse(tokenString);
  const token = tokenObj.token;
  const API_URL = "http://localhost:8000";
  return fetch(`${API_URL}/students/${id}`, {
    headers: {
      Authorization: `Token ${token}`,
      "Content-Type": "application/json",
    },
    method: "PUT",
    body: JSON.stringify(studentObj),
  });
};


