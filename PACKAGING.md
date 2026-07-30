# Shared technical base

This repo is the **canonical source** for tooling shared across Zostera's Django packages.
Changes to shared tooling start here and get propagated by hand to each sibling, then opened
as a PR in that sibling's own repo — never push straight to `main`.

- https://github.com/zostera/django-bootstrap3 — Bootstrap 3 for Django
- https://github.com/zostera/django-bootstrap4 — Bootstrap 4 for Django
- https://github.com/zostera/django-bootstrap5 — Bootstrap 5 for Django
- https://github.com/zostera/django-icons — Icons for Django
- https://github.com/zostera/django-marina — Django extensions by Zostera (this package)

## Synced identically (copy verbatim)

- `justfile`
- `.github/workflows/ci.yml`
- `.github/workflows/release.yml`
- `.github/workflows/dependabot-auto-approve-and-merge.yml`
- `.editorconfig`, `.readthedocs.yaml`
- `tox.ini` — except django-bootstrap5 adds `extras = jinja` under `[testenv]` for its
  Jinja2 integration tests. Keep that line when propagating there; don't add it elsewhere.

## Synced with per-package substitution

`pyproject.toml` sections `[build-system]`, `[tool.uv.build-backend]`, `[tool.check-manifest]`,
`[dependency-groups]`, `[tool.ruff]` / `[tool.ruff.lint]` / `[tool.ruff.lint.isort]`,
`[tool.coverage.*]` share the same shape everywhere. Substitute per package:

- distribution name / description / keywords / Django dependency floor (`[project]`)
- import module name in `known-first-party`, `[tool.coverage.paths] package`,
  `[tool.coverage.run] source`
- `module-name` key in `[tool.uv.build-backend]` — only needed for django-bootstrap3/4 (see
  naming convention below); omit it for bootstrap5/icons/marina, where it's correctly
  derived from the distribution name by default.

`MAINTAINING.md` shares the same two-section shape (version-support policy + release
process) everywhere; substitute package name and any package-specific pinned-dependency
notes (e.g. a Bootstrap CDN version).

## Naming convention (intentional split, not drift)

- **Legacy** (django-bootstrap3, django-bootstrap4): import name has no `django_` prefix —
  `src/bootstrap3/`, `src/bootstrap4/`. Requires an explicit `module-name = "bootstrap3"`
  (or `"bootstrap4"`) override in `[tool.uv.build-backend]`, since it no longer matches the
  distribution name.
- **Current** (django-bootstrap5, django-icons, django-marina): import name = distribution
  name with dashes replaced by underscores — `src/django_bootstrap5/`, `src/django_icons/`,
  `src/django_marina/`. No override needed.

Don't "fix" bootstrap3/4 to match the current convention — it's a public import path;
renaming it would be a breaking change with no upstream justification.

## Not synced

- `AGENTS.md` — each package has its own; only the "Related packages" list and general tone
  are meant to match.
- `README.md` — structure varies per package on purpose.
- `CHANGELOG.md`, package source, tests, docs content.

## Propagation process

1. Make the change here (django-marina) first. Verify with `just build` / `just lint` /
   `just tests`.
2. For each sibling, create a branch, apply the equivalent change substituting the
   per-package variables above, and verify with that repo's own `just build` / `just lint`.
3. Open a PR per repo — never push straight to `main` in any of these repos.
