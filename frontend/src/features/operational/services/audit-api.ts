/**
 * Cliente da API de auditoria — acesso à trilha de alterações.
 * Consulta paginada com filtros (usuário, recurso, período, datas).
 */

import { api } from '@/api/client';

export interface AuditLog {
  id: number;
  occurred_at: string;
  user_id: number | null;
  user_label: string;
  user_role: string;
  origin: string;
  action: string;
  resource: string;
  resource_id: number | null;
  period_id: number | null;
  before: Record<string, any> | null;
  after: Record<string, any> | null;
  summary: string | null;
  correlation_id: string | null;
}

export interface AuditLogPage {
  data: AuditLog[];
  meta: {
    total: number;
  };
  success: boolean;
}

export interface AuditFilterParams {
  page?: number;
  size?: number;
  user_id?: number;
  resource?: string;
  resource_id?: number;
  period_id?: number;
  start_date?: string;
  end_date?: string;
}

/**
 * Consulta a trilha de auditoria com filtros e paginação.
 * Retorna logs ordenados por data (mais recentes primeiro).
 */
export async function fetchAuditLogs(
  filters?: AuditFilterParams,
): Promise<AuditLogPage> {
  const params = new URLSearchParams();

  if (filters?.page) params.set('page', filters.page.toString());
  if (filters?.size) params.set('size', filters.size.toString());
  if (filters?.user_id) params.set('user_id', filters.user_id.toString());
  if (filters?.resource) params.set('resource', filters.resource);
  if (filters?.resource_id) params.set('resource_id', filters.resource_id.toString());
  if (filters?.period_id) params.set('period_id', filters.period_id.toString());
  if (filters?.start_date) params.set('start_date', filters.start_date);
  if (filters?.end_date) params.set('end_date', filters.end_date);

  const queryString = params.toString();
  const url = queryString ? `/audit?${queryString}` : '/audit';

  const response = await api.get<AuditLogPage>(url);
  return response.data;
}

/**
 * Consulta a trilha de auditoria de uma competência específica.
 */
export async function fetchPeriodAuditLogs(
  periodId: number,
  page: number = 1,
  size: number = 20,
): Promise<AuditLogPage> {
  return fetchAuditLogs({
    period_id: periodId,
    page,
    size,
  });
}

/**
 * Formata um log de auditoria para exibição.
 */
export function formatAuditLog(log: AuditLog): {
  action: string;
  actionLabel: string;
  resource: string;
  target: string;
  author: string;
  date: string;
  time: string;
} {
  const date = new Date(log.occurred_at);
  const dateStr = date.toLocaleDateString('pt-BR');
  const timeStr = date.toLocaleTimeString('pt-BR');

  const actionLabels: Record<string, string> = {
    create: '➕ Criou',
    update: '✏️ Alterou',
    delete: '🗑️ Removeu',
  };

  const resourceLabels: Record<string, string> = {
    assignment: 'Plantão',
    shift_extra: 'Hora Extra',
    doctor: 'Médico',
    user: 'Usuário',
    period: 'Competência',
  };

  const target =
    log.after?.doctor_name ||
    log.after?.name ||
    log.before?.doctor_name ||
    log.before?.name ||
    `#${log.resource_id}`;

  return {
    action: log.action,
    actionLabel: actionLabels[log.action] || log.action,
    resource: resourceLabels[log.resource] || log.resource,
    target,
    author: log.user_label,
    date: dateStr,
    time: timeStr,
  };
}
