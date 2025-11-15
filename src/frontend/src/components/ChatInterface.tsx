import { useState, useEffect, useRef } from 'react'
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
  CircularProgress,
  Tooltip,
  Button
} from '@mui/material'
import { Send, Person, SmartToy, Mic, VolumeUp, Stop } from '@mui/icons-material'
import api from '@/services/api'
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
  const [isSpeaking, setIsSpeaking] = useState(false)
  const recognitionRef = useRef<SpeechRecognition | null>(null)
  const synthesisRef = useRef<SpeechSynthesis | null>(null)

  const handleSend = async () => {
    if (!input.trim()) return

    const userMessage: Message = { role: 'user', content: input }
    setMessages(prev => [...prev, userMessage])
    setInput('')
    setLoading(true)

    try {
      const response = await api.chat({
        question: input,
        context: analysisData
      })

      const assistantMessage: Message = {
        role: 'assistant',
        content: response.answer
      }
      setMessages(prev => [...prev, assistantMessage])
    } catch (error: any) {
      const errorMessage: Message = {
        role: 'assistant',
        content: error.message || 'Sorry, I encountered an error. Please try again.'
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

  // 初始化语音识别
  useEffect(() => {
    if (typeof window !== 'undefined') {
      const SpeechRecognition = window.SpeechRecognition || (window as any).webkitSpeechRecognition
      
      if (SpeechRecognition) {
        const recognition = new SpeechRecognition()
        recognition.continuous = false
        recognition.interimResults = false
        recognition.lang = 'en-US'
        
        recognition.onstart = () => {
          setIsRecording(true)
        }
        
        recognition.onresult = (event: SpeechRecognitionEvent) => {
          const transcript = event.results[0][0].transcript
          setInput(prev => prev + (prev ? ' ' : '') + transcript)
          setIsRecording(false)
        }
        
        recognition.onerror = (event: any) => {
          console.error('Speech recognition error:', event.error)
          setIsRecording(false)
          
          let errorMessage = '语音识别错误: '
          switch (event.error) {
            case 'not-allowed':
              errorMessage = '麦克风权限被拒绝。请在浏览器设置中允许麦克风权限。'
              break
            case 'network':
              errorMessage = '网络连接错误。Web Speech API需要网络连接才能工作。\n\n解决方案：\n1. 检查网络连接\n2. 确保可以访问Google服务（语音识别使用Google服务）\n3. 如果在中国，可能需要VPN或使用其他语音输入方式'
              break
            case 'no-speech':
              errorMessage = '未检测到语音。请确保麦克风正常工作并清晰说话。'
              break
            case 'audio-capture':
              errorMessage = '无法捕获音频。请检查麦克风是否正常工作。'
              break
            case 'aborted':
              errorMessage = '语音识别被中止。'
              break
            default:
              errorMessage = `语音识别错误: ${event.error}`
          }
          
          alert(errorMessage)
        }
        
        recognition.onend = () => {
          setIsRecording(false)
        }
        
        recognitionRef.current = recognition
      }
      
      if ('speechSynthesis' in window) {
        synthesisRef.current = window.speechSynthesis
      }
    }
    
    return () => {
      if (recognitionRef.current) {
        recognitionRef.current.stop()
      }
      if (synthesisRef.current) {
        synthesisRef.current.cancel()
      }
    }
  }, [])

  const handleVoiceInput = () => {
    if (!recognitionRef.current) {
      alert('Speech recognition is not supported in your browser. Please use Chrome or Edge.')
      return
    }
    
    if (isRecording) {
      recognitionRef.current.stop()
      setIsRecording(false)
    } else {
      // 检查网络连接
      if (!navigator.onLine) {
        alert('网络连接不可用。语音识别需要网络连接。请检查网络后重试。')
        return
      }
      
      try {
        recognitionRef.current.start()
      } catch (error: any) {
        console.error('Failed to start recognition:', error)
        setIsRecording(false)
        
        // 提供更友好的错误提示
        if (error.message && error.message.includes('network')) {
          alert('网络连接错误。\n\n语音识别需要网络连接才能工作。\n\n如果持续出现此错误，请：\n1. 检查网络连接\n2. 确保可以访问Google服务\n3. 或使用手动输入代替语音输入')
        } else {
          alert(`启动语音识别失败: ${error.message || '未知错误'}\n\n请尝试手动输入问题。`)
        }
      }
    }
  }

  const handleSpeak = (text: string) => {
    if (!synthesisRef.current) {
      return
    }
    
    // 停止当前播放
    synthesisRef.current.cancel()
    
    // 提取纯文本（去除markdown格式）
    const plainText = text.replace(/[#*`_~\[\]()]/g, '').replace(/\n/g, ' ')
    
    const utterance = new SpeechSynthesisUtterance(plainText)
    utterance.lang = 'en-US'
    utterance.rate = 0.9
    utterance.pitch = 1.0
    utterance.volume = 1.0
    
    utterance.onstart = () => {
      setIsSpeaking(true)
    }
    
    utterance.onend = () => {
      setIsSpeaking(false)
    }
    
    utterance.onerror = (event) => {
      console.error('Speech synthesis error:', event)
      setIsSpeaking(false)
    }
    
    synthesisRef.current.speak(utterance)
  }

  const stopSpeaking = () => {
    if (synthesisRef.current) {
      synthesisRef.current.cancel()
      setIsSpeaking(false)
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
                          <Tooltip title={isSpeaking ? "Stop speaking" : "Read aloud"}>
                            <IconButton 
                              size="small" 
                              onClick={() => isSpeaking ? stopSpeaking() : handleSpeak(message.content)}
                              sx={{ mt: 1 }}
                              color={isSpeaking ? "error" : "default"}
                            >
                              {isSpeaking ? <Stop fontSize="small" /> : <VolumeUp fontSize="small" />}
                            </IconButton>
                          </Tooltip>
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
        <Box sx={{ display: 'flex', gap: 1, alignItems: 'flex-end' }}>
          <Tooltip title={isRecording ? "Stop recording" : "Voice input (需要网络连接)"}>
            <IconButton 
              color={isRecording ? 'error' : 'default'}
              onClick={handleVoiceInput}
              disabled={loading}
            >
              {isRecording ? <Stop /> : <Mic />}
            </IconButton>
          </Tooltip>
          <TextField
            fullWidth
            multiline
            maxRows={4}
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder={isRecording ? "Listening..." : "Ask a question about the financial statement... (或点击🎤使用语音输入)"}
            disabled={loading || isRecording}
            helperText={isRecording ? "Speak your question..." : "提示：如果语音输入无法使用，请直接手动输入问题"}
          />
          <IconButton 
            color="primary" 
            onClick={handleSend}
            disabled={loading || !input.trim() || isRecording}
          >
            <Send />
          </IconButton>
        </Box>
        {/* 常用问题快捷按钮 */}
        <Box sx={{ mt: 2, display: 'flex', gap: 1, flexWrap: 'wrap' }}>
          <Typography variant="caption" sx={{ width: '100%', mb: 0.5 }}>
            常用问题：
          </Typography>
          {[
            "What is the profit margin?",
            "Tell me about the revenue",
            "What are the risks?",
            "How is the liquidity?"
          ].map((q, idx) => (
            <Button
              key={idx}
              size="small"
              variant="outlined"
              onClick={() => setInput(q)}
              disabled={loading || isRecording}
              sx={{ fontSize: '0.75rem' }}
            >
              {q}
            </Button>
          ))}
        </Box>
      </Paper>
    </Box>
  )
}
