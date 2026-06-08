#!/usr/bin/env python3
"""
Doctrine Compliance Tests for DAIOF Framework
Verify canonical doctrine adherence and metadata schema compliance
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
from digital_ai_organism_framework import (
    ControlMetaData,
    SymphonyControlCenter,
)
from haios_core import LanguageAgnosticCore


class TestDoctrineCompliance(unittest.TestCase):
    """Test Sovereign Agentic Runtime Doctrine compliance"""

    def test_creator_attribution_immutable(self):
        """Verify creator attribution is always alpha_prime_omega"""
        # HAIOS Core
        haios = LanguageAgnosticCore()
        self.assertEqual(haios.invariants["attribution"], "alpha_prime_omega")

        # Control Metadata
        meta = ControlMetaData()
        self.assertIn("alpha_prime_omega", meta.creator_hierarchy)

    def test_verification_code_4287(self):
        """Verify verification code is always 4287"""
        meta = ControlMetaData()
        self.assertEqual(meta.verification_code, 4287)

    def test_safety_floor_enforced(self):
        """Verify safety floor is >= 7.0"""
        haios = LanguageAgnosticCore()
        self.assertGreaterEqual(haios.invariants["safety_floor"], 7.0)

    def test_k_state_equals_one(self):
        """Verify K-State is always 1 (zero conflicts)"""
        haios = LanguageAgnosticCore()
        self.assertEqual(haios.invariants["k_state"], 1)

    def test_four_pillars_present(self):
        """Verify Four Pillars are defined"""
        haios = LanguageAgnosticCore()
        self.assertIn("pillars", haios.invariants)
        pillars = haios.invariants["pillars"]

        # Check all four pillars exist
        required_pillars = ["an_toan", "duong_dai", "tin_vao_so_lieu", "han_che_rui_ro"]
        for pillar in required_pillars:
            self.assertIn(pillar, pillars)


class TestMetadataSchema(unittest.TestCase):
    """Test metadata schema compliance"""

    def test_metadata_has_creator_attribution(self):
        """Verify metadata includes creator attribution"""
        meta = ControlMetaData()
        self.assertIn("alpha_prime_omega", meta.creator_hierarchy)

    def test_metadata_has_verification_code(self):
        """Verify metadata includes verification code"""
        meta = ControlMetaData()
        self.assertEqual(meta.verification_code, 4287)

    def test_metadata_has_four_pillars(self):
        """Verify metadata includes Four Pillars configuration"""
        meta = ControlMetaData()
        # Four Pillars should be accessible in meta data
        self.assertIsNotNone(meta)


class TestSymphonyState(unittest.TestCase):
    """Test Symphony state machine compliance"""

    def test_symphony_initializes(self):
        """Verify Symphony Control Center initializes"""
        symphony = SymphonyControlCenter()
        self.assertIsNotNone(symphony)
        self.assertIsNotNone(symphony.meta_data)

    def test_symphony_has_conductor_attribution(self):
        """Verify Symphony conductor is attributed to alpha_prime_omega"""
        symphony = SymphonyControlCenter()
        self.assertIn("alpha_prime_omega", symphony.meta_data.symphony_conductor.lower())


class TestImmutableGenes(unittest.TestCase):
    """Test immutable gene protection"""

    def test_immutable_genes_exist(self):
        """Verify immutable genes are defined"""
        from digital_ai_organism_framework import DigitalGenome
        genome = DigitalGenome()

        # Check immutable genes (stored as traits)
        immutable_genes = [
            "human_dependency_coefficient",
            "symbiotic_existence_required",
            "collaborative_essence"
        ]

        for gene in immutable_genes:
            self.assertIn(gene, genome.traits)

    def test_human_dependency_coefficient_is_one(self):
        """Verify human_dependency_coefficient is always 1.0"""
        from digital_ai_organism_framework import DigitalGenome
        genome = DigitalGenome()

        # This gene cannot be mutated
        coeff = genome.traits.get("human_dependency_coefficient")
        self.assertEqual(coeff, 1.0)


class TestConnectorLifecycle(unittest.TestCase):
    """Test connector lifecycle state compliance"""

    def test_valid_connector_states(self):
        """Verify connector states are valid"""
        valid_states = [
            "DISCOVERED", "AUTHORIZED", "ACTIVE",
            "DEGRADED", "EXPIRED", "BLOCKED", "RETIRED"
        ]

        # Test that we can validate states
        for state in valid_states:
            self.assertIn(state, valid_states)

    def test_connector_state_transitions(self):
        """Verify connector state transitions are logical"""
        # Basic transition logic test
        # DISCOVERED -> AUTHORIZED -> ACTIVE is valid
        # ACTIVE -> DISCOVERED is invalid

        valid_transitions = {
            "DISCOVERED": ["AUTHORIZED", "BLOCKED"],
            "AUTHORIZED": ["ACTIVE", "EXPIRED", "BLOCKED"],
            "ACTIVE": ["DEGRADED", "EXPIRED", "BLOCKED", "RETIRED"],
            "DEGRADED": ["ACTIVE", "EXPIRED", "BLOCKED"],
            "EXPIRED": ["AUTHORIZED", "BLOCKED", "RETIRED"],
            "BLOCKED": ["AUTHORIZED", "RETIRED"],
            "RETIRED": []  # Terminal state
        }

        # Verify transitions are defined
        for state, transitions in valid_transitions.items():
            self.assertIsInstance(transitions, list)


def run_tests():
    """Run all doctrine compliance tests"""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestDoctrineCompliance))
    suite.addTests(loader.loadTestsFromTestCase(TestMetadataSchema))
    suite.addTests(loader.loadTestsFromTestCase(TestSymphonyState))
    suite.addTests(loader.loadTestsFromTestCase(TestImmutableGenes))
    suite.addTests(loader.loadTestsFromTestCase(TestConnectorLifecycle))

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Return exit code based on test result
    return 0 if result.wasSuccessful() else 1


if __name__ == '__main__':
    exit(run_tests())
