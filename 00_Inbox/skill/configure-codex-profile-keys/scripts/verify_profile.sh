#!/usr/bin/env bash
set -euo pipefail

usage() {
    cat <<'EOF'
Usage: verify_profile.sh NAME [options]
       verify_profile.sh --profile NAME [options]

Options:
  --profile NAME          Profile name (legacy/explicit form)
  --codex-home DIR        Codex home (default: $CODEX_HOME or ~/.codex)
  --shim PATH             Shim path (default: ~/.local/bin/codex)
  --skip-runtime-check    Skip the real Codex config-loading check
  -h, --help              Show this help
EOF
}

profile=""
codex_home="${CODEX_HOME:-$HOME/.codex}"
shim="$HOME/.local/bin/codex"
runtime_check=true

while (($#)); do
    case "$1" in
        --profile)
            if [[ -n "$profile" ]]; then
                printf 'Profile name was specified more than once.\n' >&2
                exit 2
            fi
            profile="${2:?missing value for --profile}"
            shift 2
            ;;
        --codex-home) codex_home="${2:?missing value for --codex-home}"; shift 2 ;;
        --shim) shim="${2:?missing value for --shim}"; shift 2 ;;
        --skip-runtime-check) runtime_check=false; shift ;;
        -h|--help) usage; exit 0 ;;
        --*)
            printf 'Unknown option: %s\n' "$1" >&2
            usage >&2
            exit 2
            ;;
        *)
            if [[ -n "$profile" ]]; then
                printf 'Unexpected argument: %s\n' "$1" >&2
                usage >&2
                exit 2
            fi
            profile="$1"
            shift
            ;;
    esac
done

if [[ ! "$profile" =~ ^[A-Za-z0-9][A-Za-z0-9-]*$ ]]; then
    printf 'Invalid or missing profile name.\n' >&2
    exit 2
fi

config_file="$codex_home/$profile.config.toml"
key_file="$codex_home/keys/$profile.key"

[[ -x "$shim" ]] || { printf 'Shim is not executable: %s\n' "$shim" >&2; exit 1; }
[[ -r "$config_file" ]] || { printf 'Missing profile config: %s\n' "$config_file" >&2; exit 1; }
[[ -r "$key_file" ]] || { printf 'Missing profile key: %s\n' "$key_file" >&2; exit 1; }

env_key="$(
    awk -F'"' '/^[[:space:]]*env_key[[:space:]]*=/{print $2; exit}' "$config_file"
)"
if [[ ! "$env_key" =~ ^[A-Za-z_][A-Za-z0-9_]*$ ]]; then
    printf 'Invalid env_key in %s: %s\n' "$config_file" "$env_key" >&2
    exit 1
fi

key_mode=""
if key_mode="$(stat -c '%a' "$key_file" 2>/dev/null)"; then
    :
elif key_mode="$(stat -f '%Lp' "$key_file" 2>/dev/null)"; then
    :
fi
if [[ -n "$key_mode" && "$key_mode" != "600" && "$key_mode" != "400" ]]; then
    printf 'Insecure key permissions (%s): %s\n' "$key_mode" "$key_file" >&2
    exit 1
fi

probe="$(mktemp)"
trap 'rm -f "$probe"' EXIT
cat > "$probe" <<'PROBE'
#!/usr/bin/env bash
set -eu
if printenv "${EXPECTED_ENV_KEY:?}" >/dev/null 2>&1; then
    printf 'loaded\n'
else
    printf 'missing\n'
fi
PROBE
chmod 700 "$probe"

probe_result="$(
    env -u "$env_key" \
        EXPECTED_ENV_KEY="$env_key" \
        CODEX_HOME="$codex_home" \
        CODEX_REAL_BIN="$probe" \
        "$shim" --profile "$profile" profile-key-probe
)"
if [[ "$probe_result" != "loaded" ]]; then
    printf 'Shim did not inject %s for profile %s.\n' "$env_key" "$profile" >&2
    exit 1
fi

if "$runtime_check"; then
    CODEX_HOME="$codex_home" "$shim" \
        --profile "$profile" debug prompt-input --help >/dev/null
fi

printf 'OK: profile %s loads its protected key through %s\n' "$profile" "$shim"
