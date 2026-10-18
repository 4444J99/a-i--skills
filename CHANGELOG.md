# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Verified skills installation: atomic build, validate, install, package, and guarded rollback from canonical source, with CI workflow, PR validation comment, and release-asset support. Addresses activation [issue #23](https://github.com/4444J99/a-i--skills/issues/23). Latest Python CI (runs 38319189660, 38319282014), Skills installation (runs 38319230387, 38411802555), Validate (runs 38319189650, 38319230233, 38319484976, 38319642649, 38319836861, 38319927575, 38320033513, 38320115522, 38320183281, 38320254778, 38336420685, 38336494265), and PR Validation Comment (runs 38319088862, 38319189699, 38319230324, 38319404998, 38319485007, 38319837022, 38319927487, 38319994806, 38320033544, 38320106502, 38320140159, 38320276277, 38336420786, 38336494233) successes recorded. Dependabot pip update (run 38411813478) succeeded on main after merge of #43.
- `code-review-checklist` skill (development category): structured five-dimension review
  guide (correctness, security, performance, readability, test coverage) with prioritized,
  file:line-cited output format. Closes #5.
- Platinum Sprint: CI/CD workflow, standardized badge row, ADR documentation
- Initial CHANGELOG following Keep a Changelog format

### Changed

- `closeout` skill made repository-agnostic: core is now a universal floor that discovers and defers to any repo-specific protocol; original ORGANVM plan-ledger ritual preserved as an opt-in overlay. (PR #50)

## [0.1.0] - 2026-02-11

### Added

- Initial public release as part of the organvm eight-organ system
- Core project structure and documentation
- README with portfolio-quality documentation

[Unreleased]: https://github.com/4444J99/a-i--skills/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/4444J99/a-i--skills/releases/tag/v0.1.0
