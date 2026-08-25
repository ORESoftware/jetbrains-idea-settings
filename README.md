# ORESoftware JetBrains settings

Shared, reviewable IDE defaults for IntelliJ IDEA and compatible JetBrains
products. The repository contains code-style, inspection, and editor settings;
it deliberately excludes accounts, licenses, recent projects, local paths,
plugin credentials, HTTP requests, and workspace state.

## Install

Use the JetBrains Settings Repository or settings-sync import flow and point it
at this Git repository. Review the incoming diff before applying it. Teams that
cannot use IDE settings synchronization can copy `.editorconfig` into a project
without importing any IDE-specific state.

The named `ORESoftware` style uses LF line endings, final newlines, a 100-column
right margin, two-space JavaScript/TypeScript indentation, and four-space Rust
indentation. The inspection profile enables baseline duplicate-code, URL,
cryptographic-hash, line-ending, and spelling diagnostics.

## Verify

```sh
python3 scripts/validate_settings.py
```

Validation parses every committed XML file, checks the required scheme/profile
contracts, and rejects obvious credential assignments. This is structural
evidence only; compatibility with a particular JetBrains build is established
when that build imports the settings.
