# Accessibility Guide — Plantão 360

**Sprint:** 13 — Golden Frontend Module
**Data:** 2026-06-27

---

## Convenções

### 1. ARIA Labels
Todo elemento interativo deve ter `aria-label`:

```tsx
<IconButton aria-label="Fechar">
  <Close />
</IconButton>

<Button aria-label="Novo médico">
  Novo Médico
</Button>

<TextField inputProps={{ aria-label: 'Nome do médico' }} />
```

### 2. Keyboard Navigation
- Tab para navegar entre elementos
- Enter/Space para ativar botões
- Escape para fechar diálogos
- Setas para navegar em listas

```tsx
<MenuItem
  onKeyDown={(e) => {
    if (e.key === 'Enter') handleAction();
  }}
>
```

### 3. Focus Management
- Foco automático no primeiro elemento ao abrir diálogos
- Trap focus dentro de diálogos
- Restaurar foco ao fechar diálogos

```tsx
<Dialog
  onEntering={() => {
    // Focus first element
  }}
>
```

### 4. Screen Reader
- Use `role` para elementos semânticos
- Use `aria-live` para atualizações dinâmicas
- Use `aria-expanded` para elementos expansíveis

```tsx
<Box role="region" aria-label="Filtros">
  {/* filters */}
</Box>

<Button aria-expanded={expanded} aria-controls="filter-panel">
  Filtros
</Button>
```

### 5. Contrast
- Texto principal: contraste mínimo 4.5:1
- Texto grande: contraste mínimo 3:1
- Componentes interativos: contraste mínimo 3:1

### 6. Alt Text
- Imagens: alt descritivo
- Ícones: aria-label ou sr-only text

```tsx
<Avatar
  src={imageUrl}
  alt={`Foto de ${doctor.name}`}
/>

<Visibility aria-label="Visualizar" />
```

---

## Checklist

- [ ] Todos os elementos interativos têm `aria-label`
- [ ] Navegação por teclado funciona
- [ ] Focus management implementado
- [ ] Screen reader consegue ler todo conteúdo
- [ ] Contraste adequado
- [ ] Alt text em todas as imagens
- [ ] ARIA roles em elementos semânticos
- [ ] aria-live em atualizações dinâmicas

---

## Referências

- `features/doctor/` — Golden Frontend Module
- `shared/components/` — Componentes com ARIA
