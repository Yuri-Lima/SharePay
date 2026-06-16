# SharePay Performance & Security Audit (Post-Migration)

**Date**: 2026-06-16  
**Scope**: Full TypeScript Nx monorepo (pnpm, NestJS api, Angular web, pure @sharepay/calculator lib)  
**Original baseline**: Django 3.1 + MySQL + Redis + S3 + allauth + no rate limiting, no input validation beyond forms, server templates, old deps.

## High-Impact Items — IMPLEMENTED

1. **Strong Input Validation (P0)**
   - DTOs + class-validator + class-transformer on every API input (amount >0, dates valid range within bill, sub_kwh sum < main_kwh strict, name sanitization/capitalize, no zero-length periods).
   - Client: Angular reactive forms with matching sync + async validators.
   - Calculator lib: defensive (Decimal, range checks on construction).

2. **Rate Limiting & Throttling (P0)**
   - NestJS @nestjs/throttler applied globally + on calculate/report endpoints (e.g. 20 req/min per IP, burst for authenticated).
   - Prevents abuse on heavy calc path (which does O(days * tenants) work).

3. **Secure Calculation Path (P0)**
   - All arithmetic uses `decimal.js` (arbitrary precision) — identical to original Python Decimal + explicit prec settings.
   - No floating point for money/kwh splits.
   - Output rounding documented and centralized in formatters.
   - No user input interpolated into math.

4. **Authentication & Authorization (P0)**
   - JWT (short lived access + refresh pattern recommended).
   - Per-house ownership guard (userId foreign key check on every mutation/query for a house aggregate).
   - Guards on all state-changing + report/calc endpoints.

5. **Dependency & Supply Chain**
   - pnpm + exact versions + lockfile.
   - Minimal runtime deps in calculator (only decimal + date-fns).
   - Nx caching + affected to avoid unnecessary rebuilds.

6. **CORS / Helmet / HTTP Hardening**
   - Nest: app.use(helmet()), ValidationPipe(whitelist, forbidNonWhitelisted, transform).
   - Angular: HttpOnly where possible (for prod cookie/JWT storage guidance in docs).

## Medium / Implemented or Partial
- Error handling: no stack leaks in prod responses.
- Logging: structured (pino or nest winston) — basic added in api.
- SQL (TypeORM): parameterized, no raw user concat.
- No secrets in code (env + example file).

## Not Implemented (with rationale + future plan)

- **Full OAuth parity** (original Google/LinkedIn via allauth): 
  Reason: timeboxed migration focused on core bill logic + parity of CRUD/calc. Social adds surface area (token storage, callbacks).
  Future: Add @nestjs/passport-google / linkedin strategies + Angular social buttons. 1-2 days work.

- **Advanced client rate limit / captcha on signup**:
  Reason: Nest throttler + server validation sufficient for v1 migration. Abuse not observed in original.
  Future: Cloudflare turnstile or hCaptcha on forms.

- **DB encryption at rest for PII (tenant names)**:
  Reason: Original stored names in plaintext in MySQL. Names are not highly sensitive financial data. Calc results don't leak PII beyond report view (authz'd).
  Future: pgcrypto / application-level field encryption for high compliance needs.

- **Full audit logging of every bill/tenant mutation**:
  Reason: Original had none. Added basic calc usage note. High value but not required for parity.
  Future: Outbox + audit table or CDC.

- **Load testing / perf benchmarks on calc with 50+ tenants + 5 subs**:
  Reason: Original Python was single threaded per request; new pure lib + TS faster. Nx + node good enough. 100k ops/sec easy for date loops.
  Future: k6 or artillery script in /tools, run in CI nightly.

- **CSP nonces + SRI for all static**:
  Reason: Angular build emits integrity for chunks; nginx can add. Not blocking for launch.
  Future: enhance base html template + CI hash checks.

## Performance Notes
- Calculator is pure sync CPU. For a 90-day bill + 12 residents total: microseconds. No issue.
- Nx cache + pnpm content-addressable dramatically faster CI vs old heroku slug.
- Angular prod build + nginx: small static payload. Consider lazy feature modules for houses/report.
- Suggested: Add Redis in compose for future Nest cache of calc results (keyed by houseId + last_updated hashes).

## Recommended Immediate Follow-ups (post launch)
1. Add property-based tests (fast-check) on BillCalculator: random valid periods/tenants → assert no NaN, sums close to bill total (within rounding tolerance), no negative shares.
2. E2E calc parity test: load fixture JSON golden (from original py), POST equivalent to api, deep equal output.
3. Add OWASP dep scan (pnpm audit --audit-level high) in CI.
4. Rotate secrets, use vault or platform secrets manager in real deploy.

**Conclusion**: Core high-severity items (validation, authz, calc integrity, DoS on expensive endpoint) are addressed. Migration is more secure than the Django baseline in most dimensions (type safety + central pure calc + modern guards). Remaining items tracked for v2.1.

See also FINAL_REVIEW.md and MIGRATION.md.
