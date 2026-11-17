import { apiClient } from "../../lib/api";

export const login = (username: string, password: string) => {
  const data = new URLSearchParams();
  data.append("username", username);
  data.append("password", password);

  return apiClient
    .post("/auth/login", data)
    .then((res) => res.data);
};
export const getMe = () => 
    apiClient
    .get("/auth/me")
    .then((res) => res.data);


