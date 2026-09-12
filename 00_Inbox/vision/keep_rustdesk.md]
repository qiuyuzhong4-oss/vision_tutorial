liantian@bing:~$ /home/liantian/setup_remote_control.sh
[sudo] liantian 的密码： 
Installing RustDesk from /home/liantian/rustdesk-1.4.8-x86_64.deb
正在读取软件包列表... 完成
正在分析软件包的依赖关系树... 完成
正在读取状态信息... 完成                 
注意，选中 'rustdesk' 而非 '/home/liantian/rustdesk-1.4.8-x86_64.deb'
下列软件包是自动安装的并且现在不需要了：
  dctrl-tools gimp-data libbabl-0.1-0 libfwupd2 libfwupdplugin5 libgcab-1.0-0
  libgegl-0.4-0 libgegl-common libgimp2.0 libmng2 libnvidia-common-580
  libnvidia-extra-580 libsmbios-c2 nvidia-compute-utils-580
  nvidia-firmware-580-580.126.09 nvidia-utils-580
使用'sudo apt autoremove'来卸载它(它们)。
将会同时安装下列软件：
  libxdo3
下列【新】软件包将被安装：
  libxdo3 rustdesk
升级了 0 个软件包，新安装了 2 个软件包，要卸载 0 个软件包，有 320 个软件包未被升级。
需要下载 21.0 kB/23.4 MB 的归档。
解压缩后会消耗 78.8 kB 的额外空间。
获取:1 /home/liantian/rustdesk-1.4.8-x86_64.deb rustdesk amd64 1.4.8 [23.4 MB]
获取:2 https://mirrors.ustc.edu.cn/ubuntu jammy/universe amd64 libxdo3 amd64 1:3.20160805.1-4 [21.0 kB]
已下载 21.0 kB，耗时 1秒 (24.0 kB/s)                 
正在选中未选择的软件包 libxdo3:amd64。
(正在读取数据库 ... 系统当前共安装有 411337 个文件和目录。)
准备解压 .../libxdo3_1%3a3.20160805.1-4_amd64.deb  ...
正在解压 libxdo3:amd64 (1:3.20160805.1-4) ...
正在选中未选择的软件包 rustdesk。
准备解压 .../rustdesk-1.4.8-x86_64.deb  ...
Failed to stop rustdesk.service: Unit rustdesk.service not loaded.
正在解压 rustdesk (1.4.8) ...
正在设置 libxdo3:amd64 (1:3.20160805.1-4) ...
正在设置 rustdesk (1.4.8) ...
Created symlink /etc/systemd/system/multi-user.target.wants/rustdesk.service → /lib/systemd/system/rustdesk.service.
正在处理用于 hicolor-icon-theme (0.17-2) 的触发器 ...
正在处理用于 gnome-menus (3.36.0-1ubuntu3) 的触发器 ...
正在处理用于 libc-bin (2.35-0ubuntu3.13) 的触发器 ...
正在处理用于 mailcap (3.70+nmu1ubuntu1) 的触发器 ...
正在处理用于 desktop-file-utils (0.26-1ubuntu3) 的触发器 ...
N: 由于文件'/home/liantian/rustdesk-1.4.8-x86_64.deb'无法被用户'_apt'访问，已脱离沙盒并提权为根用户来进行下载。 - pkgAcquire::Run (13: 权限不够)
Enabling SSH server
Synchronizing state of ssh.service with SysV service script with /lib/systemd/systemd-sysv-install.
Executing: /lib/systemd/systemd-sysv-install enable ssh
Paste SSH public key for liantian (empty to skip): 
Enabling RustDesk service
RustDesk config string for self-hosted server (empty for public server): 
RustDesk permanent password (empty to skip): 
Done!

SSH status:
● ssh.service - OpenBSD Secure Shell server
     Loaded: loaded (/lib/systemd/system/ssh.service; enabled; vendor preset: enabled)
     Active: active (running) since Sun 2026-07-12 13:34:31 CST; 1 day 16h ago
       Docs: man:sshd(8)
             man:sshd_config(5)
   Main PID: 1239 (sshd)
      Tasks: 1 (limit: 18208)
     Memory: 1.9M
        CPU: 18ms
     CGroup: /system.slice/ssh.service
             └─1239 "sshd: /usr/sbin/sshd -D [listener] 0 of 10-100 startups"


RustDesk status:
● rustdesk.service - RustDesk
     Loaded: loaded (/lib/systemd/system/rustdesk.service; enabled; vendor preset: enabled)
     Active: active (running) since Tue 2026-07-14 06:22:01 CST; 38s ago
   Main PID: 335258 (rustdesk)
      Tasks: 167 (limit: 18208)
     Memory: 157.2M
        CPU: 14.522s
     CGroup: /system.slice/rustdesk.service
             ├─335258 /usr/bin/rustdesk --service
             ├─335417 sudo -E XDG_RUNTIME_DIR=/run/user/1000 -u liantian /usr/share/rustdesk/rustdesk --server
             ├─335418 /usr/share/rustdesk/rustdesk --server
             ├─335426 /usr/share/rustdesk/rustdesk --tray
             ├─339235 /bin/sh -c "ps -u 1000 -f | grep -E 'xdg-desktop-portal' | grep -v 'grep' | tail -1 | awk '{print \$2}' | xargs -I__ cat /proc/__/environ 2>/dev/null | tr '\\0' '\\n' | grep '^XAUTHORITY=' | tail -1 | sed 's/XAUTHORITY=//g'"
             ├─339236 ps -u 1000 -f
             ├─339237 grep -E xdg-desktop-portal
             ├─339238 grep -v grep

RustDesk ID:
30598270

Local addresses:
10.85.29.148 172.17.0.1 172.18.0.1 240a:42a7:2:a33:c76:21cf:db61:c38c 240a:42a7:2:a33:61d7:644b:4355:b3d7 

