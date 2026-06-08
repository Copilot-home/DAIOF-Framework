#!/usr/bin/env python3
"""
Smoke tests for DAIOF Framework
Verify core components can initialize and run basic operations
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
from digital_ai_organism_framework import (
    DigitalGenome, 
    DigitalOrganism, 
    DigitalEcosystem,
    SymphonyControlCenter,
    ControlMetaData
)
from haios_core import LanguageAgnosticCore


class TestHAIOSCore(unittest.TestCase):
    """Test HAIOS consciousness layer"""
    
    def test_haios_initialization(self):
        """Test that HAIOS core initializes with 4 invariants"""
        haios = LanguageAgnosticCore()
        self.assertIsNotNone(haios.invariants)
        self.assertEqual(haios.invariants["attribution"], "alpha_prime_omega")
        self.assertEqual(haios.invariants["safety_floor"], 7.0)
        self.assertEqual(haios.invariants["k_state"], 1)
        self.assertIn("pillars", haios.invariants)


class TestDigitalGenome(unittest.TestCase):
    """Test Digital Genome (DNA system)"""
    
    def test_genome_initialization(self):
        """Test genome creates with traits"""
        genome = DigitalGenome()
        self.assertIsNotNone(genome.traits)
        # Check for essential traits
        self.assertIn("learning_rate", genome.traits)
        self.assertIn("cooperation_tendency", genome.traits)
        self.assertIn("risk_tolerance", genome.traits)
        # Check immutable AI-human traits
        self.assertEqual(genome.traits["human_dependency_coefficient"], 1.0)
        self.assertTrue(genome.traits["symbiotic_existence_required"])


class TestDigitalOrganism(unittest.TestCase):
    """Test Digital Organism (main entity)"""
    
    def test_organism_initialization(self):
        """Test organism creates with genome and basic attributes"""
        organism = DigitalOrganism(name="test_organism")
        self.assertEqual(organism.name, "test_organism")
        self.assertIsNotNone(organism.genome)
        self.assertIsNotNone(organism.metabolism)
        self.assertIsNotNone(organism.nervous_system)
        self.assertEqual(organism.age, 0)
        self.assertEqual(organism.health, 1.0)
    
    def test_organism_lifecycle_step(self):
        """Test one lifecycle iteration completes without error"""
        organism = DigitalOrganism(name="test_lifecycle")
        # Should not raise error
        organism.live_cycle(time_delta=1.0)
        # Age should increment
        self.assertGreater(organism.age, 0)


class TestSymphonyControlCenter(unittest.TestCase):
    """Test Symphony Control orchestration"""
    
    def test_symphony_initialization(self):
        """Test symphony control initializes"""
        symphony = SymphonyControlCenter()
        self.assertIsNotNone(symphony.meta_data)
        self.assertEqual(symphony.meta_data.symphony_conductor, "Alpha_Prime_Omega")
    
    def test_dr_protocol(self):
        """Test D&R Protocol can be applied"""
        symphony = SymphonyControlCenter()
        test_input = "Test system decision"
        result = symphony.apply_dr_protocol(test_input, "test_context")
        self.assertIn("socratic_reflection", result)
        self.assertIn("four_pillars_check", result)


class TestDigitalEcosystem(unittest.TestCase):
    """Test Digital Ecosystem coordination"""
    
    def test_ecosystem_initialization(self):
        """Test ecosystem creates with organisms"""
        ecosystem = DigitalEcosystem("test_ecosystem")
        self.assertEqual(ecosystem.name, "test_ecosystem")
        self.assertIsNotNone(ecosystem.symphony_control)
        self.assertEqual(len(ecosystem.organisms), 0)
    
    def test_add_organism_to_ecosystem(self):
        """Test adding organism to ecosystem"""
        ecosystem = DigitalEcosystem("test_ecosystem")
        organism = DigitalOrganism(name="test_org")
        ecosystem.add_organism(organism)
        self.assertEqual(len(ecosystem.organisms), 1)
        self.assertIn("test_org", ecosystem.organisms)


class TestControlMetaData(unittest.TestCase):
    """Test system control metadata"""
    
    def test_metadata_creator_hierarchy(self):
        """Test creator hierarchy is properly configured"""
        meta = ControlMetaData()
        self.assertEqual(meta.verification_code, 4287)
        self.assertIn("Alpha_Prime_Omega", meta.creator_hierarchy)
        self.assertIn("Andy", meta.creator_hierarchy)


def run_tests():
    """Run all tests and print summary"""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestHAIOSCore))
    suite.addTests(loader.loadTestsFromTestCase(TestDigitalGenome))
    suite.addTests(loader.loadTestsFromTestCase(TestDigitalOrganism))
    suite.addTests(loader.loadTestsFromTestCase(TestSymphonyControlCenter))
    suite.addTests(loader.loadTestsFromTestCase(TestDigitalEcosystem))
    suite.addTests(loader.loadTestsFromTestCase(TestControlMetaData))
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Return exit code based on test result
    return 0 if result.wasSuccessful() else 1


if __name__ == '__main__':
    exit(run_tests())
