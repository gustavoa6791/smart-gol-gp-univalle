"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import api from "@/lib/api";
import { ProtectedRoute } from "@/components/ProtectedRoute";
import type { User, Role } from "@/lib/types";
import { inputClass } from "@/components/auth-ui";

export default function UsersPage() {
  const router = useRouter();
  const [users, setUsers] = useState<User[]>([]);
  const [roles, setRoles] = useState<Role[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchData();
  }, []);

  async function fetchData() {
    try {
      const [usersRes, rolesRes] = await Promise.all([
        api.get<User[]>("/api/users"),
        api.get<Role[]>("/api/roles"),
      ]);
      setUsers(usersRes.data);
      setRoles(rolesRes.data);
    } catch (err) {
      console.error("Error fetching data", err);
    } finally {
      setLoading(false);
    }
  }

  async function handleRoleChange(userId: number, roleId: string) {
    try {
      await api.put(`/api/users/${userId}/role`, { role_id: parseInt(roleId) });
      fetchData(); // Recargar para ver los cambios
    } catch (err) {
      alert("Error al cambiar el rol del usuario");
    }
  }

  return (
    <ProtectedRoute requiredPermission="manage_users">
      <div className="min-h-screen bg-gray-50">
        <header className="flex items-center justify-between border-b bg-white px-6 py-4">
          <div className="flex items-center gap-4">
            <button onClick={() => router.push("/dashboard")} className="text-gray-500 hover:text-green-700">
              ← Volver
            </button>
            <h1 className="text-lg font-bold">Gestión de Usuarios</h1>
          </div>
          <button
            onClick={() => router.push("/admin/roles")}
            className="text-sm font-medium text-green-700 hover:underline"
          >
            Configurar Roles
          </button>
        </header>

        <main className="mx-auto max-w-4xl px-6 py-8">
          <div className="rounded-xl border bg-white shadow-sm overflow-hidden">
            {loading ? (
              <p className="p-8 text-center text-gray-400">Cargando usuarios...</p>
            ) : (
              <table className="w-full text-left border-collapse">
                <thead>
                  <tr className="bg-gray-50 border-b">
                    <th className="px-6 py-4 text-xs font-bold uppercase tracking-wider text-gray-500">Nombre</th>
                    <th className="px-6 py-4 text-xs font-bold uppercase tracking-wider text-gray-500">Correo</th>
                    <th className="px-6 py-4 text-xs font-bold uppercase tracking-wider text-gray-500">Rol Actual</th>
                    <th className="px-6 py-4 text-xs font-bold uppercase tracking-wider text-gray-500 text-right">Acciones</th>
                  </tr>
                </thead>
                <tbody className="divide-y">
                  {users.map((u) => (
                    <tr key={u.id} className="hover:bg-gray-50 transition-colors">
                      <td className="px-6 py-4 font-medium text-gray-800">{u.name}</td>
                      <td className="px-6 py-4 text-gray-600">{u.email}</td>
                      <td className="px-6 py-4">
                        <span className="inline-flex items-center rounded-full bg-green-50 px-2 py-1 text-xs font-medium text-green-700 ring-1 ring-inset ring-green-600/20">
                          {u.role?.name || "Sin rol"}
                        </span>
                      </td>
                      <td className="px-6 py-4 text-right">
                        <select
                          className="rounded-md border border-gray-300 px-2 py-1 text-xs outline-none focus:border-green-600 focus:ring-1 focus:ring-green-600"
                          value={u.role?.id || ""}
                          onChange={(e) => handleRoleChange(u.id, e.target.value)}
                        >
                          <option value="" disabled>Seleccionar rol</option>
                          {roles.map((r) => (
                            <option key={r.id} value={r.id}>
                              {r.name}
                            </option>
                          ))}
                        </select>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            )}
          </div>
        </main>
      </div>
    </ProtectedRoute>
  );
}
