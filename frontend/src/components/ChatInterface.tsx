import { useState } from 'react'
import {
  Box,
  Paper,
  TextField,
  IconButton,
  Typography,
  Avatar,
  List,
  ListItem,
  ListItemAvatar,
  ListItemText,
  Divider,
  CircularProgress
} from '@mui/material'
import { Send, Person, SmartToy, Mic, VolumeUp } from '@mui/icons-material'
import axios from 'axios'
import ReactMarkdown from 'react-markdown'

interface ChatInterfaceProps {
  analysisData: any
}

interface Message {
  role: 'user' | 'assistant'
  content: string
}

export default function ChatInterface({ analysisData }: ChatInterfaceProps) {
  const [messages, setMessages] = useState<Message[]>([
    {
      role: 'assistant',
      content: 'Hello! I\'m your financial analysis assistant. Ask me anything about the analyzed financial statement.'
    }
  ])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const [isRecording, setIsRecording] = useState(false)

  const handleSend = async () => {
    if (!input.trim()) return

    const userMessage: Message = { role: 'user', content: input }
    setMessages(prev => [...prev, userMessage])
    setInput('')
    setLoading(true)

    try {
      const response = await axios.post(`${process.env.API_URL}/api/chat`, {
        question: input,
        context: analysisData
      })

      const assistantMessage: Message = {
        role: 'assistant',
        content: response.data.answer
      }
      setMessages(prev => [...prev, assistantMessage])
    } catch (error) {
      const errorMessage: Message = {
        role: 'assistant',
        content: 'Sorry, I encountered an error. Please try again.'
      }
      setMessages(prev => [...prev, errorMessage])
    } finally {
      setLoading(false)
    }
  }

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSend()
    }
  }

  const handleVoiceInput = () => {
    // Voice recognition implementation would go here
    setIsRecording(!isRecording)
  }

  const handleSpeak = (text: string) => {
    // Text-to-speech implementation would go here
    if ('speechSynthesis' in window) {
      const utterance = new SpeechSynthesisUtterance(text)
      window.speechSynthesis.speak(utterance)
    }
  }

  return (
    <Box sx={{ height: '70vh', display: 'flex', flexDirection: 'column' }}>
      <Paper sx={{ flexGrow: 1, overflow: 'auto', p: 2, mb: 2 }}>
        <List>
          {messages.map((message, index) => (
            <Box key={index}>
              <ListItem alignItems="flex-start">
                <ListItemAvatar>
                  <Avatar sx={{ bgcolor: message.role === 'user' ? 'primary.main' : 'secondary.main' }}>
                    {message.role === 'user' ? <Person /> : <SmartToy />}
                  </Avatar>
                </ListItemAvatar>
                <ListItemText
                  primary={
                    <Typography variant="subtitle2">
                      {message.role === 'user' ? 'You' : 'AI Assistant'}
                    </Typography>
                  }
                  secondary={
                    <Box sx={{ mt: 1 }}>
                      {message.role === 'assistant' ? (
                        <>
                          <ReactMarkdown>{message.content}</ReactMarkdown>
                          <IconButton 
                            size="small" 
                            onClick={() => handleSpeak(message.content)}
                            sx={{ mt: 1 }}
                          >
                            <VolumeUp fontSize="small" />
                          </IconButton>
                        </>
                      ) : (
                        <Typography variant="body2">{message.content}</Typography>
                      )}
                    </Box>
                  }
                />
              </ListItem>
              {index < messages.length - 1 && <Divider />}
            </Box>
          ))}
          {loading && (
            <ListItem>
              <ListItemAvatar>
                <Avatar sx={{ bgcolor: 'secondary.main' }}>
                  <SmartToy />
                </Avatar>
              </ListItemAvatar>
              <ListItemText
                primary="AI Assistant"
                secondary={<CircularProgress size={20} />}
              />
            </ListItem>
          )}
        </List>
      </Paper>

      <Paper sx={{ p: 2 }}>
        <Box sx={{ display: 'flex', gap: 1 }}>
          <IconButton 
            color={isRecording ? 'error' : 'default'}
            onClick={handleVoiceInput}
          >
            <Mic />
          </IconButton>
          <TextField
            fullWidth
            multiline
            maxRows={4}
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Ask a question about the financial statement..."
            disabled={loading}
          />
          <IconButton 
            color="primary" 
            onClick={handleSend}
            disabled={loading || !input.trim()}
          >
            <Send />
          </IconButton>
        </Box>
      </Paper>
    </Box>
  )
}
