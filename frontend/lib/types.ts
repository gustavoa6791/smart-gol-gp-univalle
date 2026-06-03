// Tipos compartidos del dominio. Cada HU agrega los suyos aqui.

export type UserRole = "admin" | "organizer" | "viewer";

export interface User {
  id: number;
  name: string;
  email: string;
  role: UserRole;
  created_at?: string;
}
