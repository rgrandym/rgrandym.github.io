<!--
Sync Impact Report:
- Version change: INITIAL → 1.0.0
- New constitution creation
- Principles defined: 5 core principles
- Templates status: ✅ All aligned with new constitution
- No pending TODOs
-->

# My Website Constitution

## Core Principles

### I. Conda Environment Isolation

**MUST** use the dedicated `my_website` conda environment for all development work. Dependencies **MUST** be installed via conda first; if unavailable in conda channels, then pip may be used as fallback. This ensures reproducible builds and consistent dependency resolution across development machines.

**Rationale**: Conda provides superior environment isolation and cross-platform package management, particularly for scientific Python packages. Using a dedicated environment prevents conflicts with system Python and other projects.

### II. Lean Code Architecture

Functions and classes **MUST NOT** exceed 50 lines of code. Code **MUST** be modular with clear single responsibilities. Each unit (function/class) **MUST** have a clear, focused purpose. Avoid complex nesting.

**Rationale**: Shorter functions are easier to understand, test, and maintain. This constraint forces good design practices including proper decomposition and separation of concerns. Cognitive load is minimized when each unit fits on a single screen.

### III. Manual Testing Only

Automated test suites **MUST NOT** be created. All testing is performed manually by the developer. Code review focuses on readability and correctness through inspection.

**Rationale**: For this personal website project, the overhead of maintaining automated tests outweighs the benefits. Manual testing is sufficient given the project scope and development velocity. This principle may be revised as the project grows.

### IV. Modularity First

Code **MUST** be organized into small, reusable modules. Dependencies between modules **MUST** be explicit and minimal. Each module **MUST** have a clear interface and single responsibility.

**Rationale**: Modular architecture enables independent development, easier debugging, and better code reuse. Clear module boundaries reduce coupling and make the codebase easier to navigate and modify.

### V. Task-Focused Development

Development work **MUST** focus on the specific task requested. Summary reports, additional documentation, or tangential improvements **MUST NOT** be generated unless explicitly requested.

**Rationale**: Staying focused on the immediate task improves efficiency and prevents scope creep. Additional work should only be done when it directly serves the user's stated needs.

## Environment Management

All Python development **MUST** occur within the `my_website` conda environment. The environment **MUST** be activated before any development commands are executed.

Dependency installation priority:

1. **FIRST**: Attempt installation via `conda install <package>`
2. **FALLBACK**: If unavailable in conda, use `pip install <package>`

The environment specification **SHOULD** be maintained in an `environment.yml` file for reproducibility.

## Code Quality Standards

- Functions/classes **MUST** be under 50 lines
- Code **MUST** have clear, descriptive names
- Complex logic **MUST** be decomposed into smaller units
- Comments **SHOULD** explain "why" not "what"
- Magic numbers **MUST** be replaced with named constants

## Governance

This constitution supersedes all other development practices for the My Website project. All development decisions must align with these core principles.

**Amendment Process**:

- Amendments require explicit approval from the project maintainer
- Version increments follow semantic versioning:
  - **MAJOR**: Removal or fundamental redefinition of principles
  - **MINOR**: Addition of new principles or significant expansions
  - **PATCH**: Clarifications, wording improvements, non-semantic changes

**Compliance**:

- Every code change must be verified against these principles
- Violations must be justified and documented
- Regular reviews ensure ongoing alignment

**Version**: 1.0.0 | **Ratified**: 2025-10-07 | **Last Amended**: 2025-10-07
