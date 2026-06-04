"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import api from "@/lib/api";
import { ProtectedRoute } from "@/components/ProtectedRoute";
import type { Role } from "@/lib/types";
import { buttonClass, inputClass } from "@/components/auth-ui";

const AVAILABLE_PERMISSIONS = [
  { id: "manage_roles", label: "Gestionar Roles" },
  { id: "manage_users", label: "Gestionar Usuarios" },
  { id: "view_admin_panel", label: "Ver Panel Admin" },
  { id: "manage_tournaments", label: "Gestionar Torneos" },
  { id: "view_tournaments", label: "Ver Torneos" },
];

export default function RolesPage() {
  const router = useRouter();
  const [roles, setRoles] = useState<Role[]>([]);
  const [loading, setLoading] = useState(true);
  const [editingRole, setEditingRole] = useState<Partial<Role> | null>(null);

  useEffect(() => {
    fetchRoles();
  }, []);

  async function fetchRoles() {
    try {
      const { data } = await api.get<Role[]>("/api/roles");
      setRoles(data);
    } catch (err) {
      console.error("Error fetching roles", err);
    } finally {
      setLoading(false);
    }
  }

  async function handleSave() {
    if (!editingRole?.name) return;
    try {
      if (editingRole.id) {
        await api.put(`/api/roles/${editingRole.id}`, editingRole);
      } else {
        await api.post("/api/roles", editingRole);
      }
      setEditingRole(null);
      fetchRoles();
    } catch (err) {
      alert("Error al guardar el rol");
    }
  }

  return (
    <ProtectedRoute requiredPermission="manage_roles">
      <div className="min-h-screen bg-gray-50">
        <header className="flex items-center justify-between border-b bg-white px-6 py-4">
          <div className="flex items-center gap-4">
            <button onClick={() => router.push("/dashboard")} className="text-gray-500 hover:text-green-700">
              ← Volver
            </button>
            <h1 className="text-lg font-bold">Gestión de Roles</h1>
          </div>
          <button
            onClick={() => router.push("/admin/users")}
            className="text-sm font-medium text-green-700 hover:underline"
          >
            Gestionar Usuarios
          </button>
        </header>

        <main className="mx-auto max-w-4xl px-6 py-8">
          <div className="grid gap-6 md:grid-cols-2">
            {/* Lista de Roles */}
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <h2 className="font-semibold text-gray-700">Roles configurados</h2>
                <button
                  onClick={() => setEditingRole({ name: "", permissions: [] })}
                  className="text-xs font-bold uppercase tracking-wider text-green-700 hover:text-green-800"
                >
                  + Nuevo Rol
                </button>
              </div>
              <div className="rounded-xl border bg-white shadow-sm overflow-hidden">
                {loading ? (
                  <p className="p-4 text-center text-gray-400">Cargando...</p>
                ) : (
                  <ul className="divide-y">
                    {roles.map((role) => (
                      <li
                        key={role.id}
                        className={`p-4 hover:bg-gray-50 cursor-pointer ${
                          editingRole?.id === role.id ? "bg-green-50" : ""
                        }`}
                        onClick={() => setEditingRole(role)}
                      >
                        <p className="font-medium">{role.name}</p>
                        <p className="text-xs text-gray-500">{role.permissions.length} permisos asignados</p>
                      </li>
                    ))}
                  </ul>
                )}
              </div>
            </div>

            {/* Editor de Rol */}
            <div className="space-y-4">
              <h2 className="font-semibold text-gray-700">
                {editingRole ? (editingRole.id ? "Editar Rol" : "Crear Rol") : "Selecciona un rol"}
              </h2>
              {editingRole ? (
                <div className="rounded-xl border bg-white p-6 shadow-sm space-y-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">Nombre del Rol</label>
                    <input
                      className={inputClass}
                      value={editingRole.name}
                      onChange={(e) => setEditingRole({ ...editingRole, name: e.target.value })}
                      placeholder="Ej: Organizador"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">Permisos</label>
                    <div className="grid grid-cols-1 gap-2">
                      {AVAILABLE_PERMISSIONS.map((perm) => (
                        <label key={perm.id} className="flex items-center gap-2 p-2 rounded hover:bg-gray-50 cursor-pointer">
                          <input
                            type="checkbox"
                            className="rounded border-gray-300 text-green-600 focus:ring-green-600"
                            checked={editingRole.permissions?.includes(perm.id)}
                            onChange={(e) => {
                              const perms = editingRole.permissions || [];
                              if (e.target.checked) {
                                setEditingRole({ ...editingRole, permissions: [...perms, perm.id] });
                              } else {
                                setEditingRole({ ...editingRole, permissions: perms.filter((p) => p !== perm.id) });
                              }
                            }}
                          />
                          <span className="text-sm text-gray-600">{perm.label}</span>
                        </label>
                      ))}
                    </div>
                  </div>
                  <div className="flex gap-3 pt-2">
                    <button onClick={handleSave} className={buttonClass}>
                      Guardar cambios
                    </button>
                    <button
                      onClick={() => setEditingRole(null)}
                      className="w-full rounded-md border border-gray-300 px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-50"
                    >
                      Cancelar
                    </button>
                  </div>
                </div>
              ) : (
                <div className="flex flex-col items-center justify-center h-48 border-2 border-dashed rounded-xl text-gray-400">
                  <p>Selecciona un rol de la lista para editar sus permisos o crea uno nuevo.</p>
                </div>
              )}
            </div>
          </div>
        </main>
      </div>
    </ProtectedRoute>
  );
}
