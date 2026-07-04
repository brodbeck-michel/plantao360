/**
 * HealthPage — Plantão 360
 *
 * System health check page.
 * Uses consistent layout with other pages (Box p={3} within MainLayout).
 *
 * Sprint: 14 — Operational MVP
 * Sprint: 14.1 — Integration Review (consistent layout)
 */

import { useQuery } from '@tanstack/react-query';
import { Box, Typography, Card, CardContent, Stack, Chip, CircularProgress, Alert, AlertTitle } from '@mui/material';
import { healthApi, HealthResponse } from '../api/health';

export default function HealthPage() {
  const { data, isLoading, error } = useQuery<HealthResponse>({
    queryKey: ['health'],
    queryFn: async () => {
      const response = await healthApi.check();
      return response.data;
    },
  });

  return (
    <Box>
      <Typography variant="h5" fontWeight={600} sx={{ mb: 3 }}>
        Health Check
      </Typography>

      {isLoading && (
        <Box sx={{ display: 'flex', justifyContent: 'center', py: 4 }}>
          <CircularProgress />
        </Box>
      )}

      {error && (
        <Alert severity="error" sx={{ mb: 2 }}>
          <AlertTitle>Erro de Conexão</AlertTitle>
          Não foi possível conectar com o servidor. Verifique se o backend está rodando.
        </Alert>
      )}

      {data && (
        <Card>
          <CardContent>
            <Stack spacing={2}>
              <Stack direction="row" justifyContent="space-between" alignItems="center">
                <Typography variant="body2" color="text.secondary">Status</Typography>
                <Chip
                  label={data.status}
                  color={data.status === 'ok' ? 'success' : 'error'}
                  size="small"
                />
              </Stack>
              <Stack direction="row" justifyContent="space-between" alignItems="center">
                <Typography variant="body2" color="text.secondary">Versão</Typography>
                <Typography variant="body2" fontWeight={500}>{data.version}</Typography>
              </Stack>
              <Stack direction="row" justifyContent="space-between" alignItems="center">
                <Typography variant="body2" color="text.secondary">Ambiente</Typography>
                <Typography variant="body2" fontWeight={500}>{data.environment}</Typography>
              </Stack>
              <Stack direction="row" justifyContent="space-between" alignItems="center">
                <Typography variant="body2" color="text.secondary">Banco de Dados</Typography>
                <Chip
                  label={data.database}
                  color={data.database === 'connected' ? 'success' : 'error'}
                  size="small"
                />
              </Stack>
              <Stack direction="row" justifyContent="space-between" alignItems="center">
                <Typography variant="body2" color="text.secondary">Timestamp</Typography>
                <Typography variant="body2" fontWeight={500}>{data.timestamp}</Typography>
              </Stack>
            </Stack>
          </CardContent>
        </Card>
      )}
    </Box>
  );
}
