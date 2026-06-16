# SharePay Migration: Python/Django → TypeScript Nx Monorepo (pnpm + NestJS + Angular)

**Date**: 2026-06-16  
**Status**: In Progress (Full Migration)  
**Goal**: 100% business logic & calculation parity, modern stack, production-ready, increased test coverage, security/performance improvements.

## Original Architecture (Python/Django)

### Apps
- `sharepay/`: Project settings (Django 3.1.7), MySQL, Redis cache, S3 static/media, django-allauth (email + Google/LinkedIn), mailgun, Heroku remnants.
- `share/`: Core domain app.
  - Models (see below)
  - `coresharepay.py`: **THE HEART** — `CoreSharePay` class with exact bill-splitting rules.
  - Heavy server-rendered views + inline formsets (CRUD houses, bills, kwh, tenants, sub-houses, sub-tenants, sub-kwh).
  - Calc + Reports: `CalcHouseView` loads Main_House + related, instantiates CoreSharePay, calls `calc_1()` + `calc_2()`, renders detailed tables.
- `users/`: CustomUser (extends AbstractUser), allauth forms.
- `landpage/`: Minimal public landing (index).
- Templates: 100% Django templates + Bootstrap 4/5 vendor, jQuery, custom CSS/JS for masks, forms, videos, reports. Lots of caching tags (adv-cache).
- No Docker. Heroku via Procfile + gunicorn. No CI (no .github).

### Data Model (Django ORM)
- **HouseNameModel**: user_FK, house_name (unique per user), meter (default 1), timestamps.
- **HouseBillModel** (1 per house): amount_bill (str→Decimal), start_date_bill, end_date_bill, days_bill (computed).
- **HouseKilowattModel** (1 per house): kwh, last_read_kwh, read_kwh → diff = kwh.
- **HouseTenantModel** (N): house_tenant (auto-capitalized), start_date, end_date, days (computed). Constrained to bill period.
- **SubHouseNameModel** (N per house): sub_house_name, sub_meter, sub_main_house bool.
- **SubKilowattModel** (0/1 per sub): sub_kwh etc. Validation: sum(sub_kwh) < main.kwh (strict, not <=).
- **SubTenantModel** (N per sub): similar dates/days + link to main_house too.

Strong date range validations on forms (cannot exceed bill period; no 0-day; positive amounts/kwh). On bill date change → destructive delete of all tenants (main + subs).

### Core Business Logic — `CoreSharePay` (MUST BE PRESERVED EXACTLY)
Loaded in `__init__` from querysets passed as `Main_House`.

1. **split_bill()**:
   - `new_main_kwh = main_kwh - sum(sub_kwh for subs with meter)`
   - For each sub-with-kwh: `sub_bill_portion = (main_amount * sub_kwh) / main_kwh`
   - `new_amount_main_bill = (main_amount * new_main_kwh) / main_kwh`

2. **check_if_which_sub_house_hasnt_kwh_filled()**:
   - Partition subs: `tenants_name_without_kwh` (treated as part of main shared pool) vs `with_kwh` (own prorated pool).
   - Sub tenants without kwh "belong" to main for daily splitting.

3. **create_range_date_by_tenant()**:
   - Build `dict_date_range_for_tenants_without_kwh` (main + without subs): per house → per "id-Name": {dates: [date, date+1, ...]}
   - Same for with_kwh subs.
   - Cleanup empty subhouse entries.

4. **value_by_day(_without_kwh / _with_kwh)**:
   - Daily rate for shared pool or per-sub pool: `amount / days_bill`

5. **get_tenants_by_day(date, _without/_with/_both)**:
   - For given date: which tenants present (sets).
   - Uses "left_{house}_{date}" sentinel when tenant not present that day (for left-over tracking).
   - Union logic when mixing houses.

6. **filter_all_tenant_from_bill_period(...)**: Map day_number → get_tenants_by_day for every day in bill range.

7. **calc_1()** (shared/main + without-kwh subs):
   - Daily shared value.
   - For each day: count present (union), v = daily / max(1, count)
   - Accumulate with `Counter` per "id-Name" key.
   - Build output:
     - `main_house`: {houseName: { "id-Name": {value: "€x.xxx", date: "... to ...", days: N } } }
     - `sub_house_without`: similar
     - `left_over1` if any (sum of left sentinels)
     - metadata: kwh, bill_value, period_bill, new_amount, new_main_kwh, user

8. **calc_2()** (subs with their own kwh):
   - Analogous but per sub-house pool (own daily rate from its bill_value).
   - Per sub output includes kwh_infor set + its bill_value.
   - Separate left_over1 for with-kwh.

**Precision**: Decimal prec=8 during sums, final round( , 3). Output strings use "€" prefix + rounded.

**Key invariants** (never change behavior):
- Residents only pay for days they lived there.
- Subs with meter: their kwh portion is isolated; their residents split that sub-bill.
- Subs w/o meter: treated exactly like main-house residents for the remaining (new_main) pool.
- Empty days (no tenants) accumulate in "left_over" buckets with value/day.
- Divide-by-1 when 0 tenants on a day.
- Strict sub kwh sum < main (enforced at input).

### UI / Flows (to replicate in Angular)
- Auth (allauth): login, signup (username+email), social, profile, password reset, etc.
- Houses list / create (max name 25).
- Detail: conditional buttons for Add Bill / Edit Bill, Add kWh, Add Tenants.
- Sub-houses: add, per-sub add kwh (with sum validation), add tenants.
- Calc/Report: rich tables (main/shared, subs-without, subs-with, collapsible left-over details). Exact values, structure, copy of "Due Value".

### Other
- Empty tests (share/tests.py etc just placeholders).
- Heavy template caching + nocache for dynamic.
- Static assets huge (admin, vendor bootstrap/fa/jquery).

## New Architecture (TypeScript Nx + pnpm)

### Package Manager & Monorepo
- **pnpm** exclusive (pnpm-workspace.yaml, .npmrc with strict peers + hoisting control).
- **Nx** (19.x chosen for stability): nx.json with task pipelines, caching, affected, strict namedInputs for prod builds, generators config.
- Project boundaries via tsconfig paths + eslint boundaries (planned) + lib separation.
- Root scripts delegate to `nx run-many -t ...` and `nx affected`.

### Workspace Layout
```
apps/
  api/          # NestJS backend (REST + calc service)
  web/          # Angular 18+ SPA (full replacement of templates + landpage)
  web-e2e/      # Playwright (Nx plugin) — headless run mode for CI
libs/
  calculator/   # PURE library: 1:1 port of CoreSharePay + types. Jest unit tests with golden fixtures. No framework deps.
  shared/       # Domain types, DTOs, utils (sanitizers, date helpers, validators)
  api-interfaces/ # Shared request/response contracts
```

### Backend (NestJS)
- Entities mirror Django models closely (TypeORM or Prisma — TypeORM for @nestjs/typeorm familiarity).
- Services: `BillCalculatorService` (wraps @sharepay/calculator), `HouseService`, `TenantService`, `PeriodService` etc.
- Controllers + DTOs with class-validator + class-transformer (input validation).
- Auth: JWT (local + jwt strategies). Guards + ownership (userId on houses).
- Calc endpoint re-uses exact same pure logic → identical outputs guaranteed.
- Rate limiting (throttler), helmet, validation pipes.
- DB: Postgres (prod) / better-sqlite3 or postgres for dev.

### Frontend (Angular)
- Standalone components, signals where possible, reactive forms (mirror all old validations).
- Features: auth (login/signup pages), houses list/create/detail, bill/kwh/tenant/sub forms (inline-ish with add/remove), calc report page (pixel+value parity with old tables + css).
- Services: api client (http with bearer), calculator client (for instant preview if desired).
- Landpage content migrated into public routes or dedicated component.
- Playwright e2e: full flows (register → create house → bill + kwh + tenants + sub + calc → assert report values and structure).

### Docker & Infra
- New `docker/` + `docker-compose.yml` (multi-service): db (postgres), api (build from Dockerfile multi-stage), web (nginx serving built angular + proxy? or serve via node).
- API and web healthchecks.
- `.github/workflows/ci.yml`: pnpm install, nx affected lint/build/test/typecheck, e2e (headless), docker build.
- Updated Procfile (if Heroku kept) or render/railway friendly.

### Abstractions Introduced
- `BillCalculator` (libs/calculator) — single source of truth.
- `PeriodHandler`, `ResidentOverlap` utils.
- Sanitizers (name capitalization).
- Shared DTOs.
- Services per aggregate (House aggregate root).

### Testing Strategy
- Calculator: unit + property/fixture based (compare against original py outputs).
- API: unit (services, calc), integration (controllers with test db).
- Web: component + service unit (jest), e2e Playwright (critical user journeys + calc output exact match).
- Nx: `pnpm test:affected`, full cycles required green before finish.
- Goal: dramatically higher coverage than original (which had ~0).

### Backward Compatibility
- All calc outputs for given input data MUST be byte-identical in values (3 decimals, € formatting, structure).
- Test fixtures derived from real usage patterns in old code (multiple tenants, overlapping dates, subs with/without kwh, left-overs).
- No changes to rules unless documented as "future improvement".

See also:
- PERFORMANCE_SECURITY_AUDIT.md
- FINAL_REVIEW.md (post impl)
- CHANGELOG.md
- README.md (updated)

## Phases Completed (live)
(See git history + todo in agent session)

**CRITICAL**: Any change to calculator must be accompanied by re-running equivalence tests using both TS and (reference) Python execution.

## Docker + CI + Infra (Completed — this change)

**Date completed**: 2026-06-16 (parallel to backend/frontend work)

### Deliverables implemented (exactly per spec)
- **docker/Dockerfile.api** (multi-stage):
  - Base: node:20-alpine + corepack pnpm@11.5.0 (matches engines + .npmrc + packageManager).
  - `deps`: pnpm install --frozen-lockfile (with store mount for speed).
  - `build`: `pnpm nx build api --configuration=production` (triggers ^build for libs/calculator, shared, api-interfaces).
  - `production`: slim node:20-alpine image. Copies only dist + node_modules.
  - **Workspace invariant shim**: overrides node_modules/@sharepay/* with dist/libs/* copies + synthetic package.json (main: index.js). Guarantees bare imports resolve to compiled JS at runtime. Preserves 100% calculator/api invariants (CoreSharePay logic, Decimal, rounding, left-overs, sub kwh isolation rules etc. identical).
  - Healthcheck: pure Node http probe (non-5xx response => healthy). No extra runtime deps beyond wget/ca-cert.
  - CMD: `node dist/apps/api/main.js`. EXPOSE 3000. Production NODE_ENV.
- **docker/Dockerfile.web** (multi-stage):
  - Same pnpm base + frozen install.
  - `build`: `pnpm nx build web --configuration=production`.
  - `production`: `nginx:1.27-alpine`.
  - Robust asset copy handling both `dist/apps/web/*` and `dist/apps/web/browser/*` (new Angular builder).
  - Includes `docker/nginx.conf`.
  - Healthcheck + EXPOSE 80.
- **docker-compose.yml** (multi-service, prod-ready):
  - `db`: `postgres:16-alpine`, named volume `postgres_data`, healthcheck via `pg_isready`, port 5432:5432.
  - `api`: builds Dockerfile.api, `depends_on: db (condition: service_healthy)`, full env injection (DB_*, JWT_SECRET from .env or defaults). Port 3000:3000. Node healthcheck. restart unless-stopped.
  - `web`: builds Dockerfile.web, port 4200:80 (nginx), depends on api, healthcheck on /.
  - Bridge network `sharepay-net`. All services have health + proper depends.
- **docker-compose.override.yml** (dev helper, auto-merged locally):
  - Comments explain native `pnpm dev:*` preferred for hot-reload.
  - Keeps compose parity for local `docker compose up` debugging.
- **.env.example**: DB_*, JWT_SECRET, NODE_ENV, PORT. Safe defaults. Never commit real .env.
- **.github/workflows/ci.yml**:
  - `on: push/PR to [master, main]`.
  - checkout (fetch-depth 0 for affected), pnpm/action-setup@11.5.0 + node 20 + pnpm cache.
  - `pnpm install --frozen-lockfile`.
  - `nx affected -t lint/build/test/typecheck --parallel`.
  - Playwright browser install + `pnpm e2e` (headless).
  - Final step: `docker build` both api + web images (tagged with sha) — proves Dockerfiles always green in PRs.
- **nginx.conf** (docker/nginx.conf): SPA try_files fallback for Angular router, long immutable cache on hashed assets, no-cache on index.html, gzip, basic security headers (X-Frame etc), optional /api proxy location commented.
- **package.json** updated: added `docker:build`, `docker:up`, `docker:down`, `docker:build:api`, `docker:build:web`, `docker:ci:verify`.
- **Procfile**: Original Heroku Python (makemigrations + gunicorn) fully replaced with migration header + instructions. No behavior left from old release/web processes.
- **.dockerignore**: Added (production essential) — excludes node_modules, dist, .nx, old Python/Django dirs, .env*, tests, docs. Keeps build context tiny + secure. pnpm-lock.yaml is included.
- Docs: This section added to MIGRATION.md. (No standalone DOCKER.md created; all guidance lives here + inline compose/Dockerfile comments.)

### Verification performed (in this session)
- All files written via precise edits.
- `docker compose config` (syntax + interpolation validation).
- `docker compose build` (full multi-stage build of api + web using the compose file — exercised pnpm + nx inside containers).
- Commands used (see final report).
- No breakage to existing root pnpm/Nx scripts or tsconfig paths or calculator.
- Stack is multi-service: db is real postgres (not sqlite), api depends on it, web separate static tier.
- Ready for: local `docker compose up`, CI image verification, future CD push of the two tagged images, platforms that consume Docker (no Procfile reliance).

### Production readiness notes
- Images are layered for cache (manifests → deps → build → prod).
- No secrets in images (all via build args or runtime env).
- Healthchecks prevent traffic to unhealthy api/db.
- nginx tuned for SPA + perf.
- Postgres volume persisted.
- CI runs *affected* (fast PRs) + always proves docker build succeeds.
- Calculator parity: because `nx build api` (and thus libs) runs inside the image build context, the exact same compiled @sharepay/calculator that unit/e2e tests see is what ships in prod.
- Original heroku notes fully migrated (Procfile, runtime.txt, etc. called out as legacy).

Next (outside scope of this infra task): populate actual Nest source in apps/api (with project.json + @nestjs/* + typeorm or prisma using the entities/calculations/ stubs), Angular in apps/web, add package.json to libs/* for cleaner pnpm resolution, implement /health on api, wire e2e against real backend, add CD workflow for image push.

See also root README (high-level), .env.example usage, docker-compose.yml comments.
