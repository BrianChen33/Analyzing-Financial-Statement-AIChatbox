import { Grid, Paper, Typography, Box } from '@mui/material'
import ReactECharts from 'echarts-for-react'

interface TrendAnalysisProps {
  data: any
}

export default function TrendAnalysis({ data }: TrendAnalysisProps) {
  const { trends, historical_data, ratios, financial_data, dupont, cash_flow } = data

  const resolvedHistorical = historical_data || []
  const hasMultiPeriodData = (trends?.periods?.length ?? 0) > 1 || resolvedHistorical.length > 1

  const getMultiPeriodChartOption = () => {
    const periods = trends?.periods || resolvedHistorical.map((entry: any) => entry.period) || ['Period 1']
    const revenueValues = trends?.revenue_values || resolvedHistorical.map((entry: any) => entry.revenue || entry.sales || 0)
    const netIncomeValues = trends?.net_income_values || resolvedHistorical.map((entry: any) => entry.net_income || 0)
    const assetValues = trends?.total_assets_values || resolvedHistorical.map((entry: any) => entry.total_assets || 0)
    
    return {
      title: { text: 'Multi-Period Financial Analysis' },
      tooltip: { 
        trigger: 'axis',
        formatter: (params: any) => {
          let result = params[0].name + '<br/>'
          params.forEach((param: any) => {
            result += `${param.seriesName}: $${param.value.toLocaleString()}<br/>`
          })
          return result
        }
      },
      legend: { data: ['Revenue', 'Net Income', 'Total Assets'] },
      xAxis: { 
        type: 'category', 
        data: periods
      },
      yAxis: { 
        type: 'value',
        axisLabel: {
          formatter: (value: number) => {
            if (value >= 1000000) return `$${(value / 1000000).toFixed(1)}M`
            if (value >= 1000) return `$${(value / 1000).toFixed(1)}K`
            return `$${value}`
          }
        }
      },
      series: [
        {
          name: 'Revenue',
          type: 'line',
          data: revenueValues,
          smooth: true,
          itemStyle: { color: '#5470c6' }
        },
        {
          name: 'Net Income',
          type: 'line',
          data: netIncomeValues,
          smooth: true,
          itemStyle: { color: '#91cc75' }
        },
        {
          name: 'Total Assets',
          type: 'line',
          data: assetValues,
          smooth: true,
          itemStyle: { color: '#fac858' }
        }
      ]
    }
  }

  const getDuPontChartOption = () => {
    if (!dupont || !ratios) {
      return {
        title: { text: 'DuPont Analysis', left: 'center' },
        graphic: [{
          type: 'text',
          left: 'center',
          top: 'middle',
          style: {
            text: 'DuPont data not available',
            fontSize: 16,
            fill: '#999'
          }
        }]
      }
    }
    
    return {
      title: { text: 'DuPont Analysis - ROE Decomposition' },
      tooltip: { trigger: 'axis' },
      xAxis: { 
        type: 'category', 
        data: ['Profit Margin', 'Asset Turnover', 'Equity Multiplier', 'ROE']
      },
      yAxis: { 
        type: 'value',
        axisLabel: {
          formatter: (value: number) => {
            if (value < 10) return `${value.toFixed(2)}%`
            return `${value.toFixed(2)}x`
          }
        }
      },
      series: [{
        type: 'bar',
        data: [
          ratios.profit_margin || 0,
          (ratios.asset_turnover || 0) * 100, // Scale for visibility
          (ratios.equity_multiplier || 0) * 10, // Scale for visibility
          ratios.roe || 0
        ],
        itemStyle: {
          color: (params: any) => {
            const colors = ['#5470c6', '#91cc75', '#fac858', '#ee6666']
            return colors[params.dataIndex] || '#5470c6'
          }
        },
        label: {
          show: true,
          position: 'top',
          formatter: (params: any) => {
            const index = params.dataIndex
            if (index === 0) return `${params.value.toFixed(2)}%`
            if (index === 1) return `${(params.value / 100).toFixed(2)}x`
            if (index === 2) return `${(params.value / 10).toFixed(2)}x`
            return `${params.value.toFixed(2)}%`
          }
        }
      }]
    }
  }

  const getCashFlowChartOption = () => ({
    title: { text: 'Cash Flow Analysis' },
    tooltip: { trigger: 'axis' },
    xAxis: { type: 'category', data: ['Operating', 'Investing', 'Financing'] },
    yAxis: { type: 'value' },
    series: [{
      type: 'bar',
      data: [
        cash_flow?.operating || 0,
        cash_flow?.investing || 0,
        cash_flow?.financing || 0
      ],
      itemStyle: {
        color: (params: any) => {
          return params.value >= 0 ? '#4caf50' : '#f44336'
        }
      }
    }]
  })

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Trend Analysis
      </Typography>

      <Grid container spacing={3}>
        <Grid item xs={12}>
          <Paper sx={{ p: 2, minHeight: 120 }}>
            {hasMultiPeriodData ? (
              <ReactECharts option={getMultiPeriodChartOption()} style={{ height: 400 }} />
            ) : (
              <Box sx={{ p: 3 }}>
                <Typography variant="body1">
                  上传至少两份不同期间的报表（例如 FY2022 与 FY2023），即可解锁多期趋势分析。
                </Typography>
              </Box>
            )}
          </Paper>
        </Grid>

        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 2 }}>
            <ReactECharts option={getDuPontChartOption()} style={{ height: 400 }} />
          </Paper>
        </Grid>

        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 2 }}>
            <ReactECharts option={getCashFlowChartOption()} style={{ height: 400 }} />
          </Paper>
        </Grid>

        <Grid item xs={12}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Trend Summary
            </Typography>
            {trends?.revenue_trend && (
              <Typography variant="body1" paragraph>
                <strong>Revenue Trend:</strong> {trends.revenue_trend} 
                {trends.revenue_growth_rate && ` (${trends.revenue_growth_rate.toFixed(2)}% growth)`}
              </Typography>
            )}
            {trends?.profit_trend && (
              <Typography variant="body1" paragraph>
                <strong>Profit Trend:</strong> {trends.profit_trend}
                {trends.profit_growth_rate && ` (${trends.profit_growth_rate.toFixed(2)}% growth)`}
              </Typography>
            )}
          </Paper>
        </Grid>
      </Grid>
    </Box>
  )
}
