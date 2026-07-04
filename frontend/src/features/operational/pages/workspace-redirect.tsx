import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Box, CircularProgress, Typography } from '@mui/material';
import { apiClient } from '../../../api/client';

export function WorkspaceRedirect() {
  const navigate = useNavigate();
  const [error, setError] = useState('');

  useEffect(() => {
    const load = async () => {
      try {
        const resp = await apiClient.get('/periods?size=5&sort_by=id&sort_direction=desc');
        const periods = resp.data.data?.items || [];
        const active = periods.find((p: any) => p.status === 'draft' || p.status === 'closed');
        if (active) {
          navigate(`/app/periods/${active.id}`, { replace: true });
        } else if (periods.length > 0) {
          navigate(`/app/periods/${periods[0].id}`, { replace: true });
        } else {
          navigate('/app/periods', { replace: true });
        }
      } catch {
        setError('Erro ao carregar competencias');
      }
    };
    load();
  }, [navigate]);

  if (error) {
    return (
      <Box display="flex" flexDirection="column" justifyContent="center" alignItems="center" minHeight="60vh" gap={2}>
        <Typography variant="h6" color="error">{error}</Typography>
      </Box>
    );
  }

  return (
    <Box display="flex" justifyContent="center" alignItems="center" minHeight="60vh" gap={2}>
      <CircularProgress size={24} />
      <Typography color="text.secondary">Carregando workspace...</Typography>
    </Box>
  );
}
