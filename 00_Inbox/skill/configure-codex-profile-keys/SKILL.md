---
name: configure-codex-profile-keys
description: "Scaffold and maintain Codex CLI profile templates that use separate API-key files without manual shell exports. Use when creating a named profile and protected key placeholder with one shell command, configuring `codex --profile PROFILE`, installing the per-profile key-file shim, or repairing profile files."
---

# Configure Codex Profile Keys

Install a user-level Codex launcher that reads each profile's key from
`$CODEX_HOME/keys/<profile>.key` and injects it only into the Codex child
process.

## Safety Rules

- Never request or place an API key in chat, command arguments, profile TOML,
  shell history, source control, or skill files.
- Replace generated key placeholders locally, or use
  `scripts/set_profile_key.sh` to write a key securely.
- Keep the key directory at mode `700` and key files at mode `600`.
- Treat any key previously printed in a terminal, log, or conversation as
  exposed and recommend rotation.
- Do not patch the installed npm wrapper or compiled Codex binary. Install the
  user-level shim instead so Codex upgrades do not overwrite the setup.

## Quick Start

Run one script with the profile name:

```bash
scripts/setup_profile.sh RM
```

This installs or repairs the launcher and writes two templates without asking
for configuration values or a key. Profile names accept uppercase and
lowercase letters, digits, and hyphens. The supplied case is preserved:

```text
~/.codex/RM.config.toml
~/.codex/keys/RM.key
```

The TOML defaults to `model = "gpt-5.6"` and contains a placeholder `base_url`.
The key file contains:

```text
REPLACE_WITH_API_KEY
```

Replace both placeholders locally, then start with:

```bash
codex --profile RM
```

The older explicit form, such as `--profile daily`, remains supported.
Use `--force` only after inspecting an existing profile; replacement creates a
timestamped TOML backup.

## Repair Existing Configurations

When `env_key` contains a literal key, move that value into the protected key
file and replace the TOML field with a variable name:

```toml
env_key = "CODEX_DAILY_API_KEY"
```

Derive names as `CODEX_<UPPERCASE_PROFILE>_API_KEY`, replacing hyphens with
underscores. Never make `env_key` contain `sk-...`.

If only one global key is required, Codex's built-in auth storage can be used
instead. Prefer this skill's shim when different profiles must retain different
keys simultaneously.

## Script Responsibilities

- `scripts/setup_profile.sh NAME`: install the shim and generate both templates.
- `scripts/install_shim.sh`: install the idempotent launcher and PATH marker.
- `scripts/create_profile.sh NAME`: generate `<NAME>.config.toml`.
- `scripts/set_profile_key.sh NAME`: store `keys/<NAME>.key`.
- `scripts/verify_profile.sh`: validate files, permissions, injection, and
  optional Codex runtime config loading.
