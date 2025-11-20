export const normalizeToNumber = (value: any): number | null => {
  if (value === null || value === undefined) {
    return null
  }

  if (typeof value === 'number') {
    return Number.isFinite(value) ? value : null
  }

  if (typeof value === 'string') {
    let cleaned = value.trim()
    if (!cleaned) {
      return null
    }

    let negative = false
    if (cleaned.startsWith('(') && cleaned.endsWith(')')) {
      negative = true
      cleaned = cleaned.slice(1, -1)
    }

    cleaned = cleaned.replace(/[,$\s]/g, '')
    cleaned = cleaned.replace(/USD|usd/gi, '')

    const normalized = cleaned.replace(/[^0-9.\-]/g, '')
    if (!normalized || normalized === '-' || normalized === '.') {
      return null
    }

    const parsed = Number(normalized)
    if (!Number.isFinite(parsed)) {
      return null
    }

    return negative ? -parsed : parsed
  }

  return null
}
