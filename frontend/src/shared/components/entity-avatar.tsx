/**
 * EntityAvatar — Plantão 360
 *
 * Avatar genérico para entidades (médicos, pacientes, etc.).
 * Pode ser reutilizado por qualquer feature que precise de avatar.
 *
 * Sprint: 13 — Golden Frontend Module
 */

import React from 'react';
import { Avatar, AvatarProps } from '@mui/material';

// ============================================================
// Types
// ============================================================

interface EntityAvatarProps extends Omit<AvatarProps, 'src' | 'alt'> {
  name: string;
  src?: string;
  size?: 'small' | 'medium' | 'large';
}

// ============================================================
// Helpers
// ============================================================

function getInitials(name: string): string {
  return name
    .split(' ')
    .filter(Boolean)
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

const sizeMap: Record<'small' | 'medium' | 'large', { width: number; height: number; fontSize: string }> = {
  small: { width: 32, height: 32, fontSize: '0.75rem' },
  medium: { width: 40, height: 40, fontSize: '0.875rem' },
  large: { width: 56, height: 56, fontSize: '1.25rem' },
};

// ============================================================
// Component
// ============================================================

export function EntityAvatar({ name, src, size = 'medium', sx, ...props }: EntityAvatarProps) {
  const dimensions = sizeMap[size];

  return (
    <Avatar
      src={src}
      alt={name}
      sx={{
        width: dimensions.width,
        height: dimensions.height,
        bgcolor: src ? 'transparent' : getColorFromName(name),
        fontWeight: 600,
        fontSize: dimensions.fontSize,
        ...sx,
      }}
      {...props}
    >
      {!src && getInitials(name)}
    </Avatar>
  );
}
