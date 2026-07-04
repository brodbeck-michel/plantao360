import React from 'react';
import { Box, Typography, IconButton, Tooltip, Divider, Chip } from '@mui/material';
import { Undo as UndoIcon, Redo as RedoIcon, History as HistoryIcon } from '@mui/icons-material';
import type { HistoryAction } from '../../hooks/use-undo-redo';

interface HistoryPanelProps {
  pastActions: HistoryAction[];
  futureActions: HistoryAction[];
  onUndo: (actionId: string) => void;
  onRedo: (actionId: string) => void;
}

export function HistoryPanel({ pastActions, futureActions, onUndo, onRedo }: HistoryPanelProps) {
  if (pastActions.length === 0 && futureActions.length === 0) {
    return (
      <Box sx={{ p: 2, textAlign: 'center' }}>
        <HistoryIcon sx={{ fontSize: 32, color: '#D1D5DB', mb: 1 }} />
        <Typography variant="body2" color="text.secondary" fontSize="0.8125rem">
          Nenhuma ação registrada
        </Typography>
      </Box>
    );
  }

  return (
    <Box sx={{ maxHeight: 300, overflow: 'auto' }}>
      {pastActions.length > 0 && (
        <>
          <Typography variant="caption" color="text.secondary" px={1.5} fontWeight={600}>
            Ações anteriores
          </Typography>
          {pastActions.map((action, idx) => (
            <Box
              key={action.id}
              sx={{
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'space-between',
                px: 1.5,
                py: 0.75,
                '&:hover': { bgcolor: '#F9FAFB' },
              }}
            >
              <Typography variant="caption" color="text.primary" fontSize="0.8125rem" noWrap sx={{ flex: 1 }}>
                {action.label}
              </Typography>
              <Tooltip title="Desfazer esta ação" arrow>
                <IconButton size="small" onClick={() => onUndo(action.id)} sx={{ ml: 0.5, p: 0.25 }}>
                  <UndoIcon sx={{ fontSize: 14 }} />
                </IconButton>
              </Tooltip>
            </Box>
          ))}
        </>
      )}

      {futureActions.length > 0 && (
        <>
          {pastActions.length > 0 && <Divider sx={{ my: 1 }} />}
          <Typography variant="caption" color="text.secondary" px={1.5} fontWeight={600}>
            Ações futuras
          </Typography>
          {futureActions.map((action) => (
            <Box
              key={action.id}
              sx={{
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'space-between',
                px: 1.5,
                py: 0.75,
                opacity: 0.6,
                '&:hover': { bgcolor: '#F9FAFB', opacity: 1 },
              }}
            >
              <Typography variant="caption" color="text.secondary" fontSize="0.8125rem" noWrap sx={{ flex: 1 }}>
                {action.label}
              </Typography>
              <Tooltip title="Refazer esta ação" arrow>
                <IconButton size="small" onClick={() => onRedo(action.id)} sx={{ ml: 0.5, p: 0.25 }}>
                  <RedoIcon sx={{ fontSize: 14 }} />
                </IconButton>
              </Tooltip>
            </Box>
          ))}
        </>
      )}
    </Box>
  );
}
