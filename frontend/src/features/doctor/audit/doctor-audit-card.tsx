/**
 * DoctorAuditCard — Plantão 360
 *
 * Card de auditoria do médico.
 * Golden Frontend Module — referência oficial.
 *
 * Sprint: 13 — Golden Frontend Module
 */

import React from 'react';
import { Paper, Typography, Box, Grid, Divider } from '@mui/material';

// ============================================================
// Types
// ============================================================

interface AuditEntry {
  id: string;
  field: string;
  old_value: string | null;
  new_value: string | null;
  changed_by: string;
  changed_at: string;
}

interface DoctorAuditCardProps {
  entries: AuditEntry[];
}

// ============================================================
// Component
// ============================================================

export function DoctorAuditCard({ entries }: DoctorAuditCardProps) {
  return (
    <Paper variant="outlined" sx={{ p: 3 }}>
      <Box display="flex" alignItems="center" gap={1} mb={2}>
        <Typography variant="h6" fontWeight={600}>
          Auditoria
        </Typography>
        <Typography variant="body2" color="text.secondary">
          ({entries.length} registros)
        </Typography>
      </Box>
      {entries.length === 0 ? (
        <Typography variant="body2" color="text.secondary" textAlign="center" py={4}>
          Nenhum registro de auditoria
        </Typography>
      ) : (
        entries.map((entry, index) => (
          <React.Fragment key={entry.id}>
            <Box py={1.5}>
              <Grid container alignItems="center" spacing={2}>
                <Grid item xs={12} sm={3}>
                  <Typography variant="body2" fontWeight={500}>
                    {entry.field}
                  </Typography>
                </Grid>
                <Grid item xs={12} sm={4}>
                  <Typography variant="body2" color="text.secondary">
                    De: <strong>{entry.old_value || '(vazio)'}</strong>
                  </Typography>
                </Grid>
                <Grid item xs={12} sm={4}>
                  <Typography variant="body2" color="text.secondary">
                    Para: <strong>{entry.new_value || '(vazio)'}</strong>
                  </Typography>
                </Grid>
                <Grid item xs={12} sm={1}>
                  <Typography variant="caption" color="text.secondary">
                    {new Date(entry.changed_at).toLocaleDateString('pt-BR')}
                  </Typography>
                </Grid>
              </Grid>
            </Box>
            {index < entries.length - 1 && <Divider />}
          </React.Fragment>
        ))
      )}
    </Paper>
  );
}
