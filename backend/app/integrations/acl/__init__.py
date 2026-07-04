"""
Anti-Corruption Layer — Plantão 360

Este módulo contém a ACL que traduz dados externos para o formato do domínio.
Domain nunca importa este módulo.

Sprint: 10.5 — Domain Freeze, Application Baseline & Integration Architecture
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TypeVar

T = TypeVar("T")


class BaseACL(ABC):
    """Base para todas as ACLs."""

    @abstractmethod
    def _to_domain(self, external_data: T) -> T:
        """Traduz dados externos para formato do domínio."""
        ...

    @abstractmethod
    def _to_external(self, domain_data: T) -> T:
        """Traduz dados do domínio para formato externo."""
        ...
