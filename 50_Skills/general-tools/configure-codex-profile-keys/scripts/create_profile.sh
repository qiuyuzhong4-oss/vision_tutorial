#!/usr/bin/env bash
set -euo pipefail

usage() {
    cat <<'EOF'
Usage: create_profile.sh NAME [options]
       create_profile.sh --profile NAME [options]

Options:
  --profile NAME              Profile name (legacy/explicit form)
  --base-url URL              API base URL (default: placeholder)
  --model MODEL               Default model ID (default: gpt-5.6)
  --review-model MODEL        Review model ID (default: same as --model)
  --display-name NAME         Provider display name (default: profile name)
  --wire-api API              Wire API (default: responses)
  --reasoning-effort LEVEL    Optional reasoning effort
  --codex-home DIR            Codex home (default: $CODEX_HOME or ~/.codex)
  --force                     Back up and replace an existing profile
  -h, --help                  Show this help
EOF
}

profile=""
base_url="https://example.invalid/v1"
model="gpt-5.6"
review_model=""
display_name=""
wire_api="responses"
reasoning_effort=""
codex_home="${CODEX_HOME:-$HOME/.codex}"
force=false

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
        --base-url) base_url="${2:?missing value for --base-url}"; shift 2 ;;
        --model) model="${2:?missing value for --model}"; shift 2 ;;
        --review-model) review_model="${2:?missing value for --review-model}"; shift 2 ;;
        --display-name) display_name="${2:?missing value for --display-name}"; shift 2 ;;
        --wire-api) wire_api="${2:?missing value for --wire-api}"; shift 2 ;;
        --reasoning-effort) reasoning_effort="${2:?missing value for --reasoning-effort}"; shift 2 ;;
        --codex-home) codex_home="${2:?missing value for --codex-home}"; shift 2 ;;
        --force) force=true; shift ;;
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
    printf 'Invalid or missing profile name. Use letters, digits, and hyphens.\n' >&2
    exit 2
fi

for value in "$base_url" "$model" "$review_model" "$display_name" "$wire_api" "$reasoning_effort"; do
    if [[ "$value" == *$'\n'* || "$value" == *$'\r'* ]]; then
        printf 'Configuration values must not contain newlines.\n' >&2
        exit 2
    fi
done

toml_escape() {
    local value="$1"
    value="${value//\\/\\\\}"
    value="${value//\"/\\\"}"
    printf '%s' "$value"
}

review_model="${review_model:-$model}"
display_name="${display_name:-$profile}"
env_profile="$(printf '%s' "$profile" | tr '[:lower:]-' '[:upper:]_')"
env_key="CODEX_${env_profile}_API_KEY"
target="$codex_home/$profile.config.toml"

mkdir -p "$codex_home"
if [[ -e "$target" ]]; then
    if ! "$force"; then
        printf 'Profile already exists: %s\n' "$target" >&2
        printf 'Inspect it first, then rerun with --force if replacement is intended.\n' >&2
        exit 1
    fi
    backup="$target.bak.$(date +%Y%m%d%H%M%S)"
    cp -p "$target" "$backup"
    printf 'Backed up existing profile to: %s\n' "$backup"
fi

tmp="$(mktemp "$codex_home/.${profile}.config.toml.XXXXXX")"
trap 'rm -f "$tmp"' EXIT
umask 077

{
    printf '# Codex profile: %s\n' "$profile"
    printf '# Key file: %s/keys/%s.key\n\n' "$codex_home" "$profile"
    printf 'model_provider = "%s"\n' "$(toml_escape "$profile")"
    printf 'model = "%s"\n' "$(toml_escape "$model")"
    printf 'review_model = "%s"\n' "$(toml_escape "$review_model")"
    if [[ -n "$reasoning_effort" ]]; then
        printf 'model_reasoning_effort = "%s"\n' "$(toml_escape "$reasoning_effort")"
    fi
    printf '\n[model_providers.%s]\n' "$profile"
    printf 'name = "%s"\n' "$(toml_escape "$display_name")"
    printf 'base_url = "%s"\n' "$(toml_escape "$base_url")"
    printf 'env_key = "%s"\n' "$env_key"
    printf 'wire_api = "%s"\n' "$(toml_escape "$wire_api")"
    printf 'requires_openai_auth = true\n'
} > "$tmp"

chmod 600 "$tmp"
mv "$tmp" "$target"
trap - EXIT

printf 'Created profile: %s\n' "$target"
printf 'Environment key name: %s\n' "$env_key"
printf 'Edit base_url before use; model defaults to gpt-5.6.\n'
printf 'Expected key path: %s/keys/%s.key\n' "$codex_home" "$profile"
