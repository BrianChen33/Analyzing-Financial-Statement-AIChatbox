import { normalizeToNumber } from './number'

const candidateKeys = ['metric_value', 'value', 'current_value', 'metricValue']

const extractCandidateValue = (risk: any): any => {
  if (!risk || typeof risk !== 'object') {
    return null
  }

  for (const key of candidateKeys) {
    if (risk[key] !== undefined && risk[key] !== null) {
      return risk[key]
    }
  }

  if (typeof risk.description === 'string') {
    const match = risk.description.match(/\(([^)]+)\)/)
    if (match) {
      return match[1]
    }
    if (/n\/a/i.test(risk.description)) {
      return 'N/A'
    }
  }

  return null
}

export const isDisplayableRisk = (risk: any): boolean => {
  if (!risk) {
    return false
  }

  const candidate = extractCandidateValue(risk)
  if (typeof candidate === 'string' && candidate.trim().toUpperCase() === 'N/A') {
    return false
  }

  const numericValue = normalizeToNumber(candidate)
  if (numericValue === null) {
    return true
  }

  return numericValue !== 0
}

export const filterDisplayableRisks = (risks: any[]): any[] => {
  if (!Array.isArray(risks)) {
    return []
  }
  return risks.filter(isDisplayableRisk)
}
