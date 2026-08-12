# Git 双远程仓库配置与推送说明

这里的 `github.com-vision-utils` 不是网站域名，而是 `~/.ssh/config` 中定义的 SSH 主机别名。它最终连接 `github.com`，并指定使用专用密钥 `~/.ssh/vision_utils_deploy_ed25519`。

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

不要手动修改 `.git/HEAD`、`.git/index`、`.git/refs/` 或 `.git/logs/`。使用 Git 命令时，Git 会自动更新这些隐藏文件。

## 认识项目中的 `.git` 目录

![文件管理器中显示的 .git 目录](Image_base/git_hidden_directory.png)

`.git/` 不是项目源代码，而是 Git 为当前仓库维护的数据库，保存暂存区、提交历史、分支、标签和仓库配置等信息。它们的关系可以简单理解为：

```text
工作区中的文件 ──git add──> index（暂存区）──git commit──> objects（对象数据库）
                                                            ↑
                                            HEAD、分支和标签指向其中的提交
```

删除 `.git/` 后，代码通常还在，但该目录不再是 Git 仓库，本地提交历史、分支、标签、暂存状态、远程配置和 reflog 都会丢失。因此不要手动删除或随意修改其中的内容。

| 名称 | 主要作用 | 通常保存的内容 |
| --- | --- | --- |
| `objects/` | Git 的对象数据库 | 文件内容、目录结构、提交和带说明的标签 |
| `refs/` | 保存引用 | 本地分支、远端跟踪分支和标签所指向的提交 |
| `HEAD` | 标记当前检出位置 | 当前分支名称，或 detached HEAD 状态下的提交哈希 |
| `index` | 保存暂存区 | 下一次提交准备包含的文件快照和相关元数据 |
| `config` | 当前仓库的配置 | 远程地址、分支跟踪关系和仓库级配置 |
| `logs/` | 保存引用移动记录 | `HEAD`、本地分支等引用的 reflog |
| `hooks/` | 放置 Git 钩子脚本 | 提交、推送等操作前后自动执行的脚本 |
| `info/` | 保存仓库的辅助信息 | 本机忽略规则等信息 |
| `branches/` | 旧版 Git 的兼容目录 | 旧式远程仓库简称，现代 Git 基本不再使用 |
| `description` | 仓库描述 | 主要供 GitWeb 等工具显示 |
| `FETCH_HEAD` | 记录最近一次获取结果 | `git fetch` 获取到的远端分支及提交 |
| `ORIG_HEAD` | 记录危险操作前的位置 | 合并、变基或重置前的提交，具体是否生成取决于操作 |
| `COMMIT_EDITMSG` | 临时保存提交说明 | 最近一次编辑或使用的提交信息 |

### `objects/`：对象数据库

`objects/` 是 `.git/` 中最核心的目录。Git 不会保存 `v1.cpp`、`v2.cpp`、`v3.cpp` 这样的整套项目副本，而是用哈希标识四类对象：

- `blob`：保存文件内容，不保存文件名；
- `tree`：保存目录结构、文件名及其指向的 blob 或子 tree；
- `commit`：保存根 tree、父提交、作者、时间和提交说明；
- `tag`：保存带说明标签（annotated tag）。

```text
.git/objects/ab/cdef...              # 松散对象，ab 是哈希的前两个字符
.git/objects/pack/                   # 压缩后的对象包
```

相同文件内容可以复用同一个 blob，所以每次提交不会完整复制一遍所有文件。

### `refs/`：分支、远端跟踪分支和标签

分支和标签本质上都是指向提交的引用：

```text
refs/
├── heads/
│   ├── main                         # 本地分支
│   └── utils
├── remotes/
│   ├── origin/main                  # 远端跟踪分支
│   └── gitea/utils
└── tags/
    └── v1.0                         # 标签
```

`.git/refs/heads/main` 通常只保存一行提交哈希。部分引用可能被整理到 `packed-refs`，因此查看全部分支和标签应使用命令，不要只看 `refs/` 目录：

```bash
git branch -a
git tag
```

### `HEAD` 和 `index`

`HEAD` 表示当前检出位置。正常位于 `main` 分支时，它保存：

```text
ref: refs/heads/main
HEAD -> refs/heads/main -> 某个 commit -> 对应的项目快照
```

`HEAD` 直接保存提交哈希时，称为 **detached HEAD（分离头指针）**。`index` 是 Git 维护的二进制暂存区，记录下一次提交所用的文件路径、模式和 blob 哈希等，不是普通文件夹：

```text
修改文件 -> 工作区
git add -> index
git commit -> objects 中的新 tree 和 commit
```

`git add` 后的内容已写入对象数据库，但执行 `git commit` 后才进入提交历史。使用 `git diff --cached` 查看暂存内容。

### `config`、`logs/` 和 `hooks/`

`.git/config` 只对当前仓库生效，常见内容包括：

- `remote "origin"`、`remote "gitea"` 的远程地址；
- 本地分支所跟踪的远端分支；
- 仓库级的用户名、邮箱和其他 Git 选项。

`~/.gitconfig` 是用户的全局配置，`.git/config` 是当前仓库配置。推荐使用 `git config`、`git remote` 和 `git branch` 等命令修改。

`logs/` 保存 `HEAD` 和分支等引用的移动记录，`git reflog` 可通过它找回误删分支或错误重置前的提交。它不会记录每条普通命令，旧记录也可能过期。

`hooks/` 存放 Git 钩子脚本，例如 `pre-commit`、`commit-msg` 和 `pre-push`，可在提交或推送前执行检查。新仓库中的 `*.sample` 只是示例；去掉 `.sample` 并赋予可执行权限后才会生效。`.git/hooks/` 默认不会随代码提交，团队共享钩子可配置 `core.hooksPath`。

### 其他目录和临时文件

| 名称 | 作用 |
| --- | --- |
| `info/exclude` | 仅当前仓库副本使用的忽略规则，不会提交；团队规则应写入 `.gitignore` |
| `branches/` | 旧版 Git 保存远程仓库简称的目录，现代 Git 基本不用 |
| `description` | 主要供 GitWeb 等工具显示仓库说明 |
| `FETCH_HEAD` | 保存最近一次 `fetch` 或 `pull` 获取的远端引用和提交 |
| `ORIG_HEAD` | 保存 merge、rebase 或 reset 等操作前的位置，可能被后续操作覆盖 |
| `COMMIT_EDITMSG` | 临时保存最近使用的提交说明；正式历史应使用 `git log` 查看 |
| `packed-refs` | 集中保存经过压缩整理的分支或标签引用 |
| `MERGE_HEAD` | 正在合并时记录要合入的提交 |
| `CHERRY_PICK_HEAD` | 正在执行 cherry-pick 时记录相关提交 |
| `REBASE_HEAD`、`rebase-merge/` | 变基过程中保存状态 |
| `shallow` | 浅克隆仓库的边界提交 |
| `modules/` | 使用 Git submodule 时保存子模块仓库数据 |
| `worktrees/` | 使用 `git worktree` 时保存附加工作区信息 |

这些内容由 Git 自动创建和删除。遇到冲突时，不要手动删除它们，应使用 `git merge --abort`、`git rebase --continue` 或 `git rebase --abort` 等命令。

简单来说：`objects` 是数据库，`refs` 是分支和标签指针，`HEAD` 是当前位置，`index` 是下一次提交的清单，`logs` 是引用移动记录。日常工作应通过 Git 命令管理它们。

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

只把 `.pub` 公钥添加到 GitHub。可以添加到 GitHub 账号的 **SSH keys**，也可以添加到 `vision_utils` 仓库的 **Deploy keys**；如果使用 Deploy key 推送，必须为它启用写权限。私钥 `vision_utils_deploy_ed25519` 绝对不能上传。

然后在 `~/.ssh/config` 中加入前面展示的 `Host github.com-vision-utils` 配置，并测试：

```bash
ssh -T github.com-vision-utils
```

首次连接可能询问是否信任 GitHub 主机指纹。确认指纹属于 GitHub 后输入 `yes`，SSH 会自动更新 `~/.ssh/known_hosts`。

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

SSH 配置正确时，GitHub 推送不需要输入 GitHub 账号密码；如果私钥设置了口令，SSH 可能要求输入私钥口令。

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

Gitea 使用 HTTPS 时会提示输入用户名和密码。推荐在 Gitea 中创建个人访问令牌，并在 Password 提示处输入令牌。不要把密码或令牌写进 README、`.git/config`、远程 URL 或任何提交记录。

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

不要执行 `git push --all`，因为本仓库同时配置了 GitHub 和 Gitea，并且两个远程承担的用途不同。

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
