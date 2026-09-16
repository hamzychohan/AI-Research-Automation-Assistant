"use client";

import { AuthProvider } from "@/hooks/use-auth";
import "@/styles/global.css";

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <head>
        <title>AI Research & Automation Assistant</title>
        <meta name="description" content="AI Assistant chat interface only." />
      </head>
      <body style={{ margin: 0, padding: 0 }}>
        <AuthProvider> 
          {children}
        </AuthProvider>
      </body>
    </html>
  );
}
