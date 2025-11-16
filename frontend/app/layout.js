import './globals.css'
import { Inter } from 'next/font/google'
const inter = Inter({ subsets: ['latin'] })

export const metadata = { title: 'UTO — Universal Task Orchestrator', description: 'Multi-agent document analysis and orchestration', }

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <div className="min-h-screen bg-slate-50 text-slate-900">{children}</div>
      </body>
    </html>
  )
}
