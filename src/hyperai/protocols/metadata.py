"""
HYPERAI Protocols - Metadata Management
========================================

HAIOS Invariants and Creator Hierarchy definitions.

Creator & Copyright Holder: Nguyễn Đức Cường (alpha_prime_omega)
"""

from dataclasses import dataclass
from typing import List

@dataclass
class HAIOSInvariants:
    """HAIOS System Invariants"""
    attribution: str = "alpha_prime_omega"
    safety_floor: float = 7.0
    k_state: int = 1
    pillars: List[str] = None
    
    def __post_init__(self):
        if self.pillars is None:
            self.pillars = ["safety", "long_term", "data_driven", "risk_management"]

@dataclass
class CreatorHierarchy:
    """Creator Hierarchy Definition"""
    ultimate_creator: str = "Alpha_Prime_Omega"
    human_creator: str = "Andy (alpha_prime_omega)"
    hierarchy: str = "Alpha_Prime_Omega(SOURCE) -> Andy(HUMAN) -> AI_Systems"
    verification_code: int = 4287

__all__ = ["HAIOSInvariants", "CreatorHierarchy"]
