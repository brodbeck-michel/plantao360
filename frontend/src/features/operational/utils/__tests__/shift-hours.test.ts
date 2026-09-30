import { describe, it, expect } from 'vitest';
import { shiftHours, compareDoctorName } from '../shift-hours';

describe('shiftHours', () => {
  it('conta turno quebrado pela hora cheia', () => {
    expect(shiftHours('13:00', '18:59')).toBe(6);
    expect(shiftHours('08:00', '13:59')).toBe(6);
  });

  it('mantem turno que ja e cheio', () => {
    expect(shiftHours('07:00', '19:00')).toBe(12);
    expect(shiftHours('20:00', '23:00')).toBe(3);
  });

  it('turno que vira a meia-noite', () => {
    expect(shiftHours('19:00', '06:59')).toBe(12);
    expect(shiftHours('07:00', '07:00')).toBe(24);
  });

  it('24 plantoes de 6h somam horas inteiras', () => {
    const total = Array.from({ length: 24 }, () => shiftHours('13:00', '18:59')).reduce((s, h) => s + h, 0);
    expect(total).toBe(144);
  });

  it('horario invalido vale 0', () => {
    expect(shiftHours('', '')).toBe(0);
  });
});

describe('compareDoctorName', () => {
  it('ordena alfabetico ignorando acento e caixa', () => {
    const names = ['José Nixon', 'andre Felipe', 'Ana Beatriz', 'Élida'].map((name) => ({ name }));
    expect(names.sort(compareDoctorName).map((d) => d.name)).toEqual(['Ana Beatriz', 'andre Felipe', 'Élida', 'José Nixon']);
  });
});
