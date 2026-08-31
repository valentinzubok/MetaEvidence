import type { Metadata } from "next";
import { WalletProvider } from "@/components/WalletProvider";
import { MetaEvidenceApp } from "@/components/MetaEvidenceApp";
import "./globals.css";

export const metadata: Metadata = {
  title: "MetaEvidence Console",
  description: "Schema passport app on GenLayer Studionet — attach, audit, appeal evidence.",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        <WalletProvider>{children}</WalletProvider>
      </body>
    </html>
  );
}
