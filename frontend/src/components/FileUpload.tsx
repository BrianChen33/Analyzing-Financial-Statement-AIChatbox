import { useState, useCallback } from 'react'
import { useDropzone } from 'react-dropzone'
import { 
  Box, 
  Paper, 
  Typography, 
  Button, 
  CircularProgress,
  Alert,
  List,
  ListItem,
  ListItemText,
  ListItemIcon,
  Chip,
  FormControl,
  InputLabel,
  Select,
  MenuItem
} from '@mui/material'
import { 
  CloudUpload, 
  Description,
  Image as ImageIcon,
  TableChart
} from '@mui/icons-material'
import api from '@/services/api'

interface FileUploadProps {
  onAnalysisComplete: (data: any) => void
}

export default function FileUpload({ onAnalysisComplete }: FileUploadProps) {
  const [uploading, setUploading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [files, setFiles] = useState<File[]>([])
  const [industry, setIndustry] = useState('general')
  const industryOptions = [
    { value: 'general', label: 'General' },
    { value: 'technology', label: 'Technology' },
    { value: 'retail', label: 'Retail' },
    { value: 'manufacturing', label: 'Manufacturing' }
  ]

  const onDrop = useCallback((acceptedFiles: File[]) => {
    setFiles(acceptedFiles)
    setError(null)
  }, [])

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'application/pdf': ['.pdf'],
      'image/*': ['.png', '.jpg', '.jpeg'],
      'application/vnd.ms-excel': ['.xls'],
      'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': ['.xlsx'],
      'text/csv': ['.csv'],
      'application/xml': ['.xbrl', '.xml']
    },
    multiple: true
  })

  const handleUpload = async () => {
    if (files.length === 0) {
      setError('Please select files to upload')
      return
    }

    setUploading(true)
    setError(null)

    const formData = new FormData()
    files.forEach(file => {
      formData.append('files', file)
    })

    try {
      const data = await api.analyzeFiles(files, { industry })
      onAnalysisComplete(data)
    } catch (err: any) {
      setError(err.message || 'Failed to analyze files')
    } finally {
      setUploading(false)
    }
  }

  const getFileIcon = (filename: string) => {
    const ext = filename.split('.').pop()?.toLowerCase()
    if (ext === 'pdf') return <Description />
    if (['png', 'jpg', 'jpeg'].includes(ext || '')) return <ImageIcon />
    if (['xls', 'xlsx', 'csv', 'xbrl', 'xml'].includes(ext || '')) return <TableChart />
    return <Description />
  }

  return (
    <Box>
      <Paper sx={{ p: 2, mb: 2 }}>
        <Typography variant="body1" gutterBottom>
          Tips
        </Typography>
        <Typography variant="body2" color="text.secondary">
          • Upload annual financial statements  to strengthen KPI accuracy.<br />
          • Choose the closest industry to enable peer benchmarking and narrative insights.<br />
          • Supported formats: PDF, images, Excel, CSV, XBRL; PDF is recommended.
        </Typography>
      </Paper>
      <Paper
        {...getRootProps()}
        sx={{
          p: 4,
          textAlign: 'center',
          border: '2px dashed',
          borderColor: isDragActive ? 'primary.main' : 'grey.300',
          bgcolor: isDragActive ? 'action.hover' : 'background.paper',
          cursor: 'pointer',
          transition: 'all 0.3s',
          '&:hover': {
            borderColor: 'primary.main',
            bgcolor: 'action.hover'
          }
        }}
      >
        <input {...getInputProps()} />
        <CloudUpload sx={{ fontSize: 60, color: 'primary.main', mb: 2 }} />
        <Typography variant="h5" gutterBottom>
          {isDragActive ? 'Drop files here' : 'Drag & drop files here'}
        </Typography>
        <Typography variant="body2" color="text.secondary" paragraph>
          or click to select files
        </Typography>
        <Box sx={{ mt: 2 }}>
          <Chip label="PDF" sx={{ mr: 1 }} />
          <Chip label="Images" sx={{ mr: 1 }} />
          <Chip label="Excel" sx={{ mr: 1 }} />
          <Chip label="CSV" sx={{ mr: 1 }} />
          <Chip label="XBRL" />
        </Box>
      </Paper>

      <Paper sx={{ mt: 2, p: 2 }}>
        <FormControl fullWidth>
          <InputLabel id="industry-label">Industry Benchmark</InputLabel>
          <Select
            labelId="industry-label"
            value={industry}
            label="Industry Benchmark"
            onChange={(event) => setIndustry(event.target.value)}
          >
            {industryOptions.map((option) => (
              <MenuItem key={option.value} value={option.value}>
                {option.label}
              </MenuItem>
            ))}
          </Select>
        </FormControl>
      </Paper>

      {files.length > 0 && (
        <Paper sx={{ mt: 2, p: 2 }}>
          <Typography variant="h6" gutterBottom>
            Selected Files ({files.length})
          </Typography>
          <List>
            {files.map((file, index) => (
              <ListItem key={index}>
                <ListItemIcon>
                  {getFileIcon(file.name)}
                </ListItemIcon>
                <ListItemText 
                  primary={file.name}
                  secondary={`${(file.size / 1024).toFixed(2)} KB`}
                />
              </ListItem>
            ))}
          </List>
          <Button
            variant="contained"
            fullWidth
            onClick={handleUpload}
            disabled={uploading}
            startIcon={uploading ? <CircularProgress size={20} /> : <CloudUpload />}
          >
            {uploading ? 'Analyzing...' : 'Analyze Files'}
          </Button>
        </Paper>
      )}

      {error && (
        <Alert severity="error" sx={{ mt: 2 }}>
          {error}
        </Alert>
      )}
    </Box>
  )
}
