/**
 * HomePage — Plantão 360
 *
 * Landing page that redirects to Dashboard or shows overview.
 * Uses consistent layout with other pages (Box p={3} within MainLayout).
 *
 * Sprint: 14 — Operational MVP
 * Sprint: 14.1 — Integration Review (consistent layout)
 */

import { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Box, Typography, Card, CardContent, Stack, Button, Grid } from '@mui/material';
import { Dashboard, People, EventNote, HealthAndSafety } from '@mui/icons-material';
import { ROUTES } from '../routes/routes';

export default function HomePage() {
  const navigate = useNavigate();

  // Auto-redirect to Dashboard (operational entry point)
  useEffect(() => {
    // Don't auto-redirect — show overview instead
  }, []);

  return (
    <Box>
      <Typography variant="h5" fontWeight={600} sx={{ mb: 3 }}>
        Plantão 360
      </Typography>

      <Typography variant="body1" color="text.secondary" sx={{ mb: 3 }}>
        Sistema de gestão de plantões médicos. Selecione uma opção abaixo para começar.
      </Typography>

      <Grid container spacing={2}>
        <Grid size={{ xs: 12, sm: 6, md: 3 }}>
          <Card
            sx={{ cursor: 'pointer', '&:hover': { boxShadow: 4 } }}
            onClick={() => navigate(ROUTES.DASHBOARD)}
          >
            <CardContent>
              <Stack spacing={1}>
                <Dashboard color="primary" sx={{ fontSize: 40 }} />
                <Typography variant="h6" fontWeight={600}>
                  Dashboard
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  Visão geral operacional
                </Typography>
              </Stack>
            </CardContent>
          </Card>
        </Grid>

        <Grid size={{ xs: 12, sm: 6, md: 3 }}>
          <Card
            sx={{ cursor: 'pointer', '&:hover': { boxShadow: 4 } }}
            onClick={() => navigate(ROUTES.DOCTORS)}
          >
            <CardContent>
              <Stack spacing={1}>
                <People color="primary" sx={{ fontSize: 40 }} />
                <Typography variant="h6" fontWeight={600}>
                  Médicos
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  Gestão de pessoal médico
                </Typography>
              </Stack>
            </CardContent>
          </Card>
        </Grid>

        <Grid size={{ xs: 12, sm: 6, md: 3 }}>
          <Card
            sx={{ cursor: 'pointer', '&:hover': { boxShadow: 4 } }}
            onClick={() => navigate(ROUTES.PERIODS)}
          >
            <CardContent>
              <Stack spacing={1}>
                <EventNote color="primary" sx={{ fontSize: 40 }} />
                <Typography variant="h6" fontWeight={600}>
                  Competências
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  Períodos operacionais
                </Typography>
              </Stack>
            </CardContent>
          </Card>
        </Grid>

        <Grid size={{ xs: 12, sm: 6, md: 3 }}>
          <Card
            sx={{ cursor: 'pointer', '&:hover': { boxShadow: 4 } }}
            onClick={() => navigate(ROUTES.HEALTH)}
          >
            <CardContent>
              <Stack spacing={1}>
                <HealthAndSafety color="primary" sx={{ fontSize: 40 }} />
                <Typography variant="h6" fontWeight={600}>
                  Health Check
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  Status do sistema
                </Typography>
              </Stack>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Box>
  );
}
