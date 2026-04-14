# Contributing to Q³

Thanks for contributing to Q³.

This repository is maintained as an early-stage research and engineering codebase. The goal is
to keep the implementation technically honest, small enough to audit, and aligned with the
documented scope of the framework.

## Contribution priorities

Good contributions usually improve one of these areas:

- circuit-core correctness
- simulator correctness
- test coverage
- documentation clarity
- communication/QKD module structure
- API consistency

Low-value contributions include:

- hype-oriented copy changes
- speculative features without tests
- unsupported hardware claims
- broad rewrites without a clear architectural reason

## Before opening a change

Please make sure the change is:

- technically scoped
- documented where needed
- covered by tests if behavior changes
- consistent with the current Q³ v0.1 API direction

If you plan a larger architectural change, open an issue first and explain:

- the problem
- the proposed approach
- compatibility impact
- how the change will be validated

## Development expectations

Set up the environment:

```bash
python3 -m pip install numpy
```

Run examples:

```bash
python3 examples/bell_state.py
python3 examples/bb84_protocol.py
```

Run tests:

```bash
python3 -m unittest discover -s tests
```

## Code guidelines

- prefer explicit APIs over magic behavior
- keep public claims aligned with implemented behavior
- do not introduce unsupported “quantum” abstractions without mathematical grounding
- keep the core small and readable
- prefer additive changes over unnecessary churn in the public API

## Pull request guidance

A good pull request should include:

- a concise description of the change
- why the change is needed
- tests or examples demonstrating the behavior
- documentation updates when public behavior changes

If a change is experimental, say so directly.

## Compatibility

The repository currently keeps a soft-compatibility layer for legacy `qkd` imports. Do not remove
that compatibility casually. If a change affects compatibility, document it explicitly in the PR.
