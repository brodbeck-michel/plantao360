import React from 'react';
import { Box, Typography, CircularProgress, Fade } from '@mui/material';
import { CheckCircle as CheckIcon, Error as ErrorIcon, Undo as UndoIcon } from '@mui/icons-material';

interface SaveIndicatorProps {
  status: 'saved' | 'saving' | 'error' | 'idle';
  undoCount: number;
  redoCount: number;
  onUndo: () => void;
  onRedo: () => void;
  canUndo: boolean;
  canRedo: boolean;
  lastSaveTime?: string;
}

export function SaveIndicator({
  status,
  undoCount,
  redoCount,
  onUndo,
  onRedo,
  canUndo,
  canRedo,
  lastSaveTime,
}: SaveIndicatorProps) {
  return (
    <Box sx={{ display: 'flex', alignItems: 'center', gap: 1.5, px: 1.5, py: 0.5 }}>
      <Fade in={status === 'saving'} timeout={200}>
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 0.5 }}>
          <CircularProgress size={14} />
          <Typography variant="caption" color="text.secondary" fontSize="0.75rem">
            Salvando...
          </Typography>
        </Box>
      </Fade>

      <Fade in={status === 'saved'} timeout={300}>
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 0.5 }}>
          <CheckIcon sx={{ fontSize: 14, color: '#00995D' }} />
          <Typography variant="caption" color="text.secondary" fontSize="0.75rem">
            Salvo{lastSaveTime ? ` às ${lastSaveTime}` : ''}
          </Typography>
        </Box>
      </Fade>

      <Fade in={status === 'error'} timeout={300}>
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 0.5 }}>
          <ErrorIcon sx={{ fontSize: 14, color: '#FF4842' }} />
          <Typography variant="caption" color="error" fontSize="0.75rem">
            Erro ao salvar
          </Typography>
        </Box>
      </Fade>

      <Box sx={{ display: 'flex', alignItems: 'center', gap: 0.5, ml: 1 }}>
        <Box
          component="button"
          onClick={onUndo}
          disabled={!canUndo}
          sx={{
            display: 'flex', alignItems: 'center', gap: 0.5,
            border: 'none', bg: 'none', cursor: canUndo ? 'pointer' : 'default',
            opacity: canUndo ? 1 : 0.3, p: 0.5, borderRadius: 0.5,
            '&:hover': canUndo ? { bgcolor: '#F3F4F6' } : {},
          }}
        >
          <UndoIcon sx={{ fontSize: 14, transform: 'scaleX(-1)' }} />
          <Typography variant="caption" fontSize="0.75rem">
            {undoCount > 0 ? `Ctrl+Z (${undoCount})` : 'Ctrl+Z'}
          </Typography>
        </Box>

        <Box
          component="button"
          onClick={onRedo}
          disabled={!canRedo}
          sx={{
            display: 'flex', alignItems: 'center', gap: 0.5,
            border: 'none', bg: 'none', cursor: canRedo ? 'pointer' : 'default',
            opacity: canRedo ? 1 : 0.3, p: 0.5, borderRadius: 0.5,
            '&:hover': canRedo ? { bgcolor: '#F3F4F6' } : {},
          }}
        >
          <UndoIcon sx={{ fontSize: 14 }} />
          <Typography variant="caption" fontSize="0.75rem">
            {redoCount > 0 ? `Ctrl+Shift+Z (${redoCount})` : 'Ctrl+Shift+Z'}
          </Typography>
        </Box>
      </Box>
    </Box>
  );
}
