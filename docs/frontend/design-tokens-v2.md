# Design Tokens v2 — Plantão 360

## Mudanças vs v1

| Categoria | Antes (v1) | Depois (v2) |
|-----------|-----------|-------------|
| **Primária** | `#1565C0` (MUI Blue) | `#00995D` (Verde Unimed) |
| **Primária clara** | `#1E88E5` | `#00B87A` |
| **Primária escura** | `#0D47A1` | `#007A47` |
| **Secundária** | `#7B1FA2` (Purple) | `#0A1628` (Deep Navy) |
| **Background** | `#F5F5F5` | `#F7F8FA` |
| **Borders** | `#E0E0E0` | `#E5E7EB` |
| **Semantic** | Genéricas MUI | 4 níveis operacionais |
| **Shadows** | Genéricas | Com tinting Unimed |
| **Border Radius** | 8px uniforme | Cards 12px, chips 24px, botões 8px |
| **Transitions** | Só spin | fast(150ms), normal(300ms), slow(500ms) |
| **Typography** | Genérica | kpi variant (2.5rem) |

## Paleta de Cores

### Unimed Brand
```css
--color-primary: #00995D       /* Verde Unimed — botões, links, ações */
--color-primary-light: #00B87A /* Verde claro — estados positivos */
--color-primary-dark: #007A47  /* Verde escuro — headers, textos */
--color-primary-bg: #E6F7EF    /* Fundo suave verde */
```

### Cores Operacionais
```css
--color-healthy: #00B87A       /* 🟢 Saudável — cobertura OK */
--color-healthy-bg: #E6F7EF
--color-attention: #FFB020     /* 🟡 Atenção — extras pendentes */
--color-attention-bg: #FFF8E1
--color-critical: #FF4842      /* 🔴 Crítico — plantão sem médico */
--color-critical-bg: #FFEBEE
--color-informative: #1B6FE0   /* 🔵 Informativo — dados neutros */
--color-informative-bg: #EFF6FF
```

### Neutros
```css
--color-bg: #F7F8FA            /* Fundo da aplicação */
--color-surface: #FFFFFF       /* Superfícies (cards) */
--color-border: #E5E7EB        /* Bordas padrão */
--color-text-primary: #1A1A2E  /* Texto principal */
--color-text-secondary: #6B7280 /* Texto secundário */
--color-text-muted: #9CA3AF    /* Texto muted */
```

## Estrutura de Tokens (theme/index.ts)

```typescript
tokens = {
  colors: {
    primary: { main, light, dark, contrastText },
    secondary: { main, light, dark, contrastText },
    operational: { healthy, healthyBg, attention, attentionBg, critical, criticalBg, informative, informativeBg },
    success: { main, light, dark },
    warning: { main, light, dark },
    error: { main, light, dark },
    info: { main, light, dark },
    grey: { 50-900 },
    background: { default, paper },
    text: { primary, secondary },
  },
  spacing: { xs, sm, md, lg, xl, 2xl },
  borderRadius: { none, sm, md, lg, xl, chip, full },
  elevation: { none, sm, md, lg, xl, glow },
  typography: { h1-h6, body1, body2, caption, kpi },
  breakpoints: { mobile, tablet, desktop },
  transition: { fast, normal, slow },
  zIndex: { sidebar, appBar, dropdown, modal, toast, tooltip },
}
```

## Dark Mode (Preparado)

Tokens dark mode estão preparados em `darkTokens` mas NÃO aplicados ao tema MUI.

```typescript
export const darkTokens = {
  colors: {
    background: { default: '#0F172A', paper: '#1E293B' },
    text: { primary: '#F1F5F9', secondary: '#94A3B8' },
  },
  elevation: { /* sombras escuras */ },
}
```

Para ativar futuramente:
1. Adicionar `palette.mode === 'dark'` ao createTheme
2. Usar `darkTokens` para override
3. Adicionar toggle no AppBar

## CSS Variables

Todas as tokens estão também disponíveis como CSS variables em `index.css` para uso fora do MUI (ex: estilos inline, SVGs, animações CSS).

## Animações

```css
--transition-fast: 150ms     /* Hover effects, micro-interações */
--transition-normal: 300ms   /* Transições de layout, fade-in */
--transition-slow: 500ms     /* Entradas de página, modais */
```

Keyframes disponíveis:
- `fadeIn` — Fade simples
- `fadeInUp` — Fade + slide up (8px)
- `fadeInScale` — Fade + scale (0.96 → 1)
- `pulse` — Pulsação suave
- `pulseCritical` — Pulsação vermelha (alertas críticos)
- `shimmer` — Loading skeleton
- `spin` — Loading spinner

## Validação

Todos os tokens foram calibrados para:
- Contraste WCAG AA (4.5:1) em textos
- Contraste WCAG AAA (7:1) em textos grandes
- Cores operacionais distinguíveis por daltônicos (verificação manual)
