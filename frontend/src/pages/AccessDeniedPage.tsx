import { Box, Typography, Button } from '@mui/material';
import BlockIcon from '@mui/icons-material/Block';
import { useNavigate } from 'react-router-dom';
import { ROUTES } from '../routes/routes';
import { tokens } from '../theme';

export default function AccessDeniedPage() {
  const navigate = useNavigate();

  return (
    <Box sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', minHeight: '60vh', gap: 2 }}>
      <BlockIcon sx={{ fontSize: 64, color: tokens.colors.operational.critical }} />
      <Typography variant="h4" fontWeight={700} color={tokens.colors.text.primary}>
        Acesso Negado
      </Typography>
      <Typography variant="body1" color={tokens.colors.text.muted} textAlign="center" maxWidth={400}>
        Voce nao tem permissao para acessar esta pagina. Entre em contato com o administrador.
      </Typography>
      <Button variant="contained" onClick={() => navigate(ROUTES.DASHBOARD)} sx={{ mt: 2 }}>
        Voltar ao Dashboard
      </Button>
    </Box>
  );
}
