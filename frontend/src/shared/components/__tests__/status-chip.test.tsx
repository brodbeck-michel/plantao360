/**
 * StatusChip Test — Plantão 360
 *
 * Sprint: 12 — Frontend Architecture, Enterprise Foundation & Golden Frontend Platform
 */

import { render, screen } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import { StatusChip } from 'src/shared/components/status-chip';

describe('StatusChip', () => {
  it('renders active status', () => {
    render(<StatusChip status="active" />);
    expect(screen.getByText('Ativo')).toBeInTheDocument();
  });

  it('renders inactive status', () => {
    render(<StatusChip status="inactive" />);
    expect(screen.getByText('Inativo')).toBeInTheDocument();
  });

  it('renders pending status', () => {
    render(<StatusChip status="pending" />);
    expect(screen.getByText('Pendente')).toBeInTheDocument();
  });

  it('renders approved status', () => {
    render(<StatusChip status="approved" />);
    expect(screen.getByText('Aprovado')).toBeInTheDocument();
  });

  it('renders rejected status', () => {
    render(<StatusChip status="rejected" />);
    expect(screen.getByText('Rejeitado')).toBeInTheDocument();
  });

  it('renders completed status', () => {
    render(<StatusChip status="completed" />);
    expect(screen.getByText('Concluído')).toBeInTheDocument();
  });

  it('renders in-progress status', () => {
    render(<StatusChip status="in-progress" />);
    expect(screen.getByText('Em Progresso')).toBeInTheDocument();
  });

  it('renders custom label', () => {
    render(<StatusChip status="active" label="Custom Label" />);
    expect(screen.getByText('Custom Label')).toBeInTheDocument();
  });
});
