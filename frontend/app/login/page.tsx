"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import { useState } from "react";
import { AuthShell, Field, buttonClass, inputClass } from "@/components/auth-ui";
import api from "@/lib/api";
import { routeForRole, setSession } from "@/lib/auth";
import type { Token, User } from "@/lib/types";

export default function LoginPage() {
  const router = useRouter();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError("");
    setLoading(true);
    try {
      const { data } = await api.post<Token>("/api/auth/login", { email, password });
      setSession(data.access_token);
      // Redireccion segun rol
      const me = await api.get<User>("/api/auth/me");
      router.replace(routeForRole(me.data.role));
    } catch (err) {
      const detail = (err as { response?: { data?: { detail?: string } } })?.response?.data?.detail;
      setError(detail || "Correo o contraseña incorrectos");
      setLoading(false);
    }
  }

  return (
    <AuthShell title="Iniciar sesión" subtitle="Ingresa tus credenciales para continuar">
      <form onSubmit={handleSubmit} className="space-y-4">
        <Field label="Correo electrónico">
          <input
            type="email"
            required
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            placeholder="tu@email.com"
            className={inputClass}
          />
        </Field>
        <Field label="Contraseña">
          <input
            type="password"
            required
            minLength={6}
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            placeholder="••••••••"
            className={inputClass}
          />
        </Field>
        {error && <p className="rounded-md bg-red-50 px-3 py-2 text-sm text-red-700">{error}</p>}
        <button type="submit" disabled={loading} className={buttonClass}>
          {loading ? "Iniciando sesión…" : "Ingresar"}
        </button>
      </form>
      <p className="mt-4 text-center text-sm text-gray-500">
        ¿No tienes cuenta?{" "}
        <Link href="/register" className="font-medium text-green-700 hover:underline">
          Regístrate
        </Link>
      </p>
    </AuthShell>
  );
}
