import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Smart Gol",
  description: "Sistema de gestion de torneos deportivos",
};

export default function RootLayout({
  children,
}: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="es">
      <body>{children}</body>
    </html>
  );
}
