import type { Role } from "@/lib/types";

const TOKEN_KEY = "access_token";

/** Guarda el token para axios (localStorage) y para el middleware (cookie). */
export function setSession(token: string) {
  localStorage.setItem(TOKEN_KEY, token);
  document.cookie = `${TOKEN_KEY}=${token}; path=/; SameSite=Lax`;
}

/** Borra la sesion de ambos lados. */
export function clearSession() {
  localStorage.removeItem(TOKEN_KEY);
  document.cookie = `${TOKEN_KEY}=; path=/; max-age=0; SameSite=Lax`;
}

/**
 * Ruta destino segun el rol tras iniciar sesion.
 */
export function routeForRole(role: Role | null): string {
  // Por ahora todos van al dashboard, pero se puede personalizar segun el nombre del rol
  if (role?.name === "admin") {
    return "/dashboard";
  }
  return "/dashboard";
}
