# Git 双远程仓库配置与推送说明

本文记录 `/home/liantian/vision_utils` 当前的 Git 配置，以及以后自己配置和推送时需要
涉及的文件与命令。

## 当前配置结论

是的，当前 `vision_utils` 的 GitHub 远程仓库使用 SSH 密钥推送：

```text
origin  git@github.com-vision-utils:qiuyuzhong4-oss/vision_utils.git
```

这里的 `github.com-vision-utils` 不是网站域名，而是 `~/.ssh/config` 中定义的 SSH 主机
别名。它最终连接 `github.com`，并指定使用专用密钥
`~/.ssh/vision_utils_deploy_ed25519`。

当前两个远程仓库及对应分支是：

```text
本地 main  ──推送──> origin/main    GitHub（SSH）
本地 utils ──推送──> gitea/utils    Gitea（HTTPS）
```

## 涉及的文件结构

```text
/home/liantian/
├── .gitconfig                                      # Git 全局姓名、邮箱等配置
├── .ssh/
│   ├── config                                      # 需要配置：SSH 主机别名和密钥路径
│   ├── vision_utils_deploy_ed25519                 # 私钥，禁止上传或发给别人
│   ├── vision_utils_deploy_ed25519.pub             # 公钥，添加到 GitHub
│   └── known_hosts                                 # SSH 首次连接后自动维护
│
├── vision_utils/
│   ├── .git/
│   │   ├── config                                  # 远程地址、分支跟踪关系
│   │   ├── HEAD                                    # Git 自动维护：当前所在分支
│   │   ├── index                                   # Git 自动维护：暂存区
│   │   ├── refs/
│   │   │   ├── heads/
│   │   │   │   ├── main                           # Git 自动维护：本地 main
│   │   │   │   └── utils                          # Git 自动维护：本地 utils
│   │   │   └── remotes/
│   │   │       ├── origin/main                    # Git 自动维护：GitHub 状态
│   │   │       └── gitea/utils                    # Git 自动维护：Gitea 状态
│   │   └── logs/                                  # Git 自动维护：本地操作记录
│   ├── README.md
│   ├── bin/
│   ├── configs/
│   ├── src/
│   └── tests/
│
└── vision_tutorial/
    └── use_git.md                                  # 本文档
```

通常只需要关注下面三个配置文件：

1. `~/.gitconfig`：全局提交者姓名和邮箱；
2. `~/.ssh/config`：选择 GitHub 使用的 SSH 密钥；
3. `项目目录/.git/config`：远程地址和本地分支的跟踪关系。

不要手动修改 `.git/HEAD`、`.git/index`、`.git/refs/` 或 `.git/logs/`。使用 Git 命令时，
Git 会自动更新这些隐藏文件。

## 当前关键配置内容

### `~/.gitconfig`

当前已经配置：

```ini
[user]
    name = liantian
    email = 2707758251@qq.com
```

推荐使用命令修改，不需要直接编辑文件：

```bash
git config --global user.name "liantian"
git config --global user.email "2707758251@qq.com"
```

### `~/.ssh/config`

当前与 `vision_utils` 有关的配置是：

```sshconfig
Host github.com-vision-utils
  HostName github.com
  User git
  IdentityFile /home/liantian/.ssh/vision_utils_deploy_ed25519
  IdentitiesOnly yes
```

其中：

- `Host` 是本机使用的别名；
- `HostName` 才是真正连接的 GitHub 地址；
- `IdentityFile` 指定私钥；
- `IdentitiesOnly yes` 防止 SSH 误用其他密钥。

### `/home/liantian/vision_utils/.git/config`

与两个远程仓库有关的核心配置等价于：

```ini
[remote "origin"]
    url = git@github.com-vision-utils:qiuyuzhong4-oss/vision_utils.git
    fetch = +refs/heads/*:refs/remotes/origin/*

[branch "main"]
    remote = origin
    merge = refs/heads/main

[remote "gitea"]
    url = https://gitea.qutrobot.com/yunhai/vision_learn2026.git
    fetch = +refs/heads/*:refs/remotes/gitea/*

[branch "utils"]
    remote = gitea
    merge = refs/heads/utils
```

推荐用后面的命令生成这些配置，不要手工修改 `.git/config`。

## GitHub SSH：从零配置

当前电脑已经有密钥，不要再次运行生成命令覆盖它。只有在新电脑上没有密钥时，才执行：

```bash
ssh-keygen -t ed25519 \
  -C "vision_utils GitHub deploy key" \
  -f /home/liantian/.ssh/vision_utils_deploy_ed25519
```

设置安全的文件权限：

```bash
chmod 700 /home/liantian/.ssh
chmod 600 /home/liantian/.ssh/config
chmod 600 /home/liantian/.ssh/vision_utils_deploy_ed25519
chmod 644 /home/liantian/.ssh/vision_utils_deploy_ed25519.pub
```

查看公钥：

```bash
cat /home/liantian/.ssh/vision_utils_deploy_ed25519.pub
```

只把 `.pub` 公钥添加到 GitHub。可以添加到 GitHub 账号的 **SSH keys**，也可以添加到
`vision_utils` 仓库的 **Deploy keys**；如果使用 Deploy key 推送，必须为它启用写权限。
私钥 `vision_utils_deploy_ed25519` 绝对不能上传。

然后在 `~/.ssh/config` 中加入前面展示的 `Host github.com-vision-utils` 配置，并测试：

```bash
ssh -T github.com-vision-utils
```

首次连接可能询问是否信任 GitHub 主机指纹。确认指纹属于 GitHub 后输入 `yes`，SSH 会
自动更新 `~/.ssh/known_hosts`。

为仓库设置 GitHub SSH 远程地址：

```bash
cd /home/liantian/vision_utils
git remote set-url origin \
  git@github.com-vision-utils:qiuyuzhong4-oss/vision_utils.git
git remote -v
```

如果仓库还没有名为 `origin` 的远程，使用：

```bash
git remote add origin \
  git@github.com-vision-utils:qiuyuzhong4-oss/vision_utils.git
```

## GitHub SSH：日常推送 `main`

```bash
cd /home/liantian/vision_utils
git switch main
git pull --rebase origin main

# 修改文件后：
git status
git add <需要提交的文件或目录>
git diff --cached
git commit -m "说明本次修改"
git push origin HEAD:main
```

第一次推送一个尚未设置跟踪关系的本地 `main` 时，可以执行：

```bash
git push -u origin main
```

SSH 配置正确时，GitHub 推送不需要输入 GitHub 账号密码；如果私钥设置了口令，SSH 可能
要求输入私钥口令。

## Gitea HTTPS：一次性配置

为已有仓库添加第二个远程：

```bash
cd /home/liantian/vision_utils
git remote add gitea \
  https://gitea.qutrobot.com/yunhai/vision_learn2026.git
git fetch gitea
git remote -v
```

如果已经存在 `gitea`，需要修改地址时使用：

```bash
git remote set-url gitea \
  https://gitea.qutrobot.com/yunhai/vision_learn2026.git
```

在一台新电脑上，本地还没有 `utils`、但远端已有 `gitea/utils` 时执行：

```bash
git fetch gitea
git switch -c utils --track gitea/utils
```

如果本地已经存在 `utils`，只需要：

```bash
git switch utils
git branch --set-upstream-to=gitea/utils utils
```

## Gitea HTTPS：日常推送 `utils`

```bash
cd /home/liantian/vision_utils
git switch utils
git pull --rebase gitea utils

# 修改文件后：
git status
git add <需要提交的文件或目录>
git diff --cached
git commit -m "说明本次修改"
git push gitea HEAD:utils
```

Gitea 使用 HTTPS 时会提示输入用户名和密码。推荐在 Gitea 中创建个人访问令牌，并在
Password 提示处输入令牌。不要把密码或令牌写进 README、`.git/config`、远程 URL 或
任何提交记录。

如果出现 `fetch first` 或 `non-fast-forward`：

```bash
git pull --rebase gitea utils
# 如果有冲突，编辑冲突文件，然后：
git add <已经解决的冲突文件>
git rebase --continue
git push gitea HEAD:utils
```

不确定远端内容是否可以丢弃时，不要使用 `--force` 或 `--force-with-lease`。

## 每次推送前的检查

```bash
cd /home/liantian/vision_utils
git status
git branch -vv
git remote -v
git diff
git diff --cached
```

期望看到的分支跟踪关系是：

```text
main  -> origin/main
utils -> gitea/utils
```

为了避免推错仓库，推荐始终写完整的推送目标：

```bash
# GitHub
git push origin HEAD:main

# Gitea
git push gitea HEAD:utils
```

不要执行 `git push --all`，因为本仓库同时配置了 GitHub 和 Gitea，并且两个远程承担的
用途不同。

## 常用诊断命令

```bash
# 查看当前分支
git branch --show-current

# 查看本地分支及其跟踪的远端分支
git branch -vv

# 查看两个远程地址
git remote -v

# 测试 GitHub SSH 密钥
ssh -T github.com-vision-utils

# 查看 SSH 实际采用的主机、用户和密钥配置
ssh -G github.com-vision-utils

# 查看 Gitea 的远端分支（会要求 HTTPS 认证）
git ls-remote --heads gitea
```
