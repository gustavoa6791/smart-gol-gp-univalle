import axios from "axios";

// Cliente HTTP centralizado. El token se agrega cuando HU-001 implemente login.
const api = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000",
  headers: { "Content-Type": "application/json" },
});

// Adjunta el token (si existe) en cada request
api.interceptors.request.use((config) => {
  if (typeof window !== "undefined") {
    const token = localStorage.getItem("access_token");
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
  }
  return config;
});

// Redirige a /login ante un 401 (salvo durante el propio login)
api.interceptors.response.use(
  (res) => res,
  (error) => {
    const url: string = error.config?.url || "";
    const isAuthCall = url.includes("/api/auth/login") || url.includes("/api/auth/register");
    if (error.response?.status === 401 && typeof window !== "undefined" && !isAuthCall) {
      localStorage.removeItem("access_token");
      document.cookie = "access_token=; path=/; max-age=0; SameSite=Lax";
      window.location.href = "/login";
    }
    return Promise.reject(error);
  }
);

export default api;
