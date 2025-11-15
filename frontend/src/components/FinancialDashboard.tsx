import { Grid, Paper, Typography, Box, Card, CardContent, Chip } from '@mui/material'
import { TrendingUp, TrendingDown, Warning } from '@mui/icons-material'
import ReactECharts from 'echarts-for-react'

interface FinancialDashboardProps {
  data: any
}

export default function FinancialDashboard({ data }: FinancialDashboardProps) {
  const { financial_data, ratios, risks, trends, benchmark, industry } = data

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
    title: { text: 'Financial Ratios Overview' },
    tooltip: { trigger: 'axis', axisPointer: { type: 'shadow' } },
    legend: { data: ['Profitability', 'Liquidity', 'Leverage'] },
    xAxis: { 
      type: 'category', 
      data: ['Profit Margin', 'ROA', 'ROE', 'Current Ratio', 'Quick Ratio', 'Debt/Asset']
    },
    yAxis: { type: 'value' },
    series: [
      {
        name: 'Value',
        type: 'bar',
        data: [
          ratios?.profit_margin || 0,
          ratios?.roa || 0,
          ratios?.roe || 0,
          (ratios?.current_ratio || 0) * 10, // Scale for visibility
          (ratios?.quick_ratio || 0) * 10,
          ratios?.debt_to_asset_ratio || 0
        ],
        itemStyle: {
          color: (params: any) => {
            const colors = ['#5470c6', '#91cc75', '#fac858', '#ee6666', '#73c0de', '#3ba272']
            return colors[params.dataIndex] || '#5470c6'
          }
        }
      }
    ]
  })

  const getProfitabilityChartOption = () => ({
    title: { text: 'Profitability Analysis' },
    tooltip: { trigger: 'axis' },
    xAxis: { type: 'category', data: ['Gross Margin', 'Operating Margin', 'Profit Margin'] },
    yAxis: { type: 'value', max: 100, axisLabel: { formatter: '{value}%' } },
    series: [{
      type: 'bar',
      data: [
        ratios?.gross_margin || 0,
        ratios?.operating_margin || 0,
        ratios?.profit_margin || 0
      ],
      itemStyle: {
        color: (params: any) => {
          const value = params.value
          return value > 10 ? '#91cc75' : value > 5 ? '#fac858' : '#ee6666'
        }
      }
    }]
  })

  const formatCurrency = (value: number) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      minimumFractionDigits: 0
    }).format(value)
  }

  const formatBenchmarkValue = (metric: string, value?: number) => {
    if (value === undefined || value === null) return 'N/A'
    const percentMetrics = ['margin', 'roa', 'roe', 'debt']
    const ratioMetrics = ['ratio', 'turnover']
    if (percentMetrics.some((token) => metric.includes(token))) {
      return `${value.toFixed(2)}%`
    }
    if (ratioMetrics.some((token) => metric.includes(token))) {
      return value.toFixed(2)
    }
    return value.toFixed(2)
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
              {trends?.revenue_trend === 'decreasing' && (
                <Chip 
                  icon={<TrendingDown />} 
                  label={`${trends?.revenue_growth_rate?.toFixed(1)}%`} 
                  color="error" 
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
              {trends?.profit_trend === 'decreasing' && (
                <Chip 
                  icon={<TrendingDown />} 
                  label={`${trends?.profit_growth_rate?.toFixed(1)}%`} 
                  color="error" 
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
                Total Assets
              </Typography>
              <Typography variant="h5">
                {formatCurrency(financial_data?.total_assets || 0)}
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Typography color="text.secondary" gutterBottom>
                Equity
              </Typography>
              <Typography variant="h5">
                {formatCurrency(financial_data?.equity || 0)}
              </Typography>
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
                {ratios?.profit_margin?.toFixed(2) || 'N/A'}%
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
                {ratios?.roa?.toFixed(2) || 'N/A'}%
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Typography color="text.secondary" gutterBottom>
                ROE
              </Typography>
              <Typography variant="h5">
                {ratios?.roe?.toFixed(2) || 'N/A'}%
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Typography color="text.secondary" gutterBottom>
                Current Ratio
              </Typography>
              <Typography variant="h5">
                {ratios?.current_ratio?.toFixed(2) || 'N/A'}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Charts */}
      <Grid container spacing={3} sx={{ mb: 3 }}>
        {trends?.revenue_values && trends.revenue_values.length > 0 && (
          <Grid item xs={12} md={6}>
            <Paper sx={{ p: 2 }}>
              <ReactECharts option={getRevenueChartOption()} style={{ height: 300 }} />
            </Paper>
          </Grid>
        )}
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 2 }}>
            <ReactECharts option={getProfitabilityChartOption()} style={{ height: 300 }} />
          </Paper>
        </Grid>
        <Grid item xs={12}>
          <Paper sx={{ p: 2 }}>
            <ReactECharts option={getRatiosChartOption()} style={{ height: 350 }} />
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

      {/* Peer Benchmark */}
      {benchmark && benchmark.metrics && benchmark.metrics.length > 0 && (
        <Paper sx={{ p: 2, mt: 3 }}>
          <Typography variant="h6" gutterBottom>
            Peer Benchmarking ({benchmark.industry || industry || 'General'})
          </Typography>
          {benchmark.summary && (
            <Typography variant="body2" color="text.secondary" gutterBottom>
              {benchmark.summary}
            </Typography>
          )}
          <Grid container spacing={2}>
            {benchmark.metrics.map((metric: any, index: number) => (
              <Grid item xs={12} md={6} key={index}>
                <Card>
                  <CardContent>
                    <Typography variant="subtitle2" gutterBottom>
                      {metric.metric.replace(/_/g, ' ').toUpperCase()}
                    </Typography>
                    <Typography variant="body2">
                      Company: {formatBenchmarkValue(metric.metric, metric.company)}
                    </Typography>
                    <Typography variant="body2">
                      Benchmark: {formatBenchmarkValue(metric.metric, metric.benchmark)}
                    </Typography>
                    <Typography variant="body2" color={metric.difference >= 0 ? 'success.main' : 'error.main'}>
                      Difference: {formatBenchmarkValue(metric.metric, metric.difference)}
                    </Typography>
                  </CardContent>
                </Card>
              </Grid>
            ))}
          </Grid>
          {benchmark.alerts && benchmark.alerts.length > 0 && (
            <Box sx={{ mt: 2 }}>
              <Typography variant="subtitle2">Alerts</Typography>
              {benchmark.alerts.map((alert, idx) => (
                <Chip key={idx} label={alert} color="warning" sx={{ mr: 1, mt: 1 }} />
              ))}
            </Box>
          )}
        </Paper>
      )}
    </Box>
  )
}
