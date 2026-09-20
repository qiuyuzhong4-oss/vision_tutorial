---
name: publish-git-repositories
description: Publish, push, repair, and verify Git repositories on GitHub or Gitea. Use when setting up remotes, first push, PAT authentication, SSH keys, GitHub deploy keys, force-with-lease, fetch-first errors, rewritten history, large-file cleanup, .gitignore safety, private knowledge repositories, Gitea HTTP 413, or Chinese requests such as 推送到GitHub, git push失败, 配deploy key, 仓库上传, git历史重写, GitHub 403, Permission denied publickey.
---

# Publish Git Repositories

## Safety Rules

- Never ask the user to paste a PAT, private SSH key, deploy-key private key, or secret into chat.
- Never place a PAT in a committed file, script, README, command transcript, issue, PR, or shell history.
- Prefer SSH keys or GitHub deploy keys for long-term use. Use PAT only as a temporary bootstrap path when SSH is not available.
- Before `git add .`, inspect `.gitignore`, staged files, large files, and likely secrets.
- Do not run `git reset --hard`, history rewrite, or force push unless the user explicitly approves that risk.
- For personal knowledge bases, notes, AI chat logs, datasets, model weights, archives, and private documents, default to whitelist publishing instead of uploading the whole directory.

## First Triage

Run read-only checks from the repo root:

```bash
git status --short --branch
git remote -v
git branch -vv
find . -type f -size +50M -not -path './.git/*' -print
```

For sensitive or large repos, also check:

```bash
git status --short
git diff --cached --name-only
git ls-files --others --exclude-standard
```

If staging has already happened, inspect staged size before commit:

```bash
python3 -B -c 'import pathlib,subprocess; raw=subprocess.check_output(["git","diff","--cached","--name-only","-z"]); files=[pathlib.Path(x.decode()) for x in raw.split(b"\0") if x]; sized=sorted(((p.stat().st_size,p) for p in files if p.exists()), reverse=True); print(f"staged_files={len(files)} staged_bytes={sum(s for s,p in sized)} max_file_bytes={sized[0][0] if sized else 0}"); [print(size, path) for size,path in sized[:10]]'
```

## Normal First Push

For a new empty remote:

```bash
git remote remove origin 2>/dev/null || true
git remote add origin <remote-url>
git status
git add .
git status
git commit -m "init: import project"
git branch -M main
git push -u origin main
```

Do not initialize the remote with README, `.gitignore`, or license if the local repo already has the initial commit. If the remote is not empty, use `git pull --rebase` or `git push --force-with-lease` only after deciding whether remote commits should be preserved.

## PAT Bootstrap

Use classic PAT with the minimum required scopes when PAT is unavoidable. For a normal private or public repo push, `repo` is usually enough.

Use a variable instead of hand-typing a long URL:

```bash
TOKEN="ghp_xxx"
git remote set-url origin "https://<user>:${TOKEN}@github.com/<user>/<repo>.git"
unset TOKEN
git push -u origin main
git remote set-url origin "https://github.com/<user>/<repo>.git"
```

Afterward:

- Confirm `git remote -v` has no token.
- Clear shell history or terminal scrollback if a token appeared.
- Revoke any token exposed in chat, files, logs, screenshots, or terminal history.

If fine-grained PAT gives 403, check repository access and Contents read/write permission. Prefer classic PAT for one-time bootstrap when the user is learning the flow.

## SSH And Deploy Keys

For user-level SSH:

```bash
ssh-keygen -t ed25519 -C "<email>"
cat ~/.ssh/id_ed25519.pub
ssh -T git@github.com
git remote set-url origin git@github.com:<owner>/<repo>.git
```

For per-repository GitHub Deploy Key:

```bash
ssh-keygen -t ed25519 -C "<repo> deploy key" -f ~/.ssh/id_ed25519_<repo> -N ""
cat ~/.ssh/id_ed25519_<repo>.pub
```

Paste the public key into repository Settings -> Deploy keys. It must be one line beginning with `ssh-ed25519`. Enable write access if the key will push.

Keep the private key local. Configure the repo-local SSH command in `.git/config`, not in tracked files:

```bash
git config core.sshCommand "ssh -i ~/.ssh/id_ed25519_<repo> -o IdentitiesOnly=yes"
git config --get core.sshCommand
```

Diagnose authentication:

```bash
ssh -T -i ~/.ssh/id_ed25519_<repo> -o IdentitiesOnly=yes git@github.com
```

`Permission denied (publickey)` usually means the key is missing, pasted incorrectly, added to the wrong repo, lacks write access, or the repo is using a different private key.

## GitHub SSH 443 Fallback

When SSH port 22 or Git pack upload hangs, use GitHub SSH over HTTPS port 443:

```bash
git config core.sshCommand "ssh -p 443 -o Hostname=ssh.github.com -o HostKeyAlias=ssh.github.com -i ~/.ssh/id_ed25519_<repo> -o IdentitiesOnly=yes -o BatchMode=yes"
```

If the network remains unstable, add conservative options only after basic SSH has been tested:

```bash
git config core.sshCommand "ssh -p 443 -o Hostname=ssh.github.com -o HostKeyAlias=ssh.github.com -i ~/.ssh/id_ed25519_<repo> -o IdentitiesOnly=yes -o BatchMode=yes -o IPQoS=none"
```

Use tracing to distinguish permission, network, and pack problems:

```bash
timeout 30s git ls-remote origin
timeout 60s env GIT_TRACE=1 GIT_TRACE_PACKET=1 git push --dry-run --verbose origin main
timeout 180s env GIT_TRACE=1 GIT_TRACE_PACKET=1 git -c core.compression=0 push --progress --verbose -u origin main
```

If dry-run reports `* [new branch] main -> main`, permissions are likely correct and remaining failures are upload or network issues.

## Large Files And Private Content

Do not put these into normal Git unless the user explicitly accepts the repository policy:

- Model weights: `.pt`, `.pth`, `.onnx`, `.bin`.
- Point clouds, maps, videos, logs, datasets, archives, installers, and generated build outputs.
- Personal knowledge files, AI chat records, private notes, credentials, local config, and caches.

For a rules-only or architecture-only repository, use a whitelist `.gitignore`:

```gitignore
*

!.gitignore
!README.md
!rules/
!rules/**
```

Before publishing:

```bash
git status --short
git diff --cached --name-only
```

Only the intended whitelist files should appear.

## Common Failures

- HTTP 413 on Gitea: clean large files from history or ask the server admin to raise Nginx and Gitea upload limits. Prefer cleaning models, PDFs, GIFs, PCDs, and third-party copies out of Git.
- `fetch first` or non-fast-forward: remote has commits local lacks. Use `git pull --rebase` if preserving remote work; use `git push --force-with-lease` only for known disposable remote commits.
- `--force-with-lease` stale info: run `git fetch origin main` and retry.
- Rebase conflict confusion: use `git rebase --abort` to restore the pre-rebase state, or resolve conflicts then `git add` and `git rebase --continue`.
- Broken remote URL after pasted token: inspect `git remote -v`, then recreate origin with a clean URL.
- Rewritten history: tell teammates to backup local untracked assets, `git fetch origin`, then explicitly choose whether `git reset --hard origin/main` is appropriate.

## Gitea And History Rewrite

For Gitea with small upload limits, first remove large files from the index and history:

```bash
git rm --cached <file-or-path>
git-filter-repo --invert-paths --path-glob '<large-path-glob>'
git reflog expire --expire=now --all
git gc --prune=now --aggressive
```

Warn that `git-filter-repo` rewrites commit hashes. Existing clones cannot safely use ordinary `git pull` without a deliberate migration plan.

## Final Verification

After push:

```bash
git remote -v
git branch -vv
git status --short --branch
git rev-parse HEAD
git ls-remote origin refs/heads/main
```

The local `HEAD` and remote `refs/heads/main` hashes should match. Confirm `.gitignore` prevented build products, logs, caches, large binary assets, local configs, and secrets from being committed.

## Response Pattern

When helping publish a repo, report:

- Remote type and authentication method used.
- Files or classes of files intentionally excluded.
- Commands run or exact commands the user should run.
- Final local and remote commit hashes when available.
- Any remaining safety risk, especially leaked tokens, private data, large files, or history rewrites.
