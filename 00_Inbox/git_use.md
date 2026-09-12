# R2_Vision 仓库使用指南

> 写给 **liantian** 的同事
> 第一次 clone / pull 这个仓库时**务必先读完这一节**,否则可能把本地的模型、标定数据冲掉

---

## 0. 这个仓库里**没有**什么

由于 Git 服务端(Gitea)对单次推送有 1MB 的体积限制,以下内容**不在仓库里**,你 clone 下来后**不会看到这些文件**,需要自己准备:

| 路径 | 是什么 | 来源 |
|------|--------|------|
| `src/rc_camera/model/*.pt` | YOLO 训练好的模型权重 | 团队网盘/OSS,见 §4 |
| `src/rc_camera_driver/models/*.pt` | 训练好的模型权重 | 同上 |
| `src/rc_camera_driver/models/*/weapon.bin` | OpenVINO 推理用的 .bin | 同上 |
| `src/rc_camera_driver/models/*/kfs.bin` | OpenVINO 推理用的 .bin | 同上 |
| `src/rc_camera_driver/models/*/gan.bin` | OpenVINO 推理用的 .bin | 同上 |
| `src/rc_nav/rc_nav_bringup/PCD/*.pcd` | 建好的点云地图 | 团队共享,见 §4 |
| `src/data/output/calib_rms.npy` 等 | 相机标定结果 | 自己标定 |
| `src/rc_nav/rc_localization/FAST_LIO/doc/*` | 第三方 FAST-LIO 仓库的 README 截图/动图 | 不需要,FAST-LIO 是 git submodule 风格的第三方 |
| `src/rc_nav/rc_simulation/livox_laser_simulation_RO2/scan_mode/mid360.csv` | Livox 仿真配置 | 找 liantian 要 |

**.pt 和 .bin 不在仓库**这件事是**故意的**(不然推不上 Gitea),团队约定走网盘共享,见 §4。

---

## 1. 第一次拉取 (全新 clone)

适用于你电脑里**没有**这个项目,或要换一台机器。

```bash
# 1. 选好目标目录(比如桌面)
cd ~/桌面

# 2. clone (会提示输入 Gitea 用户名密码,用户名 liantian,密码找 liantian 要)
git clone https://gitea.qutrobot.top/liantian/26_R2_version.git
# 等几秒,1.5MB 一会就下完

# 3. 进入项目
cd 26_R2_version

# 4. 装 ROS 2 humble (如果还没装),参考 README.md

# 5. 装 r2-ai conda 环境,装好以后:
export CONDA_SH="$HOME/miniconda3/etc/profile.d/conda.sh"
# (路径按你本机实际调整,脚本里默认找 $CONDA_SH,找不到会报错)

# 6. 从网盘下模型和地图,放到对应位置 (见 §4)

# 7. 编译
./build.sh

# 8. 启动
./mission.sh   # 或 ./run.sh / ./version.sh / ./camera.sh,看你要启哪些节点
```

---

## 2. 关键提醒:历史被重写过

**这个仓库的 git 历史在 2026-06-13 经历过一次重写** (`git filter-repo`),目的是清掉几个大文件(GIF、PDF、.pt、.bin 等),让仓库体积从 90MB 降到 1.5MB。

**重写后,所有 commit 的 hash 都变了**。所以你**不能用普通的 `git pull`** 来同步,会报:

```
fatal: refusing to merge unrelated histories
```

**正确做法见下一节**。

---

## 3. 你本地已有项目,要同步新代码

⚠️ **操作前先备份你的本地模型和标定数据**!下面有 `git reset --hard`,会丢你本地所有未提交的改动。

```bash
cd ~/桌面/26_R2_version

# 1. 备份本地的模型和标定数据 (重置会清掉这些)
mkdir -p /tmp/r2_backup
cp -r src/rc_camera/model/*.pt /tmp/r2_backup/ 2>/dev/null || true
cp -r src/rc_camera_driver/models /tmp/r2_backup/ 2>/dev/null || true
cp -r src/data/output /tmp/r2_backup/output 2>/dev/null || true
# (其他你自己加的、git 里没有的东西,自己看着备份)

# 2. 拉取远端最新状态
git fetch origin

# 3. ⚠️ 强制对齐到远端 main,这一步会丢你本地所有未提交的改动
git reset --hard origin/main

# 4. 恢复备份
cp /tmp/r2_backup/*.pt src/rc_camera/model/ 2>/dev/null || true
cp -r /tmp/r2_backup/models/* src/rc_camera_driver/models/ 2>/dev/null || true
cp -r /tmp/r2_backup/output/* src/data/output/ 2>/dev/null || true

# 5. 检查
git status          # 应该只剩几个 .pt/.bin 显示 "untracked" (被 .gitignore 拦下)
ls src/rc_camera/model/   # 应该有 weapon.pt kfs.pt gan.pt 三个文件
```

**为什么 `git reset --hard` 而不是 `git pull`?**
因为 commit hash 全变了,git 认为你的本地历史和远端是"两个不相关的分支",pull 会拒绝合并。`reset --hard` 直接把本地指针指向远端,丢弃老历史。

---

## 4. 模型和地图从哪拿

**还在搭**。需要 liantian 在团队网盘/OSS 上传以下内容,放到对应位置:

```
src/rc_camera/model/
├── weapon.pt        # 武器识别模型 (~6MB)
├── kfs.pt           # KFS 识别模型 (~6MB)
└── gan.pt           # 矿石识别模型 (~6MB)

src/rc_camera_driver/models/
├── weapon.pt
├── kfs.pt
├── gan.pt
├── weapon_openvino_model/
│   ├── weapon.bin   # OpenVINO 编译后 (~12MB)
│   └── weapon.xml
├── kfs_openvino_model/
│   ├── kfs.bin
│   └── kfs.xml
└── gan_openvino_model/
    ├── gan.bin
    └── gan.xml

src/rc_nav/rc_nav_bringup/PCD/
└── RC_2026.pcd      # 建好的点云地图
```

> TODO: liantian 填一下网盘链接,这里换成具体地址
> 计划方案: 1) Git LFS (需要 Gitea 服务端开启 LFS 支持)  2) 团队 OSS  3) 内部网盘

---

## 5. 启动脚本的 conda 路径

`mission.sh` / `camera.sh` 现在通过环境变量 `CONDA_SH` 找 conda,而不是硬编码路径。第一次用之前:

```bash
# 加进 ~/.bashrc 让所有终端都生效
echo 'export CONDA_SH="$HOME/miniconda3/etc/profile.d/conda.sh"' >> ~/.bashrc
source ~/.bashrc

# 验证
ls "$CONDA_SH"   # 应该能列出来
```

如果你用的是 miniforge / anaconda,路径不一样,自己改:
- miniforge: `~/miniforge3/etc/profile.d/conda.sh`
- anaconda: `~/anaconda3/etc/profile.d/conda.sh`

---

# 附录:liantian 推送时踩的坑 (给后面的人参考)

## A.1 第一次推送报 HTTP 413

**现象:**
```
error: RPC 失败。HTTP 413 curl 22 The requested URL returned error: 413
send-pack: unexpected disconnect while reading sideband packet
```

**原因:** Gitea 反向代理的 Nginx 默认 `client_max_body_size 1m`,本地要推 83MB(1500+ 对象),超过了限制。

**解决思路 (按推荐顺序):**

### 方案 1 (推荐): 清理大文件

不能入 git 的东西:
- 模型权重 (`.pt`, `.bin`) - 用 LFS 或网盘
- 论文/截图/动图 (`.pdf`, `.gif`, `.png`) - 不应该入主仓
- 第三方仓库完整代码 (比如 FAST-LIO、small-gicp) - 改用 git submodule 引用
- 大 CSV / PCD / PLY 数据 - 走网盘

具体做的步骤(顺序很重要,**先理解为啥要这样**,见 §A.6):

```bash
# 1. 更新 .gitignore,加上所有不想跟踪的路径
# 2. git rm --cached <文件>  从索引里移除(本地文件保留)
#    ⚠️ 这一步只让"最新 commit"看不到这些文件,历史里还在
# 3. ⚠️ 必须重写历史,否则 push 时 git 仍然要打包历史里的 blob
#    这一步会重写所有 commit hash,远端必须 --force,同事必须 reset --hard
pip3 install --user git-filter-repo
git filter-repo --force \
  --path src/rc_camera_driver/models \
  --path src/rc_nav/rc_localization/FAST_LIO/doc \
  --path src/rc_nav/rc_simulation/pb_rc_simulation/meshes \
  --path src/rc_nav/rc_perception/linefit_ground_segementation_ros2/doc \
  --path src/rc_nav/rc_localization/small_gicp_relocalization/third_party/small_gicp/data \
  --path src/rc_nav/rc_localization/small_gicp_relocalization/third_party/small_gicp/docs/assets \
  --path src/rc_nav/rc_localization/point_lio/Log \
  --invert-paths
git reflog expire --expire=now --all
git gc --prune=now --aggressive
du -sh .git  # 实测: 100M → 4.3M
```

### 方案 2: 改 Gitea 服务端 Nginx 限制 (如果你是服务器管理员)

```nginx
# /etc/nginx/conf.d/gitea.conf
client_max_body_size 500m;
```
然后 `sudo nginx -s reload`。Gitea 自身的 `app.ini` 也有对应项:
```ini
[server]
LFS_MAX_FILE_SIZE = 1073741824
UPLOAD_FILE_SIZE_MAX = 1073741824
```

### 方案 3: 改用 Git LFS

```bash
git lfs install
git lfs track "*.pt"
git lfs track "*.bin"
git add .gitattributes
git commit -m "track with LFS"
```
⚠️ 需要 Gitea 服务端开启 LFS 支持。

## A.2 推送被拒绝 (fetch first)

**现象:**
```
! [rejected]        main -> main (fetch first)
error: 无法推送一些引用到 '...'
```

**原因:** 远端有本地没有的 commit,通常是建仓库时勾选了"自动初始化"产生了一个 README。

**解决:**
```bash
# 新仓库直接覆盖:
git push -u origin main --force
```

## A.3 远程地址写错 / 已存在

```bash
# 改 URL
git remote set-url origin https://gitea.qutrobot.top/liantian/26_R2_version.git

# 删掉重建
git remote remove origin
git remote add origin https://gitea.qutrobot.top/liantian/26_R2_version.git
```

## A.4 shell 脚本里硬编码 /home/robofish/...

仓库里原本的 `run.sh` / `mission.sh` / `camera.sh` 里有 `/home/robofish/...` 这种**前同事的本机路径**。已经全部清理过:
- 脚本里的 `cd` 改成 `$SCRIPT_DIR` (自动定位脚本所在目录)
- conda 路径改成读 `$CONDA_SH` 环境变量,缺省 `$HOME/miniconda3/...`

**改动后请确认:** `grep -rn "robofish\|/home/" . --exclude-dir=.git | grep -v '\.md'` 应该没有结果。

## A.5 git-filter-repo 注意事项

`git-filter-repo` 会**重写所有 commit 的 hash**,改完后:
- 本地: 直接用,没影响
- 远端: `git push --force` 才能推上去
- 同事: 必须用 `git reset --hard origin/main` 而不是 `git pull` (见 §3)

---

## A.6 取消跟踪 ≠ push 体积变小 —— 何时必须 filter-repo

**这一节是 2026-06-21 才补的,前面 §A.1 没写清楚。**

`.gitignore` 和 `git rm --cached` **只影响"未来"**:
- `.gitignore` 让新文件不被 `git add`
- `git rm --cached` 让某个文件从"已跟踪"变成"未跟踪",**磁盘文件保留**
- 它们都**不动历史**,历史里那些 blob 还在 `.git/objects/` 里躺着

后果:你 `git push` 时,git 要把"远端没有"的所有对象打包上传,历史里的旧 blob **全部要被装进 pack**。所以即使你刚刚 `git rm --cached` 删了 50MB 的文件,这次 push 的 pack 体积**不会变小**,该 413 还是 413。

**判断何时必须 filter-repo**:
- ✅ push pack 体积远超 Gitea 限制(典型 > 50MB,容易触发 413)
- ✅ 历史里残留着 `.pt` / `.bin` / 大 `*.pcd` / `*.ply` / `*.bag` / 视频文件等
- ✅ 远端只有你一个人在用,或者你能通知所有协作者

**filter-repo 是"破坏性"操作**,用它之前要确认:
1. 当前 `.git` 已经备份(见下面命令)
2. 远端允许 `--force` push,或者你愿意"删远端 main + 重建"
3. 没有未通知的协作者(他们的本地历史会和远端脱钩,必须 `git reset --hard origin/main`)

**完整流程(2026-06-21 实测,把 100M → 4.3M)**:
```bash
cd ~/桌面/26_R2_version

# 0) 备份!这一步不可逆
BAK=".git.bak.$(date +%Y%m%d_%H%M%S)"
cp -r .git "$BAK"
echo "备份: $BAK"

# 1) 装 filter-repo(没装就装)
#    pipx install git-filter-repo
#    或: pip install --user git-filter-repo

# 2) 清历史
git filter-repo --force \
  --path src/rc_camera_driver/models \
  --path src/rc_nav/rc_localization/FAST_LIO/doc \
  --path src/rc_nav/rc_simulation/pb_rc_simulation/meshes \
  --path src/rc_nav/rc_perception/linefit_ground_segementation_ros2/doc \
  --path src/rc_nav/rc_localization/small_gicp_relocalization/third_party/small_gicp/data \
  --path src/rc_nav/rc_localization/small_gicp_relocalization/third_party/small_gicp/docs/assets \
  --path src/rc_nav/rc_localization/point_lio/Log \
  --invert-paths

# 3) 收紧
git reflog expire --expire=now --all
git gc --prune=now --aggressive

# 4) 看效果
du -sh .git   # 应该比备份小一个数量级

# 5) 推(走 SSH,见 §A.7)
git push gitea main --force

# 6) 远端成功后再观察几天,确认没问题,删备份
rm -rf "$BAK"
```

**回滚**(如果 filter-repo 后出问题):
```bash
rm -rf .git
mv "$BAK" .git
# 历史就回到 filter-repo 之前的状态
```

---

## A.7 Gitea SSH 配置(非标准端口 222)

HTTPS 在我们这台 Gitea 上有几个烦人的小毛病:
- 每次 push 都要输用户名密码
- URL 偶尔出现奇怪的编码(比如 `https://%0Dliantian@...` 这种)
- Gitea 实例有时候会重定向到非标准域名

**SSH 一次配置,之后免输入**。本仓库的 Gitea SSH 信息:
- 域名: `gitea.qutrobot.top`(其实指向 `154.37.212.77`)
- 端口: **`222`**(不是默认 22,所以必须写配置)
- 用户: `git`
- 仓库: `liantian/26_R2_version`

**首次配置步骤**:

```bash
# 1) 看有没有现成 key,没就生成一对
ls ~/.ssh/id_*.pub 2>/dev/null
# 啥也没有的话:
ssh-keygen -t ed25519 -C "liantian@你的邮箱"
# 一路回车,密码留空

# 2) 公钥贴到 Gitea 网页
#    https://gitea.qutrobot.top/user/settings/keys → 增加密钥
cat ~/.ssh/id_ed25519.pub   # 复制输出贴上去
#    名称随便写,比如 "robofish-laptop"

# 3) 写 ~/.ssh/config(关键,端口 222 必须靠这个)
mkdir -p ~/.ssh && chmod 700 ~/.ssh
touch ~/.ssh/config && chmod 600 ~/.ssh/config
cat >> ~/.ssh/config << 'EOF'

# Gitea for liantian's 26_R2_version project
# 两个域名都指向同一台机器,端口 222 非标准
Host gitea.qutrobot.top 154.37.212.77
    HostName 154.37.212.77
    Port 222
    User git
    IdentityFile ~/.ssh/id_ed25519   # 或 id_rsa,看你用哪对
    IdentitiesOnly yes               # 防止 SSH 乱试别的 key
    PreferredAuthentications publickey
    StrictHostKeyChecking accept-new  # 第一次自动接受 host key
EOF

# 4) 改 remote URL
cd ~/桌面/26_R2_version
git remote set-url gitea ssh://git@gitea.qutrobot.top:222/liantian/26_R2_version.git

# 5) 验证(第一次会提示 "Are you sure",输 yes 即可)
ssh -T git@154.37.212.77
# 期望输出:
#   Hi there, <username>! You've successfully authenticated,
#   but Gitea does not provide shell access.

# 6) 干跑确认路径通
git push gitea main --dry-run --force
# 期望输出: To ssh://gitea.qutrobot.top:222/...
#          + <old-sha>...<new-sha> main -> main (forced update)
```

**几个常见坑**:

- **`Permission denied (publickey)`**: 多半是 `IdentityFile` 路径写错,或 Gitea 端没保存公钥。跑 `ssh -vT git@154.37.212.77` 看 "Offering public key: ..." 那行,确认它在试你**期望的那把**。
- **端口没生效**: 没写 `~/.ssh/config` 时,直接 `ssh://git@gitea.qutrobot.top:222/...` 也能用(端口写在 URL 里),但更推荐用 config,后续 `ssh git@154.37.212.77` 这种简写也能用。
- **`StrictHostKeyChecking no`**: **不要**用 `no`,它会无视 host key 变化,容易被中间人攻击。用 `accept-new`(接受新的、但拒绝已变更的)。
- **HTTPS 还能用吗**: 能。`gitea` remote 改成 SSH 后,`origin`(GitHub)还是 HTTPS。两条腿走路没问题。
- **换机器**: 重复步骤 1、2、3。每台机器一对 key,Gitea 上一个用户可以挂多把 key(命名区分即可)。

**何时用 SSH / 何时用 HTTPS**:
- ✅ SSH: 你自己的主力开发机,长期用同一个仓库
- ✅ HTTPS: 临时机器,或者不想配 key
- ⚠️ HTTPS 不会解决 413!那是体积问题,见 §A.6

---

## 写在最后

如果这份文档过时了,直接改;有坑再加,别等踩完才补。
