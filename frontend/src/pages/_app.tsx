import type { AppProps } from 'next/app'
import { ThemeProvider, createTheme, CssBaseline } from '@mui/material'
import { useState, useMemo } from 'react'
import '@/styles/globals.css'
import { AuthProvider } from '@/context/AuthContext'

export default function App({ Component, pageProps }: AppProps) {
  const [darkMode, setDarkMode] = useState(false)

  const theme = useMemo(
    () =>
      createTheme({
        palette: {
          mode: darkMode ? 'dark' : 'light',
          primary: {
            main: '#2563eb',
          },
          secondary: {
            main: '#f97316',
          },
          background: {
            default: darkMode ? '#0f172a' : '#f7f8f9',
            paper: darkMode ? '#1e293b' : '#ffffff',
          },
        },
        shape: {
          borderRadius: 16,
        },
        typography: {
          fontFamily: '"Inter", "Roboto", sans-serif',
          h4: {
            fontWeight: 600,
          },
        },
      }),
    [darkMode]
  )

  return (
    <AuthProvider>
      <ThemeProvider theme={theme}>
        <CssBaseline />
        <Component {...pageProps} darkMode={darkMode} setDarkMode={setDarkMode} />
      </ThemeProvider>
    </AuthProvider>
  )
}
