// Tipos compartidos del dominio. Cada HU agrega los suyos aqui.

export interface Role {
  id: number;
  name: string;
  permissions: string[];
}

export interface User {
  id: number;
  name: string;
  email: string;
  role: Role | null;
  created_at?: string;
}

export interface Token {
  access_token: string;
  token_type: string;
}
