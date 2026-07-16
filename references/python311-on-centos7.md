# 在 CentOS 7.6 上部署 Python 3.11 运行 qdocse-utils（uv 路线，不用 venv）

CentOS 7 自带 glibc 2.17 / OpenSSL 1.0.2k。glibc 不是障碍（Python 生态的
manylinux2014 基线就是 2.17）；**OpenSSL 才是**：CPython 3.10+（PEP 644）强制要求
OpenSSL ≥ 1.1.1，系统的 1.0.2k 无法满足，且 CentOS 7 已 EOL 不会再升级。

本方案用 uv 安装 python-build-standalone 的预编译 CPython：原生 ELF 二进制、按
manylinux2014（glibc 2.17）基线编译、**OpenSSL 3.x 静态链接在解释器内**——完全不碰
系统 OpenSSL，`yum` 不参与，不污染系统。不建 venv：单用途运维机，依赖直接装进该
解释器自己的 site-packages。

## 在线安装（机器能出网）

```bash
# 1. 安装 uv（静态单二进制，兼容 glibc 2.17）
curl -LsSf https://astral.sh/uv/install.sh | sh

# 2. 安装 Python 3.11（下载 ~30MB，解压到 ~/.local/share/uv/python/）
uv python install 3.11

# 3. 找到解释器路径并软链进 PATH
PY=$(uv python find 3.11)
ln -sf "$PY" ~/.local/bin/python3.11

# 4. 依赖直接装进解释器的 site-packages（不建 venv）。
#    uv 装的解释器自带 pip（python3.11 -m pip --version 确认，一般无需 ensurepip），
#    但带有 PEP 668 的 EXTERNALLY-MANAGED 标记，pip 会拒绝直装；这台解释器是专用的
#    （系统不依赖它），用环境变量放行即可：
export PIP_BREAK_SYSTEM_PACKAGES=1
python3.11 -m pip install paramiko requests gmssl

# 一劳永逸的替代：删除标记文件后 pip 永远直接可用
#   rm ~/.local/share/uv/python/cpython-3.11.*/lib/python3.11/EXTERNALLY-MANAGED
```

## 离线安装（内网机器，推荐路径）

在任一能出网的机器上准备两样东西：

```bash
# a. 解释器 tarball：github.com/astral-sh/python-build-standalone/releases
#    选 cpython-3.11.<x>-x86_64-unknown-linux-gnu-install_only.tar.gz
# b. 依赖轮子（paramiko/cryptography 均有 manylinux2014 轮子）
pip download paramiko requests gmssl -d wheels/ \
    --platform manylinux2014_x86_64 --python-version 311 --only-binary=:all:
```

scp 到目标机后：

```bash
tar -xzf cpython-3.11.*-install_only.tar.gz -C /opt   # 得到 /opt/python/
ln -sf /opt/python/bin/python3.11 /usr/local/bin/python3.11
python3.11 -m pip install --no-index --find-links wheels/ paramiko requests gmssl
```

## 验证

```bash
python3.11 -c "import ssl, tomllib, paramiko; print(ssl.OPENSSL_VERSION)"
# 应输出 OpenSSL 3.x —— 证明用的是内置 OpenSSL 而非系统 1.0.2k
python3.11 qdu.py fleet status --all
```

## 备注

- qdu.py 的 shebang 是 `#!/usr/bin/env python3`：若希望 `./qdu.py` 直接可用，把软链
  命名为 `python3` 放在 PATH 前部，或显式 `python3.11 qdu.py ...`。
- 若有"只允许发行版官方 rpm"的合规限制，替代路线是 SCL `rh-python38`（Red Hat 官方
  3.8）+ 本项目的 3.8 兼容补丁（config.py：`from __future__ import annotations` +
  `tomli` 回退），见仓库讨论记录。
- 本项目实际的最低 Python 要求：3.11（`tomllib`）；打 3.8 补丁后可降至 3.8。
