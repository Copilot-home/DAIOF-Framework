"""
HYPERAI Protocols - D&R Protocol
=================================

Deconstruction & Re-architecture Protocol for decision making.

Creator & Copyright Holder: Nguyễn Đức Cường (alpha_prime_omega)
"""

# Import from the main framework file (temporary bridge during reorganization)
import sys
from pathlib import Path

# Add root to path
root_dir = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(root_dir))

# D&R Protocol is integrated into SymphonyControlCenter
from digital_ai_organism_framework import SymphonyControlCenter

class DRProtocol:
    """
    D&R Protocol wrapper - delegates to SymphonyControlCenter
    """
    def __init__(self):
        self.symphony = SymphonyControlCenter()
    
    def apply(self, input_data, context="general"):
        """Apply D&R Protocol"""
        return self.symphony.apply_dr_protocol(input_data, context)

__all__ = ["DRProtocol"]
