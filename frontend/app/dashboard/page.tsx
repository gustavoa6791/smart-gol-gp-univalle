"use client";

import { useRouter } from "next/navigation";
import { clearSession } from "@/lib/auth";
import { useCurrentUser } from "@/lib/useCurrentUser";

const ROLE_LABEL: Record<string, string> = {
  admin: "Administrador",
  organizer: "Organizador",
  viewer: "Espectador",
};

export default function DashboardPage() {
  const router = useRouter();
  const { user, loading } = useCurrentUser();

  function logout() {
    clearSession();
    router.replace("/login");
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <header className="flex items-center justify-between border-b bg-white px-6 py-4">
        <span className="text-lg font-bold text-green-700">⚽ Smart Gol</span>
        <button
          onClick={logout}
          className="rounded-md border border-gray-300 px-3 py-1.5 text-sm font-medium text-gray-700 transition hover:bg-gray-100"
        >
          Cerrar sesión
        </button>
      </header>

      <main className="mx-auto max-w-2xl px-6 py-12">
        {loading && <p className="text-gray-400">Cargando…</p>}
        {!loading && user && (
          <div className="rounded-xl border bg-white p-8 shadow-sm">
            <h1 className="text-2xl font-bold">Hola, {user.name}</h1>
            <p className="mt-1 text-gray-500">{user.email}</p>
            <div className="mt-4 inline-flex items-center gap-2 rounded-full bg-green-100 px-3 py-1 text-sm font-medium text-green-800">
              Rol: {ROLE_LABEL[user.role] ?? user.role}
            </div>
            <p className="mt-6 text-sm text-gray-500">
              Sesión iniciada correctamente. Las funciones por rol se agregan en las próximas HU.
            </p>
          </div>
        )}
      </main>
    </div>
  );
}
