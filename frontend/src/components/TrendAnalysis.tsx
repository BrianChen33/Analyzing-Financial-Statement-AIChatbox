import { Grid, Paper, Typography, Box } from '@mui/material'
import ReactECharts from 'echarts-for-react'

interface TrendAnalysisProps {
  data: any
}

export default function TrendAnalysis({ data }: TrendAnalysisProps) {
  const { trends, historical_data } = data

  const getMultiPeriodChartOption = () => ({
    title: { text: 'Multi-Period Financial Analysis' },
    tooltip: { trigger: 'axis' },
    legend: { data: ['Revenue', 'Net Income', 'Total Assets'] },
    xAxis: { 
      type: 'category', 
      data: historical_data?.periods || ['Period 1', 'Period 2', 'Period 3'] 
    },
    yAxis: { type: 'value' },
    series: [
      {
        name: 'Revenue',
        type: 'line',
        data: historical_data?.revenue || [],
        smooth: true
      },
      {
        name: 'Net Income',
        type: 'line',
        data: historical_data?.net_income || [],
        smooth: true
      },
      {
        name: 'Total Assets',
        type: 'line',
        data: historical_data?.total_assets || [],
        smooth: true
      }
    ]
  })

  const getDuPontChartOption = () => ({
    title: { text: 'DuPont Analysis' },
    tooltip: { trigger: 'item' },
    series: [{
      type: 'sunburst',
      data: [
        {
          name: 'ROE',
          children: [
            {
              name: 'Profit Margin',
              value: data.ratios?.profit_margin || 0,
              children: [
                { name: 'Net Income', value: data.financial_data?.net_income || 0 },
                { name: 'Revenue', value: data.financial_data?.revenue || 0 }
              ]
            },
            {
              name: 'Asset Turnover',
              value: 100,
              children: [
                { name: 'Revenue', value: data.financial_data?.revenue || 0 },
                { name: 'Assets', value: data.financial_data?.total_assets || 0 }
              ]
            },
            {
              name: 'Equity Multiplier',
              value: 100
            }
          ]
        }
      ],
      radius: ['15%', '80%'],
      label: { rotate: 'radial' }
    }]
  })

  const getCashFlowChartOption = () => ({
    title: { text: 'Cash Flow Analysis' },
    tooltip: { trigger: 'axis' },
    xAxis: { type: 'category', data: ['Operating', 'Investing', 'Financing'] },
    yAxis: { type: 'value' },
    series: [{
      type: 'bar',
      data: [
        data.cash_flow?.operating || 0,
        data.cash_flow?.investing || 0,
        data.cash_flow?.financing || 0
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
          <Paper sx={{ p: 2 }}>
            <ReactECharts option={getMultiPeriodChartOption()} style={{ height: 400 }} />
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
