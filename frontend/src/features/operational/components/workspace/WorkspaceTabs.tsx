import React from 'react';
import { Tabs, Tab, Box } from '@mui/material';
import {
  TableChart as PlanilhaIcon,
  Assessment as ResumoIcon,
  People as MedicosIcon,
  AccessTime as TurnosIcon,
  AttachMoney as FinanceiroIcon,
  Description as RelatoriosIcon,
} from '@mui/icons-material';

const TAB_CONFIG = [
  { label: 'Planilha', icon: <PlanilhaIcon sx={{ fontSize: 16 }} /> },
  { label: 'Resumo', icon: <ResumoIcon sx={{ fontSize: 16 }} /> },
  { label: 'Médicos', icon: <MedicosIcon sx={{ fontSize: 16 }} /> },
  { label: 'Turnos', icon: <TurnosIcon sx={{ fontSize: 16 }} /> },
  { label: 'Financeiro', icon: <FinanceiroIcon sx={{ fontSize: 16 }} /> },
  { label: 'Relatórios', icon: <RelatoriosIcon sx={{ fontSize: 16 }} /> },
];

interface WorkspaceTabsProps {
  activeTab: number;
  onTabChange: (tab: number) => void;
}

export function WorkspaceTabs({ activeTab, onTabChange }: WorkspaceTabsProps) {
  return (
    <Box sx={{ borderBottom: 1, borderColor: 'divider', mb: 1 }}>
      <Tabs
        value={activeTab}
        onChange={(_, v) => onTabChange(v)}
        variant="scrollable"
        scrollButtons="auto"
        sx={{
          minHeight: 36,
          '& .MuiTab-root': {
            minHeight: 36,
            fontSize: '0.8125rem',
            fontWeight: 500,
            textTransform: 'none',
          },
        }}
      >
        {TAB_CONFIG.map((tab, i) => (
          <Tab key={i} label={tab.label} icon={tab.icon} iconPosition="start" />
        ))}
      </Tabs>
    </Box>
  );
}
