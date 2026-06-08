#!/usr/bin/env python3
"""
Digital Ecosystem Service
Runs the digital organism ecosystem cycles
"""

import time
import sys
import os

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    import digital_ai_organism_framework

    print('🌟 Digital Ecosystem Started')
    ecosystem = digital_ai_organism_framework.DigitalEcosystem("HYPERAI_Ecosystem")

    while True:
        try:
            # Run ecosystem cycle
            result = ecosystem.run_cycle()
            print(f'🔄 Ecosystem Cycle: {result}')

            time.sleep(120)  # Run every 2 minutes
        except Exception as e:
            print(f'❌ Ecosystem Error: {e}')
            time.sleep(60)

except ImportError as e:
    print(f'❌ Import Error: {e}')
    print('Available modules:', [m for m in sys.modules.keys() if 'digital' in m])
    sys.exit(1)