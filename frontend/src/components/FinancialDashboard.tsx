import { Box, Card, CardContent, Chip, Grid, List, ListItem, ListItemIcon, ListItemText, Paper, Stack, Typography } from '@mui/material'
import { TrendingUp, TrendingDown, Warning, InfoOutlined } from '@mui/icons-material'
import ReactECharts from 'echarts-for-react'
import { normalizeToNumber } from '@/utils/number'
import { filterDisplayableRisks } from '@/utils/risk'

interface FinancialDashboardProps {
  data: any
}

const formatPercentValue = (value: any): string => {
  const num = normalizeToNumber(value)
  return num === null ? 'N/A' : `${num.toFixed(2)}%`
}

const formatRatioValue = (value: any): string => {
  const num = normalizeToNumber(value)
  return num === null ? 'N/A' : num.toFixed(2)
}

const asChartSeries = (values?: any[]) => (values || []).map((value) => normalizeToNumber(value) ?? 0)

export default function FinancialDashboard({ data }: FinancialDashboardProps) {
  const metrics = data.financial_data || {}
  const ratios = data.ratios || {}
  const risks = filterDisplayableRisks(data.risks)
  const trends = data.trends || {}
  const benchmark = data.benchmark
  const industry = data.industry
  const metadata = data.llm_metadata || {}
  const llmNotes: string[] = Array.isArray(data.llm_notes) ? data.llm_notes : []
  const revenueGrowthRate = normalizeToNumber(trends?.revenue_growth_rate)
  const profitGrowthRate = normalizeToNumber(trends?.profit_growth_rate)

  const revenueValue = normalizeToNumber(metrics.revenue ?? metrics.sales)
  const netIncomeValue = normalizeToNumber(metrics.net_income)
  const totalAssetsValue = normalizeToNumber(metrics.total_assets)
  const equityValue = normalizeToNumber(metrics.equity)
  const currentRatioValue = normalizeToNumber(ratios.current_ratio)

  const getRevenueChartOption = () => ({
    title: { text: 'Revenue Trend' },
    tooltip: { trigger: 'axis' },
    xAxis: { type: 'category', data: trends?.periods || [] },
    yAxis: { type: 'value' },
    series: [{
      data: asChartSeries(trends?.revenue_values),
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
          normalizeToNumber(ratios?.profit_margin) ?? 0,
          normalizeToNumber(ratios?.roa) ?? 0,
          normalizeToNumber(ratios?.roe) ?? 0,
          (normalizeToNumber(ratios?.current_ratio) ?? 0) * 10, // Scale for visibility
          (normalizeToNumber(ratios?.quick_ratio) ?? 0) * 10,
          normalizeToNumber(ratios?.debt_to_asset_ratio) ?? 0
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
        normalizeToNumber(ratios?.gross_margin) ?? 0,
        normalizeToNumber(ratios?.operating_margin) ?? 0,
        normalizeToNumber(ratios?.profit_margin) ?? 0
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
    const num = normalizeToNumber(value)
    if (num === null) return 'N/A'
    const percentMetrics = ['margin', 'roa', 'roe', 'debt']
    const ratioMetrics = ['ratio', 'turnover']
    if (percentMetrics.some((token) => metric.includes(token))) {
      return `${num.toFixed(2)}%`
    }
    if (ratioMetrics.some((token) => metric.includes(token))) {
      return num.toFixed(2)
    }
    return num.toFixed(2)
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
                {revenueValue === null ? 'N/A' : formatCurrency(revenueValue)}
              </Typography>
              {trends?.revenue_trend === 'increasing' && (
                <Chip 
                  icon={<TrendingUp />} 
                  label={revenueGrowthRate === null ? 'N/A' : `+${revenueGrowthRate.toFixed(1)}%`} 
                  color="success" 
                  size="small" 
                  sx={{ mt: 1 }}
                />
              )}
              {trends?.revenue_trend === 'decreasing' && (
                <Chip 
                  icon={<TrendingDown />} 
                  label={revenueGrowthRate === null ? 'N/A' : `${revenueGrowthRate.toFixed(1)}%`} 
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
                {netIncomeValue === null ? 'N/A' : formatCurrency(netIncomeValue)}
              </Typography>
              {trends?.profit_trend === 'increasing' && (
                <Chip 
                  icon={<TrendingUp />} 
                  label={profitGrowthRate === null ? 'N/A' : `+${profitGrowthRate.toFixed(1)}%`} 
                  color="success" 
                  size="small" 
                  sx={{ mt: 1 }}
                />
              )}
              {trends?.profit_trend === 'decreasing' && (
                <Chip 
                  icon={<TrendingDown />} 
                  label={profitGrowthRate === null ? 'N/A' : `${profitGrowthRate.toFixed(1)}%`} 
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
                {totalAssetsValue === null ? 'N/A' : formatCurrency(totalAssetsValue)}
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
                {equityValue === null ? 'N/A' : formatCurrency(equityValue)}
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
                {formatPercentValue(ratios?.profit_margin)}
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
                {formatPercentValue(ratios?.roa)}
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
                {formatPercentValue(ratios?.roe)}
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
                {formatRatioValue(currentRatioValue)}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {(metadata.entity || metadata.period_label || metadata.currency || llmNotes.length > 0) && (
        <Paper sx={{ p: 2, mb: 3 }}>
          <Typography variant="h6" gutterBottom>
            Data provenance
          </Typography>
          <Stack direction={{ xs: 'column', sm: 'row' }} spacing={1} flexWrap="wrap" sx={{ mb: llmNotes.length ? 1.5 : 0 }}>
            {metadata.entity && <Chip label={`Entity: ${metadata.entity}`} />}
            {(metadata.period_label || data.period) && <Chip label={`Period: ${metadata.period_label || data.period}`} />}
            {metadata.fiscal_year && <Chip label={`Fiscal year: ${metadata.fiscal_year}`} />}
            <Chip label={`Currency: ${metadata.currency || 'USD'}`} />
          </Stack>
          {llmNotes.length > 0 && (
            <List dense>
              {llmNotes.map((note, index) => (
                <ListItem key={index} sx={{ py: 0.5 }}>
                  <ListItemIcon sx={{ minWidth: 32 }}>
                    <InfoOutlined fontSize="small" />
                  </ListItemIcon>
                  <ListItemText primary={note} />
                </ListItem>
              ))}
            </List>
          )}
        </Paper>
      )}

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
