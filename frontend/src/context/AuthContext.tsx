import { createContext, useContext, useState, useEffect, useCallback } from 'react'
import api, { AuthUser } from '@/services/api'

interface AuthContextState {
  user: AuthUser | null
  initializing: boolean
  login: (email: string, password: string) => Promise<void>
  register: (name: string, email: string, password: string) => Promise<void>
  logout: () => void
}

const AuthContext = createContext<AuthContextState | undefined>(undefined)
const STORAGE_KEY = 'afsa_user'

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<AuthUser | null>(null)
  const [initializing, setInitializing] = useState(true)

  useEffect(() => {
    if (typeof window === 'undefined') {
      return
    }
    const stored = window.localStorage.getItem(STORAGE_KEY)
    if (stored) {
      try {
        const parsed: AuthUser = JSON.parse(stored)
        setUser(parsed)
      } catch (error) {
        console.warn('Failed to parse stored auth user', error)
        window.localStorage.removeItem(STORAGE_KEY)
      }
    }
    setInitializing(false)
  }, [])

  const persistUser = useCallback((nextUser: AuthUser) => {
    setUser(nextUser)
    if (typeof window !== 'undefined') {
      window.localStorage.setItem(STORAGE_KEY, JSON.stringify(nextUser))
    }
  }, [])

  const login = useCallback(async (email: string, password: string) => {
    const response = await api.login({ email, password })
    persistUser(response.user)
  }, [persistUser])

  const register = useCallback(async (name: string, email: string, password: string) => {
    const response = await api.register({ name, email, password })
    persistUser(response.user)
  }, [persistUser])

  const logout = useCallback(() => {
    setUser(null)
    if (typeof window !== 'undefined') {
      window.localStorage.removeItem(STORAGE_KEY)
    }
  }, [])

  return (
    <AuthContext.Provider value={{ user, initializing, login, register, logout }}>
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  const context = useContext(AuthContext)
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider')
  }
  return context
}
