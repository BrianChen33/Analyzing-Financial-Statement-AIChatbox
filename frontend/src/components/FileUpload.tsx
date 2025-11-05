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
  Chip
} from '@mui/material'
import { 
  CloudUpload, 
  Description,
  Image,
  TableChart
} from '@mui/icons-material'
import axios from 'axios'

interface FileUploadProps {
  onAnalysisComplete: (data: any) => void
}

export default function FileUpload({ onAnalysisComplete }: FileUploadProps) {
  const [uploading, setUploading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [files, setFiles] = useState<File[]>([])

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
      const response = await axios.post(
        `${process.env.API_URL}/api/analyze`,
        formData,
        {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        }
      )
      onAnalysisComplete(response.data)
    } catch (err: any) {
      setError(err.response?.data?.message || 'Failed to analyze files')
    } finally {
      setUploading(false)
    }
  }

  const getFileIcon = (filename: string) => {
    const ext = filename.split('.').pop()?.toLowerCase()
    if (ext === 'pdf') return <Description />
    if (['png', 'jpg', 'jpeg'].includes(ext || '')) return <Image />
    if (['xls', 'xlsx', 'csv', 'xbrl', 'xml'].includes(ext || '')) return <TableChart />
    return <Description />
  }

  return (
    <Box>
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
