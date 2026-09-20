#!/usr/bin/env bash
set -euo pipefail

usage() {
    cat <<'EOF'
Usage: setup_profile.sh NAME [options]

Create Codex profile and key templates in one command.

Options:
  --codex-home DIR        Codex home (default: $CODEX_HOME or ~/.codex)
  --force                 Back up and replace existing template files
  -h, --help              Show this help
EOF
}

profile=""
codex_home="${CODEX_HOME:-$HOME/.codex}"
force=false

while (($#)); do
    case "$1" in
        --codex-home)
            codex_home="${2:?missing value for --codex-home}"
            shift 2
            ;;
        --force)
            force=true
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
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

config_file="$codex_home/$profile.config.toml"
key_file="$codex_home/keys/$profile.key"
if [[ "$force" != true && ( -e "$config_file" || -e "$key_file" ) ]]; then
    printf 'Profile files already exist for %s.\n' "$profile" >&2
    printf 'Rerun with --force to back up and replace them.\n' >&2
    exit 1
fi

script_dir="$(
    CDPATH= cd -- "$(dirname -- "${BASH_SOURCE[0]}")"
    pwd
)"

"$script_dir/install_shim.sh" --codex-home "$codex_home"

create_args=("$profile" --codex-home "$codex_home")

if "$force"; then
    create_args+=(--force)
fi

"$script_dir/create_profile.sh" "${create_args[@]}"

keys_dir="$codex_home/keys"
mkdir -p "$keys_dir"
chmod 700 "$keys_dir"

if [[ -e "$key_file" && "$force" == true ]]; then
    key_backup="$key_file.bak.$(date +%Y%m%d%H%M%S)"
    cp -p "$key_file" "$key_backup"
    printf 'Backed up existing key file to: %s\n' "$key_backup"
fi

umask 077
key_tmp="$(mktemp "$keys_dir/.${profile}.key.XXXXXX")"
trap 'rm -f "$key_tmp"' EXIT
printf '%s\n' 'REPLACE_WITH_API_KEY' > "$key_tmp"
chmod 600 "$key_tmp"
mv "$key_tmp" "$key_file"
trap - EXIT

printf 'Created key template: %s\n' "$key_file"
printf '\nProfile templates created.\n'
printf 'Config: %s/%s.config.toml\n' "$codex_home" "$profile"
printf 'Key: %s/keys/%s.key\n' "$codex_home" "$profile"
printf 'Replace base_url and REPLACE_WITH_API_KEY before starting Codex.\n'
