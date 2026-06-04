"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";
import { useCurrentUser } from "@/lib/useCurrentUser";

export function ProtectedRoute({
  children,
  requiredPermission,
}: {
  children: React.ReactNode;
  requiredPermission?: string;
}) {
  const { user, loading } = useCurrentUser();
  const router = useRouter();

  useEffect(() => {
    if (!loading) {
      if (!user) {
        router.push("/login");
      } else if (requiredPermission && (!user.role || !user.role.permissions.includes(requiredPermission))) {
        router.push("/dashboard");
      }
    }
  }, [user, loading, router, requiredPermission]);

  if (loading) {
    return <div className="p-8 text-center text-gray-500">Cargando...</div>;
  }

  if (!user || (requiredPermission && (!user.role || !user.role.permissions.includes(requiredPermission)))) {
    return null;
  }

  return <>{children}</>;
}
