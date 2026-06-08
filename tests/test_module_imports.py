#!/usr/bin/env python3
"""
Module Import Tests - Verify hyperai module structure
====================================================

Tests the new modular structure in src/hyperai/

Creator: Nguyễn Đức Cường (alpha_prime_omega)
Verification: 4287
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest


class TestModuleImports(unittest.TestCase):
    """Test that all module imports work correctly"""
    
    def test_core_imports(self):
        """Test core module imports"""
        try:
            from src.hyperai import HAIOSCore, HAIOSRuntime
            self.assertIsNotNone(HAIOSCore)
            self.assertIsNotNone(HAIOSRuntime)
        except ImportError as e:
            self.fail(f"Core imports failed: {e}")
    
    def test_component_imports(self):
        """Test component module imports"""
        try:
            from src.hyperai import (
                DigitalGenome,
                DigitalMetabolism,
                DigitalNervousSystem,
                DigitalOrganism
            )
            self.assertIsNotNone(DigitalGenome)
            self.assertIsNotNone(DigitalMetabolism)
            self.assertIsNotNone(DigitalNervousSystem)
            self.assertIsNotNone(DigitalOrganism)
        except ImportError as e:
            self.fail(f"Component imports failed: {e}")
    
    def test_ecosystem_imports(self):
        """Test ecosystem module imports"""
        try:
            from src.hyperai import DigitalEcosystem
            self.assertIsNotNone(DigitalEcosystem)
        except ImportError as e:
            self.fail(f"Ecosystem imports failed: {e}")
    
    def test_protocol_imports(self):
        """Test protocol module imports"""
        try:
            from src.hyperai import (
                SymphonyControlCenter,
                ControlMetaData,
                DRProtocol
            )
            self.assertIsNotNone(SymphonyControlCenter)
            self.assertIsNotNone(ControlMetaData)
            self.assertIsNotNone(DRProtocol)
        except ImportError as e:
            self.fail(f"Protocol imports failed: {e}")
    
    def test_metadata_imports(self):
        """Test metadata imports"""
        try:
            from src.hyperai import HAIOSInvariants, CreatorHierarchy
            self.assertIsNotNone(HAIOSInvariants)
            self.assertIsNotNone(CreatorHierarchy)
        except ImportError as e:
            self.fail(f"Metadata imports failed: {e}")
    
    def test_haios_core_instantiation(self):
        """Test that HAIOSCore can be instantiated"""
        from src.hyperai import HAIOSCore
        core = HAIOSCore()
        self.assertIsNotNone(core.invariants)
        self.assertEqual(core.invariants["attribution"], "alpha_prime_omega")
        self.assertEqual(core.invariants["k_state"], 1)
    
    def test_digital_organism_creation(self):
        """Test that DigitalOrganism can be created from module import"""
        from src.hyperai import DigitalOrganism
        organism = DigitalOrganism(name="test_module_organism")
        self.assertEqual(organism.name, "test_module_organism")
        self.assertIsNotNone(organism.genome)
    
    def test_symphony_control_instantiation(self):
        """Test Symphony Control Center from module import"""
        from src.hyperai import SymphonyControlCenter
        symphony = SymphonyControlCenter()
        self.assertIsNotNone(symphony.meta_data)
    
    def test_backward_compatibility(self):
        """Test that old root-level imports still work"""
        try:
            from digital_ai_organism_framework import (
                DigitalOrganism as OldOrganism,
                DigitalGenome as OldGenome
            )
            from haios_core import LanguageAgnosticCore as OldCore
            
            self.assertIsNotNone(OldOrganism)
            self.assertIsNotNone(OldGenome)
            self.assertIsNotNone(OldCore)
        except ImportError as e:
            self.fail(f"Backward compatibility broken: {e}")


class TestModuleStructure(unittest.TestCase):
    """Test module structure integrity"""
    
    def test_module_all_exports(self):
        """Test that __all__ exports are correct"""
        import src.hyperai
        
        # Check that key exports are in __all__
        expected_exports = [
            "HAIOSCore",
            "DigitalOrganism",
            "DigitalEcosystem",
            "SymphonyControlCenter",
        ]
        
        for export in expected_exports:
            self.assertIn(export, src.hyperai.__all__)
    
    def test_version_and_metadata(self):
        """Test module version and metadata"""
        import src.hyperai
        
        self.assertTrue(hasattr(src.hyperai, '__version__'))
        self.assertTrue(hasattr(src.hyperai, '__author__'))
        self.assertEqual(src.hyperai.__author__, "Nguyễn Đức Cường (alpha_prime_omega)")


def run_tests():
    """Run all module tests"""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    suite.addTests(loader.loadTestsFromTestCase(TestModuleImports))
    suite.addTests(loader.loadTestsFromTestCase(TestModuleStructure))
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return 0 if result.wasSuccessful() else 1


if __name__ == '__main__':
    exit(run_tests())
