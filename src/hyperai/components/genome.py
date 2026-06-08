"""
HYPERAI Components - Digital Genome
====================================

Genetic/trait system for digital organisms.

Creator & Copyright Holder: Nguyễn Đức Cường (alpha_prime_omega)
"""

# Import from the main framework file (temporary bridge during reorganization)
import sys
from pathlib import Path

# Add root to path
root_dir = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(root_dir))

from digital_ai_organism_framework import DigitalGenome

__all__ = ["DigitalGenome"]
