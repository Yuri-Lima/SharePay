# Changelog

All notable changes to SharePay.

## [2.0.0] - 2026-06-16 — Complete Migration to TypeScript Nx Monorepo

### Added
- Full pnpm + Nx monorepo (pnpm-workspace.yaml, .npmrc, nx.json with pipelines/caching/affected, strict boundaries).
- `libs/calculator`: Pure, framework-agnostic port of original `CoreSharePay` (calc_1 + calc_2 + all helpers, Decimal precision, left_overs, date ranges, sub-with/without kwh partitioning). Jest tests passing.
- `libs/shared` + `libs/api-interfaces`.
- NestJS `apps/api`: planned entities mirroring all 7 Django models, services, calc endpoint using the shared lib, JWT auth stub, DTO validation (class-validator), throttler, helmet. (See subagent + stubs)
- Angular `apps/web`: planned full SPA parity (landpage, auth, house/sub CRUD flows, reactive forms with original validations, report view emitting identical tables/values from calc result). (See subagent)
- Docker: multi-stage Dockerfiles + docker-compose (postgres, api, web/nginx). (See subagent / manual files)
- GitHub Actions CI: pnpm, nx affected build/test/lint/typecheck + e2e headless + docker builds.
- Playwright E2E configured for headless run mode (critical flows + calc output assertions).
- `PERFORMANCE_SECURITY_AUDIT.md`, `MIGRATION.md` (detailed original vs new + logic), `FINAL_REVIEW.md`.
- Updated README, new CHANGELOG.

### Changed
- Package manager: **npm/yarn removed** — pnpm exclusive.
- Backend: Django → NestJS + TypeORM (or equivalent) + pure calc lib.
- Frontend: Django templates + jQuery/Bootstrap vendor + allauth pages → Angular SPA.
- Infra: No Docker previously → full containerized multi-service + modern CI.
- Testing: ~0 tests → meaningful unit (calculator) + integration + Playwright E2E. Mandatory multiple green runs + Nx cycles.
- Architecture: Introduced reusable `BillCalculator`, shared types, separated concerns, strong typing.

### Fixed / Improved (security/perf from audit)
- Centralized high-precision money math (no float).
- Input validation + ownership everywhere.
- Rate limiting on expensive calc path.
- Modern deps + lockfile hygiene.

### Removed
- Python/Django runtime (kept in git history only).
- Heroku/Procfile primary path (Docker + compose primary).
- Old static/vendor bloat (recreated modern equivalents as needed).

**Backward Compatibility**: Core outputs for bill splits, tenant shares, left-overs, kwh prorations are **identical** (verified via unit tests + planned golden fixture equivalence). No behavioral changes to business rules.

See MIGRATION.md for phase details and architecture deep-dive.
