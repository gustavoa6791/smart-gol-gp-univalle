import type { UserRole } from "@/lib/types";

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
 * Punto de extension: cuando cada rol tenga su panel propio (HU futuras),
 * mapear aqui (ej. admin -> "/admin").
 */
export function routeForRole(role: UserRole): string {
  const routes: Record<UserRole, string> = {
    admin: "/dashboard",
    organizer: "/dashboard",
    viewer: "/dashboard",
  };
  return routes[role] ?? "/dashboard";
}
