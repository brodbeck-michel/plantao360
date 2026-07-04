import { createTheme } from '@mui/material/styles';
import { ptBR } from '@mui/material/locale';

export const theme = createTheme(
  {
    palette: {
      primary: {
        main: '#1976d2',
      },
      secondary: {
        main: '#9c27b0',
      },
      background: {
        default: '#f5f5f5',
      },
    },
    typography: {
      fontFamily: '"Roboto", "Helvetica", "Arial", sans-serif',
    },
  },
  ptBR
);
