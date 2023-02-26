# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.0] - 2022-xx-xx

### Added

- `ruff` linter

### Changed

- `sysrepo` tests all got replaced by a containerized instance of Arista CEOS

### Removed

- Dropped Python3.7 - Only 3.8 and above is supported.
- `sysrepo` container and dependencies. No tests or reliance on this container anymore.
- `xmltodict` library has been removed. The user should parse XML as they please.
- Flake8 (Replaced by Ruff)
- Pydocstyle (Replaced by Ruff)

## [1.1.0] - 2022-10-06

### Added

- Normalized the result output between vendors to include 'ok' key
- Pipeline to publish to pypi/github

### Changed

- Containerlab IP addresses for local integration testings changed
- Added env variable to docker-compose to run integration tests in containers
- Ability to run all tests from pytest or container
- Tests showing how to use the `extras` for defining the `platform` as the key of `name`

### Fixed

- GH Actions Badge was pointing to previous fork on the Nornir organization

## [1.0.1] - 2022-02-08

### Added

- Local integration tests with ContainerLab

### Changed

- Lowered requirement version for `ncclient`

### Fixed

- Several integration tests are OS versions changed from previous eve-ng lab

## [1.0.0] - 2022-01-17

### Changed

- Removed dependencies locking python version between a range.
- Removed unused dev env dependencies
- Removed version pinning on dev dependencies
- Dropped support for python3.6

## [0.1.0] - 2020-09-10

### Added

- netconf_capabilities - Return server capabilities from target
- netconf_get - Returns state data based on the supplied xpath
- netconf_get_config - Returns configuration from specified configuration store (default="running")
- netconf_edit_config - Edits configuration on specified datastore (default="running")
- netconf_lock - Locks or Unlocks a specified datastore (default="lock")
- netconf_commit - Commits a change
- readme
- Integration tests
