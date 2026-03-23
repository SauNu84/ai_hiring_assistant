'use client'

import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'

export default function ResultsPage() {
  const router = useRouter()
  const [loaded, setLoaded] = useState(false)

  useEffect(() => {
    const raw = sessionStorage.getItem('evaluation_result')
    if (!raw) {
      router.replace('/evaluate')
    } else {
      setLoaded(true)
    }
  }, [router])

  if (!loaded) return null

  return (
    <div className="py-16 text-center text-gray-500">
      <p className="text-lg font-medium">Results coming soon.</p>
      <p className="mt-2 text-sm">Evaluation data received — results UI is being built.</p>
      <button
        onClick={() => router.push('/evaluate')}
        className="mt-6 rounded-lg bg-blue-600 px-5 py-2 text-sm font-medium text-white hover:bg-blue-700"
      >
        Back to evaluate
      </button>
    </div>
  )
}
