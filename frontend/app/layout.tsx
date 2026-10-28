import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "DocMind AI | Chat with Your Documents",
  description:
    "A multilingual AI document assistant that lets you upload PDF, DOCX, and PPTX files, ask questions in Arabic or English, and receive source-grounded answers using RAG.",
  applicationName: "DocMind AI",
  keywords: [
    "DocMind AI",
    "RAG",
    "document AI",
    "Arabic AI",
    "multilingual AI",
    "PDF question answering",
    "FastAPI",
    "Next.js",
    "Gemini",
  ],
  authors: [{ name: "Ziyad Alghamdi" }],
  creator: "Ziyad Alghamdi",
  metadataBase: new URL("https://docmind-ai-smoky.vercel.app"),
  openGraph: {
    title: "DocMind AI",
    description:
      "Upload documents and ask questions in Arabic or English with source-grounded answers powered by RAG.",
    url: "https://docmind-ai-smoky.vercel.app",
    siteName: "DocMind AI",
    type: "website",
  },
  twitter: {
    card: "summary_large_image",
    title: "DocMind AI",
    description:
      "A multilingual RAG-powered AI assistant for PDF, DOCX, and PPTX documents.",
  },
};

export default function RootLayout({ children }: LayoutProps<"/">) {
  return (
    <html
      lang="en"
      className={`${geistSans.variable} ${geistMono.variable} h-full antialiased`}
    >
      <body className="min-h-full flex flex-col">{children}</body>
    </html>
  );
}
