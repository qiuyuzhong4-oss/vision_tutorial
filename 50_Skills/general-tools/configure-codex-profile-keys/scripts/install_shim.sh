#!/usr/bin/env bash
set -euo pipefail

usage() {
    cat <<'EOF'
Usage: install_shim.sh [options]

Options:
  --codex-home DIR   Codex home directory (default: $CODEX_HOME or ~/.codex)
  --install-dir DIR  Shim install directory (default: ~/.local/bin)
  --real-codex PATH  Real Codex executable to launch
  --shell-rc FILE    Shell startup file to update
  --no-path-update   Do not modify a shell startup file
  -h, --help         Show this help
EOF
}

codex_home="${CODEX_HOME:-$HOME/.codex}"
install_dir="$HOME/.local/bin"
real_codex=""
shell_rc=""
update_path=true

while (($#)); do
    case "$1" in
        --codex-home)
            codex_home="${2:?missing value for --codex-home}"
            shift 2
            ;;
        --install-dir)
            install_dir="${2:?missing value for --install-dir}"
            shift 2
            ;;
        --real-codex)
            real_codex="${2:?missing value for --real-codex}"
            shift 2
            ;;
        --shell-rc)
            shell_rc="${2:?missing value for --shell-rc}"
            shift 2
            ;;
        --no-path-update)
            update_path=false
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        *)
            printf 'Unknown option: %s\n' "$1" >&2
            usage >&2
            exit 2
            ;;
    esac
done

shim_path="$install_dir/codex"
state_file="$codex_home/profile-key-shim.real-bin"

if [[ -z "$real_codex" && -r "$state_file" ]]; then
    IFS= read -r real_codex < "$state_file"
fi

if [[ -z "$real_codex" || ! -x "$real_codex" ]]; then
    real_codex=""
    while IFS= read -r candidate; do
        [[ -n "$candidate" ]] || continue
        [[ "$candidate" == "$shim_path" ]] && continue
        if [[ -x "$candidate" ]]; then
            real_codex="$candidate"
            break
        fi
    done < <(type -aP codex 2>/dev/null | awk '!seen[$0]++')
fi

if [[ -z "$real_codex" && -x "$HOME/.npm-global/bin/codex" ]]; then
    real_codex="$HOME/.npm-global/bin/codex"
fi

if [[ -z "$real_codex" || ! -x "$real_codex" ]]; then
    printf 'Could not locate the real Codex executable. Use --real-codex PATH.\n' >&2
    exit 1
fi

mkdir -p "$codex_home/keys" "$install_dir"
chmod 700 "$codex_home/keys"

umask 077
printf '%s\n' "$real_codex" > "$state_file"
chmod 600 "$state_file"

shim_tmp="$(mktemp "$install_dir/.codex-profile-key-shim.XXXXXX")"
trap 'rm -f "$shim_tmp"' EXIT

cat > "$shim_tmp" <<'SHIM'
#!/usr/bin/env bash
set -euo pipefail

codex_home="${CODEX_HOME:-$HOME/.codex}"
real_codex="${CODEX_REAL_BIN:-}"
state_file="$codex_home/profile-key-shim.real-bin"

if [[ -z "$real_codex" && -r "$state_file" ]]; then
    IFS= read -r real_codex < "$state_file"
fi

if [[ -z "$real_codex" || ! -x "$real_codex" ]]; then
    printf 'Codex profile-key shim cannot find the real executable.\n' >&2
    printf 'Run install_shim.sh again or set CODEX_REAL_BIN.\n' >&2
    exit 127
fi

profile=""
args=("$@")
for ((i = 0; i < ${#args[@]}; i++)); do
    case "${args[$i]}" in
        -p|--profile)
            if ((i + 1 < ${#args[@]})); then
                profile="${args[$((i + 1))]}"
            fi
            ;;
        --profile=*)
            profile="${args[$i]#*=}"
            ;;
    esac
done

if [[ -n "$profile" ]]; then
    config_file="$codex_home/$profile.config.toml"
    key_file="$codex_home/keys/$profile.key"

    if [[ -f "$config_file" ]]; then
        env_key="$(
            awk -F'"' \
                '/^[[:space:]]*env_key[[:space:]]*=/{print $2; exit}' \
                "$config_file"
        )"

        if [[ -n "$env_key" ]]; then
            if [[ ! "$env_key" =~ ^[A-Za-z_][A-Za-z0-9_]*$ ]]; then
                printf 'Invalid env_key in %s: %s\n' "$config_file" "$env_key" >&2
                exit 2
            fi

            if [[ -z "${!env_key-}" ]]; then
                if [[ ! -r "$key_file" ]]; then
                    printf 'Missing profile key file: %s\n' "$key_file" >&2
                    exit 2
                fi

                key_mode=""
                if key_mode="$(stat -c '%a' "$key_file" 2>/dev/null)"; then
                    :
                elif key_mode="$(stat -f '%Lp' "$key_file" 2>/dev/null)"; then
                    :
                fi
                if [[ -n "$key_mode" && "$key_mode" != "600" && "$key_mode" != "400" ]]; then
                    printf 'Insecure profile key permissions (%s): %s\n' \
                        "$key_mode" "$key_file" >&2
                    exit 2
                fi

                api_key="$(<"$key_file")"
                api_key="${api_key//$'\r'/}"
                if [[ -z "$api_key" || "$api_key" == *$'\n'* ]]; then
                    printf 'Profile key must contain exactly one non-empty line: %s\n' \
                        "$key_file" >&2
                    exit 2
                fi

                printf -v "$env_key" '%s' "$api_key"
                export "$env_key"
                unset api_key
            fi
        fi
    fi
fi

exec "$real_codex" "$@"
SHIM

chmod 755 "$shim_tmp"
mv "$shim_tmp" "$shim_path"
trap - EXIT

if "$update_path"; then
    if [[ -z "$shell_rc" ]]; then
        case "${SHELL##*/}" in
            zsh) shell_rc="$HOME/.zshrc" ;;
            *) shell_rc="$HOME/.bashrc" ;;
        esac
    fi

    marker_start="# >>> codex profile key shim >>>"
    marker_end="# <<< codex profile key shim <<<"
    touch "$shell_rc"
    if ! grep -Fq "$marker_start" "$shell_rc"; then
        {
            printf '\n%s\n' "$marker_start"
            printf 'export PATH=%q:$PATH\n' "$install_dir"
            printf '%s\n' "$marker_end"
        } >> "$shell_rc"
    fi
fi

printf 'Installed Codex profile-key shim: %s\n' "$shim_path"
printf 'Recorded real Codex executable: %s\n' "$real_codex"
printf 'Key directory: %s\n' "$codex_home/keys"
if "$update_path"; then
    printf 'Reload the shell with: source %s\n' "$shell_rc"
fi
