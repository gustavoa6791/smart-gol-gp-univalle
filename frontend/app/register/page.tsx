"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import { useState } from "react";
import { AuthShell, Field, buttonClass, inputClass } from "@/components/auth-ui";
import api from "@/lib/api";
import { routeForRole, setSession } from "@/lib/auth";
import type { Token, User } from "@/lib/types";

export default function RegisterPage() {
  const router = useRouter();
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError("");
    setLoading(true);
    try {
      // Registro publico (siempre rol viewer) y autologin
      await api.post("/api/auth/register", { name, email, password });
      const { data } = await api.post<Token>("/api/auth/login", { email, password });
      setSession(data.access_token);
      const me = await api.get<User>("/api/auth/me");
      router.replace(routeForRole(me.data.role));
    } catch (err) {
      const detail = (err as { response?: { data?: { detail?: string } } })?.response?.data?.detail;
      setError(detail || "No se pudo completar el registro");
      setLoading(false);
    }
  }

  return (
    <AuthShell title="Crear cuenta" subtitle="Te registrarás con rol de espectador (viewer)">
      <form onSubmit={handleSubmit} className="space-y-4">
        <Field label="Nombre">
          <input
            type="text"
            required
            value={name}
            onChange={(e) => setName(e.target.value)}
            placeholder="Tu nombre"
            className={inputClass}
          />
        </Field>
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
            placeholder="Mínimo 6 caracteres"
            className={inputClass}
          />
        </Field>
        {error && <p className="rounded-md bg-red-50 px-3 py-2 text-sm text-red-700">{error}</p>}
        <button type="submit" disabled={loading} className={buttonClass}>
          {loading ? "Creando cuenta…" : "Registrarme"}
        </button>
      </form>
      <p className="mt-4 text-center text-sm text-gray-500">
        ¿Ya tienes cuenta?{" "}
        <Link href="/login" className="font-medium text-green-700 hover:underline">
          Inicia sesión
        </Link>
      </p>
    </AuthShell>
  );
}
