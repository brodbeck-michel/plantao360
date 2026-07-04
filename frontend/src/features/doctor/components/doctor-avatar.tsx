/**
 * Doctor Avatar Component — Plantão 360
 *
 * Componente de avatar para médicos.
 * Golden Frontend Module — referência oficial.
 *
 * Sprint: 12 — Frontend Architecture, Enterprise Foundation & Golden Frontend Platform
 */

import React from 'react';
import { Avatar } from '@mui/material';

// ============================================================
// Types
// ============================================================

interface DoctorAvatarProps {
  name: string;
  size?: 'small' | 'medium' | 'large';
}

// ============================================================
// Helpers
// ============================================================

function getInitials(name: string): string {
  return name
    .split(' ')
    .map((n) => n[0])
    .join('')
    .toUpperCase()
    .slice(0, 2);
}

function getColorFromName(name: string): string {
  const colors = [
    '#1565C0', '#2E7D32', '#F57F17', '#C62828', '#7B1FA2',
    '#00838F', '#EF6C00', '#AD1457', '#283593', '#558B2F',
  ];
  let hash = 0;
  for (let i = 0; i < name.length; i++) {
    hash = name.charCodeAt(i) + ((hash << 5) - hash);
  }
  return colors[Math.abs(hash) % colors.length];
}

// ============================================================
// Sizes
// ============================================================

const sizeMap = {
  small: 32,
  medium: 40,
  large: 56,
};

// ============================================================
// Component
// ============================================================

export function DoctorAvatar({ name, size = 'medium' }: DoctorAvatarProps) {
  return (
    <Avatar
      sx={{
        width: sizeMap[size],
        height: sizeMap[size],
        bgcolor: getColorFromName(name),
        fontWeight: 600,
        fontSize: size === 'small' ? '0.75rem' : size === 'large' ? '1.25rem' : '0.875rem',
      }}
    >
      {getInitials(name)}
    </Avatar>
  );
}
