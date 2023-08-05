# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## v0.1.4 - 2021-08-04
Added
- Add `--remove_wrapping` option to remove text wrapping in the body content of
  a chapter
- Capture the book title from the file if found and not explicitly set through
  `--title` option

Fixed
- Fix no paragraph separation for txt file without single-line spacing for
  markdown
- Fix issues raised by PyLint

Changed
- Parse more different chapter headers
- Refactor argument parsing

## v0.1.3 - 2021-07-24
Fixed
- Fix no parsing and split by introduction chapter
- Fix issues raised by PyLint

Changed
- Switch license to AGPL-3

## v0.1.2 - 2021-07-20
Added
- Add option to set metadata for ebook
- Add missing requirements.txt
- Show full help message when missing required argument

Changed
- Use better way to check for input file
- Print message using click.ecto
- Code formatting

## v0.1.1 - 2021-07-13

Added
- Enable logging for debugging and showing status
- Set log level through `LOG` environment variable

Fixed
- Check for missing filename, empty file content, and missing chapters

## v0.1.0 - 2021-07-08

Added
- Initial public release
- Support converting txt file in Chinese language into epub format
