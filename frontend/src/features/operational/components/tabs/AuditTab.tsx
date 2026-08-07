/**
 * Aba de histórico de auditoria no workspace.
 * Exibe a trilha de alterações da competência.
 * Visível apenas para ADMIN e COORDENADOR.
 */

import { useState, useEffect } from 'react';
import {
  fetchPeriodAuditLogs,
  formatAuditLog,
  AuditLog,
} from '@/features/operational/services/audit-api';

interface AuditTabProps {
  periodId: number;
}

export function AuditTab({ periodId }: AuditTabProps) {
  const [logs, setLogs] = useState<AuditLog[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [page, setPage] = useState(1);
  const [total, setTotal] = useState(0);

  const pageSize = 20;

  useEffect(() => {
    const loadAuditLogs = async () => {
      setLoading(true);
      setError(null);
      try {
        const response = await fetchPeriodAuditLogs(periodId, page, pageSize);
        setLogs(response.data);
        setTotal(response.meta.total);
      } catch (err) {
        setError('Erro ao carregar histórico de auditoria');
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    loadAuditLogs();
  }, [periodId, page]);

  if (loading && logs.length === 0) {
    return (
      <div className="flex items-center justify-center h-64">
        <p className="text-gray-500">Carregando histórico...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex items-center justify-center h-64">
        <p className="text-red-500">{error}</p>
      </div>
    );
  }

  if (logs.length === 0) {
    return (
      <div className="flex flex-col items-center justify-center h-64 text-gray-500">
        <p className="text-lg mb-2">📋 Nenhum histórico registrado</p>
        <p className="text-sm">
          A trilha de auditoria começa a registrar alterações a partir do deploy desta
          feature.
        </p>
      </div>
    );
  }

  const totalPages = Math.ceil(total / pageSize);

  return (
    <div className="p-4">
      <div className="space-y-3">
        {logs.map((log) => {
          const formatted = formatAuditLog(log);
          return (
            <div
              key={log.id}
              className="border rounded-lg p-3 bg-white hover:shadow-sm transition-shadow"
            >
              <div className="flex items-start justify-between">
                <div className="flex-1">
                  <div className="flex items-center gap-2 mb-1">
                    <span className="font-medium text-gray-900">
                      {formatted.actionLabel} {formatted.resource}
                    </span>
                    <span className="text-sm text-gray-600">
                      por {formatted.author}
                    </span>
                  </div>
                  <div className="text-sm text-gray-700">
                    <strong>{formatted.target}</strong>
                  </div>
                  {log.summary && (
                    <div className="text-sm text-gray-600 mt-1">{log.summary}</div>
                  )}
                  <div className="flex gap-4 mt-2 text-xs text-gray-500">
                    <span>📅 {formatted.date}</span>
                    <span>🕐 {formatted.time}</span>
                  </div>
                </div>
              </div>
            </div>
          );
        })}
      </div>

      {totalPages > 1 && (
        <div className="flex justify-center gap-2 mt-6">
          <button
            onClick={() => setPage((p) => Math.max(1, p - 1))}
            disabled={page === 1}
            className="px-3 py-1 text-sm border rounded disabled:opacity-50"
          >
            ← Anterior
          </button>
          <span className="px-3 py-1 text-sm text-gray-600">
            Página {page} de {totalPages}
          </span>
          <button
            onClick={() => setPage((p) => Math.min(totalPages, p + 1))}
            disabled={page === totalPages}
            className="px-3 py-1 text-sm border rounded disabled:opacity-50"
          >
            Próxima →
          </button>
        </div>
      )}
    </div>
  );
}
