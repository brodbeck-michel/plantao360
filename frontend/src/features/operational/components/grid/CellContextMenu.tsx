import React from 'react';
import { Menu, MenuItem, ListItemIcon, ListItemText, Divider, Typography } from '@mui/material';
import { ContentCopy, ContentPaste, Delete, CalendarMonth } from '@mui/icons-material';

interface ContextMenuItem {
  label: string;
  icon: React.ReactNode;
  onClick: () => void;
  disabled?: boolean;
  divider?: boolean;
}

interface CellContextMenuProps {
  open: boolean;
  anchorEl: HTMLElement | null;
  onClose: () => void;
  onCopyDoctor: () => void;
  onPaste: () => void;
  onClearCell: () => void;
  onDuplicateDay: () => void;
  onDuplicateWeek: () => void;
  hasClipboardData: boolean;
  hasAssignments: boolean;
  canModify?: boolean;
}

export function CellContextMenu({
  open,
  anchorEl,
  onClose,
  onCopyDoctor,
  onPaste,
  onClearCell,
  onDuplicateDay,
  onDuplicateWeek,
  hasClipboardData,
  hasAssignments,
  canModify = false,
}: CellContextMenuProps) {
  const menuItems: ContextMenuItem[] = [
    {
      label: 'Copiar médico',
      icon: <ContentCopy sx={{ fontSize: 18 }} />,
      onClick: () => { onCopyDoctor(); onClose(); },
      disabled: !hasAssignments || !canModify,
    },
    {
      label: 'Colar médico',
      icon: <ContentPaste sx={{ fontSize: 18 }} />,
      onClick: () => { onPaste(); onClose(); },
      disabled: !hasClipboardData || !canModify,
    },
    { label: '', icon: null, onClick: () => {}, divider: true },
    {
      label: 'Duplicar dia inteiro',
      icon: <CalendarMonth sx={{ fontSize: 18 }} />,
      onClick: () => { onDuplicateDay(); onClose(); },
      disabled: !canModify,
    },
    {
      label: 'Duplicar semana',
      icon: <CalendarMonth sx={{ fontSize: 18 }} />,
      onClick: () => { onDuplicateWeek(); onClose(); },
      disabled: !canModify,
    },
    { label: '', icon: null, onClick: () => {}, divider: true },
    {
      label: 'Limpar célula',
      icon: <Delete sx={{ fontSize: 18 }} />,
      onClick: () => { onClearCell(); onClose(); },
      disabled: !hasAssignments || !canModify,
    },
  ];

  return (
    <Menu
      open={open}
      anchorEl={anchorEl}
      onClose={onClose}
      PaperProps={{
        sx: {
          minWidth: 200,
          mt: 1,
          boxShadow: '0 4px 20px rgba(0,0,0,0.12)',
          borderRadius: 1.5,
        },
      }}
    >
      {menuItems.map((item, index) => {
        if (item.divider) return <Divider key={index} sx={{ my: 0.5 }} />;
        return (
          <MenuItem
            key={index}
            onClick={item.onClick}
            disabled={item.disabled}
            sx={{ py: 1, px: 1.5 }}
          >
            <ListItemIcon sx={{ minWidth: 32, color: item.disabled ? '#D1D5DB' : '#6B7280' }}>
              {item.icon}
            </ListItemIcon>
            <ListItemText
              primary={item.label}
              primaryTypographyProps={{
                fontSize: '0.875rem',
                color: item.disabled ? '#D1D5DB' : '#374151',
              }}
            />
          </MenuItem>
        );
      })}
    </Menu>
  );
}
