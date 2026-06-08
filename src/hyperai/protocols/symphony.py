#!/usr/bin/env python3
"""
Symphony Control Center - System Orchestration

Creator: Nguyễn Đức Cường (alpha_prime_omega)
Original Creation: October 30, 2025
Verification: 4287
"""

import sys
from pathlib import Path

# Add root directory to path to import from root-level modules
root_dir = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(root_dir))

# Import from root-level implementation
from digital_ai_organism_framework import SymphonyControlCenter, ControlMetaData, SymphonyState

__all__ = ["SymphonyControlCenter", "ControlMetaData", "SymphonyState"]
"""
HYPERAI Protocols - Symphony Control Center

Symphony orchestration, control metadata, and system state management.

Creator & Copyright Holder: Nguyễn Đức Cường (alpha_prime_omega)
"""

# Import from the main framework file (temporary bridge during reorganization)
import sys
from pathlib import Path

# Add root to path to import from digital_ai_organism_framework
root_dir = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(root_dir))

from digital_ai_organism_framework import (
    SymphonyState,
    ControlMetaData,
    SymphonyControlCenter
)

__all__ = [
    "SymphonyState",
    "ControlMetaData",
    "SymphonyControlCenter",
]
