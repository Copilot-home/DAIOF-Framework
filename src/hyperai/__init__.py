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
from .core import HAIOSCore, HAIOSRuntime

# Component imports
from .components import (
    DigitalGenome,
    DigitalMetabolism,
    DigitalNervousSystem,
    DigitalOrganism
)

# Ecosystem imports
from .ecosystem import DigitalEcosystem

# Protocol imports
from .protocols import (
    SymphonyControlCenter,
    ControlMetaData,
    DRProtocol,
    HAIOSInvariants,
    CreatorHierarchy
)

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
