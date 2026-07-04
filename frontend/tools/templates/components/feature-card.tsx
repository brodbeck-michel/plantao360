/**
 * {{FEATURE_PASCAL}} Card — Plantão 360
 *
 * Card de resumo para {{FEATURE_NAME}}.
 * Generated from Golden Module (Doctor).
 */

import React from 'react';
import { Card, CardContent, Typography, Box, Chip } from '@mui/material';
import { useNavigate } from 'react-router-dom';
import { EntityAvatar } from '../../../shared/components/entity-avatar';
import type { {{FEATURE_PASCAL}} } from '../types/{{FEATURE_NAME}}-types';
import { ROUTES } from '../../../routes/routes';

interface {{FEATURE_PASCAL}}CardProps {
  {{FEATURE_NAME}}: {{FEATURE_PASCAL}};
}

export function {{FEATURE_PASCAL}}Card({ {{FEATURE_NAME}} }: {{FEATURE_PASCAL}}CardProps) {
  const navigate = useNavigate();

  return (
    <Card
      onClick={() => navigate(`${ROUTES.{{FEATURE_NAME.upper()}}}/${{FEATURE_NAME}.id}`)}
      sx={{ cursor: 'pointer', '&:hover': { boxShadow: 2 } }}
    >
      <CardContent>
        <Box display="flex" alignItems="center" gap={2}>
          <EntityAvatar name={${FEATURE_NAME}.name} size="large" />
          <Box flex={1}>
            <Typography variant="h6" fontWeight={600}>
              {${FEATURE_NAME}.name}
            </Typography>
          </Box>
          <Chip
            label={${FEATURE_NAME}.active ? 'Ativo' : 'Inativo'}
            color={${FEATURE_NAME}.active ? 'success' : 'default'}
            size="small"
          />
        </Box>
      </CardContent>
    </Card>
  );
}
