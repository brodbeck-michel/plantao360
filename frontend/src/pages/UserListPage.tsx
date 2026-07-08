import React, { useState, useEffect } from 'react';
import {
  Box, Typography, Table, TableBody, TableCell, TableContainer, TableHead, TableRow,
  Paper, IconButton, Chip, Button, Dialog, DialogTitle, DialogContent, DialogActions,
  TextField, MenuItem, Alert, Tooltip,
} from '@mui/material';
import { Add, Edit, Delete, LockReset, CheckCircle, Block } from '@mui/icons-material';
import { usersApi, type User } from '../api/users';
import { tokens } from '../theme';
import { useAuth } from '../contexts/AuthContext';
import { canEdit } from '../rbac';

const ROLE_LABELS: Record<string, string> = {
  ADMIN: 'Administrador',
  COORDENADOR: 'Coordenador',
  FINANCEIRO: 'Financeiro',
  MEDICO: 'Medico',
  CONSULTA: 'Consulta',
};

const ROLE_COLORS: Record<string, string> = {
  ADMIN: tokens.colors.primary.main,
  COORDENADOR: tokens.colors.operational.attention,
  FINANCEIRO: tokens.colors.success.main,
  MEDICO: tokens.colors.info.main,
  CONSULTA: tokens.colors.text.muted,
};

interface FormData {
  name: string;
  email: string;
  password: string;
  role: string;
}

const INITIAL_FORM: FormData = { name: '', email: '', password: '', role: 'CONSULTA' };

export default function UserListPage() {
  const { user } = useAuth();
  const canModify = canEdit(user?.role, 'usuarios');
  const [users, setUsers] = useState<User[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [dialogOpen, setDialogOpen] = useState(false);
  const [passwordDialogOpen, setPasswordDialogOpen] = useState(false);
  const [editingUser, setEditingUser] = useState<User | null>(null);
  const [passwordUserId, setPasswordUserId] = useState<number | null>(null);
  const [form, setForm] = useState<FormData>(INITIAL_FORM);
  const [newPassword, setNewPassword] = useState('');
  const [saving, setSaving] = useState(false);

  const loadUsers = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await usersApi.list();
      setUsers(data);
    } catch {
      setError('Erro ao carregar usuarios');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { loadUsers(); }, []);

  const handleOpenCreate = () => {
    setEditingUser(null);
    setForm(INITIAL_FORM);
    setDialogOpen(true);
  };

  const handleOpenEdit = (user: User) => {
    setEditingUser(user);
    setForm({ name: user.name, email: user.email, password: '', role: user.role });
    setDialogOpen(true);
  };

  const handleOpenPassword = (userId: number) => {
    setPasswordUserId(userId);
    setNewPassword('');
    setPasswordDialogOpen(true);
  };

  const handleSave = async () => {
    setSaving(true);
    try {
      if (editingUser) {
        const updateData: Record<string, unknown> = { name: form.name, email: form.email, role: form.role };
        await usersApi.update(editingUser.id, updateData);
      } else {
        await usersApi.create(form);
      }
      setDialogOpen(false);
      await loadUsers();
    } catch {
      setError('Erro ao salvar usuario');
    } finally {
      setSaving(false);
    }
  };

  const handlePasswordChange = async () => {
    if (!passwordUserId || !newPassword) return;
    setSaving(true);
    try {
      await usersApi.changePassword(passwordUserId, newPassword);
      setPasswordDialogOpen(false);
    } catch {
      setError('Erro ao alterar senha');
    } finally {
      setSaving(false);
    }
  };

  const handleToggleActive = async (user: User) => {
    try {
      if (user.active) {
        await usersApi.deactivate(user.id);
      } else {
        await usersApi.activate(user.id);
      }
      await loadUsers();
    } catch {
      setError('Erro ao alterar status do usuario');
    }
  };

  return (
    <Box>
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
        <Typography variant="h5" fontWeight={700}>Usuarios</Typography>
        {canModify && (
          <Button variant="contained" startIcon={<Add />} onClick={handleOpenCreate}>
            Novo Usuario
          </Button>
        )}
      </Box>

      {error && <Alert severity="error" sx={{ mb: 2 }} onClose={() => setError(null)}>{error}</Alert>}

      <TableContainer component={Paper} sx={{ borderRadius: tokens.borderRadius.lg }}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell sx={{ fontWeight: 600 }}>Nome</TableCell>
              <TableCell sx={{ fontWeight: 600 }}>Email</TableCell>
              <TableCell sx={{ fontWeight: 600 }}>Perfil</TableCell>
              <TableCell sx={{ fontWeight: 600 }}>Status</TableCell>
              <TableCell sx={{ fontWeight: 600 }}>Ultimo Login</TableCell>
              <TableCell sx={{ fontWeight: 600 }} align="right">Acoes</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {users.map((user) => (
              <TableRow key={user.id} hover>
                <TableCell>{user.name}</TableCell>
                <TableCell>{user.email}</TableCell>
                <TableCell>
                  <Chip
                    label={ROLE_LABELS[user.role] || user.role}
                    size="small"
                    sx={{ bgcolor: (ROLE_COLORS[user.role] || tokens.colors.text.muted) + '18', color: ROLE_COLORS[user.role] || tokens.colors.text.muted, fontWeight: 600 }}
                  />
                </TableCell>
                <TableCell>
                  <Chip
                    icon={user.active ? <CheckCircle sx={{ fontSize: 14 }} /> : <Block sx={{ fontSize: 14 }} />}
                    label={user.active ? 'Ativo' : 'Inativo'}
                    size="small"
                    sx={{ bgcolor: user.active ? tokens.colors.operational.healthy + '18' : tokens.colors.operational.critical + '18', color: user.active ? tokens.colors.operational.healthy : tokens.colors.operational.critical, fontWeight: 600 }}
                  />
                </TableCell>
                <TableCell>
                  {user.last_login
                    ? new Date(user.last_login).toLocaleDateString('pt-BR')
                    : '-'}
                </TableCell>
                <TableCell align="right">
                  {canModify && (
                    <>
                      <Tooltip title="Editar">
                        <IconButton size="small" onClick={() => handleOpenEdit(user)}>
                          <Edit fontSize="small" />
                        </IconButton>
                      </Tooltip>
                      <Tooltip title="Alterar senha">
                        <IconButton size="small" onClick={() => handleOpenPassword(user.id)}>
                          <LockReset fontSize="small" />
                        </IconButton>
                      </Tooltip>
                      <Tooltip title={user.active ? 'Desativar' : 'Ativar'}>
                        <IconButton size="small" onClick={() => handleToggleActive(user)} sx={{ color: user.active ? tokens.colors.operational.critical : tokens.colors.operational.healthy }}>
                          {user.active ? <Block fontSize="small" /> : <CheckCircle fontSize="small" />}
                        </IconButton>
                      </Tooltip>
                    </>
                  )}
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>

      <Dialog open={dialogOpen} onClose={() => setDialogOpen(false)} maxWidth="sm" fullWidth>
        <DialogTitle>{editingUser ? 'Editar Usuario' : 'Novo Usuario'}</DialogTitle>
        <DialogContent sx={{ display: 'flex', flexDirection: 'column', gap: 2, pt: '16px !important' }}>
          <TextField label="Nome" value={form.name} onChange={(e) => setForm({ ...form, name: e.target.value })} fullWidth />
          <TextField label="Email" value={form.email} onChange={(e) => setForm({ ...form, email: e.target.value })} fullWidth type="email" />
          {!editingUser && (
            <TextField label="Senha" value={form.password} onChange={(e) => setForm({ ...form, password: e.target.value })} fullWidth type="password" />
          )}
          <TextField label="Perfil" value={form.role} onChange={(e) => setForm({ ...form, role: e.target.value })} select fullWidth>
            <MenuItem value="ADMIN">Administrador</MenuItem>
            <MenuItem value="COORDENADOR">Coordenador</MenuItem>
            <MenuItem value="FINANCEIRO">Financeiro</MenuItem>
            <MenuItem value="MEDICO">Medico</MenuItem>
            <MenuItem value="CONSULTA">Consulta</MenuItem>
          </TextField>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setDialogOpen(false)}>Cancelar</Button>
          <Button onClick={handleSave} variant="contained" disabled={saving}>
            {saving ? 'Salvando...' : 'Salvar'}
          </Button>
        </DialogActions>
      </Dialog>

      <Dialog open={passwordDialogOpen} onClose={() => setPasswordDialogOpen(false)} maxWidth="sm" fullWidth>
        <DialogTitle>Alterar Senha</DialogTitle>
        <DialogContent sx={{ pt: '16px !important' }}>
          <TextField
            label="Nova Senha"
            value={newPassword}
            onChange={(e) => setNewPassword(e.target.value)}
            fullWidth
            type="password"
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setPasswordDialogOpen(false)}>Cancelar</Button>
          <Button onClick={handlePasswordChange} variant="contained" disabled={saving || !newPassword}>
            {saving ? 'Salvando...' : 'Alterar Senha'}
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
}
