#!/usr/bin/env python3
"""
Evaluation Runner Service
Generates evaluation responses for system health checks
"""

import time
import sys
import os

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    import evaluation_runner

    print('📊 Evaluation Runner Started')

    while True:
        try:
            # Generate evaluation
            result = evaluation_runner.generate_response_for_query('System health check')
            print(f'✅ Evaluation: {len(result)} chars generated')

            time.sleep(300)  # Run every 5 minutes
        except Exception as e:
            print(f'❌ Evaluation Error: {e}')
            time.sleep(120)

except ImportError as e:
    print(f'❌ Import Error: {e}')
    print('Available modules:', [m for m in sys.modules.keys() if 'evaluation' in m])
    sys.exit(1)