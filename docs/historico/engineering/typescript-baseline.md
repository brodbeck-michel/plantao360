# TypeScript Baseline — Plantão 360

**Versão do TypeScript:** ^5.4.0
**Data de establishimento:** 2026-06-28
**Sprint:** 14.3 — Production Readiness
**Status:** Baseline oficial do projeto

---

## 1. Versão e Configuração

### Compilador

| Campo | Valor |
|-------|-------|
| TypeScript | ^5.4.0 |
| Target | ES2020 |
| Module | ESNext |
| Module Resolution | bundler |
| JSX | react-jsx |
| Lib | ES2020, DOM, DOM.Iterable |

### tsconfig.json Oficial

```json
{
  "compilerOptions": {
    "target": "ES2020",
    "useDefineForClassFields": true,
    "lib": ["ES2020", "DOM", "DOM.Iterable"],
    "module": "ESNext",
    "skipLibCheck": false,
    "moduleResolution": "bundler",
    "allowImportingTsExtensions": true,
    "isolatedModules": true,
    "moduleDetection": "force",
    "noEmit": true,
    "jsx": "react-jsx",
    "strict": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noFallthroughCasesInSwitch": true,
    "baseUrl": ".",
    "paths": {
      "@/*": ["src/*"]
    }
  },
  "include": ["src", "vite-env.d.ts"]
}
```

---

## 2. Regras Obrigatórias do tsconfig

| Regra | Valor | Justificativa |
|-------|-------|---------------|
| `strict` | `true` | Habilita todos os checks de tipo strictos |
| `skipLibCheck` | `false` | Valida tipos de dependências externas |
| `noUnusedLocals` | `true` | Previne código morto |
| `noUnusedParameters` | `true` | Previne parâmetros esquecidos |
| `noFallthroughCasesInSwitch` | `true` | Previne bugs em switch/case |
| `noEmit` | `true` | Vite cuida do build; TypeScript apenas valida |
| `isolatedModules` | `true` | Compatível com esbuild/Vite |
| `moduleDetection` | `force` | Trata todos os arquivos como módulos |

### Regras que NÃO devem ser alteradas

- `skipLibCheck` deve permanecer `false` — foi `true` como workaround; agora é baseline
- `strict` deve permanecer `true` — não há justificativa para desabilitar
- `noEmit` deve permanecer `true` — TypeScript é apenas um validador, não gera output

---

## 3. Política de Tipagem

### 3.1 Uso de `any`

**Proibido** sem justificativa documentada. Cada uso de `any` deve ter:

1. Comentário explicando por que o tipo correto não é viável
2. Referência ao issue/ticket se aplicável
3. Data de revisão programada

**Exceções permitidas:**
- Callbacks de bibliotecas externas que não expõem tipos adequados
- Integrações com APIs de terceiros sem tipos
- Casts temporários durante migração (com ticket associado)

### 3.2 Uso de `unknown`

**Permitido e encorajado** como alternativa ao `any`:

```typescript
// CORRETO
function processData(input: unknown) {
  if (typeof input === 'string') {
    // input é string aqui
  }
}

// INCORRETO
function processData(input: any) {
  // Sem verificação de tipo
}
```

**Casos de uso:**
- Dados de API com forma desconhecida
- Payloads de webhook
- Dados de localStorage/sessionStorage
- Retorno de `JSON.parse()`

### 3.3 Uso de `never`

**Permitido** para:
- Exhaustive checks em switch/if-else
- Funções que nunca retornam (throw, infinite loop)
- Types utilitários

```typescript
// Exhaustive check — CORRETO
function assertNever(x: never): never {
  throw new Error(`Unexpected value: ${x}`);
}

switch (status) {
  case 'active': break;
  case 'inactive': break;
  default: assertNever(status);
}
```

### 3.4 Uso de `as` (Type Assertions)

**Permitido** com restrições:

1. **`as` para narrowing** — Permitido quando o tipo é conhecido por构造:
   ```typescript
   const data = response.data as Doctor;
   ```

2. **`as` para bypass** — Requer justificativa:
   ```typescript
   // Permitido: API retorna tipo genérico
   const config = rawConfig as ApiClientConfig;
   ```

3. **`as any`** — Proibido (ver seção 3.1)

4. **Dupla asserção** — Proibida:
   ```typescript
   // PROIBIDO
   const x = value as unknown as SpecificType;
   ```

### 3.5 Uso de `@ts-ignore` e `@ts-expect-error`

**Proibido** sem justificativa documentada. Cada uso deve conter:

```typescript
// @ts-expect-error — Justificativa: biblioteca não expõe tipo correto
// Ticket: PLT-123 | Revisão: 2026-07-15
libraryCall(withInvalidArgs);
```

**Regras:**
- `@ts-except-error` é preferível a `@ts-ignore` (valida que o erro ainda existe)
- Todo `@ts-expect-error` deve ter data de revisão
- Revisão máxima: 30 dias

---

## 4. Tratamento de Bibliotecas Externas

### 4.1 Bibliotecas com tipos completos

Usar diretamente — não re-declarar:

```typescript
import { Button } from '@mui/material';
import { useQuery } from '@tanstack/react-query';
```

### 4.2 Bibliotecas sem tipos ou com tipos incompletos

1. Verificar se `@types/<package>` existe
2. Se não existir, criar declaração em `src/types/global.d.ts`:
   ```typescript
   declare module 'package-without-types' {
     export function doSomething(arg: string): unknown;
   }
   ```
3. Documentar por que o tipo é `unknown` e não `any`

### 4.3 MUI (Material-UI)

- Usar componentes de `@mui/material` diretamente
- **Grid v1** é o padrão: `<Grid xs={12} sm={6}>`
- **Grid v2** (`<Grid size={{ xs: 12 }}>`) é instável — não usar em produção
- `@mui/icons-material` deve ser importado componente a componente:
  ```typescript
  import { Refresh as RefreshIcon } from '@mui/icons-material';
  ```

### 4.4 React Query

- Chaves de query devem usar `queryKeys` de `src/services/query-keys.ts`
- Nunca criar chaves inline
- Usar `as const` para chaves imutáveis

---

## 5. Quality Gates Obrigatórios

### 5.1 Ordem de Execução

```
TypeScript (tsc -b)
    ↓
ESLint
    ↓
Testes (vitest)
    ↓
Build (vite build)
    ↓
Architecture Validator
    ↓
Golden Guard
```

### 5.2 Critérios de Passagem

| Gate | Critério | Comando |
|------|----------|---------|
| TypeScript | 0 erros | `tsc -b` |
| ESLint | 0 erros, 0 warnings | `eslint src/ --ext .ts,.tsx --max-warnings 0` |
| Testes | Todos passando | `vitest run` |
| Build | Exit code 0 | `vite build` |
| Architecture | Exit code 0 | `python tools/validate_architecture.py --all` |
| Golden Guard | Exit code 0 | `python tools/golden_guard.py` |

### 5.3 Bloqueio de Merge

- **Nenhum merge** pode ocorrer se qualquer gate falhar
- PRs devem mostrar todos os gates verde antes de merge
- Exceção: apenas o owner do repo pode forçar merge com gate falho (requer justificativa)

### 5.4 Execução Local

```bash
# Verificação completa
cd frontend
tsc -b && npm run lint && npm test && npm run build

# Verificação rápida (desenvolvimento)
cd frontend
tsc -b
```

---

## 6. Padrões de Código

### 6.1 Imports

```typescript
// 1. React (se necessário para React.FC etc.)
import React from 'react';

// 2. Bibliotecas externas
import { Box, Typography } from '@mui/material';
import { useQuery } from '@tanstack/react-query';

// 3. Internos com alias
import { queryKeys } from '@/services/query-keys';
import { StatusChip } from '@/shared/components/status-chip';

// 4. Internos com caminho relativo
import { apiClient } from '../../api/client';

// 5. Tipos
import type { Doctor } from '@/types';
```

### 6.2 Nomenclatura

| Tipo | Formato | Exemplo |
|------|---------|---------|
| Componente | PascalCase | `DoctorListPage` |
| Hook | camelCase com `use` | `useDoctors` |
| Função | camelCase | `fetchDoctors` |
| Constante | UPPER_SNAKE_CASE | `API_BASE_URL` |
| Tipo/Interface | PascalCase | `DoctorListParams` |
| Arquivo de componente | kebab-case | `doctor-list-page.tsx` |
| Arquivo de util | kebab-case | `query-factory.ts` |

### 6.3 Exports

```typescript
// Componente nomeado
export function MyComponent() { ... }

// Hook nomeado
export function useMyHook() { ... }

// Constante nomeada
export const MY_CONSTANT = 'value';

// Tipo nomeado
export interface MyType { ... }
```

---

## 7. Exceções Conhecidas

As seguintes exceções são aceitas e documentadas:

| Arquivo | Exceção | Motivo | Revisão |
|---------|---------|--------|---------|
| `src/api/client.ts` | `as InternalAxiosRequestConfig & { __context?: RequestContext }` | Axios não expõe tipo para interceptors | 2026-07-15 |
| `src/shared/utils/feature-validator.ts` | Usa APIs Node.js (`fs`, `path`) | Ferramenta de validação offline, não roda no browser | N/A (excluída do build) |

---

## 8. Histórico

| Data | Autor | Alteração |
|------|-------|-----------|
| 2026-06-28 | Sprint 14.3 | Establishimento da baseline oficial |

---

**Este documento é parte da baseline oficial do projeto. Alterações requerem aprovação do tech lead.**
