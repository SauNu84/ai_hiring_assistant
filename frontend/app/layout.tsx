import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: 'AI Hiring Assistant',
  description: 'Evaluate your CV against any job description and get actionable gap analysis.',
}

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body className="min-h-screen bg-gray-50 text-gray-900 antialiased">
        <header className="border-b border-gray-200 bg-white">
          <div className="mx-auto max-w-4xl px-4 py-4">
            <h1 className="text-xl font-semibold tracking-tight">AI Hiring Assistant</h1>
          </div>
        </header>
        <main className="mx-auto max-w-4xl px-4 py-8">{children}</main>
      </body>
    </html>
  )
}
