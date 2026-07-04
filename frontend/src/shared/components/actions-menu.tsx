/**
 * ActionsMenu — Plantão 360
 *
 * Menu de ações genérico reutilizável.
 * Sprint: 13 — Golden Frontend Module
 */

import React, { useState } from 'react';
import { IconButton, Menu, MenuItem, ListItemIcon, ListItemText } from '@mui/material';
import { MoreVert } from '@mui/icons-material';

// ============================================================
// Types
// ============================================================

export interface ActionItem {
  id: string;
  label: string;
  icon?: React.ReactNode;
  onClick: () => void;
  disabled?: boolean;
  divider?: boolean;
  color?: 'inherit' | 'error' | 'warning' | 'info';
}

interface ActionsMenuProps {
  actions: ActionItem[];
  ariaLabel?: string;
}

// ============================================================
// Component
// ============================================================

export function ActionsMenu({ actions, ariaLabel = 'Ações' }: ActionsMenuProps) {
  const [anchorEl, setAnchorEl] = useState<null | HTMLElement>(null);
  const open = Boolean(anchorEl);

  const handleOpen = (event: React.MouseEvent<HTMLElement>) => {
    setAnchorEl(event.currentTarget);
  };

  const handleClose = () => {
    setAnchorEl(null);
  };

  const handleAction = (action: ActionItem) => {
    action.onClick();
    handleClose();
  };

  return (
    <>
      <IconButton
        size="small"
        onClick={handleOpen}
        aria-label={ariaLabel}
        aria-haspopup="true"
        aria-expanded={open}
      >
        <MoreVert fontSize="small" />
      </IconButton>
      <Menu
        anchorEl={anchorEl}
        open={open}
        onClose={handleClose}
        anchorOrigin={{ vertical: 'bottom', horizontal: 'right' }}
        transformOrigin={{ vertical: 'top', horizontal: 'right' }}
        role="menu"
      >
        {actions.map((action, index) => (
          <MenuItem
            key={action.id}
            onClick={() => handleAction(action)}
            disabled={action.disabled}
            role="menuitem"
            divider={action.divider}
            sx={action.color ? { color: `${action.color}.main` } : undefined}
          >
            {action.icon && <ListItemIcon sx={action.color ? { color: `${action.color}.main` } : undefined}>{action.icon}</ListItemIcon>}
            <ListItemText>{action.label}</ListItemText>
          </MenuItem>
        ))}
      </Menu>
    </>
  );
}
