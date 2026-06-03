"use client";

import { useEffect, useState } from "react";
import api from "@/lib/api";
import type { User } from "@/lib/types";

/** Carga el usuario autenticado desde /api/auth/me. */
export function useCurrentUser() {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let active = true;
    api
      .get<User>("/api/auth/me")
      .then((res) => active && setUser(res.data))
      .catch(() => active && setUser(null))
      .finally(() => active && setLoading(false));
    return () => {
      active = false;
    };
  }, []);

  return { user, loading };
}
