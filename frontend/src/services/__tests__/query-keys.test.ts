/**
 * Query Factory Test — Plantão 360
 *
 * Sprint: 12 — Frontend Architecture, Enterprise Foundation & Golden Frontend Platform
 */

import { describe, it, expect, vi, beforeEach } from 'vitest';
import { queryKeys } from 'src/services/query-keys';

describe('Query Keys', () => {
  describe('doctors', () => {
    it('creates list key with no params', () => {
      const key = queryKeys.doctors.list({});
      expect(key).toEqual(['doctors', 'list', {}]);
    });

    it('creates list key with params', () => {
      const key = queryKeys.doctors.list({ name: 'João', active: true });
      expect(key).toEqual(['doctors', 'list', { name: 'João', active: true }]);
    });

    it('creates detail key', () => {
      const key = queryKeys.doctors.detail('123');
      expect(key).toEqual(['doctors', 'detail', '123']);
    });
  });

  describe('periods', () => {
    it('creates list key with no params', () => {
      const key = queryKeys.periods.list({});
      expect(key).toEqual(['periods', 'list', {}]);
    });

    it('creates detail key', () => {
      const key = queryKeys.periods.detail('123');
      expect(key).toEqual(['periods', 'detail', '123']);
    });
  });

  describe('shifts', () => {
    it('creates list key with no params', () => {
      const key = queryKeys.shifts.list({});
      expect(key).toEqual(['shifts', 'list', {}]);
    });

    it('creates detail key', () => {
      const key = queryKeys.shifts.detail('123');
      expect(key).toEqual(['shifts', 'detail', '123']);
    });
  });

  describe('assignments', () => {
    it('creates list key with no params', () => {
      const key = queryKeys.assignments.list({});
      expect(key).toEqual(['assignments', 'list', {}]);
    });

    it('creates detail key', () => {
      const key = queryKeys.assignments.detail('123');
      expect(key).toEqual(['assignments', 'detail', '123']);
    });
  });

  describe('kpis', () => {
    it('creates list key', () => {
      const key = queryKeys.kpis.list();
      expect(key).toEqual(['kpis', 'list']);
    });
  });

  describe('explainability', () => {
    it('creates entity key', () => {
      const key = queryKeys.explainability.entity('shift', '123');
      expect(key).toEqual(['explainability', 'shift', '123']);
    });
  });
});
