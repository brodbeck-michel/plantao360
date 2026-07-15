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
  const [formError, setFormError] = useState<string | null>(null);
  const [newPassword, setNewPassword] = useState('');
  const [passwordError, setPasswordError] = useState<string | null>(null);
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
    setFormError(null);
    setDialogOpen(true);
  };

  const handleOpenEdit = (user: User) => {
    setEditingUser(user);
    setForm({ name: user.name, email: user.email, password: '', role: user.role });
    setFormError(null);
    setDialogOpen(true);
  };

  const handleOpenPassword = (userId: number) => {
    setPasswordUserId(userId);
    setNewPassword('');
    setPasswordError(null);
    setPasswordDialogOpen(true);
  };

  const handleSave = async () => {
    // Validação no cliente — evita o erro genérico do servidor e orienta o usuário.
    const name = form.name.trim();
    const email = form.email.trim();
    if (!name || !email) {
      setFormError('Preencha nome e email.');
      return;
    }
    if (!editingUser && form.password.length < 6) {
      setFormError('A senha deve ter ao menos 6 caracteres.');
      return;
    }
    setFormError(null);
    setSaving(true);
    try {
      if (editingUser) {
        const updateData: Record<string, unknown> = { name, email, role: form.role };
        await usersApi.update(editingUser.id, updateData);
      } else {
        await usersApi.create({ ...form, name, email });
      }
      setDialogOpen(false);
      await loadUsers();
    } catch (err) {
      // O apiClient (mapError) já traduz o erro; mostramos a mensagem real, não uma genérica.
      setFormError((err as { message?: string })?.message || 'Erro ao salvar usuário.');
    } finally {
      setSaving(false);
    }
  };

  const handlePasswordChange = async () => {
    if (!passwordUserId || !newPassword) return;
    // Validação no cliente + erro dentro do dialog (mesmo padrão do B-01).
    if (newPassword.length < 6) {
      setPasswordError('A senha deve ter ao menos 6 caracteres.');
      return;
    }
    setPasswordError(null);
    setSaving(true);
    try {
      await usersApi.changePassword(passwordUserId, newPassword);
      setPasswordDialogOpen(false);
    } catch (err) {
      setPasswordError((err as { message?: string })?.message || 'Erro ao alterar senha.');
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
          {formError && <Alert severity="error" onClose={() => setFormError(null)}>{formError}</Alert>}
          <TextField label="Nome" value={form.name} onChange={(e) => setForm({ ...form, name: e.target.value })} fullWidth required />
          <TextField label="Email" value={form.email} onChange={(e) => setForm({ ...form, email: e.target.value })} fullWidth type="email" required />
          {!editingUser && (
            <TextField label="Senha" value={form.password} onChange={(e) => setForm({ ...form, password: e.target.value })} fullWidth type="password" required helperText="Mínimo 6 caracteres" />
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
        <DialogContent sx={{ display: 'flex', flexDirection: 'column', gap: 2, pt: '16px !important' }}>
          {passwordError && <Alert severity="error" onClose={() => setPasswordError(null)}>{passwordError}</Alert>}
          <TextField
            label="Nova Senha"
            value={newPassword}
            onChange={(e) => setNewPassword(e.target.value)}
            fullWidth
            type="password"
            required
            helperText="Mínimo 6 caracteres"
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
