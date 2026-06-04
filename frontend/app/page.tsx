"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import api from "@/lib/api";

type Health = { status: string; database: string };

export default function Home() {
  const [health, setHealth] = useState<Health | null>(null);
  const [error, setError] = useState(false);

  useEffect(() => {
    api
      .get<Health>("/api/health")
      .then((res) => setHealth(res.data))
      .catch(() => setError(true));
  }, []);

  return (
    <main className="flex min-h-screen flex-col items-center justify-center gap-4 p-8">
      <h1 className="text-3xl font-bold text-green-700">Smart Gol</h1>
      <p className="text-gray-500">Sistema de gestión de torneos deportivos.</p>

      <Link
        href="/login"
        className="rounded-md bg-green-600 px-5 py-2 text-sm font-medium text-white transition hover:bg-green-700"
      >
        Iniciar sesión
      </Link>

      <div className="rounded-lg border px-6 py-4 text-sm">
        <p className="font-medium">Estado del backend:</p>
        {error && <p className="text-red-600">No se pudo conectar al backend.</p>}
        {!error && !health && <p className="text-gray-400">Consultando…</p>}
        {health && (
          <ul className="mt-1 text-gray-700">
            <li>API: {health.status}</li>
            <li>Base de datos: {health.database}</li>
          </ul>
        )}
      </div>
    </main>
  );
}
