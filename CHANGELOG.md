# Changelog
Format: [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)

Versioning: [Semantic Versioning](https://semver.org/spec/v2.0.0.html)

## [Unreleased]
### Changed
* migrated packaging metadata to `pyproject.toml`
* added optional dependencies for test and documentation workflows
* updated documentation and CI to install project extras instead of ad hoc dependency lists

## [1.0.0] - 2019-04-05
### Added
* data set information, overloading __str__ (issue #19)
* plotting classes (simplifies usage, each data set is only able to call its functions) (issue #22)
* opal logger (issue #18)
* ASCII loss file parser and data set (issue #29)

### Changed
* avoid duplicated code in data sets (issue #20)
* AMR to general interface (issue #21)
* classes for data computation (issue #23)
* cleaned up timing directory, time data set etc. part of general interface (issue #28)

### Removed
* pyH5root directory and files (issue #25)
* deprecated profiling directory and files (issue #26)
* deprecated amrPlots directory and files (issue #27)

### Fixed
* switching between plotting styles (issue #24)
