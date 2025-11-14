import type { AppProps } from 'next/app'
import { ThemeProvider, createTheme, CssBaseline } from '@mui/material'
import { useState, useMemo } from 'react'
import '@/styles/globals.css'

export default function App({ Component, pageProps }: AppProps) {
  const [darkMode, setDarkMode] = useState(false)

  const theme = useMemo(
    () =>
      createTheme({
        palette: {
          mode: darkMode ? 'dark' : 'light',
          primary: {
            main: '#1976d2',
          },
          secondary: {
            main: '#dc004e',
          },
        },
      }),
    [darkMode]
  )

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Component {...pageProps} darkMode={darkMode} setDarkMode={setDarkMode} />
    </ThemeProvider>
  )
}
