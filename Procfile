# DEPRECATED / MIGRATED
# Original Heroku Python/Django release + gunicorn web process.
# Full migration to pnpm + Nx + NestJS + Angular completed.
#
# Production deployment now uses Docker:
#   - Multi-stage: docker/Dockerfile.api (Nest build + Node prod)
#   - Multi-stage: docker/Dockerfile.web (Angular build + nginx:alpine)
#   - Orchestration: docker-compose.yml (postgres:16 + api + web) with healthchecks
#   - CI: .github/workflows/ci.yml (pnpm frozen + nx affected + e2e + docker build)
#
# For container platforms (Heroku container stack, Railway, Render, Fly.io, ECS, K8s, etc.):
#   Use the Dockerfiles directly. API equivalent start: node dist/apps/api/main.js
#   Web is fully static (no server process).
#
# Local legacy (if you must): keep old python stack separate.
# See MIGRATION.md (Docker & Infra section), .env.example, docker-compose.yml

# Optional container-friendly hint (if using herokuish or similar):
# web: node dist/apps/api/main.js
# release: echo "Use docker build for full stack now"