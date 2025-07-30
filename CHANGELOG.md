# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.0] - 2025-01-19

### Added

- SCORE2-Diabetes cardiovascular risk algorithm implementation
  - Comprehensive risk calculation for diabetic patients
  - Support for multiple risk regions and calibration
  - Extensive test coverage with diverse patient profiles
- SCORE2 cardiovascular risk algorithm implementation
  - Risk assessment for non-diabetic patients
  - Region-specific calibration (Belgium/Low Risk by default)
  - Comprehensive test suite
- Enhanced biomarker processing capabilities
  - JSON processor for biomarker data
  - Improved biomarker extraction utilities
  - Standardized biomarker schemas with Pydantic

### Changed

- Comprehensive type hints throughout the codebase
  - Enhanced type safety and IDE support
  - Better code documentation through types
- Improved code organization and module structure
  - Reorganized test directories for clarity
  - Standardized import statements for package consistency
  - Renamed source directory from `src` to `vitals`
- Enhanced test coverage
  - Expanded test cases for all algorithms
  - Added diverse patient profiles for testing
  - Improved test naming conventions

### Fixed

- Type hint issues with proper TypedDict approach
- Import consistency across the package
- Test function naming conventions
- Unit suffix casing standardized to lowercase
- MyPy errors resolved

### Technical Improvements

- Added pre-commit hooks for code quality
- Configured GitHub Actions for automated code review
- Enhanced development workflow with Makefile
- Added comprehensive coding style guidelines

## [0.1.0] - Initial Release

### Added

- PhenoAge algorithm implementation (Levine's method)
- Basic biomarker processing functionality
- Initial project structure and setup
- Basic test suite
- README documentation
