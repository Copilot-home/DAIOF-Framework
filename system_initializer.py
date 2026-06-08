#!/usr/bin/env python3
"""
System Initializer - DAIOF Framework
Tuân thủ D&R Protocol & 4 Trụ cột
Creator: Nguyễn Đức Cường (alpha_prime_omega)
"""

import logging
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Any

from haios_core import LanguageAgnosticCore
from digital_ai_organism_framework import (
    ControlMetaData,
    SymphonyControlCenter,
    DigitalEcosystem,
    SymphonyState
)

def setup_logging():
    """Setup logging system với creator recognition"""
    logger = logging.getLogger("DAIOF_Initializer")
    logger.setLevel(logging.INFO)
    
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            '🎼[DAIOF] %(asctime)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    
    return logger

def initialize_full_system(logger: logging.Logger) -> Dict[str, Any]:
    """
    Khởi tạo toàn bộ hệ thống theo D&R Protocol
    Returns: Dict containing all system components
    """
    # 1. HAIOS Core
    logger.info("🧬 Initializing HAIOS Core...")
    haios = LanguageAgnosticCore()
    logger.info("✅ HAIOS Core activated")
    
    # 2. Control Metadata
    logger.info("🎯 Configuring Control Metadata...")
    meta = ControlMetaData(
        creator="Nguyễn Đức Cường (alpha_prime_omega)",
        verification_code=4287,
        framework_name="HYPERAI Framework",
        license_type="MIT License"
    )
    # Setup extended creator attributes
    meta.creator = "Andy (alpha_prime_omega)"
    # Unified creator field - no separation
    meta.creator_hierarchy = "Alpha_Prime_Omega(USER) -> Andy(HUMAN=CREATOR) -> AI_Systems"
    logger.info("✅ Control Metadata configured")
    
    # 3. Symphony Control
    logger.info("🎼 Initializing Symphony Control...")
    symphony = SymphonyControlCenter()
    symphony.meta_data = meta
    symphony.register_component("haios_core", haios)
    logger.info("✅ Symphony Control online")
    
    # 4. Digital Ecosystem
    logger.info("🌱 Creating Digital Ecosystem...")
    ecosystem = DigitalEcosystem("PrimaryEcosystem")
    ecosystem.symphony_control = symphony
    logger.info("✅ Digital Ecosystem created")
    
    # 5. System Health Check
    health_check = {
        "haios_status": haios.invariants["k_state"] == 1,
        "symphony_state": symphony.meta_data.symphony_state == SymphonyState.PERFORMING,
        "ecosystem_health": ecosystem.environment_parameters["resource_abundance"] == 1.0
    }
    
    if all(health_check.values()):
        logger.info("🎉 Full system initialization successful!")
    else:
        logger.warning("⚠️ System initialized with warnings")
        logger.info(f"Health check results: {health_check}")
    
    return {
        "haios": haios,
        "symphony": symphony,
        "ecosystem": ecosystem,
        "health_check": health_check
    }

def main():
    """Main execution function"""
    logger = setup_logging()
    
    logger.info("=" * 50)
    logger.info("🚀 DAIOF SYSTEM INITIALIZATION")
    logger.info("Creator: Nguyễn Đức Cường (alpha_prime_omega)")
    logger.info("=" * 50)
    
    try:
        system = initialize_full_system(logger)
        
        # Save initialization report
        report_path = Path("system_initialization_report.json")
        with open(report_path, "w") as f:
            json.dump({
                "timestamp": datetime.now().isoformat(),
                "health_check": system["health_check"]
            }, f, indent=2)
        
        logger.info(f"📝 Initialization report saved to {report_path}")
        
    except Exception as e:
        logger.error(f"❌ Initialization failed: {str(e)}")
        raise

if __name__ == "__main__":
    main()