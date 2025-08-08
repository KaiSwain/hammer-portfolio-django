const tokenString = localStorage.getItem("token");
const tokenObj = JSON.parse(tokenString);
const token = tokenObj.token;
const API_URL = "http://localhost:8000";

export const getdetails = () => {
  return fetch(`${API_URL}/details/`, {
    headers: { Authorization: `Token ${token}` },
  }).then((res) => res.json());
};



