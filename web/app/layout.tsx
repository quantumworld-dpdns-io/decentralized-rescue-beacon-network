import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Rescue Beacon Network",
  description: "Decentralized rescue beacon network dashboard",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        <nav>
          <span className="title">Rescue Beacon Network</span>
          <a href="/">Dashboard</a>
          <a href="/nodes">Nodes</a>
          <a href="/packets">Packets</a>
          <a href="/audit">Audit Log</a>
        </nav>
        <main>{children}</main>
      </body>
    </html>
  );
}
