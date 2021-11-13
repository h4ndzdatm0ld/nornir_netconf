# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

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
