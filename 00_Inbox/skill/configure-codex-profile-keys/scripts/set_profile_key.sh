#!/usr/bin/env bash
set -euo pipefail

usage() {
    cat <<'EOF'
Usage: set_profile_key.sh NAME [options]
       set_profile_key.sh --profile NAME [options]

Options:
  --profile NAME      Profile name (legacy/explicit form)
  --from-file FILE    Import the key from an existing protected file
  --codex-home DIR    Codex home (default: $CODEX_HOME or ~/.codex)
  --force             Replace an existing profile key
  -h, --help          Show this help

Without --from-file, the script prompts silently on /dev/tty. If no terminal
is available, it reads the key from standard input. Never pass a key as a
command-line argument.
EOF
}

profile=""
source_file=""
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
        --from-file) source_file="${2:?missing value for --from-file}"; shift 2 ;;
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
    printf 'Invalid or missing profile name.\n' >&2
    exit 2
fi

keys_dir="$codex_home/keys"
target="$keys_dir/$profile.key"
mkdir -p "$keys_dir"
chmod 700 "$keys_dir"

if [[ -e "$target" && "$force" != true ]]; then
    printf 'Profile key already exists: %s\n' "$target" >&2
    printf 'Rerun with --force to rotate or replace it.\n' >&2
    exit 1
fi

api_key=""
if [[ -n "$source_file" ]]; then
    [[ -r "$source_file" ]] || { printf 'Cannot read: %s\n' "$source_file" >&2; exit 1; }
    api_key="$(<"$source_file")"
elif [[ -r /dev/tty ]]; then
    printf 'API key for profile %s: ' "$profile" > /dev/tty
    IFS= read -r -s api_key < /dev/tty
    printf '\n' > /dev/tty
else
    api_key="$(cat)"
fi

api_key="${api_key//$'\r'/}"
if [[ -z "$api_key" || "$api_key" == *$'\n'* ]]; then
    unset api_key
    printf 'API key input must contain exactly one non-empty line.\n' >&2
    exit 2
fi

umask 077
tmp="$(mktemp "$keys_dir/.${profile}.key.XXXXXX")"
trap 'rm -f "$tmp"; unset api_key' EXIT
printf '%s\n' "$api_key" > "$tmp"
chmod 600 "$tmp"
mv "$tmp" "$target"
unset api_key
trap - EXIT

printf 'Stored profile key: %s\n' "$target"
printf 'Permissions: 600\n'
