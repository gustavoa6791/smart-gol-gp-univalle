import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";

// En Next.js 16 el middleware se define en proxy.ts y se exporta como `proxy`.

// Rutas accesibles sin sesion.
const PUBLIC_ROUTES = ["/", "/login", "/register"];

export function proxy(request: NextRequest) {
  const token = request.cookies.get("access_token")?.value;
  const { pathname } = request.nextUrl;
  const isPublic = PUBLIC_ROUTES.includes(pathname);

  // Sin sesion en ruta protegida -> al login
  if (!token && !isPublic) {
    return NextResponse.redirect(new URL("/login", request.url));
  }

  // Con sesion intentando ir a login/registro -> al dashboard
  if (token && (pathname === "/login" || pathname === "/register")) {
    return NextResponse.redirect(new URL("/dashboard", request.url));
  }

  return NextResponse.next();
}

export const config = {
  // Excluye internos de Next, la API y archivos con extension (assets).
  matcher: ["/((?!_next|favicon.ico|api|.*\\..*).*)"],
};
