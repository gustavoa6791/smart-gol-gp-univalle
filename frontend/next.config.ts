import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // Reenvia /api/* al backend (Docker) para evitar CORS y centralizar la URL.
  async rewrites() {
    return [
      {
        source: "/api/:path*",
        destination: `${process.env.BACKEND_URL || "http://localhost:8000"}/api/:path*`,
      },
    ];
  },
};

export default nextConfig;
