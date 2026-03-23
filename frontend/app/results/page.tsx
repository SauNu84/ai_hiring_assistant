'use client'

import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'

// ── Types ────────────────────────────────────────────────────────────────────

interface DimensionScores {
  technical_skills: number
  experience_level: number
  domain_fit: number
  keyword_alignment: number
}

interface HardGap {
  requirement: string
  advice: string
  resources: string[]
}

interface SoftGap {
  requirement: string
  advice: string
}

interface HiddenStrength {
  skill: string
  jd_mapping: string
  reframe_suggestion: string
}

interface CvImprovements {
  summary_rewrite: string
  skills_section_rewrite: string
  highlight_suggestions: string[]
}

interface Evaluation {
  overall_score: number
  dimension_scores: DimensionScores
  verdict: string
  hard_gaps: HardGap[]
  soft_gaps: SoftGap[]
  hidden_strengths: HiddenStrength[]
  cv_improvements: CvImprovements
}

interface EvaluationResult {
  evaluation_id: string
  jd: Record<string, unknown>
  cv: Record<string, unknown>
  evaluation: Evaluation
}

// ── Helpers ──────────────────────────────────────────────────────────────────

function scoreColor(score: number): string {
  if (score >= 70) return 'text-green-600'
  if (score >= 50) return 'text-amber-500'
  return 'text-red-500'
}

function scoreBg(score: number): string {
  if (score >= 70) return 'bg-green-500'
  if (score >= 50) return 'bg-amber-400'
  return 'bg-red-400'
}

function scoreBadge(score: number): string {
  if (score >= 70) return 'bg-green-100 text-green-700'
  if (score >= 50) return 'bg-amber-100 text-amber-700'
  return 'bg-red-100 text-red-700'
}

function verdictLabel(verdict: string): string {
  const map: Record<string, string> = {
    strong_match: 'Strong Match',
    good_match: 'Good Match',
    partial_match: 'Partial Match',
    weak_match: 'Weak Match',
    poor_match: 'Poor Match',
  }
  return map[verdict] ?? verdict
}

const DIMENSION_META: { key: keyof DimensionScores; label: string; max: number }[] = [
  { key: 'technical_skills', label: 'Technical Skills', max: 35 },
  { key: 'experience_level', label: 'Experience Level', max: 25 },
  { key: 'domain_fit', label: 'Domain Fit', max: 20 },
  { key: 'keyword_alignment', label: 'Keyword Alignment', max: 20 },
]

// ── Sub-components ────────────────────────────────────────────────────────────

function Section({ title, children }: { title: string; children: React.ReactNode }) {
  return (
    <section className="rounded-xl border border-gray-200 bg-white p-6 shadow-sm">
      <h2 className="mb-4 text-lg font-semibold">{title}</h2>
      {children}
    </section>
  )
}

function ProgressBar({ value, max }: { value: number; max: number }) {
  const pct = Math.min(100, Math.round((value / max) * 100))
  return (
    <div className="h-2 w-full overflow-hidden rounded-full bg-gray-100">
      <div
        className={`h-full rounded-full transition-all ${scoreBg(Math.round((value / max) * 100))}`}
        style={{ width: `${pct}%` }}
      />
    </div>
  )
}

function AccordionItem({ title, children }: { title: string; children: React.ReactNode }) {
  const [open, setOpen] = useState(false)
  return (
    <div className="border-b border-gray-100 last:border-0">
      <button
        type="button"
        onClick={() => setOpen((v) => !v)}
        className="flex w-full items-center justify-between py-3 text-left text-sm font-medium text-gray-800 hover:text-blue-600"
      >
        {title}
        <svg
          className={`h-4 w-4 flex-shrink-0 text-gray-400 transition-transform ${open ? 'rotate-180' : ''}`}
          fill="none" viewBox="0 0 24 24" stroke="currentColor"
        >
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
        </svg>
      </button>
      {open && <div className="pb-4 text-sm text-gray-600">{children}</div>}
    </div>
  )
}

// ── Main Page ─────────────────────────────────────────────────────────────────

export default function ResultsPage() {
  const router = useRouter()
  const [result, setResult] = useState<EvaluationResult | null>(null)

  useEffect(() => {
    const raw = sessionStorage.getItem('evaluation_result')
    if (!raw) { router.replace('/evaluate'); return }
    try {
      setResult(JSON.parse(raw))
    } catch {
      router.replace('/evaluate')
    }
  }, [router])

  if (!result) return null

  const ev = result.evaluation
  const score = ev.overall_score ?? 0

  function downloadCvSection() {
    const text = [
      'AI HIRING ASSISTANT — CV IMPROVEMENT SUGGESTIONS',
      '='.repeat(50),
      '',
      'DISCLAIMER: This rewrites presentation, not facts.',
      'Your experience remains unchanged.',
      '',
      '── SUMMARY REWRITE ──',
      ev.cv_improvements.summary_rewrite,
      '',
      '── SKILLS SECTION REWRITE ──',
      ev.cv_improvements.skills_section_rewrite,
      '',
      '── HIGHLIGHT SUGGESTIONS ──',
      ...(ev.cv_improvements.highlight_suggestions ?? []).map((s, i) => `${i + 1}. ${s}`),
    ].join('\n')

    const blob = new Blob([text], { type: 'text/plain' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = 'cv-improvements.txt'
    a.click()
    URL.revokeObjectURL(url)
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold">Evaluation Results</h2>
          <p className="mt-1 text-sm text-gray-500">ID: {result.evaluation_id}</p>
        </div>
        <button
          onClick={() => router.push('/evaluate')}
          className="rounded-lg border border-gray-200 bg-white px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-50"
        >
          New evaluation
        </button>
      </div>

      {/* Overall score */}
      <Section title="Overall Fit Score">
        <div className="flex items-center gap-6">
          <div className={`text-7xl font-extrabold tabular-nums ${scoreColor(score)}`}>
            {score}
          </div>
          <div className="flex-1">
            <div className={`mb-2 inline-block rounded-full px-3 py-1 text-sm font-semibold ${scoreBadge(score)}`}>
              {verdictLabel(ev.verdict)}
            </div>
            <div className="h-3 w-full overflow-hidden rounded-full bg-gray-100">
              <div
                className={`h-full rounded-full ${scoreBg(score)}`}
                style={{ width: `${score}%` }}
              />
            </div>
            <p className="mt-2 text-xs text-gray-400">Score out of 100</p>
          </div>
        </div>
      </Section>

      {/* Dimension breakdown */}
      <Section title="Dimension Breakdown">
        <div className="space-y-4">
          {DIMENSION_META.map(({ key, label, max }) => {
            const val = ev.dimension_scores?.[key] ?? 0
            return (
              <div key={key}>
                <div className="mb-1 flex justify-between text-sm">
                  <span className="font-medium text-gray-700">{label}</span>
                  <span className={`font-semibold ${scoreColor(Math.round((val / max) * 100))}`}>
                    {val} / {max}
                  </span>
                </div>
                <ProgressBar value={val} max={max} />
              </div>
            )
          })}
        </div>
      </Section>

      {/* Gap analysis */}
      {((ev.hard_gaps?.length ?? 0) > 0 || (ev.soft_gaps?.length ?? 0) > 0) && (
        <Section title="Gap Analysis">
          {(ev.hard_gaps?.length ?? 0) > 0 && (
            <div className="mb-6">
              <h3 className="mb-3 text-sm font-semibold uppercase tracking-wide text-red-500">
                Hard Gaps
              </h3>
              <div className="overflow-hidden rounded-lg border border-gray-200">
                <table className="w-full text-sm">
                  <thead className="bg-gray-50 text-xs font-medium uppercase text-gray-500">
                    <tr>
                      <th className="px-4 py-2 text-left">JD Requires</th>
                      <th className="px-4 py-2 text-left">Advice &amp; Resources</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-gray-100">
                    {ev.hard_gaps.map((gap, i) => (
                      <tr key={i} className="align-top">
                        <td className="px-4 py-3 font-medium text-gray-800">{gap.requirement}</td>
                        <td className="px-4 py-3 text-gray-600">
                          <p>{gap.advice}</p>
                          {gap.resources?.length > 0 && (
                            <ul className="mt-2 space-y-1">
                              {gap.resources.map((r, j) => (
                                <li key={j}>
                                  <a
                                    href={r.startsWith('http') ? r : undefined}
                                    target="_blank"
                                    rel="noopener noreferrer"
                                    className={`text-xs ${r.startsWith('http') ? 'text-blue-600 underline hover:text-blue-800' : 'text-gray-500'}`}
                                  >
                                    {r}
                                  </a>
                                </li>
                              ))}
                            </ul>
                          )}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          )}

          {(ev.soft_gaps?.length ?? 0) > 0 && (
            <div>
              <h3 className="mb-3 text-sm font-semibold uppercase tracking-wide text-amber-500">
                Soft Gaps
              </h3>
              <div className="space-y-0 divide-y divide-gray-100 rounded-lg border border-gray-200">
                {ev.soft_gaps.map((gap, i) => (
                  <AccordionItem key={i} title={gap.requirement}>
                    <p>{gap.advice}</p>
                  </AccordionItem>
                ))}
              </div>
            </div>
          )}
        </Section>
      )}

      {/* Hidden strengths */}
      {(ev.hidden_strengths?.length ?? 0) > 0 && (
        <Section title="Hidden Strengths">
          <p className="mb-4 text-sm text-gray-500">
            Skills you already have that map to the JD — reframe them to stand out.
          </p>
          <div className="space-y-3">
            {ev.hidden_strengths.map((hs, i) => (
              <div key={i} className="rounded-lg bg-green-50 p-4">
                <div className="flex items-center gap-2">
                  <span className="rounded-full bg-green-100 px-2 py-0.5 text-xs font-medium text-green-700">
                    {hs.skill}
                  </span>
                  <span className="text-xs text-gray-400">maps to</span>
                  <span className="text-xs font-medium text-gray-600">{hs.jd_mapping}</span>
                </div>
                <p className="mt-2 text-sm text-gray-600">{hs.reframe_suggestion}</p>
              </div>
            ))}
          </div>
        </Section>
      )}

      {/* CV rewrite section */}
      {ev.cv_improvements && (
        <Section title="CV Improvement Suggestions">
          <p className="mb-4 rounded-lg bg-amber-50 px-4 py-3 text-sm text-amber-700">
            <strong>Disclaimer:</strong> This rewrites presentation, not facts.
            Your experience remains unchanged.
          </p>

          <div className="mb-6 grid gap-6 md:grid-cols-2">
            {/* Summary */}
            <div>
              <h3 className="mb-2 text-sm font-semibold text-gray-700">Summary — Original</h3>
              <div className="min-h-[80px] rounded-lg bg-gray-50 p-3 text-sm text-gray-600">
                {(result.cv as Record<string, unknown>)?.summary as string ?? (
                  <span className="text-gray-400 italic">Not extracted</span>
                )}
              </div>
            </div>
            <div>
              <h3 className="mb-2 text-sm font-semibold text-green-700">Summary — Suggested Rewrite</h3>
              <div className="min-h-[80px] rounded-lg bg-green-50 p-3 text-sm text-gray-700">
                {ev.cv_improvements.summary_rewrite}
              </div>
            </div>

            {/* Skills */}
            <div>
              <h3 className="mb-2 text-sm font-semibold text-gray-700">Skills — Original</h3>
              <div className="min-h-[80px] rounded-lg bg-gray-50 p-3 text-sm text-gray-600">
                {Array.isArray((result.cv as Record<string, unknown>)?.skills)
                  ? ((result.cv as Record<string, string[]>).skills).join(', ')
                  : <span className="text-gray-400 italic">Not extracted</span>
                }
              </div>
            </div>
            <div>
              <h3 className="mb-2 text-sm font-semibold text-green-700">Skills — Suggested Rewrite</h3>
              <div className="min-h-[80px] rounded-lg bg-green-50 p-3 text-sm text-gray-700">
                {ev.cv_improvements.skills_section_rewrite}
              </div>
            </div>
          </div>

          {/* Highlight suggestions */}
          {(ev.cv_improvements.highlight_suggestions?.length ?? 0) > 0 && (
            <div className="mb-6">
              <h3 className="mb-3 text-sm font-semibold text-gray-700">
                Top Skills to Add / Improve
              </h3>
              <ol className="space-y-2">
                {ev.cv_improvements.highlight_suggestions.map((s, i) => (
                  <li key={i} className="flex gap-2 text-sm">
                    <span className="flex h-5 w-5 flex-shrink-0 items-center justify-center rounded-full bg-blue-100 text-xs font-bold text-blue-700">
                      {i + 1}
                    </span>
                    <span className="text-gray-700">{s}</span>
                  </li>
                ))}
              </ol>
            </div>
          )}

          <button
            onClick={downloadCvSection}
            className="flex items-center gap-2 rounded-lg border border-gray-200 bg-white px-4 py-2 text-sm font-medium text-gray-700 shadow-sm hover:bg-gray-50"
          >
            <svg className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2}
                d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
            </svg>
            Download suggestions (plain text)
          </button>
        </Section>
      )}
    </div>
  )
}
