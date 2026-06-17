import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "TraitTrace — Ephemeral Zero-Party MarTech Engine",
  description: "Privacy-first, cookie-less gamified storefront personalization built for Epsilon's TeXpedition Hackathon.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className="antialiased select-none">
        {children}
      </body>
    </html>
  );
}
