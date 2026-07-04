#!/usr/bin/env python3
"""
Feature Generator — Plantão 360

Gera automaticamente uma nova feature completa a partir do Golden Module.

Uso:
    python feature_generator.py <FeatureName> [--owner <owner>] [--golden]

Exemplo:
    python feature_generator.py Period
    python feature_generator.py Coverage --owner "Time A"
"""

import os
import sys
import json
import shutil
from pathlib import Path
from datetime import datetime

# ============================================================
# Constants
# ============================================================

FRONTEND_ROOT = Path(__file__).parent.parent
FEATURES_DIR = FRONTEND_ROOT / "src" / "features"
SHARED_DIR = FRONTEND_ROOT / "src" / "shared"
TEMPLATES_DIR = Path(__file__).parent / "templates"
GOLDEN_MODULE = "doctor"

# ============================================================
# Feature Structure
# ============================================================

FEATURE_DIRECTORIES = [
    "api",
    "components",
    "dialogs",
    "details",
    "filters",
    "forms",
    "hooks",
    "history",
    "audit",
    "pages",
    "services",
    "tables",
    "types",
    "utils",
    "manifest",
    "tests",
]

# ============================================================
# Template Generators
# ============================================================

def generate_types(feature_name: str, feature_pascal: str) -> str:
    return f'''/**
 * {feature_pascal} Types — Plantão 360
 *
 * Tipos específicos do módulo de {feature_pascal}.
 * Generated from Golden Module (Doctor).
 *
 * Sprint: 13.5 — Frontend Platform Governance
 */

import type {{ {feature_pascal}, {feature_pascal}Summary, AuditEntry }} from '../../../types';

// ============================================================
// Re-exports
// ============================================================

export type {{ {feature_pascal}, {feature_pascal}Summary, AuditEntry }};

// ============================================================
// Feature-specific Types
// ============================================================

export interface {feature_pascal}Filters {{
  name?: string;
  active?: boolean;
}}

export interface {feature_pascal}ListSort {{
  field: 'name' | 'created_at';
  direction: 'asc' | 'desc';
}}

// ============================================================
// Page State Types
// ============================================================

export interface {feature_pascal}ListState {{
  filters: {feature_pascal}Filters;
  sort: {feature_pascal}ListSort;
  page: number;
  pageSize: number;
}}

export interface {feature_pascal}FormState {{
  name: string;
}}
'''


def generate_api(feature_name: str, feature_pascal: str, feature_camel: str) -> str:
    return f'''/**
 * {feature_pascal} API Service — Plantão 360
 *
 * Serviço de API para o módulo de {feature_pascal}.
 * Generated from Golden Module (Doctor).
 *
 * Sprint: 13.5 — Frontend Platform Governance
 */

import {{ apiClient }} from '../../../api/client';
import {{ queryKeys }} from '../../../services/query-keys';
import {{ createQuery, createMutation, createPaginatedQuery }} from '../../../services/query-factory';
import type {{ {feature_pascal}, {feature_pascal}Summary }} from '../../../types';
import type {{ UseQueryOptions }} from '@tanstack/react-query';
import type {{ AppError }} from '../../../api/client';

// ============================================================
// Types
// ============================================================

export interface {feature_pascal}ListParams {{
  page?: number;
  page_size?: number;
  name?: string;
  active?: boolean;
}}

export interface Create{feature_pascal}Data {{
  name: string;
}}

export interface Update{feature_pascal}Data {{
  id: string;
  name?: string;
  active?: boolean;
}}

// ============================================================
// Queries
// ============================================================

export const {feature_camel}Queries = {{
  list: (params?: {feature_pascal}ListParams) =>
    createPaginatedQuery<{feature_pascal}>(
      queryKeys.{feature_name}.list(params || {{}}),
      '/{feature_name}',
      params
    ),

  detail: (id: string, options?: Omit<UseQueryOptions<{feature_pascal}, AppError>, 'queryKey' | 'queryFn'>) =>
    createQuery<{feature_pascal}>(
      queryKeys.{feature_name}.detail(id),
      '/{feature_name}/' + id,
      options
    ),

  summary: (id: string) =>
    createQuery<{feature_pascal}Summary>(
      [...queryKeys.{feature_name}.detail(id), 'summary'],
      '/query/{feature_name}?{feature_name}_id=' + id
    ),
}};

// ============================================================
// Mutations
// ============================================================

export const {feature_camel}Mutations = {{
  create: () =>
    createMutation<{feature_pascal}, Create{feature_pascal}Data>('/{feature_name}', 'POST'),

  update: () =>
    createMutation<{feature_pascal}, Omit<Update{feature_pascal}Data, 'id'>>(
      '/{feature_name}',
      'PUT'
    ),

  delete: () =>
    createMutation<void, string>('/{feature_name}', 'DELETE'),
}};
'''


def generate_hooks(feature_name: str, feature_pascal: str, feature_camel: str) -> str:
    return f'''/**
 * use{feature_pascal}s — Plantão 360
 *
 * Hooks para gerenciar {feature_name}.
 * Generated from Golden Module (Doctor).
 *
 * Sprint: 13.5 — Frontend Platform Governance
 */

import {{ useState, useCallback }} from 'react';
import {{ useQuery, useMutation, useQueryClient }} from '@tanstack/react-query';
import {{ {feature_camel}Queries, {feature_camel}Mutations }} from '../services/{feature_name}-api';
import {{ queryKeys }} from '../../../services/query-keys';
import type {{ {feature_pascal}ListParams }} from '../services/{feature_name}-api';
import type {{ {feature_pascal}Filters, {feature_pascal}ListSort }} from '../types/{feature_name}-types';

// ============================================================
// Query Hooks
// ============================================================

export function use{feature_pascal}sList(params?: {feature_pascal}ListParams) {{
  return useQuery({feature_camel}Queries.list(params));
}}

export function use{feature_pascal}Detail(id: string) {{
  return useQuery({feature_camel}Queries.detail(id));
}}

export function use{feature_pascal}Summary(id: string) {{
  return useQuery({feature_camel}Queries.summary(id));
}}

// ============================================================
// Mutation Hooks
// ============================================================

export function useCreate{feature_pascal}() {{
  const queryClient = useQueryClient();

  return useMutation({{
    ...{feature_camel}Mutations.create(),
    onSuccess: () => {{
      queryClient.invalidateQueries({{ queryKey: queryKeys.{feature_name}.all }});
    }},
  }});
}}

export function useUpdate{feature_pascal}() {{
  const queryClient = useQueryClient();

  return useMutation({{
    ...{feature_camel}Mutations.update(),
    onSuccess: (data) => {{
      queryClient.invalidateQueries({{ queryKey: queryKeys.{feature_name}.all }});
      queryClient.setQueryData(queryKeys.{feature_name}.detail(data.id), data);
    }},
  }});
}}

export function useDelete{feature_pascal}() {{
  const queryClient = useQueryClient();

  return useMutation({{
    ...{feature_camel}Mutations.delete(),
    onSuccess: () => {{
      queryClient.invalidateQueries({{ queryKey: queryKeys.{feature_name}.all }});
    }},
  }});
}}

// ============================================================
// Composite Hooks
// ============================================================

export function use{feature_pascal}Filters() {{
  const [filters, setFilters] = useState<{feature_pascal}Filters>({{}});

  const updateFilter = useCallback((partial: Partial<{feature_pascal}Filters>) => {{
    setFilters((prev) => ({{ ...prev, ...partial }}));
  }}, []);

  const clearFilters = useCallback(() => {{
    setFilters({{}});
  }}, []);

  return {{ filters, updateFilter, clearFilters }};
}}

export function use{feature_pascal}Sort() {{
  const [sort, setSort] = useState<{feature_pascal}ListSort>({{ field: 'name', direction: 'asc' }});

  const updateSort = useCallback((field: string, direction: 'asc' | 'desc') => {{
    setSort({{ field: field as {feature_pascal}ListSort['field'], direction }});
  }}, []);

  return {{ sort, updateSort }};
}}

export function use{feature_pascal}Pagination() {{
  const [page, setPage] = useState(0);
  const [pageSize, setPageSize] = useState(10);

  const updatePage = useCallback((newPage: number) => {{
    setPage(newPage);
  }}, []);

  const updatePageSize = useCallback((newPageSize: number) => {{
    setPageSize(newPageSize);
    setPage(0);
  }}, []);

  return {{ page, pageSize, updatePage, updatePageSize }};
}}

export function use{feature_pascal}Selection() {{
  const [selectedIds, setSelectedIds] = useState<string[]>([]);

  const updateSelection = useCallback((ids: string[]) => {{
    setSelectedIds(ids);
  }}, []);

  const clearSelection = useCallback(() => {{
    setSelectedIds([]);
  }}, []);

  return {{ selectedIds, updateSelection, clearSelection }};
}}
'''


def generate_manifest(feature_name: str, feature_pascal: str) -> str:
    return json.dumps({
        "name": feature_name,
        "version": "1.0.0",
        "description": f"Módulo de gestão de {feature_name}",
        "type": "feature",
        "golden_module": False,
        "generated_from": "doctor",
        "golden_version": "1.0.0",
        "owner": "unassigned",
        "maturity": "alpha",
        "routes": {
            "list": {
                "path": f"/app/{feature_name}",
                "component": f"{feature_pascal}ListPage",
                "personas": ["coordenador", "administrador"],
                "endpoints": [f"GET /api/v1/{feature_name}"],
            },
            "detail": {
                "path": f"/app/{feature_name}/:id",
                "component": f"{feature_pascal}DetailPage",
                "personas": ["coordenador", "administrador"],
                "endpoints": [f"GET /api/v1/{feature_name}/{{id}}"],
            },
        },
        "components": [f"{feature_pascal}Card", f"{feature_pascal}Header", f"{feature_pascal}Toolbar"],
        "hooks": [
            f"use{feature_pascal}sList",
            f"use{feature_pascal}Detail",
            f"useCreate{feature_pascal}",
            f"useUpdate{feature_pascal}",
            f"useDelete{feature_pascal}",
        ],
        "services": [f"{feature_name}Queries", f"{feature_name}Mutations"],
        "types": [feature_pascal, f"{feature_pascal}Filters", f"{feature_pascal}ListSort"],
        "tests": {},
        "shared_dependencies": [
            "EntityAvatar",
            "StatusChip",
            "PageHeader",
            "DataTable",
            "FilterBar",
            "EmptyState",
            "LoadingSpinner",
            "ErrorBoundary",
            "ConfirmDialog",
            "ActionsMenu",
        ],
    }, indent=2)


def generate_index(feature_name: str, feature_pascal: str) -> str:
    return f'''/**
 * {feature_pascal} Feature Index — Plantão 360
 *
 * Barrel do módulo de {feature_pascal}.
 * Generated from Golden Module (Doctor).
 *
 * Sprint: 13.5 — Frontend Platform Governance
 */

// Components
export {{ {feature_pascal}Card }} from './components/{feature_name}-card';
export {{ {feature_pascal}Header }} from './components/{feature_name}-header';
export {{ {feature_pascal}Toolbar }} from './components/{feature_name}-toolbar';

// Hooks
export {{
  use{feature_pascal}sList,
  use{feature_pascal}Detail,
  useCreate{feature_pascal},
  useUpdate{feature_pascal},
  useDelete{feature_pascal},
  use{feature_pascal}Filters,
  use{feature_pascal}Sort,
  use{feature_pascal}Pagination,
  use{feature_pascal}Selection,
}} from './hooks/use-{feature_name}s';

// Types
export type {{
  {feature_pascal},
  {feature_pascal}Filters,
  {feature_pascal}ListSort,
}} from './types/{feature_name}-types';
'''


# ============================================================
# Main Generator
# ============================================================

def generate_feature(feature_name: str, owner: str = "unassigned", golden: bool = False):
    """Generate a complete feature from Golden Module."""
    feature_pascal = feature_name.capitalize()
    feature_camel = feature_name.lower()

    print(f"\n🔧 Generating feature: {feature_pascal}")
    print(f"   Owner: {owner}")
    print(f"   Golden: {golden}\n")

    # Create feature directory
    feature_dir = FEATURES_DIR / feature_name
    if feature_dir.exists():
        print(f"❌ Feature '{feature_name}' already exists!")
        return False

    # Create directories
    for dir_name in FEATURE_DIRECTORIES:
        dir_path = feature_dir / dir_name
        dir_path.mkdir(parents=True, exist_ok=True)
        print(f"   ✅ Created: {dir_name}/")

    # Generate files
    files = {
        f"types/{feature_name}-types.ts": generate_types(feature_name, feature_pascal),
        f"services/{feature_name}-api.ts": generate_api(feature_name, feature_pascal, feature_camel),
        f"hooks/use-{feature_name}s.ts": generate_hooks(feature_name, feature_pascal, feature_camel),
        f"manifest/{feature_name}.json": generate_manifest(feature_name, feature_pascal),
        f"index.ts": generate_index(feature_name, feature_pascal),
    }

    for file_path, content in files.items():
        full_path = feature_dir / file_path
        full_path.parent.mkdir(parents=True, exist_ok=True)
        full_path.write_text(content, encoding="utf-8")
        print(f"   ✅ Generated: {file_path}")

    print(f"\n✅ Feature '{feature_pascal}' generated successfully!")
    print(f"   Location: {feature_dir}")
    print(f"\n📋 Next steps:")
    print(f"   1. Implement pages in pages/")
    print(f"   2. Implement components in components/")
    print(f"   3. Implement dialogs in dialogs/")
    print(f"   4. Run: npm run frontend:validate")
    print(f"   5. Run: npm run frontend:score\n")

    return True


# ============================================================
# CLI
# ============================================================

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python feature_generator.py <FeatureName> [--owner <owner>] [--golden]")
        print("Exemplo: python feature_generator.py Period")
        sys.exit(1)

    feature_name = sys.argv[1]
    owner = "unassigned"
    golden = False

    if "--owner" in sys.argv:
        idx = sys.argv.index("--owner")
        if idx + 1 < len(sys.argv):
            owner = sys.argv[idx + 1]

    if "--golden" in sys.argv:
        golden = True

    generate_feature(feature_name, owner, golden)
