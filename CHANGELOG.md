# Changelog

<!-- version list -->

## v2.6.1 (2026-10-27)

### Bug Fixes

- Annotate the CGI response as text and the optional session
  ([#16](https://github.com/Aohzan/pypx800/pull/16),
  [`dc3c9aa`](https://github.com/Aohzan/pypx800/commit/dc3c9aab181160460960aa1649ce8f529a9ce625))

- Wait between the CGI retries without blocking the event loop
  ([#17](https://github.com/Aohzan/pypx800/pull/17),
  [`0123fec`](https://github.com/Aohzan/pypx800/commit/0123fece3defcdc991912ddaf8a9c2d39d8399f4))


## v2.6.0 (2026-10-13)

### Build System

- Package with pyproject.toml and uv
  ([`dc1b726`](https://github.com/Aohzan/pypx800/commit/dc1b7268d4ccb212a7e41fcdd4e66cade60b1fd6))

### Continuous Integration

- Keep actions and dependencies up to date with Dependabot
  ([`6bdf137`](https://github.com/Aohzan/pypx800/commit/6bdf1376904463235494a91b9f355338f6fa605a))

- Release to PyPI with python-semantic-release
  ([`096c9c4`](https://github.com/Aohzan/pypx800/commit/096c9c44e6a66a4b37f9da93a74633f2749e83b6))

### Features

- Add support for virtual analog input from X200ph
  ([#10](https://github.com/Aohzan/pypx800/pull/10),
  [`320b555`](https://github.com/Aohzan/pypx800/commit/320b555c66b868c2f7ab0c93ecf6b6874451e34f))


## 2.5.1

- Fix context error with request timeout
- Lint

## 2.5.0

- Add set value for VA and Counter

## 2.4.0

- Add counter support
- Add key property to get value from global_get function

## 2.3.0

- Add pulse commands to X-4VR

## 2.2.0

- Add Virtual Analog Input

## 2.1.2

- Set check request status to True by default
- Fix params order to avoid crash
- Create session at init
- Reduce default timeout

## 2.1.1

- Fix import order

## 2.1.0

- Simplest objects import

## 2.0.0

- Rewrite with async support

## 1.8.0

- Retry request n times before raise an exception (3 by default)
- No boolean return for action anymore
- No XPWM request if no username specified

## 1.7.0

- Add transition for lights toggle

## 1.6.2

- Add X-4FP support
- Fix optional parameters

## 1.5

- Fix cover id with many extensions

## 1.4

- Fix

## 1.3

- Add Stop for VR

## 1.2

- Fix set VR position

## 1.1

- Fix VR position

## 1.0

- Breaking changes, see the README
- Add X-4VR support

## 0.7

- Add support for X-THL

## 0.6

- Add XPWM values to global get

## 0.5

- Replace global get by "Get=all"

## 0.1

- initial release
