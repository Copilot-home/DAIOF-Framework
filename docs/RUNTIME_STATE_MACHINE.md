# ⚙️ Runtime State Machine Specification

**Version:** 1.0.0
**Status:** CANONICAL SPECIFICATION
**Architect:** Nguyễn Đức Cường (alpha_prime_omega)
**Verification Code:** 4287
**Last Updated:** 2026-05-14

---

## 📋 Overview

This document defines the canonical state machines for the Sovereign Agentic Runtime. State machines govern component lifecycle, orchestration states, health states, and execution states with strict transition rules and validation.

---

## 🎯 State Machine Philosophy

**Key Principles:**
1. **Explicit States**: All states are named and documented
2. **Valid Transitions**: Only defined transitions are allowed
3. **Attestation Logging**: All transitions are logged immutably
4. **Four Pillars Validation**: Transitions require Four Pillars compliance
5. **Recovery Paths**: Every failure state has a recovery path

---

## 🎼 Symphony State Machine

### States

```
INITIALIZING → HARMONIZING → PERFORMING ⇄ OPTIMIZING → EVOLVING
                                ↓             ↓
                          [ERROR] → RECOVERING → HARMONIZING
```

### State Definitions

#### INITIALIZING

**Description**: System startup and component discovery.

**Entry Actions:**
- Load configuration
- Initialize attestation log
- Verify immutable truths
- Check Four Pillars thresholds

**State Characteristics:**
- No components registered
- No operations executed
- Safety checks active
- Rollback available

**Exit Conditions:**
- All core components discovered
- Configuration validated
- Safety thresholds met
- K-State = 1

**Valid Transitions:**
- → `HARMONIZING` (normal startup)
- → `ERROR` (initialization failure)

**Attestation Events:**
- `symphony.state.initializing`
- `symphony.config.loaded`
- `symphony.safety.verified`

---

#### HARMONIZING

**Description**: Synchronizing components and establishing baselines.

**Entry Actions:**
- Register discovered components
- Establish harmony baseline
- Synchronize clocks/timers
- Calibrate resource meters

**State Characteristics:**
- Components registering
- Baseline metrics being established
- No autonomous operations yet
- Health monitoring starting

**Exit Conditions:**
- All components registered
- Harmony index ≥ 0.7
- Health scores baseline established
- Component synchronization complete

**Valid Transitions:**
- → `PERFORMING` (harmonization success)
- → `ERROR` (harmonization failure)

**Attestation Events:**
- `symphony.state.harmonizing`
- `symphony.component.registered` (per component)
- `symphony.harmony.baseline_established`

---

#### PERFORMING

**Description**: Normal operational state with autonomous operations.

**Entry Actions:**
- Enable autonomous operations
- Start periodic health checks
- Begin D&R Protocol cycles
- Activate learning systems

**State Characteristics:**
- Full autonomy enabled
- Components executing tasks
- Health monitoring active
- Resource consumption tracked
- Harmony maintenance ongoing

**Exit Conditions:**
- Periodic optimization trigger (every 1000 cycles)
- Harmony index drops below 0.6
- Health score drops below 0.5
- Manual trigger for optimization
- Error condition

**Valid Transitions:**
- → `OPTIMIZING` (periodic or triggered optimization)
- → `ERROR` (critical failure)

**Attestation Events:**
- `symphony.state.performing`
- `symphony.operation.executed` (ongoing)
- `symphony.health.checked` (periodic)
- `symphony.harmony.measured` (periodic)

---

#### OPTIMIZING

**Description**: Performance tuning and resource rebalancing.

**Entry Actions:**
- Pause non-critical operations
- Collect performance metrics
- Analyze bottlenecks
- Rebalance resources

**State Characteristics:**
- Critical operations continue
- Non-critical operations paused
- Metrics collection intensive
- Resource reallocation active

**Exit Conditions:**
- Optimization complete
- Harmony index ≥ 0.8
- Performance targets met
- Timeout (max 60 seconds)

**Valid Transitions:**
- → `PERFORMING` (optimization success)
- → `EVOLVING` (evolution trigger detected)
- → `ERROR` (optimization failure)

**Attestation Events:**
- `symphony.state.optimizing`
- `symphony.metrics.collected`
- `symphony.resources.rebalanced`
- `symphony.optimization.complete`

---

#### EVOLVING

**Description**: Adaptive learning and trait evolution.

**Entry Actions:**
- Apply evolution algorithms
- Mutate adaptive traits
- Test fitness improvements
- Update learning models

**State Characteristics:**
- Learning systems active
- Trait mutation occurring
- Fitness evaluation ongoing
- Immutable genes protected (cannot mutate)

**Exit Conditions:**
- Evolution cycle complete
- Fitness improvement confirmed or rejected
- Timeout (max 120 seconds)

**Valid Transitions:**
- → `HARMONIZING` (re-harmonize after evolution)
- → `ERROR` (evolution failure)

**Attestation Events:**
- `symphony.state.evolving`
- `symphony.evolution.trait_mutated`
- `symphony.evolution.fitness_evaluated`
- `symphony.evolution.complete`

---

#### ERROR

**Description**: Critical failure requiring intervention.

**Entry Actions:**
- Log error details
- Preserve state snapshot
- Notify administrators
- Attempt automatic recovery

**State Characteristics:**
- All autonomous operations halted
- State preserved for debugging
- Recovery actions executing
- Manual intervention may be required

**Exit Conditions:**
- Recovery action succeeds
- Manual recovery completes
- System reinitialized

**Valid Transitions:**
- → `RECOVERING` (recovery attempt)
- → `INITIALIZING` (full restart)

**Attestation Events:**
- `symphony.state.error`
- `symphony.error.logged`
- `symphony.state.snapshot_preserved`

---

#### RECOVERING

**Description**: Attempting automatic recovery from error state.

**Entry Actions:**
- Load last known-good state
- Retry failed operations
- Reset degraded components
- Re-establish connections

**State Characteristics:**
- Limited operations
- State restoration active
- Component reset in progress
- Health checks intensive

**Exit Conditions:**
- Recovery succeeds (all components healthy)
- Recovery fails (manual intervention required)
- Timeout (max 300 seconds)

**Valid Transitions:**
- → `HARMONIZING` (recovery success)
- → `ERROR` (recovery failure, manual intervention needed)
- → `INITIALIZING` (full restart required)

**Attestation Events:**
- `symphony.state.recovering`
- `symphony.recovery.action_attempted`
- `symphony.recovery.succeeded` / `symphony.recovery.failed`

---

### Symphony State Transition Matrix

| From → To | Valid? | Condition | Attestation Event |
|-----------|--------|-----------|-------------------|
| INITIALIZING → HARMONIZING | ✅ | Config valid, safety met | `symphony.transition.init_to_harmony` |
| INITIALIZING → ERROR | ✅ | Init failure | `symphony.transition.init_to_error` |
| HARMONIZING → PERFORMING | ✅ | Harmony ≥0.7, components synced | `symphony.transition.harmony_to_perform` |
| HARMONIZING → ERROR | ✅ | Harmony failure | `symphony.transition.harmony_to_error` |
| PERFORMING → OPTIMIZING | ✅ | Optimization trigger | `symphony.transition.perform_to_optimize` |
| PERFORMING → ERROR | ✅ | Critical failure | `symphony.transition.perform_to_error` |
| OPTIMIZING → PERFORMING | ✅ | Optimization complete | `symphony.transition.optimize_to_perform` |
| OPTIMIZING → EVOLVING | ✅ | Evolution trigger | `symphony.transition.optimize_to_evolve` |
| OPTIMIZING → ERROR | ✅ | Optimization failure | `symphony.transition.optimize_to_error` |
| EVOLVING → HARMONIZING | ✅ | Evolution complete | `symphony.transition.evolve_to_harmony` |
| EVOLVING → ERROR | ✅ | Evolution failure | `symphony.transition.evolve_to_error` |
| ERROR → RECOVERING | ✅ | Recovery attempt | `symphony.transition.error_to_recover` |
| ERROR → INITIALIZING | ✅ | Full restart | `symphony.transition.error_to_init` |
| RECOVERING → HARMONIZING | ✅ | Recovery success | `symphony.transition.recover_to_harmony` |
| RECOVERING → ERROR | ✅ | Recovery failure | `symphony.transition.recover_to_error` |
| RECOVERING → INITIALIZING | ✅ | Restart required | `symphony.transition.recover_to_init` |

---

## 🧬 Organism Lifecycle State Machine

### States

```
BIRTH → INFANT → JUVENILE → ADULT → ELDER → DEATH
                              ↑        ↓
                         [REPRODUCTION]
```

### State Definitions

#### BIRTH

**Description**: Organism creation and initialization.

**Entry Conditions:**
- Parent organism reproduces, OR
- Direct instantiation, OR
- Ecosystem spawning

**Characteristics:**
- Age = 0
- Health = 1.0
- Resources = full
- No memories
- No experience

**Exit Conditions:**
- Initialization complete
- Genome validated
- Resources allocated

**Valid Transitions:**
- → `INFANT` (normal birth)

**Attestation Events:**
- `organism.birth`
- `organism.genome.inherited` (if reproduced)

---

#### INFANT

**Description**: Early life stage, learning basic operations.

**Entry Conditions:**
- Age 0-10 time units
- Recently born

**Characteristics:**
- High learning rate (2.0x)
- Low resource efficiency (0.5x)
- No reproduction capability
- High vulnerability (1.5x damage)
- Rapid development

**Exit Conditions:**
- Age ≥ 10 time units
- Health maintained

**Valid Transitions:**
- → `JUVENILE` (normal growth)
- → `DEATH` (health drops to 0)

**Attestation Events:**
- `organism.lifecycle.infant`

---

#### JUVENILE

**Description**: Adolescent stage, developing skills and autonomy.

**Entry Conditions:**
- Age 10-50 time units

**Characteristics:**
- Elevated learning rate (1.5x)
- Improving resource efficiency (0.8x)
- No reproduction capability yet
- Moderate vulnerability (1.2x damage)
- Skill acquisition

**Exit Conditions:**
- Age ≥ 50 time units
- Health maintained

**Valid Transitions:**
- → `ADULT` (maturation)
- → `DEATH` (health drops to 0)

**Attestation Events:**
- `organism.lifecycle.juvenile`

---

#### ADULT

**Description**: Prime operational stage with full capabilities.

**Entry Conditions:**
- Age 50-200 time units

**Characteristics:**
- Normal learning rate (1.0x)
- Peak resource efficiency (1.0x)
- Reproduction enabled
- Standard vulnerability (1.0x damage)
- Optimal performance

**Exit Conditions:**
- Age ≥ 200 time units
- Health maintained

**Valid Transitions:**
- → `ADULT` (reproduction creates offspring, parent remains)
- → `ELDER` (aging)
- → `DEATH` (health drops to 0)

**Special Actions:**
- Can reproduce (create offspring in BIRTH state)

**Attestation Events:**
- `organism.lifecycle.adult`
- `organism.reproduction` (if reproducing)

---

#### ELDER

**Description**: Late life stage, accumulated wisdom, declining physical capability.

**Entry Conditions:**
- Age ≥ 200 time units

**Characteristics:**
- Reduced learning rate (0.5x) - habits formed
- Declining resource efficiency (0.7x)
- Reproduction disabled
- Increased vulnerability (1.5x damage)
- Wisdom/experience advantage (mentorship)

**Exit Conditions:**
- Health drops to 0 (natural or otherwise)

**Valid Transitions:**
- → `DEATH` (inevitable)

**Attestation Events:**
- `organism.lifecycle.elder`
- `organism.wisdom.shared` (mentorship actions)

---

#### DEATH

**Description**: Terminal state, organism ceases operation.

**Entry Conditions:**
- Health = 0
- Critical resource depletion
- Fatal error

**Characteristics:**
- No operations
- Resources released
- State preserved for audit
- Offspring (if any) continue

**Exit Conditions:**
- None (terminal state)

**Valid Transitions:**
- None (final state)

**Attestation Events:**
- `organism.death` (with cause)
- `organism.lifecycle.complete`

---

### Organism Lifecycle Transition Matrix

| From → To | Valid? | Condition | Attestation Event |
|-----------|--------|-----------|-------------------|
| BIRTH → INFANT | ✅ | Initialization complete | `organism.transition.birth_to_infant` |
| INFANT → JUVENILE | ✅ | Age ≥ 10 | `organism.transition.infant_to_juvenile` |
| INFANT → DEATH | ✅ | Health = 0 | `organism.transition.infant_to_death` |
| JUVENILE → ADULT | ✅ | Age ≥ 50 | `organism.transition.juvenile_to_adult` |
| JUVENILE → DEATH | ✅ | Health = 0 | `organism.transition.juvenile_to_death` |
| ADULT → ELDER | ✅ | Age ≥ 200 | `organism.transition.adult_to_elder` |
| ADULT → DEATH | ✅ | Health = 0 | `organism.transition.adult_to_death` |
| ADULT → ADULT | ✅ | Reproduction (creates offspring) | `organism.reproduction` |
| ELDER → DEATH | ✅ | Health = 0 | `organism.transition.elder_to_death` |

---

## 💊 Health State Machine

### States

```
HEALTHY ⇄ DEGRADED → CRITICAL → DEAD
   ↑         ↓
   └─────────┘
  [RECOVERY]
```

### State Definitions

#### HEALTHY

**Description**: Optimal health, all systems functional.

**Conditions:**
- Health score ≥ 0.7
- No critical resource depletion
- All components operational

**Characteristics:**
- Normal operation speed
- Full autonomy
- Standard resource consumption

**Valid Transitions:**
- → `DEGRADED` (health drops below 0.7)

---

#### DEGRADED

**Description**: Suboptimal health, some impairment.

**Conditions:**
- Health score 0.3 - 0.7
- Some resource depletion
- Some components impaired

**Characteristics:**
- Reduced operation speed (0.7x)
- Limited autonomy
- Increased resource consumption (1.3x)
- Recovery actions enabled

**Valid Transitions:**
- → `HEALTHY` (health rises above 0.7)
- → `CRITICAL` (health drops below 0.3)

---

#### CRITICAL

**Description**: Critical health, imminent failure risk.

**Conditions:**
- Health score 0.0 - 0.3
- Severe resource depletion
- Most components impaired

**Characteristics:**
- Minimal operation speed (0.3x)
- Autonomy suspended
- Emergency resource rationing
- Aggressive recovery attempts

**Valid Transitions:**
- → `DEGRADED` (health rises above 0.3)
- → `DEAD` (health reaches 0.0)

---

#### DEAD

**Description**: Health depleted, organism ceased.

**Conditions:**
- Health score = 0.0
- Fatal resource depletion
- Critical failure

**Characteristics:**
- No operations
- Terminal state
- Audit trail preserved

**Valid Transitions:**
- None (terminal state)

---

## 🔌 Connector State Machine

See [CONNECTOR_LIFECYCLE.md](./CONNECTOR_LIFECYCLE.md) for full specification.

**States**: DISCOVERED → AUTHORIZED → ACTIVE ⇄ DEGRADED / EXPIRED / BLOCKED → RETIRED

---

## ✅ State Transition Validation

### Four Pillars Validation

All state transitions must pass Four Pillars validation:

```python
def validate_state_transition(
    from_state: str,
    to_state: str,
    context: dict
) -> tuple[bool, float, str]:
    """
    Validate state transition against Four Pillars.

    Returns:
        (is_valid, composite_score, reason)
    """
    scores = {
        'an_toan': 0.0,      # Safety
        'duong_dai': 0.0,     # Long-term
        'tin_vao_so_lieu': 0.0,  # Data-driven
        'han_che_rui_ro': 0.0    # Risk minimization
    }

    # Safety check
    if context.get('health_score', 1.0) < 0.3 and to_state != 'CRITICAL':
        scores['an_toan'] = 5.0  # Unsafe transition
    else:
        scores['an_toan'] = 9.0

    # Long-term check
    if to_state in ['DEAD', 'RETIRED'] and context.get('age', 0) < 50:
        scores['duong_dai'] = 6.0  # Premature end
    else:
        scores['duong_dai'] = 8.5

    # Data-driven check
    if context.get('evidence_count', 0) < 3:
        scores['tin_vao_so_lieu'] = 6.5  # Insufficient data
    else:
        scores['tin_vao_so_lieu'] = 9.0

    # Risk minimization check
    if to_state == 'ERROR' or to_state == 'CRITICAL':
        scores['han_che_rui_ro'] = 7.0  # Higher risk
    else:
        scores['han_che_rui_ro'] = 8.5

    composite = sum(scores.values()) / len(scores)

    is_valid = composite >= 7.5  # Composite threshold
    reason = f"Composite score: {composite:.2f} (threshold: 7.5)"

    return (is_valid, composite, reason)
```

---

## 📝 Attestation Event Schema

All state transitions are logged:

```python
{
    "event_id": "uuid-v4",
    "event_type": "state_transition",
    "component_id": "symphony-1",
    "component_type": "SymphonyControlCenter",
    "timestamp": "2026-05-14T23:47:24.959Z",
    "sequence": 12345,

    "transition": {
        "from_state": "PERFORMING",
        "to_state": "OPTIMIZING",
        "trigger": "periodic_optimization_cycle",
        "validation_result": {
            "is_valid": true,
            "composite_score": 8.75,
            "pillars": {
                "an_toan": 9.0,
                "duong_dai": 8.5,
                "tin_vao_so_lieu": 9.0,
                "han_che_rui_ro": 8.5
            }
        }
    },

    "context": {
        "health_score": 0.95,
        "harmony_index": 0.88,
        "k_state": 1,
        "active_components": 8,
        "cycle_count": 1000
    },

    "hash": "sha256-of-event-plus-previous-hash",
    "signature": "alpha_prime_omega"
}
```

---

## ✅ Compliance Requirements

All state machines must:
- [ ] Define all states explicitly
- [ ] Document all valid transitions
- [ ] Validate transitions with Four Pillars
- [ ] Log all transitions to attestation log
- [ ] Provide recovery paths for failure states
- [ ] Enforce immutability (no direct state mutation)
- [ ] Maintain K-State = 1 throughout

**Validation**: Run `pytest tests/test_state_machine.py` to verify compliance.

---

## 📚 Related Documentation

- [Sovereign Agentic Runtime Doctrine](./SOVEREIGN_AGENTIC_RUNTIME_DOCTRINE.md)
- [Connector Lifecycle](./CONNECTOR_LIFECYCLE.md)
- [Metadata Schema](./METADATA_SCHEMA.md)
- [Execution Evidence Registry](./EXECUTION_EVIDENCE_REGISTRY.md)

---

**End of Runtime State Machine Specification v1.0.0**

*Signed: Nguyễn Đức Cường (alpha_prime_omega)*
*Verification: 4287*
*Date: 2026-05-14*
