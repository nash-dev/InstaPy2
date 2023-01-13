# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [WIP]
## [0.0.30] - 2023-01-13
> Below is a minimal changelog. More changes have been made but they aren't worth detailing.
### Added
- Added new authentication, logging, persistence and utility classes.
- Added new like function with support for hashtags, locations and usernames.

### Changed
- Uppercased all enums.
- Improved media interaction validation function.
    - **TODO**
        - Add new validation functions when implemented.
- Improved media obtaining function.
    - **TODO**
        - Improve handling of previously interacted with media.
- Improved error handling of all crash-prone functions.

### Fixed
- Fixed an issue where `limitations.is_account_appropriate` would not return the correct value.