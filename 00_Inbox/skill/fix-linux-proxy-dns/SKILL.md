---
name: fix-linux-proxy-dns
description: Diagnose and repair Linux desktop networking cases where browsers or websites fail when VPN/proxy is off while other apps such as WeChat/QQ still connect. Use for symptoms like stale GNOME/system proxy, Clash/Mihomo/Mihomo Party ports left in proxy settings, broken manual DNS, NetworkManager DNS issues, or Chinese-language requests such as 不开VPN打不开网站, 不开代理网页打不开, 微信QQ能联网但浏览器打不开.
---

# Fix Linux Proxy DNS

## Approach

Treat this as a proxy/DNS split-brain problem until proven otherwise. Browser traffic often follows GNOME/system proxy or browser proxy settings, while chat apps may use direct sockets or their own networking stack.

Start with read-only checks. Apply changes only when the user asks to fix the system or approves the specific action. In sandboxed environments, network namespace, D-Bus, `nmcli`, `resolvectl`, `ip`, or `ss` may need escalation to inspect the real host state.

Do not dump VPN subscription profiles, node lists, UUIDs, tokens, account emails, or full browser preference files into the response. Redact or summarize sensitive proxy configuration.

## Diagnose

Check these areas in order:

1. System and shell proxy state:

```bash
env | grep -Ei '^(http_proxy|https_proxy|all_proxy|no_proxy|HTTP_PROXY|HTTPS_PROXY|ALL_PROXY|NO_PROXY)='
gsettings list-recursively org.gnome.system.proxy
```

2. Local proxy listeners and proxy/VPN processes:

```bash
ss -ltnp | grep -E ':(7890|7891|7892|1080|10808|20170)\b' || true
ps -ef | grep -Ei 'clash|mihomo|v2ray|xray|sing-box|verge|proxy|vpn|tailscale|wireguard|openvpn' | grep -v grep || true
```

3. Active route, connection, and DNS:

```bash
ip route show
nmcli -t -f NAME,UUID,TYPE,DEVICE con show --active
nmcli dev show
resolvectl status
```

4. Direct versus proxied connectivity:

```bash
curl -I --noproxy '*' --connect-timeout 5 --max-time 8 https://www.baidu.com
curl -I --connect-timeout 5 --max-time 8 https://www.baidu.com
```

Interpretation:

- Direct fails but proxied succeeds: stale system proxy or direct DNS/connectivity problem is likely.
- `Resolving timed out`: DNS is likely the immediate problem.
- GNOME proxy `mode 'manual'` with `127.0.0.1:<port>`: browsers may depend on a local proxy app.
- Local proxy app running with system proxy enabled: turning off VPN inside the app may leave browsers pointed at the local port.

## DNS Tests

Test the configured DNS servers before changing them:

```bash
dig +time=2 +tries=1 @<dns-server> www.baidu.com A
```

Choose DNS servers that respond on the user's actual network. For users in mainland China, common candidates to test are `223.5.5.5`, `119.29.29.29`, `180.76.76.76`, and the current router/ISP DNS. Do not hardcode these if the user is elsewhere or tests fail.

## Repair

Use the active NetworkManager connection name instead of assuming it is `51`:

```bash
nmcli -t -f NAME,TYPE,DEVICE con show --active
```

If stale system proxy is the problem, disable GNOME system proxy:

```bash
gsettings set org.gnome.system.proxy mode none
```

If a proxy app such as Mihomo Party keeps re-enabling system proxy, disable its system-proxy option in the app UI when possible. If editing files, change only the app's general config key after reading the nearby lines. For Mihomo Party this may look like:

```yaml
sysProxy:
  enable: false
```

If DNS is broken or unstable, update the active connection with DNS servers that passed tests:

```bash
nmcli con mod "<connection-name>" ipv4.ignore-auto-dns yes ipv4.dns "<dns1> <dns2> <dns3>"
nmcli con down "<connection-name>"
nmcli con up "<connection-name>"
```

If router/ISP DNS is preferred, set `ipv4.ignore-auto-dns no` and clear manual DNS instead:

```bash
nmcli con mod "<connection-name>" ipv4.ignore-auto-dns no ipv4.dns ""
nmcli con down "<connection-name>"
nmcli con up "<connection-name>"
```

Warn the user that reconnecting the active Wi-Fi briefly interrupts network access.

## Verify

Confirm the final state:

```bash
gsettings get org.gnome.system.proxy mode
nmcli con show "<connection-name>" | grep -Ei 'ipv4\.(dns|ignore-auto-dns)'
curl -I --noproxy '*' --connect-timeout 5 --max-time 8 https://www.baidu.com
```

Report the specific changed settings and the direct connectivity result. Clarify that sites requiring a VPN/proxy, such as blocked foreign services, may still fail when VPN is off; the repair targets ordinary/direct web access.
