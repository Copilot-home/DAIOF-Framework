# Post-Merge CI Closure

## Objective

Restore the repository-owned CI path after PR #110 merged with a malformed ecosystem validation block.

## Execution boundary

- Source changes are isolated on `fix/post-merge-ci-closure`.
- `main` is not edited directly.
- GitHub Actions is the remote verification oracle.
- Copilot and other quota-bound agents are not part of the critical path.
- Merge remains a human decision after required checks pass.

## Corrected validation path

1. Checkout the pull-request head or push ref deterministically.
2. Install repository and test dependencies.
3. Run critical flake8 checks.
4. Verify immutable genes and doctrine compliance.
5. Execute the test suite with coverage.
6. Validate `SymphonyControlCenter`.
7. Execute one `DigitalOrganism.live_cycle`.
8. Construct `DigitalEcosystem(name=...)`, add five named organisms, and run `simulate_time_step(0.1)`.
9. Regenerate and validate `governance/workflow_manifest.json` from the final workflow tree.

## Acceptance gates

- Workflow YAML parses successfully.
- No call to the nonexistent `simulate_generation` API remains.
- `DigitalEcosystem` is always initialized with an explicit name.
- The ecosystem smoke test asserts population and simulation time.
- Governance manifest validation returns no errors.
- Repository-owned GitHub checks pass before review readiness or merge.

## Product and developer experience

The CI output uses stable, descriptive step names and reports the resolved Python runtime. Validation failures are localized to lifecycle, ecosystem, tests, governance, or security instead of being hidden inside a single opaque script.
