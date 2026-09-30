"""Lakebase-backed :class:`RegistryStore` implementation.

Stores registry-shaped data in PostgreSQL tables on a Databricks
Lakebase instance. Optional backend — ``psycopg`` is imported lazily,
so volume-only deployments do not need the ``lakebase`` extra
installed.

Submodules
----------
- :mod:`back.objects.registry.store.lakebase.store` — the
  :class:`LakebaseRegistryStore` class.
- :mod:`back.objects.registry.store.lakebase.LakebaseRegistryDocuments`
  — document corpus mixin inherited by the store.
- :mod:`back.objects.registry.store.lakebase.LakebaseRegistryCollab`
  — comments and tasks mixin.
- :mod:`back.objects.registry.store.lakebase.LakebaseRegistryEditLocks`
  — single-editor lock mixin.
- :mod:`back.objects.registry.store.lakebase.LakebaseRegistryAnalytics`
  — graph analytics cache and run history mixin.
- :mod:`back.objects.registry.store.lakebase.LakebaseRegistryReviewEvents`
  — review/validation audit mixin.
- :mod:`back.objects.registry.store.lakebase.LakebaseRegistryChangeEvents`
  — ontology/mapping change audit mixin.
- :mod:`back.objects.registry.store.lakebase.LakebaseRegistryBuildRuns`
  — Knowledge Graph build-run trace mixin.
- :mod:`back.objects.registry.store.lakebase.LakebaseRegistryCatalog`
  — domain folders, versions, and permissions mixin.
- :mod:`back.objects.registry.store.lakebase.LakebaseRegistrySchedules`
  — scheduled tasks and history mixin.
- :mod:`back.objects.registry.store.lakebase.LakebaseRegistryBootstrap`
  — initialize, grants, and permission diagnostics mixin.
- :mod:`back.objects.registry.store.lakebase.LakebaseRegistryGlobalConfig`
  — instance-wide JSONB global_config mixin.
- ``schema.sql`` — idempotent DDL applied on first
  ``initialize()``; the schema name is parameterised via the
  ``__SCHEMA__`` token at runtime.

Authentication is handled by
:class:`back.core.databricks.lakebase.LakebaseAuth` (sources ``PG*`` env vars
and mints short-lived Lakebase JWTs via the workspace SDK).
"""

from __future__ import annotations

from .LakebaseRegistryAnalytics import LakebaseRegistryAnalytics
from .LakebaseRegistryBootstrap import LakebaseRegistryBootstrap
from .LakebaseRegistryBuildRuns import LakebaseRegistryBuildRuns
from .LakebaseRegistryCatalog import LakebaseRegistryCatalog
from .LakebaseRegistryChangeEvents import LakebaseRegistryChangeEvents
from .LakebaseRegistryCollab import LakebaseRegistryCollab
from .LakebaseRegistryDocuments import LakebaseRegistryDocuments
from .LakebaseRegistryEditLocks import LakebaseRegistryEditLocks
from .LakebaseRegistryGlobalConfig import LakebaseRegistryGlobalConfig
from .LakebaseRegistryReviewEvents import LakebaseRegistryReviewEvents
from .LakebaseRegistrySchedules import LakebaseRegistrySchedules
from .store import LakebaseRegistryStore

__all__ = [
    "LakebaseRegistryAnalytics",
    "LakebaseRegistryBootstrap",
    "LakebaseRegistryBuildRuns",
    "LakebaseRegistryCatalog",
    "LakebaseRegistryChangeEvents",
    "LakebaseRegistryCollab",
    "LakebaseRegistryDocuments",
    "LakebaseRegistryEditLocks",
    "LakebaseRegistryGlobalConfig",
    "LakebaseRegistryReviewEvents",
    "LakebaseRegistrySchedules",
    "LakebaseRegistryStore",
]
