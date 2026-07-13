# Research — Baseline de Testes Confiável

Decisões técnicas (Decisão / Justificativa / Alternativas descartadas). Ancoradas em código real.

## D1 — Autenticar testes de integração via override de `get_current_user`

**Decisão**: nos apps de teste, instalar
`test_app.dependency_overrides[get_current_user] = lambda: <User ADMIN falso>`, do mesmo jeito
que já se faz com `get_db`.

**Justificativa**: `app/core/security/dependencies.py` mostra que `require_role(*roles)` faz
internamente `current_user = Depends(get_current_user)`. Logo, um único override de
`get_current_user` satisfaz **tanto** os routers com `dependencies=[Depends(get_current_user)]`
**quanto** os endpoints com `require_role("ADMIN")` (o usuário falso é ADMIN → passa no check de
papel). Ponto único, sem tokens.

**Alternativas descartadas**:
- Login real + token por teste: lento, acopla os testes ao fluxo de auth, e exigiria semear um
  usuário em cada app in-memory.
- Override por endpoint/rota: repetitivo e frágil (muitos `Depends`).
- Desligar auth globalmente em teste: mascararia regressões de RBAC.

## D2 — Helper compartilhado no `conftest.py` da pasta integration

**Decisão**: criar `app/tests/integration/conftest.py` com (a) um `User` ADMIN falso e (b) um
helper `install_auth_override(app)`. Cada `client` fixture existente chama o helper (uma linha),
mantendo seu app/rota/seed próprios.

**Justificativa**: os testes de integração já seguem um padrão estável (cada arquivo monta seu
`test_app` com o(s) router(s) que testa e faz `dependency_overrides[get_db]`). Um helper
compartilhado dá o efeito de "fixture compartilhada" (FR-002) com **churn mínimo** e sem
reescrever a montagem de cada app — respeitando o Princípio I.

**Alternativas descartadas**:
- `client` fixture única no conftest com todos os routers: refatoração maior, risco de quebrar o
  seeding específico de cada arquivo; ganho pequeno para o objetivo (verde confiável).

## D3 — Formato do usuário ADMIN falso

**Decisão**: instância não-persistida de `app.models.user.User` com `id=1`, `role="ADMIN"`,
`active=True`, `name`/`email` preenchidos.

**Justificativa**: `get_current_user` retorna um `User`; alguns endpoints usam `current_user.id`
(ex.: troca de senha). Um `User` com `id` e `role` cobre os dois usos sem tocar o banco.

**Alternativas descartadas**: `SimpleNamespace`/mock — funciona, mas um `User` real evita
surpresas de atributo e é mais fiel.

## D4 — Testes-contadores: deletar, não "atualizar o número"

**Decisão**: remover as asserções de contagem de enums/eventos
(`test_domain_events::test_domain_event_name_count`, `test_remuneration_events`,
`test_payroll_events`) e revisar `test_shift_constants`. Se um arquivo só tiver a contagem,
apaga-se o arquivo; se tiver asserções de comportamento úteis, mantém-se só essas.

**Justificativa**: `assert 45 == 38` quebra a cada constante nova e não protege comportamento —
é passivo (Princípio III). Atualizar o número apenas adia a próxima quebra.

**Alternativas descartadas**: atualizar o número mágico (chuta a lata adiante); converter em
teste de comportamento quando não há comportamento a testar (não force).

## D5 — `test_manifests.py`: deletar

**Decisão**: remover `app/tests/unit/test_manifests.py`.

**Justificativa**: importa `manifest_loader`, módulo inexistente — resquício da cerimônia de
"module manifest" (ADR-016), que a constituição supera. Ele **quebra a coleção** inteira da
suíte, então some junto com o resto do aparato de manifest na Fase 2/3.

**Alternativas descartadas**: recriar `manifest_loader` só para o teste passar — reviveria
cerimônia que vamos remover.

## D6 — Atualizar testes desatualizados (sem mudar produto)

**Decisão**: corrigir as **fixtures/asserções**, não o código de produção:
- `test_doctor_mapper`: a fixture cria um Doctor sem `specialty`/`doctor_type`, mas o
  `DoctorResponseDTO` exige esses campos (migrations 004/005 os tornaram obrigatórios, com
  default no banco). Passar os campos na fixture.
- `test_settings_factory`: `ProductionSettings()` agora falha rápido com segredo fraco
  (hardening). Atualizar o teste para fornecer segredo forte **ou** asseverar que rejeita o
  fraco.
- `test_shift_service`: alinhar a asserção ao comportamento atual do serviço (a inspecionar).

**Justificativa**: os campos/validações refletem comportamento **correto** de produção; o
vermelho é só desatualização do teste. Mudar o produto para o teste passar violaria o escopo.

## D7 — Gate de cobertura realista

**Decisão**: remover `--cov-fail-under=80` do `addopts` padrão em `pyproject.toml` (linha 46) e
ajustar `[tool.coverage.report] fail_under` (linha 56) para o valor **medido** após o verde
(documentado), a ser elevado gradualmente. A cobertura continua sendo **relatada**, só deixa de
reprovar artificialmente.

**Justificativa**: 80% fixo reprova a suíte mesmo com testes passando e num subconjunto derruba
tudo — treina a equipe a ignorar o CI (pior que não ter gate). Um número honesto que sobe com o
tempo é mais útil (Princípio III).

**Alternativas descartadas**: manter 80% (irreal hoje); fingir cobertura com testes vazios.

## Observações

- Ambiente de teste: `ENVIRONMENT=test`, SQLite in-memory; o `conftest.py` raiz já limpa o cache
  de settings. Nada disso muda.
- A validação usa a imagem `plantao360-backend-test` (rebuild rápido, camada de pip em cache).
- Após o verde, a suíte passa a ser a rede de segurança do colapso do `domain/` (próxima feature
  da Fase 2).
