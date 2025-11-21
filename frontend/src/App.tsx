import { useState } from 'react'
import { ThemeProvider, createTheme } from '@mui/material/styles'
import CssBaseline from '@mui/material/CssBaseline'
import { Box, Container, Typography, Button } from '@mui/material'

const theme = createTheme({
  palette: {
    mode: 'light',
    primary: {
      main: '#1976d2',
    },
    secondary: {
      main: '#dc004e',
    },
  },
})

function App() {
  const [count, setCount] = useState(0)

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Container maxWidth="lg">
        <Box sx={{ my: 4, textAlign: 'center' }}>
          <Typography variant="h2" component="h1" gutterBottom>
            貿易DX管理システム
          </Typography>
          <Typography variant="h5" component="h2" gutterBottom color="text.secondary">
            Trade Management System v2.1
          </Typography>
          <Box sx={{ mt: 4 }}>
            <Button 
              variant="contained" 
              onClick={() => setCount((count) => count + 1)}
              size="large"
            >
              カウント: {count}
            </Button>
          </Box>
          <Typography variant="body1" sx={{ mt: 4 }} color="text.secondary">
            フロントエンド初期セットアップ完了
          </Typography>
        </Box>
      </Container>
    </ThemeProvider>
  )
}

export default App

