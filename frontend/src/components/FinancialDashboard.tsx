import { Grid, Paper, Typography, Box, Card, CardContent, Chip } from '@mui/material'
import { TrendingUp, TrendingDown, Warning } from '@mui/icons-material'
import ReactECharts from 'echarts-for-react'

interface FinancialDashboardProps {
  data: any
}

export default function FinancialDashboard({ data }: FinancialDashboardProps) {
  const { financial_data, ratios, risks, trends } = data

  const getRevenueChartOption = () => ({
    title: { text: 'Revenue Trend' },
    tooltip: { trigger: 'axis' },
    xAxis: { type: 'category', data: trends?.periods || [] },
    yAxis: { type: 'value' },
    series: [{
      data: trends?.revenue_values || [],
      type: 'line',
      smooth: true,
      areaStyle: { opacity: 0.3 }
    }]
  })

  const getRatiosChartOption = () => ({
    title: { text: 'Financial Ratios' },
    tooltip: { trigger: 'item' },
    radar: {
      indicator: [
        { name: 'Profit Margin', max: 100 },
        { name: 'ROA', max: 100 },
        { name: 'ROE', max: 100 },
        { name: 'Debt Ratio', max: 100, invert: true }
      ]
    },
    series: [{
      type: 'radar',
      data: [{
        value: [
          ratios?.profit_margin || 0,
          ratios?.roa || 0,
          ratios?.roe || 0,
          ratios?.debt_to_asset_ratio || 0
        ],
        name: 'Current Period'
      }]
    }]
  })

  const formatCurrency = (value: number) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      minimumFractionDigits: 0
    }).format(value)
  }

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Financial Dashboard
      </Typography>

      {/* Key Metrics */}
      <Grid container spacing={3} sx={{ mb: 3 }}>
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Typography color="text.secondary" gutterBottom>
                Revenue
              </Typography>
              <Typography variant="h5">
                {formatCurrency(financial_data?.revenue || 0)}
              </Typography>
              {trends?.revenue_trend === 'increasing' && (
                <Chip 
                  icon={<TrendingUp />} 
                  label={`+${trends?.revenue_growth_rate?.toFixed(1)}%`} 
                  color="success" 
                  size="small" 
                  sx={{ mt: 1 }}
                />
              )}
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Typography color="text.secondary" gutterBottom>
                Net Income
              </Typography>
              <Typography variant="h5">
                {formatCurrency(financial_data?.net_income || 0)}
              </Typography>
              {trends?.profit_trend === 'increasing' && (
                <Chip 
                  icon={<TrendingUp />} 
                  label={`+${trends?.profit_growth_rate?.toFixed(1)}%`} 
                  color="success" 
                  size="small" 
                  sx={{ mt: 1 }}
                />
              )}
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Typography color="text.secondary" gutterBottom>
                Profit Margin
              </Typography>
              <Typography variant="h5">
                {ratios?.profit_margin?.toFixed(2)}%
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Typography color="text.secondary" gutterBottom>
                ROA
              </Typography>
              <Typography variant="h5">
                {ratios?.roa?.toFixed(2)}%
              </Typography>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Charts */}
      <Grid container spacing={3} sx={{ mb: 3 }}>
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 2 }}>
            <ReactECharts option={getRevenueChartOption()} style={{ height: 300 }} />
          </Paper>
        </Grid>
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 2 }}>
            <ReactECharts option={getRatiosChartOption()} style={{ height: 300 }} />
          </Paper>
        </Grid>
      </Grid>

      {/* Risks */}
      {risks && risks.length > 0 && (
        <Paper sx={{ p: 2 }}>
          <Typography variant="h6" gutterBottom>
            <Warning sx={{ verticalAlign: 'middle', mr: 1 }} />
            Risk Assessment
          </Typography>
          <Grid container spacing={2}>
            {risks.map((risk: any, index: number) => (
              <Grid item xs={12} md={6} key={index}>
                <Card>
                  <CardContent>
                    <Typography variant="h6" color={risk.severity === 'High' ? 'error' : 'warning'}>
                      {risk.type}
                    </Typography>
                    <Chip 
                      label={risk.severity} 
                      color={risk.severity === 'High' ? 'error' : 'warning'}
                      size="small"
                      sx={{ mb: 1 }}
                    />
                    <Typography variant="body2">
                      {risk.description}
                    </Typography>
                  </CardContent>
                </Card>
              </Grid>
            ))}
          </Grid>
        </Paper>
      )}
    </Box>
  )
}
