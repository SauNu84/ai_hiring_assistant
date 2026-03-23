'use client'

import { useState, useRef } from 'react'
import { useRouter } from 'next/navigation'

type JdMode = 'url' | 'file'

const ACCEPTED_TYPES = ['application/pdf', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document']
const ACCEPTED_EXTENSIONS = ['.pdf', '.docx']

function FileDropzone({
  label,
  file,
  onFile,
  error,
}: {
  label: string
  file: File | null
  onFile: (f: File) => void
  error?: string
}) {
  const inputRef = useRef<HTMLInputElement>(null)
  const [dragOver, setDragOver] = useState(false)

  function handleDrop(e: React.DragEvent) {
    e.preventDefault()
    setDragOver(false)
    const dropped = e.dataTransfer.files[0]
    if (dropped) onFile(dropped)
  }

  function handleChange(e: React.ChangeEvent<HTMLInputElement>) {
    const selected = e.target.files?.[0]
    if (selected) onFile(selected)
  }

  return (
    <div>
      <label className="mb-1 block text-sm font-medium text-gray-700">{label}</label>
      <div
        onClick={() => inputRef.current?.click()}
        onDragOver={(e) => { e.preventDefault(); setDragOver(true) }}
        onDragLeave={() => setDragOver(false)}
        onDrop={handleDrop}
        className={`flex cursor-pointer flex-col items-center justify-center rounded-lg border-2 border-dashed px-4 py-8 transition-colors
          ${dragOver ? 'border-blue-400 bg-blue-50' : 'border-gray-300 bg-white hover:border-gray-400'}
          ${error ? 'border-red-400' : ''}`}
      >
        <svg className="mb-2 h-8 w-8 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5}
            d="M3 16.5v2.25A2.25 2.25 0 005.25 21h13.5A2.25 2.25 0 0021 18.75V16.5m-13.5-9L12 3m0 0l4.5 4.5M12 3v13.5" />
        </svg>
        {file ? (
          <span className="text-sm font-medium text-gray-700">{file.name}</span>
        ) : (
          <>
            <span className="text-sm text-gray-500">
              Drop file here or <span className="text-blue-600 underline">browse</span>
            </span>
            <span className="mt-1 text-xs text-gray-400">PDF or DOCX, max 10 MB</span>
          </>
        )}
        <input
          ref={inputRef}
          type="file"
          accept={ACCEPTED_EXTENSIONS.join(',')}
          className="hidden"
          onChange={handleChange}
        />
      </div>
      {error && <p className="mt-1 text-xs text-red-600">{error}</p>}
    </div>
  )
}

export default function EvaluatePage() {
  const router = useRouter()

  const [jdMode, setJdMode] = useState<JdMode>('url')
  const [jdUrl, setJdUrl] = useState('')
  const [jdFile, setJdFile] = useState<File | null>(null)
  const [cvFile, setCvFile] = useState<File | null>(null)
  const [loading, setLoading] = useState(false)
  const [apiError, setApiError] = useState('')
  const [fieldErrors, setFieldErrors] = useState<Record<string, string>>({})

  function validateFile(file: File | null, field: string): string {
    if (!file) return `${field} is required.`
    if (!ACCEPTED_TYPES.includes(file.type)) return 'Only PDF or DOCX files are accepted.'
    if (file.size > 10 * 1024 * 1024) return 'File must be under 10 MB.'
    return ''
  }

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault()
    setApiError('')

    const errors: Record<string, string> = {}

    if (jdMode === 'url') {
      if (!jdUrl.trim()) errors.jdUrl = 'Job description URL is required.'
      else {
        try { new URL(jdUrl) } catch { errors.jdUrl = 'Enter a valid URL.' }
      }
    } else {
      const err = validateFile(jdFile, 'Job description file')
      if (err) errors.jdFile = err
    }

    const cvErr = validateFile(cvFile, 'CV file')
    if (cvErr) errors.cvFile = cvErr

    if (Object.keys(errors).length > 0) {
      setFieldErrors(errors)
      return
    }
    setFieldErrors({})

    setLoading(true)
    try {
      const formData = new FormData()
      formData.append('cv_file', cvFile!)

      let endpoint: string
      if (jdMode === 'url') {
        endpoint = '/api/evaluate/url'
        formData.append('jd_url', jdUrl.trim())
      } else {
        endpoint = '/api/evaluate/upload'
        formData.append('jd_file', jdFile!)
      }

      const res = await fetch(endpoint, { method: 'POST', body: formData })

      if (!res.ok) {
        const data = await res.json().catch(() => ({}))
        throw new Error(data.error ?? `Server error: ${res.status}`)
      }

      const result = await res.json()
      sessionStorage.setItem('evaluation_result', JSON.stringify(result))
      router.push('/results')
    } catch (err) {
      setApiError(err instanceof Error ? err.message : 'Something went wrong. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="mx-auto max-w-2xl">
      <div className="mb-8">
        <h2 className="text-2xl font-bold">Evaluate your CV</h2>
        <p className="mt-1 text-gray-500">
          Upload your CV and a job description to get an instant fit score and gap analysis.
        </p>
      </div>

      <form onSubmit={handleSubmit} className="space-y-6" noValidate>
        {/* JD Section */}
        <div className="rounded-xl border border-gray-200 bg-white p-6 shadow-sm">
          <h3 className="mb-4 text-base font-semibold">Job Description</h3>

          {/* Mode toggle */}
          <div className="mb-4 flex rounded-lg border border-gray-200 bg-gray-50 p-1">
            <button
              type="button"
              onClick={() => { setJdMode('url'); setFieldErrors({}) }}
              className={`flex-1 rounded-md px-4 py-2 text-sm font-medium transition-colors
                ${jdMode === 'url' ? 'bg-white shadow-sm text-gray-900' : 'text-gray-500 hover:text-gray-700'}`}
            >
              Paste URL
            </button>
            <button
              type="button"
              onClick={() => { setJdMode('file'); setFieldErrors({}) }}
              className={`flex-1 rounded-md px-4 py-2 text-sm font-medium transition-colors
                ${jdMode === 'file' ? 'bg-white shadow-sm text-gray-900' : 'text-gray-500 hover:text-gray-700'}`}
            >
              Upload file
            </button>
          </div>

          {jdMode === 'url' ? (
            <div>
              <label className="mb-1 block text-sm font-medium text-gray-700">
                Job posting URL
              </label>
              <input
                type="url"
                value={jdUrl}
                onChange={(e) => setJdUrl(e.target.value)}
                placeholder="https://jobs.example.com/senior-engineer"
                className={`w-full rounded-lg border px-3 py-2 text-sm shadow-sm outline-none transition
                  focus:border-blue-500 focus:ring-2 focus:ring-blue-100
                  ${fieldErrors.jdUrl ? 'border-red-400' : 'border-gray-300'}`}
              />
              {fieldErrors.jdUrl && (
                <p className="mt-1 text-xs text-red-600">{fieldErrors.jdUrl}</p>
              )}
            </div>
          ) : (
            <FileDropzone
              label="Job description (PDF or DOCX)"
              file={jdFile}
              onFile={setJdFile}
              error={fieldErrors.jdFile}
            />
          )}
        </div>

        {/* CV Section */}
        <div className="rounded-xl border border-gray-200 bg-white p-6 shadow-sm">
          <h3 className="mb-4 text-base font-semibold">Your CV</h3>
          <FileDropzone
            label="CV / Resume (PDF or DOCX)"
            file={cvFile}
            onFile={setCvFile}
            error={fieldErrors.cvFile}
          />
        </div>

        {/* API error */}
        {apiError && (
          <div className="rounded-lg border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700">
            {apiError}
          </div>
        )}

        <button
          type="submit"
          disabled={loading}
          className="flex w-full items-center justify-center gap-2 rounded-lg bg-blue-600 px-6 py-3 text-sm font-semibold text-white shadow-sm transition hover:bg-blue-700 disabled:cursor-not-allowed disabled:opacity-60"
        >
          {loading ? (
            <>
              <svg className="h-4 w-4 animate-spin" fill="none" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                <path className="opacity-75" fill="currentColor"
                  d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
              </svg>
              Evaluating your CV&hellip;
            </>
          ) : (
            'Evaluate Now'
          )}
        </button>

        {loading && (
          <p className="text-center text-xs text-gray-400">
            This usually takes 15–30 seconds. Please don&apos;t close the tab.
          </p>
        )}
      </form>
    </div>
  )
}
