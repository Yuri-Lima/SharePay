# DIG DEEP REVIEW — Post 4-Agent Feature Evaluation (2026-06-16)

**Orchestrator (main agent) synthesis after spawning + receiving results from FeatureEvalAgent-1..4 + exhaustive additional tool use (reads of sync + all cited files, greps, test runs, typecheck, proxy/env/auth inspection).**

## Executive Summary from Agents (condensed from FEATURE_EVAL_SYNC.md appends)
All 4 agents followed protocol exactly:
- Read FEATURE_EVAL_SYNC.md first.
- Performed deep tool-driven analysis (multiple read_file + grep + list_dir on FEATURE_EVAL_SYNC, MIGRATION, FINAL_REVIEW, PERFORMANCE, calculator.ts:1-500+, houses.*.ts full (controller 173 lines, service 376 lines), core/houses.service.ts 260 lines mock, house-detail  (full), calc-report (full), entities, DTOs, shared, legacy templates/houses/calc_bill/*, coresharepay.py cross refs, playwright.config, app.config, auth.*, proxy, etc.).
- Appended **only material non-duplicative** structured sections (REAL-API-WIRING, E2E-PARITY-TESTS, PRINT-PDF-AUTOFILL, FAQ-README-SEED) with file:line citations, parity-specific risks (drift in CalculatorService mapping lines 25-77, left_ sentinel accumulation 345-359/442-456, sub-kwh strict < 295-300, destructive bill date 115-122, camel vs snake shape at entities vs Angular interface + CoreInput builder, auth fake btoa vs real JwtStrategy, proxy :8000 vs :3000+prefix, no interceptor attached), adjusted P/C (all confirmed P0/H for 1+2, P1/M for 3, P2/M for 4), mandatory verification (nx test calculator 3x+, full roundtrip via real /calculate + deep equal on €.xxx + left_over1 shape + "id-Name" + no NaN/neg, e2e headless multi-run, typecheck/build).
- Each produced 3-sentence exec summary.
- No app source edits except the required single append each to the shared md.

Key cross-agent consensus (beyond my pre-spawn baseline):
- The "migration complete" commit (72466da) delivered excellent backend surface + the pure BillCalculator (single source, tests green, high fidelity to coresharepay split/partition/sentinel/round/€ rules) + infra, but the Angular is 100% demo against localStorage + direct lib calc (never hits guarded /calculate or nested CRUD). This is the exact "partial wiring" called out in its own FINAL_REVIEW:31 and MIGRATION:229.
- Highest risk to the sacred "100% exact outputs / no behavioral drift" is **in the mapping layer** (runCalculationForHouse) + **shape adapter** during wiring + **leaving report on client calc** after "wiring CRUD".
- E2E currently proves 0 of the real stack (no auth, no DB relations, no loadFull, no /calculate). Adding journeys without fixing decoupling is wasted (or actively misleading).
- Small GitHub issues (#13 Print, #12 autofill) are safe low-risk (post-calc UI only; use shared daysBetween; zero-dep print + @media for left_overs).
- Docs/FAQ must be truthful about current mock state or risk new issues.

## Additional Dig-Deep Verification Performed (Orchestrator)
- **Tests baseline (post-agents, pre-impl)**: 
  - `pnpm nx test calculator --skip-nx-cache`: 3/3 green (structure, sub isolation, left-over accumulation) — 0.256s.
  - `pnpm nx test api --testPathPattern=houses`: 2/2 green (defined + capitalize via shared).
  - Full typecheck (calculator + web + api + libs): all clean (tsc --noEmit on respective tsconfigs).
  - Lint: root task absent (expected; per-package ok).
- Inspected proxy.conf.json (targets 8000, old Django), environment.ts (admits mock), app.config.ts (withInterceptors([]) — critical), auth.service.ts (fully fake btoa + comments "Simulate", no real http to /auth/* despite HttpClient injected), houses.controller (full surface + calculate), houses.service Nest (all methods + strict rules present), calculator.service (mapping is the contract), core/houses.service mock (calculate at ~221-254 does the local new BillCalculator).
- Cross-checked camel (entities: houseName/amountBill/startDateBill/houseTenant/subHouseName/subKwh + calculator.service mapping) vs snake (Angular House iface + 40+ bindings in detail/report + CoreInput builder in mock) — confirmed major hidden contract.
- Confirmed no current path from SPA to real POST /:id/calculate (report + detail always local).
- No changes to any calc logic, types, or output shape anywhere in tree (good).
- Agent sync md protocol worked: 4 distinct high-signal appends, no bloat, all referenced failure modes (drift, incomplete, subagent, over-engineer).

## Risks Confirmed / Heightened
1. **Semantic drift on wiring** (top LLM failure from research ~40% rate): any ad-hoc client date/amount/id math, missing sub.kilowatts[0] or FK shape in map, or report continuing to use local calc after "API wired" will produce different €/left_over/new_main_kwh vs golden (coresharepay + lib spec + FINAL_REVIEW sample).
2. **Auth token reality**: fake btoa will 401 on every guarded route. Must make AuthService do real POST /api/auth/login (Nest returns access_token or equivalent; strategy expects sub as id or username).
3. **Proxy + prefix + interceptor**: 3 places must align (proxy target :3000, env, app.config provide the interceptor that reads AuthService token and adds Bearer).
4. **Component sync**: house-detail uses mix reactive + per-sub standalone ngModel dicts; on real http load must repopulate those dicts + handle async saves + error shapes (server {sub_kwh: 'msg'} vs client string[]).
5. **Verification gap**: even after wiring, without updated E2E hitting real /calculate + golden deep-equal, we re-create the exact situation the migration prompt and its FINAL_REVIEW warned against ("units green but integration not proven").
6. Sub-kwh == main rejection, destructive deletes, left_ sentinel aggregation, divide-by-1 must be exercised in real persisted journey.

## Recommended Immediate Next (for autonomous impl start of P0 Feature 1)
- Make core/houses.service.ts a hybrid: real HTTP mode (preferred when token) with snake<->camel mappers (keep public API + templates untouched to minimize blast radius), fall back to mock only for demo/offline. calculate() becomes http POST + return result (no local BillCalculator call in prod path).
- Wire interceptor (app.config), fix proxy to 3000, make AuthService call real /auth endpoints (store real token).
- Convert house-detail + calc-report call sites to async (promises/observables), add minimal loading/error UI.
- After every batch of edits: `pnpm nx typecheck`, `pnpm nx test calculator`, manual roundtrip via real API if services up.
- Do **not** touch libs/calculator, calculator.service (Nest), entities, or output shapes.
- Update FEATURE_EVAL_SYNC.md or add note only if material new risk found during edits.
- Once basic flows work (house create -> bill/kwh/tenant/sub -> real calculate -> report values match direct lib on same data), mark Feature 1 "started" and move to E2E wiring + golden fixtures (Feature 2).

## Sign-off
Agents performed high-quality, protocol-adherent, parity-obsessed evaluations with concrete citations and guardrails. Combined with fresh test/type runs (all green) and file inspections, the state is well understood. The most important work is now **Feature 1 real wiring** (unblocks everything, highest drift risk if done sloppily). 

Implementation of top feature begins immediately after this review + creation of the extremely hard prompt (per user request: "create a extreammly hard prompt where it would make the model struggled to implement. Do a reseach... After all of that start the implementation without asking me anything").

No user questions will be asked. All changes will be precise, minimal where possible, verified with required cycles, and will not alter calculator behavior.

— Orchestrator (main), 2026-06-16 (post 4 subagents + verification)
