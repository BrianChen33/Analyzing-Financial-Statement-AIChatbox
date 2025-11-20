import { useState, MouseEvent } from 'react'
import {
  Box,
  Grid,
  Paper,
  Typography,
  IconButton,
  Button,
  Stack,
  Chip,
  CircularProgress,
  BottomNavigation,
  BottomNavigationAction,
  useMediaQuery,
  useTheme,
  Avatar,
  Alert,
  Tabs,
  Tab,
  TextField,
  Menu,
  MenuItem
} from '@mui/material'
import {
  Brightness4,
  Brightness7,
  Download,
  HomeRounded,
  CloudUploadRounded,
  AnalyticsRounded,
  QuestionAnswerRounded,
  LogoutRounded,
  CheckCircleOutline
} from '@mui/icons-material'
import FileUpload from '@/components/FileUpload'
import FinancialDashboard from '@/components/FinancialDashboard'
import ChatInterface from '@/components/ChatInterface'
import api from '@/services/api'
import { useAuth } from '@/context/AuthContext'
import { normalizeToNumber } from '@/utils/number'
import { filterDisplayableRisks } from '@/utils/risk'

interface HomeProps {
  darkMode: boolean
  setDarkMode: (mode: boolean) => void
}

const NAV_ITEMS = [
  { key: 'overview', label: 'Home', icon: <HomeRounded fontSize="small" /> },
  { key: 'upload', label: 'Upload', icon: <CloudUploadRounded fontSize="small" /> },
  { key: 'dashboard', label: 'Dashboard', icon: <AnalyticsRounded fontSize="small" /> },
  { key: 'qa', label: 'Q&A', icon: <QuestionAnswerRounded fontSize="small" /> }
]

export default function Home({ darkMode, setDarkMode }: HomeProps) {
  const theme = useTheme()
  const isDesktop = useMediaQuery(theme.breakpoints.up('lg'))
  const { user, initializing, logout } = useAuth()
  const [activeNav, setActiveNav] = useState<string>('overview')
  const [analysisData, setAnalysisData] = useState<any>(null)
  const [avatarMenuAnchor, setAvatarMenuAnchor] = useState<null | HTMLElement>(null)

  const handleAnalysisComplete = (data: any) => {
    setAnalysisData(data)
    setActiveNav('dashboard')
  }

  const handleExportReport = async (format: string = 'markdown') => {
    if (!analysisData) {
      alert('No analysis data available to export')
      return
    }
    try {
      const result = await api.exportReport(analysisData, format)
      const blob = new Blob([result.content], {
        type: format === 'markdown' ? 'text/markdown' : 'text/plain'
      })
      const url = window.URL.createObjectURL(blob)
      const link = document.createElement('a')
      link.href = url
      link.download = result.filename
      document.body.appendChild(link)
      link.click()
      document.body.removeChild(link)
      window.URL.revokeObjectURL(url)
    } catch (error: any) {
      alert(`Export failed: ${error.message}`)
    }
  }
  
  const handleAvatarMenuClose = () => setAvatarMenuAnchor(null)
  const handleAvatarClick = (event: MouseEvent<HTMLButtonElement>) => {
    setAvatarMenuAnchor(event.currentTarget)
  }
  const handleLogout = () => {
    handleAvatarMenuClose()
    logout()
  }

  if (initializing) {
    return (
      <Box sx={{ minHeight: '100vh', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
        <CircularProgress />
      </Box>
    )
  }

  if (!user) {
    return <AuthPanel />
  }

  const renderContent = () => {
    switch (activeNav) {
      case 'overview':
        return <OverviewSection analysisData={analysisData} onGoUpload={() => setActiveNav('upload')} />
      case 'upload':
        return <FileUpload onAnalysisComplete={handleAnalysisComplete} />
      case 'dashboard':
        return analysisData ? <FinancialDashboard data={analysisData} /> : (
          <EmptyState
            title="Upload a statement to unlock the dashboard"
            description="Your KPIs, ratios, and peer benchmarks will appear here after the first analysis."
            actionLabel="Upload now"
            onAction={() => setActiveNav('upload')}
          />
        )
      case 'qa':
        return <ChatInterface analysisData={analysisData} user={user} />
      default:
        return null
    }
  }

  return (
    <Box sx={{ display: 'flex', minHeight: '100vh', bgcolor: 'background.default' }}>
      {isDesktop && (
        <Paper
          component="nav"
          elevation={0}
          sx={{
            width: 260,
            borderRadius: 0,
            borderRight: `1px solid ${theme.palette.divider}`,
            p: 3,
            display: 'flex',
            flexDirection: 'column'
          }}
        >
          <Box>
            <Typography variant="h5" fontWeight={700} gutterBottom>
              AI Finance
            </Typography>
            <Typography variant="body2" color="text.secondary">
              Intelligent financial analysis workspace - by Group 17
            </Typography>
          </Box>
          <Stack spacing={1.5} sx={{ mt: 4 }}>
            {NAV_ITEMS.map((item) => (
              <Button
                key={item.key}
                onClick={() => setActiveNav(item.key)}
                startIcon={item.icon}
                variant={activeNav === item.key ? 'contained' : 'text'}
                color={activeNav === item.key ? 'primary' : 'inherit'}
                sx={{
                  justifyContent: 'flex-start',
                  textTransform: 'none',
                  borderRadius: 2,
                  fontWeight: activeNav === item.key ? 600 : 500
                }}
              >
                {item.label}
              </Button>
            ))}
          </Stack>
          <Box sx={{ mt: 'auto' }}>
            <Button
              variant="outlined"
              fullWidth
              startIcon={<LogoutRounded />}
              onClick={logout}
              sx={{ borderRadius: 2 }}
            >
              Sign out
            </Button>
          </Box>
        </Paper>
      )}

      <Box sx={{ flexGrow: 1, display: 'flex', flexDirection: 'column' }}>
        <Paper
          elevation={0}
          sx={{
            borderRadius: 0,
            borderBottom: `1px solid ${theme.palette.divider}`,
            p: { xs: 2, md: 3 },
            display: 'flex',
            alignItems: { xs: 'flex-start', sm: 'center' },
            flexDirection: { xs: 'column', sm: 'row' },
            justifyContent: 'space-between',
            gap: 2,
            position: 'sticky',
            top: 0,
            zIndex: theme.zIndex.appBar,
            bgcolor: 'background.paper'
          }}
        >
          <Box>
            <Typography variant="subtitle2" color="text.secondary">
              Financial Statement AI Analyzer
            </Typography>
            <Typography variant="h5" fontWeight={700}>
              Welcome back, {user.name.split(' ')[0]}
            </Typography>
          </Box>
          <Stack direction="row" spacing={1} alignItems="center">
            {analysisData && (
              <Button
                variant="contained"
                startIcon={<Download />}
                onClick={() => handleExportReport('markdown')}
                sx={{ borderRadius: 2 }}
              >
                Export report
              </Button>
            )}
            <IconButton onClick={() => setDarkMode(!darkMode)}>
              {darkMode ? <Brightness7 /> : <Brightness4 />}
            </IconButton>
            <IconButton onClick={handleAvatarClick} sx={{ p: 0 }}>
              <Avatar sx={{ bgcolor: 'primary.main' }}>
                {user.name ? user.name.charAt(0).toUpperCase() : 'U'}
              </Avatar>
            </IconButton>
            <Menu
              anchorEl={avatarMenuAnchor}
              open={Boolean(avatarMenuAnchor)}
              onClose={handleAvatarMenuClose}
              anchorOrigin={{ vertical: 'bottom', horizontal: 'right' }}
              transformOrigin={{ vertical: 'top', horizontal: 'right' }}
            >
              <MenuItem onClick={handleLogout}>
                <LogoutRounded fontSize="small" sx={{ mr: 1 }} />
                Sign out
              </MenuItem>
            </Menu>
          </Stack>
        </Paper>

        <Box component="main" sx={{ flexGrow: 1, p: { xs: 2, md: 4 } }}>
          {renderContent()}
        </Box>

        {!isDesktop && (
          <Paper
            elevation={3}
            sx={{
              position: 'sticky',
              bottom: 0,
              left: 0,
              right: 0,
              zIndex: theme.zIndex.appBar,
              bgcolor: 'background.paper'
            }}
          >
            <BottomNavigation
              value={activeNav}
              onChange={(_, value) => setActiveNav(value)}
              showLabels
            >
              {NAV_ITEMS.map((item) => (
                <BottomNavigationAction
                  key={item.key}
                  value={item.key}
                  label={item.label}
                  icon={item.icon}
                />
              ))}
            </BottomNavigation>
          </Paper>
        )}
      </Box>
    </Box>
  )
}

interface EmptyStateProps {
  title: string
  description: string
  actionLabel?: string
  onAction?: () => void
}

function EmptyState({ title, description, actionLabel, onAction }: EmptyStateProps) {
  return (
    <Paper
      sx={{
        p: 4,
        textAlign: 'center',
        border: '1px dashed',
        borderColor: 'divider',
        bgcolor: 'background.paper'
      }}
    >
      <Typography variant="h6" gutterBottom>
        {title}
      </Typography>
      <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
        {description}
      </Typography>
      {actionLabel && onAction && (
        <Button variant="contained" onClick={onAction} sx={{ borderRadius: 2 }}>
          {actionLabel}
        </Button>
      )}
    </Paper>
  )
}

interface OverviewProps {
  analysisData: any
  onGoUpload: () => void
}

function OverviewSection({ analysisData, onGoUpload }: OverviewProps) {
  if (!analysisData) {
    return (
      <EmptyState
        title="Upload financial statements to get started"
        description="Drop PDF, Excel, CSV, or XBRL files to unlock interactive dashboards, chat, and peer benchmarks."
        actionLabel="Go to upload"
        onAction={onGoUpload}
      />
    )
  }

  const formatCurrencyValue = (value: any) => {
    const num = normalizeToNumber(value)
    if (num === null) return 'N/A'
    return new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD', minimumFractionDigits: 0 }).format(num)
  }

  const formatPercentValue = (value: any) => {
    const num = normalizeToNumber(value)
    return num === null ? 'N/A' : `${num.toFixed(2)}%`
  }

  const formatTrend = (value: any) => {
    const num = normalizeToNumber(value)
    return num === null ? undefined : `${num.toFixed(1)}%`
  }

  const financial = analysisData.financial_data || {}
  const ratios = analysisData.ratios || {}
  const trends = analysisData.trends || {}
  const metadata = analysisData.llm_metadata || {}
  const llmNotes: string[] = Array.isArray(analysisData.llm_notes) ? analysisData.llm_notes : []
  const risks = filterDisplayableRisks(analysisData.risks)

  const highlights = [
    {
      label: 'Revenue',
      value: formatCurrencyValue(financial.revenue ?? financial.sales),
      helper: trends.revenue_trend ? `Revenue is ${trends.revenue_trend}` : undefined,
      trend: formatTrend(trends.revenue_growth_rate),
      positive: (trends.revenue_growth_rate || 0) >= 0
    },
    {
      label: 'Net income',
      value: formatCurrencyValue(financial.net_income),
      helper: trends.profit_trend ? `Profit is ${trends.profit_trend}` : undefined,
      trend: formatTrend(trends.profit_growth_rate),
      positive: (trends.profit_growth_rate || 0) >= 0
    },
    {
      label: 'Profit margin',
      value: formatPercentValue(ratios.profit_margin),
      helper: 'Net profit / Revenue'
    },
    {
      label: 'ROE',
      value: formatPercentValue(ratios.roe),
      helper: 'Return on equity'
    }
  ]

  return (
    <Stack spacing={3}>
      <Paper sx={{ p: 3 }}>
        <Typography variant="h6" gutterBottom>
          Key metrics
        </Typography>
        <Grid container spacing={2}>
          {highlights.map((item) => (
            <Grid item xs={12} sm={6} md={3} key={item.label}>
              <StatCard {...item} />
            </Grid>
          ))}
        </Grid>
        {(metadata.entity || metadata.period_label || llmNotes.length > 0) && (
          <Stack spacing={1.5} sx={{ mt: 2 }}>
            <Stack direction="row" spacing={1} flexWrap="wrap">
              {metadata.entity && <Chip label={`Entity: ${metadata.entity}`} />}
              {(metadata.period_label || analysisData.period) && <Chip label={`Period: ${metadata.period_label || analysisData.period}`} />}
              {metadata.currency && <Chip label={`Currency: ${metadata.currency}`} />}
            </Stack>
            {llmNotes.length > 0 && (
              <Stack spacing={0.5}>
                {llmNotes.map((note, idx) => (
                  <Typography key={idx} variant="body2" color="text.secondary">
                    • {note}
                  </Typography>
                ))}
              </Stack>
            )}
          </Stack>
        )}
      </Paper>

      {analysisData.benchmark && (
        <Paper sx={{ p: 3 }}>
          <Typography variant="h6" gutterBottom>
            Peer benchmarking
          </Typography>
          <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
            {analysisData.benchmark.summary || 'Comparing your metrics with industry peers.'}
          </Typography>
          <Stack direction="row" spacing={1} flexWrap="wrap">
            <Chip label={`Industry: ${analysisData.industry || analysisData.benchmark.industry || 'General'}`} />
            <Chip label={`Files analyzed: ${analysisData.files_analyzed || 1}`} />
            <Chip label={`Risks detected: ${risks.length}`} />
          </Stack>
        </Paper>
      )}

      {risks.length > 0 && (
        <Paper sx={{ p: 3 }}>
          <Typography variant="h6" gutterBottom>
            Risk highlights
          </Typography>
          <Grid container spacing={2}>
            {risks.slice(0, 3).map((risk: any, index: number) => (
              <Grid item xs={12} md={4} key={index}>
                <Paper variant="outlined" sx={{ p: 2, borderRadius: 2 }}>
                  <Typography variant="subtitle2" gutterBottom>
                    {risk.type}
                  </Typography>
                  <Chip
                    label={risk.severity}
                    color={risk.severity === 'High' ? 'error' : 'warning'}
                    size="small"
                  />
                  <Typography variant="body2" sx={{ mt: 1 }}>
                    {risk.description}
                  </Typography>
                </Paper>
              </Grid>
            ))}
          </Grid>
        </Paper>
      )}
    </Stack>
  )
}

interface StatCardProps {
  label: string
  value: string
  helper?: string
  trend?: string
  positive?: boolean
}

function StatCard({ label, value, helper, trend, positive }: StatCardProps) {
  return (
    <Paper variant="outlined" sx={{ p: 2.5, borderRadius: 2 }}>
      <Typography variant="body2" color="text.secondary">
        {label}
      </Typography>
      <Typography variant="h5" sx={{ mt: 1 }}>
        {value}
      </Typography>
      {helper && (
        <Typography variant="caption" color="text.secondary">
          {helper}
        </Typography>
      )}
      {trend && (
        <Chip
          size="small"
          label={trend}
          color={positive ? 'success' : 'error'}
          sx={{ mt: 1 }}
        />
      )}
    </Paper>
  )
}

function AuthPanel() {
  const { login, register } = useAuth()
  const [mode, setMode] = useState<'login' | 'register'>('login')
  const [form, setForm] = useState({ name: '', email: '', password: '' })
  const [submitting, setSubmitting] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault()
    setSubmitting(true)
    setError(null)
    try {
      if (mode === 'login') {
        await login(form.email, form.password)
      } else {
        await register(form.name || 'Analyst', form.email, form.password)
      }
    } catch (err: any) {
      setError(err.message || 'Authentication failed')
    } finally {
      setSubmitting(false)
    }
  }

  return (
    <Box
      sx={{
        minHeight: '100vh',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        bgcolor: 'background.default',
        p: 2
      }}
    >
      <Grid container component={Paper} elevation={8} sx={{ maxWidth: 900, borderRadius: 4 }}>
        <Grid
          item
          xs={12}
          md={6}
          sx={{
            p: { xs: 4, md: 6 },
            bgcolor: 'primary.main',
            color: 'primary.contrastText',
            borderRadius: { md: '32px 0 0 32px', xs: '32px 32px 0 0' }
          }}
        >
          <Typography variant="h4" fontWeight={700} gutterBottom>
            Financial Statement AI
          </Typography>
          <Typography variant="body1" sx={{ mb: 4 }}>
            Analyze PDF, Excel, CSV, and XBRL files, visualize KPIs, and chat with an AI copilot trained on your data.
          </Typography>
          <Stack spacing={2}>
            {['Responsive dashboard inspired by Next.js sample', 'Secure login with saved chat history', 'Material UI components tuned for finance teams'].map((item) => (
              <Stack direction="row" spacing={1} alignItems="center" key={item}>
                <CheckCircleOutline />
                <Typography variant="body2">{item}</Typography>
              </Stack>
            ))}
          </Stack>
        </Grid>
        <Grid item xs={12} md={6} sx={{ p: { xs: 4, md: 6 } }}>
          <Stack spacing={3} component="form" onSubmit={handleSubmit}>
            <Box>
              <Tabs value={mode} onChange={(_, value) => setMode(value)} sx={{ mb: 2 }}>
                <Tab label="Login" value="login" />
                <Tab label="Register" value="register" />
              </Tabs>
              <Typography variant="h5" fontWeight={600}>
                {mode === 'login' ? 'Sign in to continue' : 'Create your workspace access'}
              </Typography>
            </Box>
            {error && <Alert severity="error">{error}</Alert>}
            {mode === 'register' && (
              <TextField
                label="Full name"
                value={form.name}
                onChange={(e) => setForm({ ...form, name: e.target.value })}
                fullWidth
                required
              />
            )}
            <TextField
              label="Email"
              type="email"
              value={form.email}
              onChange={(e) => setForm({ ...form, email: e.target.value })}
              fullWidth
              required
            />
            <TextField
              label="Password"
              type="password"
              value={form.password}
              onChange={(e) => setForm({ ...form, password: e.target.value })}
              fullWidth
              required
            />
            <Button
              type="submit"
              variant="contained"
              size="large"
              disabled={submitting}
              sx={{ borderRadius: 2 }}
            >
              {submitting ? 'Submitting...' : mode === 'login' ? 'Login' : 'Create account'}
            </Button>
          </Stack>
        </Grid>
      </Grid>
    </Box>
  )
}
