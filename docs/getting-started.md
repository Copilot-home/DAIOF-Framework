---
layout: default
title: Getting Started
---

# Getting Started with DAIOF

## Installation

### Requirements

- Python 3.8 or higher
- NumPy
- Basic understanding of Python OOP

### Install from GitHub

```bash
# Clone repository
git clone https://github.com/NguyenCuong1989/DAIOF-Framework.git
cd DAIOF-Framework

# Install dependencies
pip install -r requirements.txt
```

## Your First Organism

Create a simple digital organism:

```python
from digital_ai_organism_framework import DigitalOrganism

# Create organism
organism = DigitalOrganism()

# Check its genome
print("Immutable Genes:")
for gene, value in organism.genome.IMMUTABLE_GENES.items():
    print(f"  {gene}: {value}")

print("\nMutable Genes:")
for gene in organism.genome.MUTABLE_GENE_RANGES:
    print(f"  {gene}: {organism.genome.genes[gene]:.4f}")
```

## Organism Lifecycle

Simulate an organism's life:

```python
from digital_ai_organism_framework import DigitalOrganism

organism = DigitalOrganism()

for cycle in range(100):
    # Perceive environment
    perception = organism.nervous_system.perceive({
        'temperature': 0.5,
        'resources': 0.8
    })
    
    # Make decision
    action = organism.nervous_system.decide(perception)
    
    # Metabolize
    organism.metabolism.cycle({
        'cpu': 0.1,
        'memory': 0.1,
        'knowledge': 0.05
    })
    
    # Provide human interaction (CRITICAL!)
    if cycle % 10 == 0:
        organism.register_human_interaction()
    
    # Check health
    print(f"Cycle {cycle}: Health = {organism.health:.3f}")
    
    if not organism.alive:
        print(f"Organism died at cycle {cycle}")
        break
```

## Creating an Ecosystem

Multiple organisms working together:

```python
from digital_ai_organism_framework import DigitalEcosystem, DigitalOrganism

# Create ecosystem
ecosystem = DigitalEcosystem()

# Add organisms
for i in range(10):
    ecosystem.add_organism(DigitalOrganism())

# Simulate generations
for generation in range(20):
    ecosystem.simulate_generation()
    
    print(f"Generation {generation}:")
    print(f"  Population: {len(ecosystem.organisms)}")
    print(f"  Harmony: {ecosystem.harmony_index:.3f}")
    print(f"  Avg Health: {ecosystem.average_health:.3f}")
```

## What Happens Without Humans?

See the mandatory human dependency in action:

```python
from digital_ai_organism_framework import DigitalOrganism

organism = DigitalOrganism()

print("Simulating organism WITHOUT human interaction:")
for cycle in range(10):
    organism.metabolism.cycle({'cpu': 0.1, 'memory': 0.1})
    print(f"Cycle {cycle}: Health = {organism.health:.3f}")

# Organism health drops by 99% per cycle!
```

## Next Steps

- [Core Concepts](concepts.html) - Understand the philosophy
- [API Reference](api.html) - Full API documentation
- [Tutorials](tutorials.html) - Step-by-step guides
- [Examples](examples.html) - Real-world use cases

---

## Attribution

**Framework Creator**: Nguyễn Đức Cường (alpha_prime_omega)  
**Original Creation**: October 30, 2025  
**Framework**: HYPERAI - Digital AI Organism Framework  
**License**: MIT License

When using this framework, you MUST credit:
> "Powered by HYPERAI Framework"  
> "Creator: Nguyễn Đức Cường (alpha_prime_omega)"  
> "Original Creation: October 30, 2025"

---

[← Back to Home](index.html)
