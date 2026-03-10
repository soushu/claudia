import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "claudia",
  description: "Personal AI chat powered by Claude",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="ja">
      <body>{children}</body>
    </html>
  );
}
