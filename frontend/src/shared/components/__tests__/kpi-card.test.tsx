/**
 * KPICard Test — Plantão 360
 *
 * Sprint: 12 — Frontend Architecture, Enterprise Foundation & Golden Frontend Platform
 */

import { render, screen } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import { KPICard } from 'src/shared/components/kpi-card';

describe('KPICard', () => {
  it('renders title and value', () => {
    render(<KPICard title="Taxa de Cobertura" value={85} />);
    expect(screen.getByText('Taxa de Cobertura')).toBeInTheDocument();
    expect(screen.getByText('85%')).toBeInTheDocument();
  });

  it('renders trend indicator', () => {
    render(<KPICard title="Taxa de Cobertura" value={85} trend="up" />);
    expect(screen.getByText('↑')).toBeInTheDocument();
  });

  it('renders down trend', () => {
    render(<KPICard title="Taxa de Cobertura" value={85} trend="down" />);
    expect(screen.getByText('↓')).toBeInTheDocument();
  });

  it('renders neutral trend', () => {
    render(<KPICard title="Taxa de Cobertura" value={85} trend="neutral" />);
    expect(screen.getByText('→')).toBeInTheDocument();
  });

  it('renders target when provided', () => {
    render(<KPICard title="Taxa de Cobertura" value={85} target={90} />);
    expect(screen.getByText('/ 90%')).toBeInTheDocument();
  });

  it('renders description when provided', () => {
    render(
      <KPICard
        title="Taxa de Cobertura"
        value={85}
        description="Meta: 90%"
      />
    );
    expect(screen.getByText('Meta: 90%')).toBeInTheDocument();
  });
});
