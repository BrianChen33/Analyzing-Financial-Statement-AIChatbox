# Financial Statement AI Analyzer - Frontend

Next.js + Material-UI frontend for the Financial Statement AI Chatbox.

## Features

- 📤 Multi-format file upload (PDF, Excel, CSV, XBRL, Images)
- 📊 Interactive financial dashboard with charts
- 💬 AI-powered chat interface
- 📈 Trend analysis and DuPont decomposition
- 🎤 Voice input support (coming soon)
- 🔊 Text-to-speech output
- 🌓 Dark mode support
- 📱 Responsive design

## Setup

### Prerequisites

- Node.js 18+ and npm

### Installation

```bash
cd frontend
npm install
```

### Configuration

Create a `.env.local` file:

```
API_URL=http://localhost:8000
```

### Development

```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser.

### Build

```bash
npm run build
npm start
```

## Project Structure

```
frontend/
├── src/
│   ├── components/     # React components
│   │   ├── FileUpload.tsx
│   │   ├── FinancialDashboard.tsx
│   │   ├── ChatInterface.tsx
│   │   └── TrendAnalysis.tsx
│   ├── pages/          # Next.js pages
│   │   ├── _app.tsx
│   │   ├── _document.tsx
│   │   └── index.tsx
│   ├── styles/         # Global styles
│   └── utils/          # Utility functions
├── public/             # Static assets
├── package.json
├── tsconfig.json
└── next.config.js
```

## Components

### FileUpload
Drag-and-drop file upload with support for multiple formats.

### FinancialDashboard
Displays key metrics, charts, and risk assessment.

### ChatInterface
Interactive Q&A with AI assistant, supporting text and voice input/output.

### TrendAnalysis
Multi-period trend analysis with DuPont decomposition and cash flow charts.

## Technologies

- **Next.js 14**: React framework
- **Material-UI 5**: Component library
- **TypeScript**: Type safety
- **ECharts**: Data visualization
- **Axios**: HTTP client
- **React Dropzone**: File upload
