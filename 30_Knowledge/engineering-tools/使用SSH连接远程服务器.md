# 使用SSH连接远程服务器（Windows / Ubuntu）

<p align='right'><b>--neozng1@hnu.edu.cn</b></p>

本文介绍如何在 Windows 和 Ubuntu 环境下使用 SSH 连接远程服务器。SSH 常用于登录 Linux 服务器、上传下载文件、远程执行命令等场景。

连接前需要准备以下信息：

- 服务器 IP 地址或域名，例如 `192.168.1.100` 或 `example.com`
- 服务器用户名，例如 `root`、`ubuntu`、`liantian`
- SSH 端口，默认是 `22`，如果服务器修改过端口，需要使用实际端口
- 登录方式：密码登录或密钥登录

## 一、Windows 下使用 SSH

### 1. 安装 OpenSSH 客户端

Windows 10 及其以上版本都原生支持了 SSH 的安装，打开设置，在应用和功能中选择**可选功能**一项：

![image-20220421155224953](typora-user-images\image-20220421155224953.png)

随后添加我们需要的功能：

![image-20220421155313084](typora-user-images\image-20220421155313084.png)

因为我们要连接到服务器端，本机作为客户端，所以在里面搜索**OpenSSH客户端**（如果希望本机作为服务器，则安装OpenSSH服务器端应用），选中并安装：

![image-20220421155407923](typora-user-images\image-20220421155407923.png)

安装好之后，还需要启动OpenSSH的服务。打开任务管理器（ctrl+alt+delete或右键任务栏打开），选择**服务**选项卡，点击**打开服务**：

![image-20220421155638148](typora-user-images\image-20220421155638148.png)

随后找到 OpenSSH Authentication Agent 这一项，右键，点击启动。若**启动**是灰色的，则点击进入**属性**，将启动类型改为**自动**：

![image-20220421160046466](typora-user-images\image-20220421160046466.png)

随后验证安装，打开一个命令提示符（win+R，输入cmd后回车），在cmd中输入`ssh`后回车，若出现如下界面则表示安装成功：

![image-20220421160440965](typora-user-images\image-20220421160440965.png)

若安装的是**服务器端**（客户端无须此步骤），最后还需要启动SSH服务，**以管理员权限启动CMD**：

![image-20220421160905119](typora-user-images\image-20220421160905119.png)

输入`net start sshd`后回车，若显示：

![image-20220421161523496](typora-user-images\image-20220421161523496.png)

说明启动成功。

### 2. 生成密钥对

打开一个cmd，输入`ssh-keygen`然后回车：

![image-20220421161634875](typora-user-images\image-20220421161634875.png)

会出现上图所示的命令，询问你将密钥存储在什么地方，小白直接按回车即可。

![image-20220421161744556](typora-user-images\image-20220421161744556.png)

然后出现上图所示的提示，让你输入保护访问密码，若创建后之后每次建立SSH连接都需要输入解锁密钥的密码。为了方便起见，直接回车：

![image-20220421161949205](typora-user-images\image-20220421161949205.png)

然后就会生成你的用于ssh连接的公私钥了。如果没有修改，那么它们被保存在默认路径下，去看看：

![image-20220421162057250](typora-user-images\image-20220421162057250.png)

有两个文件，上面的是**私钥**，千万不要告诉别人；下面的是公钥，需要把它加入服务器端的可信列表中。在前一步设置密码的时候，就是对私钥的访问进行加密，防止私钥泄露。不过在自己的电脑上一般比较安全，可以选择不加。

### 3. 将公钥添加到远程服务器

如果使用密钥登录，需要把本机生成的公钥添加到服务器用户目录下的 `~/.ssh/authorized_keys` 文件中。

在 Windows 的 cmd 中查看公钥内容：

```cmd
type %USERPROFILE%\.ssh\id_rsa.pub
```

如果生成密钥时使用的是新格式 `ed25519`，则查看：

```cmd
type %USERPROFILE%\.ssh\id_ed25519.pub
```

复制输出的整行内容，然后登录服务器，将其追加到服务器对应用户的 `~/.ssh/authorized_keys` 中。注意：`.pub` 文件是公钥，可以放到服务器；没有 `.pub` 后缀的是私钥，不能发给别人。

### 4. 连接远程服务器

打开 cmd 或 PowerShell，输入：

```cmd
ssh 用户名@服务器IP
```

例如：

```cmd
ssh ubuntu@192.168.1.100
```

如果服务器 SSH 端口不是默认的 `22`，需要加上 `-p` 参数：

```cmd
ssh ubuntu@192.168.1.100 -p 2222
```

如果需要指定私钥文件：

```cmd
ssh -i %USERPROFILE%\.ssh\id_rsa ubuntu@192.168.1.100
```

第一次连接时会提示是否信任服务器指纹，确认 IP 或域名无误后输入 `yes` 回车即可。

## 二、Ubuntu 下使用 SSH

Ubuntu 通常自带 SSH 客户端，可以直接使用 `ssh` 命令。如果没有安装，按下面步骤安装。

### 1. 检查或安装 OpenSSH 客户端

打开终端，输入：

```bash
ssh -V
```

如果能看到 OpenSSH 版本信息，说明客户端已经安装。若提示找不到命令，则安装：

```bash
sudo apt update
sudo apt install openssh-client
```

安装完成后再次执行：

```bash
ssh -V
```

确认安装成功。

### 2. 使用密码连接远程服务器

最基本的连接命令是：

```bash
ssh 用户名@服务器IP
```

例如：

```bash
ssh ubuntu@192.168.1.100
```

如果服务器使用非默认端口，例如 `2222`：

```bash
ssh ubuntu@192.168.1.100 -p 2222
```

第一次连接时会出现类似下面的提示：

```text
Are you sure you want to continue connecting (yes/no/[fingerprint])?
```

确认服务器地址正确后，输入 `yes`，然后按照提示输入服务器用户密码。

### 3. 在 Ubuntu 上生成密钥对

推荐使用 `ed25519` 类型密钥：

```bash
ssh-keygen -t ed25519 -C "your_email@example.com"
```

如果服务器较旧，不支持 `ed25519`，可以使用 RSA：

```bash
ssh-keygen -t rsa -b 4096 -C "your_email@example.com"
```

生成过程中会询问保存路径，直接回车即可使用默认路径：

- 私钥：`~/.ssh/id_ed25519` 或 `~/.ssh/id_rsa`
- 公钥：`~/.ssh/id_ed25519.pub` 或 `~/.ssh/id_rsa.pub`

私钥只能保存在本机，不能上传或发送给他人；公钥可以添加到远程服务器。

### 4. 上传公钥到服务器

Ubuntu 下推荐使用 `ssh-copy-id` 自动上传公钥：

```bash
ssh-copy-id -i ~/.ssh/id_ed25519.pub 用户名@服务器IP
```

例如：

```bash
ssh-copy-id -i ~/.ssh/id_ed25519.pub ubuntu@192.168.1.100
```

如果服务器 SSH 端口不是 `22`：

```bash
ssh-copy-id -i ~/.ssh/id_ed25519.pub -p 2222 ubuntu@192.168.1.100
```

上传完成后，再次连接服务器：

```bash
ssh ubuntu@192.168.1.100
```

如果配置成功，通常不再需要输入服务器用户密码。

如果没有 `ssh-copy-id` 命令，也可以手动复制公钥：

```bash
cat ~/.ssh/id_ed25519.pub
```

复制输出内容后，登录服务器执行：

```bash
mkdir -p ~/.ssh
chmod 700 ~/.ssh
echo "这里粘贴你的公钥内容" >> ~/.ssh/authorized_keys
chmod 600 ~/.ssh/authorized_keys
```

### 5. 使用指定私钥连接

当有多个密钥时，可以通过 `-i` 指定使用哪个私钥：

```bash
ssh -i ~/.ssh/id_ed25519 ubuntu@192.168.1.100
```

如果服务器使用非默认端口：

```bash
ssh -i ~/.ssh/id_ed25519 ubuntu@192.168.1.100 -p 2222
```

### 6. 配置 SSH 快捷登录

如果经常连接同一台服务器，可以编辑 `~/.ssh/config`：

```bash
nano ~/.ssh/config
```

写入：

```text
Host myserver
    HostName 192.168.1.100
    User ubuntu
    Port 22
    IdentityFile ~/.ssh/id_ed25519
```

保存后修改权限：

```bash
chmod 600 ~/.ssh/config
```

之后只需要输入：

```bash
ssh myserver
```

即可连接服务器。

### 7. 上传和下载文件

可以使用 `scp` 在本地和服务器之间传输文件。

从 Ubuntu 本地上传文件到服务器：

```bash
scp local_file.txt ubuntu@192.168.1.100:/home/ubuntu/
```

从服务器下载文件到 Ubuntu 本地当前目录：

```bash
scp ubuntu@192.168.1.100:/home/ubuntu/remote_file.txt ./
```

如果需要传输文件夹，加入 `-r`：

```bash
scp -r local_folder ubuntu@192.168.1.100:/home/ubuntu/
```

如果服务器端口不是 `22`，`scp` 使用大写 `-P` 指定端口：

```bash
scp -P 2222 local_file.txt ubuntu@192.168.1.100:/home/ubuntu/
```

### 8. Ubuntu 作为 SSH 服务器

如果希望别人通过 SSH 连接到这台 Ubuntu 电脑，需要安装并启动 SSH 服务端：

```bash
sudo apt update
sudo apt install openssh-server
sudo systemctl enable --now ssh
```

查看 SSH 服务状态：

```bash
sudo systemctl status ssh
```

查看本机 IP 地址：

```bash
ip addr
```

如果开启了防火墙，需要允许 SSH：

```bash
sudo ufw allow ssh
sudo ufw status
```

其他电脑即可使用下面命令连接这台 Ubuntu：

```bash
ssh 用户名@Ubuntu主机IP
```

## 三、常见问题

### 1. `Permission denied (publickey)`

常见原因：

- 公钥没有正确添加到服务器的 `~/.ssh/authorized_keys`
- 连接时使用了错误的用户名
- 指定了错误的私钥文件
- 服务器禁止密码登录，但本机密钥没有配置好

可以使用详细模式查看原因：

```bash
ssh -v 用户名@服务器IP
```

### 2. `Connection refused`

说明服务器拒绝连接，常见原因：

- 服务器没有启动 SSH 服务
- SSH 端口写错了
- 服务器防火墙或云服务器安全组没有放行 SSH 端口

如果你能登录服务器本机，可以检查：

```bash
sudo systemctl status ssh
```

### 3. `Connection timed out`

说明网络无法连通，常见原因：

- IP 地址或域名写错
- 本机和服务器网络不通
- 云服务器安全组没有开放对应端口
- 校园网、公司网或防火墙拦截了连接

### 4. 密钥文件权限过宽

在 Ubuntu 中如果私钥权限过宽，SSH 会拒绝使用该私钥。可以修正权限：

```bash
chmod 700 ~/.ssh
chmod 600 ~/.ssh/id_ed25519
chmod 600 ~/.ssh/config
```

如果使用 RSA 私钥，则执行：

```bash
chmod 600 ~/.ssh/id_rsa
```

记得再VScode里面也有用来管理ssh的插件也可以看看那个