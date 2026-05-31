"""
HYPERAI Framework - Digital Organism System
============================================

A framework for creating self-evolving, self-maintaining AI entities
Philosophy: Biological principles applied to digital systems

Creator & Copyright Holder: Nguyễn Đức Cường (alpha_prime_omega)
Verification Code: 4287
Original Creation Date: October 30, 2025

MIT License: https://opensource.org/licenses/MIT
"""

__version__ = "1.0.0"
__author__ = "Nguyễn Đức Cường (alpha_prime_omega)"
__copyright__ = "Copyright (c) 2025 Nguyễn Đức Cường"

# Core imports
from .core.haios_core import HAIOSCore
from .core.haios_runtime import HAIOSRuntime

# Component imports
from .components.genome import DigitalGenome
from .components.metabolism import DigitalMetabolism
from .components.nervous_system import DigitalNervousSystem
from .components.organism import DigitalOrganism

# Ecosystem imports
from .ecosystem.ecosystem import DigitalEcosystem

# Protocol imports
from .protocols.symphony import SymphonyControlCenter, ControlMetaData
from .protocols.dr_protocol import DRProtocol

# Metadata imports
from .protocols.metadata import HAIOSInvariants, CreatorHierarchy

__all__ = [
    # Core
    "HAIOSCore",
    "HAIOSRuntime",
    
    # Components
    "DigitalGenome",
    "DigitalMetabolism",
    "DigitalNervousSystem",
    "DigitalOrganism",
    
    # Ecosystem
    "DigitalEcosystem",
    
    # Protocols
    "SymphonyControlCenter",
    "ControlMetaData",
    "DRProtocol",
    
    # Metadata
    "HAIOSInvariants",
    "CreatorHierarchy",
]


def main():
    """
    CLI entry point for the HYPERAI Framework.

    Usage:
        hyperai          — Run the default demo showing organism lifecycle
        python -m hyperai — Same as above
    """
    import sys

    print("=" * 60)
    print("🧬 HYPERAI Framework — Digital AI Organism Framework (DAIOF)")
    print(f"   Version: {__version__}")
    print(f"   Creator: {__author__}")
    print("=" * 60)
    print()

    try:
        # Quick health check: instantiate core components
        core = HAIOSCore()
        print(f"✅ HAIOS Core initialized (invariants: {len(core.invariants)})")

        organism = DigitalOrganism(name="demo_organism")
        print(f"✅ Digital Organism '{organism.name}' created (health: {organism.health:.2f})")

        # Run a few lifecycle steps
        for i in range(5):
            organism.live_cycle(time_delta=1.0)
        print(f"✅ Lifecycle running (age: {organism.age}, health: {organism.health:.2f})")

        ecosystem = DigitalEcosystem(name="demo_ecosystem")
        ecosystem.add_organism(organism)
        print(f"✅ Ecosystem '{ecosystem.name}' with {len(ecosystem.organisms)} organism(s)")

        print()
        print("🎯 Framework is healthy and operational.")
        print("   See https://github.com/NguyenCuong1989/DAIOF-Framework for docs.")

    except Exception as exc:
        print(f"❌ Framework health check failed: {exc}", file=sys.stderr)
        sys.exit(1)
