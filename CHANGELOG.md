# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.1] - 2020-07-04

### Added

- This CHANGELOG
- Automatize image builing on Github Actions.
- Automatize test on Github Actions.
- Added code coverage with [Codecov](https://codecov.io/gh/gabraganca/quickstar) and Gitub Actions.

### Changed

- Atmospheric/atomic models moved to container.

### Removed

- Bootstrap script that downloaded atmospheric/atomic models.

## [0.1.0] - 2020-06-13

### Added

- Simple python wrapper to Synplot.
- Celery worker to synthesize interact with the wrapper aforementioned.
- Asynchornous API to send request to synthesize and get results to Celery.
- Docker files to the API and the worker.
- Docker Compose file orchestrating all the services (RabbitMQ, Redis, API, worker, flower).
- Bash scritp to bootstrap the repository (downloads atomic and atmospheric models).

[Unreleased]: https://github.com/gabraganca/quickstar/compare/v0.1.0...HEAD
[0.1.1]: https://github.com/gabraganca/quickstar/compare/v0.1.0...v0.1.1
[0.1.0]: https://github.com/gabraganca/quickstar/releases/tag/v0.1.0
