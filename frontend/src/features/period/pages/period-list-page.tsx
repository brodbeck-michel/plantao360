import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Container, Typography, Box, Button, Paper, IconButton, Tooltip, Chip,
  Dialog, DialogTitle, DialogContent, DialogActions,
} from '@mui/material';
import {
  Add as AddIcon, Edit as EditIcon, Delete as DeleteIcon,
  OpenInNew as OpenIcon, ContentCopy as DuplicateIcon,
  Lock as CloseIcon, LockOpen as ReopenIcon,
} from '@mui/icons-material';
import { DataTable, Column } from '../../../shared/components/data-table';
import { StatusChip } from '../../../shared/components/status-chip';
import { useErrorExperience } from '../../../shared/hooks/use-error-experience';
import { PeriodDialog } from '../dialogs/period-dialog';
import {
  usePeriodList, useDeletePeriod, useClosePeriod,
  useReopenPeriod, useDuplicatePeriod,
} from '../hooks/use-periods';
import { MONTH_NAMES, STATUS_LABELS } from '../types/period-types';
import type { PeriodData } from '../types/period-types';

export function PeriodListPage() {
  const navigate = useNavigate();
  const { showError, showSuccess } = useErrorExperience();
  const [dialogOpen, setDialogOpen] = useState(false);
  const [dialogMode, setDialogMode] = useState<'create' | 'edit'>('create');
  const [editingPeriod, setEditingPeriod] = useState<PeriodData | undefined>();
  const [deleteConfirm, setDeleteConfirm] = useState<PeriodData | null>(null);
  const [closeConfirm, setCloseConfirm] = useState<PeriodData | null>(null);
  const [reopenConfirm, setReopenConfirm] = useState<PeriodData | null>(null);

  const { data, isLoading } = usePeriodList({ page: 1, size: 100, sort_by: 'year', sort_direction: 'desc' });
  const deleteMutation = useDeletePeriod();
  const closeMutation = useClosePeriod();
  const reopenMutation = useReopenPeriod();
  const duplicateMutation = useDuplicatePeriod();

  const periods: PeriodData[] = Array.isArray(data) ? data : (data?.items || data?.data || []);

  const handleDelete = async () => {
    if (!deleteConfirm) return;
    try {
      await deleteMutation.mutateAsync(deleteConfirm.id);
      showSuccess('Competencia excluida com sucesso');
      setDeleteConfirm(null);
    } catch (error) {
      showError(error);
    }
  };

  const handleClose = async () => {
    if (!closeConfirm) return;
    try {
      await closeMutation.mutateAsync(closeConfirm.id);
      showSuccess('Competencia fechada com sucesso');
      setCloseConfirm(null);
    } catch (error) {
      showError(error);
    }
  };

  const handleReopen = async () => {
    if (!reopenConfirm) return;
    try {
      await reopenMutation.mutateAsync(reopenConfirm.id);
      showSuccess('Competencia reaberta com sucesso');
      setReopenConfirm(null);
    } catch (error) {
      showError(error);
    }
  };

  const handleDuplicate = async (period: PeriodData) => {
    try {
      await duplicateMutation.mutateAsync(period.id);
      showSuccess('Competencia duplicada com sucesso');
    } catch (error) {
      showError(error);
    }
  };

  const columns: Column<PeriodData>[] = [
    {
      id: 'year',
      label: 'Ano',
      sortable: true,
      render: (row) => <Typography fontWeight={600}>{row.year}</Typography>,
    },
    {
      id: 'month',
      label: 'Mes',
      sortable: true,
      render: (row) => MONTH_NAMES[row.month - 1] || row.month,
    },
    {
      id: 'status',
      label: 'Status',
      sortable: true,
      render: (row) => <StatusChip status={row.status as any} />,
    },
    {
      id: 'created_at',
      label: 'Criado em',
      render: (row) => new Date(row.created_at).toLocaleDateString('pt-BR'),
    },
    {
      id: 'actions',
      label: 'Acoes',
      width: 200,
      render: (row) => (
        <Box display="flex" gap={0.5}>
          <Tooltip title="Abrir competencia">
            <IconButton size="small" onClick={() => navigate(`/app/periods/${row.id}`)}>
              <OpenIcon fontSize="small" />
            </IconButton>
          </Tooltip>
          <Tooltip title="Editar">
            <IconButton size="small" onClick={() => { setEditingPeriod(row); setDialogMode('edit'); setDialogOpen(true); }}>
              <EditIcon fontSize="small" />
            </IconButton>
          </Tooltip>
          {row.status === 'draft' && (
            <>
              <Tooltip title="Fechar">
                <IconButton size="small" onClick={() => setCloseConfirm(row)}>
                  <CloseIcon fontSize="small" />
                </IconButton>
              </Tooltip>
              <Tooltip title="Duplicar">
                <IconButton size="small" onClick={() => handleDuplicate(row)}>
                  <DuplicateIcon fontSize="small" />
                </IconButton>
              </Tooltip>
              <Tooltip title="Excluir">
                <IconButton size="small" onClick={() => setDeleteConfirm(row)}>
                  <DeleteIcon fontSize="small" />
                </IconButton>
              </Tooltip>
            </>
          )}
          {row.status === 'closed' && (
            <Tooltip title="Reabrir">
              <IconButton size="small" onClick={() => setReopenConfirm(row)}>
                <ReopenIcon fontSize="small" />
              </IconButton>
            </Tooltip>
          )}
        </Box>
      ),
    },
  ];

  return (
    <Container maxWidth="lg">
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
        <Typography variant="h4" fontWeight={600}>
          Competencias
        </Typography>
        <Button
          variant="contained"
          startIcon={<AddIcon />}
          onClick={() => { setEditingPeriod(undefined); setDialogMode('create'); setDialogOpen(true); }}
        >
          Nova Competencia
        </Button>
      </Box>

      <DataTable
        columns={columns}
        data={periods as any}
        total={periods.length}
        loading={isLoading}
        sortBy="year"
        sortOrder="desc"
        emptyMessage="Nenhuma competencia encontrada"
      />

      <PeriodDialog
        open={dialogOpen}
        onClose={() => { setDialogOpen(false); setEditingPeriod(undefined); }}
        mode={dialogMode}
        initialData={editingPeriod ? { id: editingPeriod.id, year: editingPeriod.year, month: editingPeriod.month } : undefined}
      />

      <Dialog open={!!deleteConfirm} onClose={() => setDeleteConfirm(null)}>
        <DialogTitle>Excluir Competencia?</DialogTitle>
        <DialogContent>
          <Typography>Tem certeza que deseja excluir a competencia {deleteConfirm && MONTH_NAMES[deleteConfirm.month - 1]} {deleteConfirm?.year}?</Typography>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setDeleteConfirm(null)}>Cancelar</Button>
          <Button onClick={handleDelete} color="error" variant="contained">Excluir</Button>
        </DialogActions>
      </Dialog>

      <Dialog open={!!closeConfirm} onClose={() => setCloseConfirm(null)}>
        <DialogTitle>Fechar Competencia?</DialogTitle>
        <DialogContent>
          <Typography>Fechar a competencia {closeConfirm && MONTH_NAMES[closeConfirm.month - 1]} {closeConfirm?.year}? Esta acao bloqueara edicoes.</Typography>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setCloseConfirm(null)}>Cancelar</Button>
          <Button onClick={handleClose} color="warning" variant="contained">Fechar</Button>
        </DialogActions>
      </Dialog>

      <Dialog open={!!reopenConfirm} onClose={() => setReopenConfirm(null)}>
        <DialogTitle>Reabrir Competencia?</DialogTitle>
        <DialogContent>
          <Typography>Reabrir a competencia {reopenConfirm && MONTH_NAMES[reopenConfirm.month - 1]} {reopenConfirm?.year}? Permitira edicoes novamente.</Typography>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setReopenConfirm(null)}>Cancelar</Button>
          <Button onClick={handleReopen} color="primary" variant="contained">Reabrir</Button>
        </DialogActions>
      </Dialog>
    </Container>
  );
}
