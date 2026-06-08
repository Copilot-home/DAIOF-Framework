#!/usr/bin/env python3
"""
Integration tests for DAIOF Framework
Verify end-to-end workflows: lifecycle, ecosystem evolution, D&R protocol,
and 4 Pillars scoring with real data.
"""

import sys
import os
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from digital_ai_organism_framework import (
    DigitalGenome,
    DigitalOrganism,
    DigitalEcosystem,
    SymphonyControlCenter,
    ControlMetaData,
)
from haios_core import LanguageAgnosticCore


class TestOrganismLifecycle(unittest.TestCase):
    """Multi-step organism lifecycle tests."""

    def test_organism_survives_100_cycles(self):
        """Organism should survive 100 lifecycle iterations with health >= 0."""
        organism = DigitalOrganism(name="endurance_test")
        for _ in range(100):
            organism.live_cycle(time_delta=1.0)
        self.assertGreaterEqual(organism.health, 0, "Organism health went negative")
        self.assertGreater(organism.age, 0, "Organism should have aged")

    def test_organism_metabolism_consumes_resources(self):
        """After multiple metabolism operations the resource state should change."""
        organism = DigitalOrganism(name="metabolism_test")
        initial_health = organism.metabolism.get_resource_health()
        for _ in range(20):
            organism.metabolism.consume_resources("think", amount=1.0)
        after_health = organism.metabolism.get_resource_health()
        self.assertLess(after_health, initial_health, "Resources should decrease after consumption")

    def test_genome_immutable_genes_cannot_change(self):
        """Immutable genes must retain their values after mutations."""
        genome = DigitalGenome()
        # human_dependency_coefficient is immutable
        original = genome.traits["human_dependency_coefficient"]
        # Run some mutations
        for _ in range(50):
            genome.mutate()
        self.assertEqual(
            genome.traits["human_dependency_coefficient"],
            original,
            "Immutable gene was mutated!",
        )


class TestEcosystemEvolution(unittest.TestCase):
    """Multi-organism ecosystem tests."""

    def test_ecosystem_multi_generation(self):
        """Ecosystem should handle 10 simulation steps without crashing."""
        eco = DigitalEcosystem(name="evolution_test")
        for i in range(5):
            eco.add_organism(DigitalOrganism(name=f"org_{i}"))
        for _ in range(10):
            eco.simulate_time_step(time_delta=1.0)
        self.assertGreaterEqual(len(eco.organisms), 1, "All organisms died")

    def test_ecosystem_add_and_remove(self):
        """Adding and removing organisms should be consistent."""
        eco = DigitalEcosystem(name="add_remove_test")
        org = DigitalOrganism(name="temp_org")
        eco.add_organism(org)
        self.assertIn("temp_org", eco.organisms)
        self.assertEqual(len(eco.organisms), 1)


class TestDRProtocolIntegration(unittest.TestCase):
    """D&R Protocol end-to-end tests."""

    def test_dr_protocol_returns_all_phases(self):
        """apply_dr_protocol must return deconstructed, focal_point, and optimized_solution."""
        symphony = SymphonyControlCenter()
        result = symphony.apply_dr_protocol(
            "We need a safe data-driven solution for long-term risk mitigation",
            context="integration_test",
        )
        self.assertIn("deconstructed", result)
        self.assertIn("focal_point", result)
        self.assertIn("optimized_solution", result)
        self.assertIn("four_pillars_check", result)
        self.assertIn("socratic_reflection", result)
        self.assertIn("creator_signature", result)

    def test_dr_protocol_pillar_scores_are_numeric(self):
        """Focal-point pillar_scores should be floats in [0, 1]."""
        symphony = SymphonyControlCenter()
        result = symphony.apply_dr_protocol("safe future data protect", "score_test")
        scores = result["focal_point"]["pillar_scores"]
        for pillar, score in scores.items():
            self.assertIsInstance(score, float, f"{pillar} score is not float")
            self.assertGreaterEqual(score, 0.0, f"{pillar} score < 0")
            self.assertLessEqual(score, 1.0, f"{pillar} score > 1")


class TestFourPillarsValidation(unittest.TestCase):
    """Verify that 4 Pillars scoring returns numeric scores, not just booleans."""

    def setUp(self):
        self.symphony = SymphonyControlCenter()

    def test_pillars_return_scores_and_composite(self):
        """_validate_four_pillars should return score floats and composite."""
        solution = {
            "plan": "Deploy safe backup with data metrics and risk mitigation for long-term sustainability"
        }
        result = self.symphony._validate_four_pillars(solution)
        # Must have score keys
        self.assertIn("safety_score", result)
        self.assertIn("long_term_score", result)
        self.assertIn("data_driven_score", result)
        self.assertIn("risk_score", result)
        self.assertIn("composite_score", result)
        self.assertIn("composite_pass", result)
        # Scores should be floats
        for key in ["safety_score", "long_term_score", "data_driven_score", "risk_score", "composite_score"]:
            self.assertIsInstance(result[key], float, f"{key} should be float")

    def test_pillars_empty_input_returns_zero(self):
        """Empty input should yield zero scores."""
        result = self.symphony._validate_four_pillars({})
        self.assertEqual(result["safety_score"], 0.0)
        self.assertEqual(result["composite_score"], 0.0)
        self.assertFalse(result["composite_pass"])

    def test_pillars_safety_heavy_input(self):
        """Safety-heavy input should have high safety_score."""
        solution = "safe secure protect validate rollback backup"
        result = self.symphony._validate_four_pillars(solution)
        self.assertGreater(result["safety_score"], 0.0)


class TestHAIOSInvariants(unittest.TestCase):
    """Verify HAIOS invariants are enforced."""

    def test_attribution_is_immutable(self):
        haios = LanguageAgnosticCore()
        self.assertEqual(haios.invariants["attribution"], "alpha_prime_omega")

    def test_safety_floor(self):
        haios = LanguageAgnosticCore()
        self.assertGreaterEqual(haios.invariants["safety_floor"], 7.0)

    def test_k_state_is_one(self):
        haios = LanguageAgnosticCore()
        self.assertEqual(haios.invariants["k_state"], 1)

    def test_four_pillars_present(self):
        haios = LanguageAgnosticCore()
        pillars = haios.invariants["pillars"]
        self.assertIn("an_toan", pillars)
        self.assertIn("duong_dai", pillars)
        self.assertIn("tin_vao_so_lieu", pillars)
        self.assertIn("han_che_rui_ro", pillars)


if __name__ == "__main__":
    unittest.main()
