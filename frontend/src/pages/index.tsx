import { useState } from 'react'
import { 
  Box, 
  Container, 
  Grid, 
  Paper, 
  Typography, 
  AppBar, 
  Toolbar, 
  IconButton,
  Tabs,
  Tab
} from '@mui/material'
import { 
  Brightness4, 
  Brightness7, 
  Upload,
  Assessment,
  Chat,
  TrendingUp
} from '@mui/icons-material'
import FileUpload from '@/components/FileUpload'
import FinancialDashboard from '@/components/FinancialDashboard'
import ChatInterface from '@/components/ChatInterface'
import TrendAnalysis from '@/components/TrendAnalysis'

interface HomeProps {
  darkMode: boolean
  setDarkMode: (mode: boolean) => void
}

export default function Home({ darkMode, setDarkMode }: HomeProps) {
  const [currentTab, setCurrentTab] = useState(0)
  const [analysisData, setAnalysisData] = useState<any>(null)

  const handleTabChange = (event: React.SyntheticEvent, newValue: number) => {
    setCurrentTab(newValue)
  }

  const handleAnalysisComplete = (data: any) => {
    setAnalysisData(data)
    setCurrentTab(1) // Switch to dashboard tab
  }

  return (
    <Box sx={{ flexGrow: 1, minHeight: '100vh', bgcolor: 'background.default' }}>
      <AppBar position="static">
        <Toolbar>
          <Assessment sx={{ mr: 2 }} />
          <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
            Financial Statement AI Analyzer
          </Typography>
          <IconButton onClick={() => setDarkMode(!darkMode)} color="inherit">
            {darkMode ? <Brightness7 /> : <Brightness4 />}
          </IconButton>
        </Toolbar>
      </AppBar>

      <Container maxWidth="xl" sx={{ mt: 4, mb: 4 }}>
        <Paper sx={{ p: 2, mb: 3 }}>
          <Tabs value={currentTab} onChange={handleTabChange} centered>
            <Tab icon={<Upload />} label="Upload" />
            <Tab icon={<Assessment />} label="Dashboard" disabled={!analysisData} />
            <Tab icon={<Chat />} label="Q&A" disabled={!analysisData} />
            <Tab icon={<TrendingUp />} label="Trends" disabled={!analysisData} />
          </Tabs>
        </Paper>

        {currentTab === 0 && (
          <FileUpload onAnalysisComplete={handleAnalysisComplete} />
        )}

        {currentTab === 1 && analysisData && (
          <FinancialDashboard data={analysisData} />
        )}

        {currentTab === 2 && analysisData && (
          <ChatInterface analysisData={analysisData} />
        )}

        {currentTab === 3 && analysisData && (
          <TrendAnalysis data={analysisData} />
        )}
      </Container>
    </Box>
  )
}
