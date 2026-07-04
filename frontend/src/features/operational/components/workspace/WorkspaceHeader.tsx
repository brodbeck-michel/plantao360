import React, { useState } from 'react';
import { Box, Typography, Chip, Button, Tooltip, Menu, MenuItem, ListItemIcon, ListItemText } from '@mui/material';
import {
  Refresh as RefreshIcon,
  MoreVert as MoreIcon,
  Lock as CloseIcon,
  LockOpen as ReopenIcon,
  ContentCopy as DuplicateIcon,
  Delete as DeleteIcon,
  CalendarMonth as CopyIcon,
} from '@mui/icons-material';
import { TemporalNav } from '../navigation/TemporalNav';
import type { PeriodInfo, WorkspaceSummary } from '../../types/operational-types';
import { STATUS_LABELS, getStatusColor } from '../../../../shared/constants/status-colors';

interface WorkspaceHeaderProps {
  period: PeriodInfo;
  summary?: WorkspaceSummary;
  onNavigate: (offset: number) => void;
  onRefresh: () => void;
  onPeriodAction?: (action: 'close' | 'reopen' | 'duplicate' | 'delete' | 'copy-from') => void;
}

export function WorkspaceHeader({ period, summary, onNavigate, onRefresh, onPeriodAction }: WorkspaceHeaderProps) {
  const [anchorEl, setAnchorEl] = useState<null | HTMLElement>(null);
  const statusColor = getStatusColor(period.status);

  return (
    <Box display="flex" alignItems="center" justifyContent="space-between" mb={2}>
      <Box display="flex" alignItems="center" gap={3}>
        <TemporalNav period={period} onNavigate={onNavigate} />
        <Box>
          <Typography variant="caption" color="text.secondary" fontSize="0.6875rem">
            PS Unimed Tubarao
          </Typography>
          {summary && (
            <Box display="flex" gap={2} mt={0.5}>
              <Tooltip title="Cobertura" arrow>
                <Typography variant="caption" fontWeight={600} fontSize="0.6875rem"
                  color={summary.coverage_rate >= 90 ? '#00B87A' : summary.coverage_rate >= 50 ? '#FFB020' : '#FF4842'}>
                  {summary.coverage_rate}%
                </Typography>
              </Tooltip>
              <Tooltip title="Turnos preenchidos" arrow>
                <Typography variant="caption" fontWeight={600} fontSize="0.6875rem" color="#6B7280">
                  {summary.filled_shifts}/{summary.total_shifts} turnos
                </Typography>
              </Tooltip>
              <Tooltip title="Horas totais" arrow>
                <Typography variant="caption" fontWeight={600} fontSize="0.6875rem" color="#6B7280">
                  {summary.total_hours}h
                </Typography>
              </Tooltip>
            </Box>
          )}
        </Box>
      </Box>
      <Box display="flex" alignItems="center" gap={1}>
        <Chip
          label={STATUS_LABELS[period.status] || period.status}
          size="small"
          color={statusColor}
          variant="outlined"
        />
        <Button
          size="small"
          variant="outlined"
          startIcon={<RefreshIcon />}
          onClick={onRefresh}
        >
          Atualizar
        </Button>
        <Button
          size="small"
          variant="outlined"
          onClick={(e) => setAnchorEl(e.currentTarget)}
        >
          <MoreIcon sx={{ fontSize: 18 }} />
        </Button>
        <Menu anchorEl={anchorEl} open={Boolean(anchorEl)} onClose={() => setAnchorEl(null)}>
          {period.status === 'draft' && (
            <MenuItem onClick={() => { setAnchorEl(null); onPeriodAction?.('close'); }}>
              <ListItemIcon><CloseIcon sx={{ fontSize: 18 }} /></ListItemIcon>
              <ListItemText>Fechar Competencia</ListItemText>
            </MenuItem>
          )}
          {period.status === 'closed' && (
            <MenuItem onClick={() => { setAnchorEl(null); onPeriodAction?.('reopen'); }}>
              <ListItemIcon><ReopenIcon sx={{ fontSize: 18 }} /></ListItemIcon>
              <ListItemText>Reabrir Competencia</ListItemText>
            </MenuItem>
          )}
          <MenuItem onClick={() => { setAnchorEl(null); onPeriodAction?.('duplicate'); }}>
            <ListItemIcon><DuplicateIcon sx={{ fontSize: 18 }} /></ListItemIcon>
            <ListItemText>Duplicar Competencia</ListItemText>
          </MenuItem>
          <MenuItem onClick={() => { setAnchorEl(null); onPeriodAction?.('copy-from'); }}>
            <ListItemIcon><CopyIcon sx={{ fontSize: 18 }} /></ListItemIcon>
            <ListItemText>Copiar Mes Anterior</ListItemText>
          </MenuItem>
          {period.status === 'draft' && (
            <MenuItem onClick={() => { setAnchorEl(null); onPeriodAction?.('delete'); }} sx={{ color: '#FF4842' }}>
              <ListItemIcon><DeleteIcon sx={{ fontSize: 18, color: '#FF4842' }} /></ListItemIcon>
              <ListItemText>Excluir Competencia</ListItemText>
            </MenuItem>
          )}
        </Menu>
      </Box>
    </Box>
  );
}
