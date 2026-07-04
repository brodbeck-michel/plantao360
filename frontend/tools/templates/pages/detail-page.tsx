/**
 * {{FEATURE_PASCAL}} Detail Page — Plantão 360
 *
 * Página de detalhes de {{FEATURE_NAME}}.
 * Generated from Golden Module (Doctor).
 */

import React from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { Box, Button, Tabs, Tab } from '@mui/material';
import { ArrowBack } from '@mui/icons-material';
import {{FEATURE_PASCAL}}Header } from '../components/{{FEATURE_NAME}}-header';
import {{FEATURE_PASCAL}}DetailsPanel } from '../details/{{FEATURE_NAME}}-details-panel';
import {{FEATURE_PASCAL}}HistoryTimeline } from '../history/{{FEATURE_NAME}}-history-timeline';
import {{FEATURE_PASCAL}}AuditCard } from '../audit/{{FEATURE_NAME}}-audit-card';
import { LoadingSpinner } from '../../../shared/components/loading-spinner';
import { ErrorBoundary } from '../../../shared/components/error-boundary';
import { use{{FEATURE_PASCAL}}Detail } from '../hooks/use-{{FEATURE_NAME}}s';
import { ROUTES } from '../../../routes/routes';

export function {{FEATURE_PASCAL}}DetailPage() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [tab, setTab] = React.useState(0);
  const { data: item, isLoading } = use{{FEATURE_PASCAL}}Detail(id!);

  if (isLoading) return <LoadingSpinner message="Carregando..." />;
  if (!item) return <Box p={3}><Alert severity="error">Registro não encontrado.</Alert></Box>;

  return (
    <ErrorBoundary>
      <Box p={3}>
        {{FEATURE_PASCAL}}Header
          subtitle={item.name}
          actions={<Button startIcon={<ArrowBack />} onClick={() => navigate(ROUTES.{{FEATURE_NAME.upper()}})}>Voltar</Button>}
        />
        <Tabs value={tab} onChange={(_, v) => setTab(v)} sx={{ mb: 3 }}>
          <Tab label="Detalhes" />
          <Tab label="Histórico" />
          <Tab label="Auditoria" />
        </Tabs>
        {tab === 0 && {{FEATURE_PASCAL}}DetailsPanel item={item} />}
        {tab === 1 && {{FEATURE_PASCAL}}HistoryTimeline events={[]} />}
        {tab === 2 && {{FEATURE_PASCAL}}AuditCard entries={[]} />}
      </Box>
    </ErrorBoundary>
  );
}
