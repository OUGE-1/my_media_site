# -*- coding: utf-8 -*-
"""
Gitee 项目安装器（精简版）
核心功能：下载项目代码

环境和依赖相关操作仅询问用户，默认不执行

用法：python gitee_installer.py
"""

import os
import sys
import json
import shutil
import zipfile
import subprocess
import tempfile
import urllib.request
import urllib.error


# ========== 默认配置 ==========
DEFAULT_CONFIG = {
    "gitee_owner": "xiaotu20",
    "gitee_repo": "my_media_site",
    "gitee_branch": "main",
    "install_dir": "",
    "use_git": True,
    "token": "",
}
CONFIG_FILE = "installer_config.json"
# ============================


# ========== 终端颜色 ==========
class C:
    RESET = "\033[0m"
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    CYAN = "\033[96m"
    MAGENTA = "\033[95m"
    BOLD = "\033[1m"

    @classmethod
    def disable(cls):
        cls.RESET = cls.RED = cls.GREEN = cls.YELLOW = ""
        cls.BLUE = cls.CYAN = cls.MAGENTA = cls.BOLD = ""

    @staticmethod
    def _enable_ansi():
        if sys.platform != "win32":
            return True
        try:
            import ctypes
            k = ctypes.windll.kernel32
            k.SetConsoleMode(k.GetStdHandle(-11), 7)
            return True
        except Exception:
            return False


if not C._enable_ansi():
    C.disable()


def info(msg):  print(f"{C.CYAN}[INFO]{C.RESET} {msg}")
def ok(msg):    print(f"{C.GREEN}[ OK ]{C.RESET} {msg}")
def warn(msg):  print(f"{C.YELLOW}[WARN]{C.RESET} {msg}")
def error(msg): print(f"{C.RED}[FAIL]{C.RESET} {msg}")
def title(msg):
    print(f"\n{C.BOLD}{C.BLUE}{'=' * 60}{C.RESET}")
    print(f"{C.BOLD}{C.BLUE}  {msg}{C.RESET}")
    print(f"{C.BOLD}{C.BLUE}{'=' * 60}{C.RESET}")


# ========== 配置读写 ==========
def load_config():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                cfg = json.load(f)
            merged = DEFAULT_CONFIG.copy()
            merged.update(cfg)
            return merged
        except Exception as e:
            warn(f"读取配置失败：{e}")
    return DEFAULT_CONFIG.copy()


def save_config(cfg):
    try:
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(cfg, f, ensure_ascii=False, indent=2)
    except Exception as e:
        warn(f"保存配置失败：{e}")


# ========== 交互 ==========
def ask(prompt, default=""):
    if default:
        raw = input(f"{C.CYAN}?{C.RESET} {prompt} [{C.YELLOW}{default}{C.RESET}]: ").strip()
        return raw if raw else default
    while True:
        raw = input(f"{C.CYAN}?{C.RESET} {prompt}: ").strip()
        if raw:
            return raw
        warn("不能为空")


def ask_yes_no(prompt, default=True):
    suffix = "Y/n" if default else "y/N"
    raw = input(f"{C.CYAN}?{C.RESET} {prompt} [{suffix}]: ").strip().lower()
    if not raw:
        return default
    return raw in ("y", "yes", "是")


# ========== Git 检测 ==========
def has_git():
    try:
        r = subprocess.run("git --version", shell=True,
                           capture_output=True, text=True, timeout=10)
        return r.returncode == 0
    except Exception:
        return False


# ========== 下载：Git ==========
def download_via_git(cfg, target_dir):
    repo_url = f"https://gitee.com/{cfg['gitee_owner']}/{cfg['gitee_repo']}.git"
    info(f"Git 克隆：{repo_url}")

    if os.path.isdir(target_dir) and os.listdir(target_dir):
        if not ask_yes_no(f"目标目录已存在且非空：{target_dir}\n  是否继续？", default=False):
            return False
        # 已存在则尝试 pull
        warn("目标目录已存在，尝试 pull 更新…")
        cmd = f'cd /d "{target_dir}" && git pull origin {cfg["gitee_branch"]}'
        r = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if r.returncode != 0:
            error(f"pull 失败：{r.stderr.strip()}")
            return False
        ok("代码已更新")
        return True

    cmd = f'git clone -b {cfg["gitee_branch"]} "{repo_url}" "{target_dir}"'
    r = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if r.returncode != 0:
        error(f"克隆失败：{r.stderr.strip()}")
        return False
    ok(f"已克隆到：{target_dir}")
    return True


# ========== 下载：API ==========
def download_via_api(cfg, target_dir):
    token = cfg.get("token", "").strip()
    if not token:
        token = input(f"{C.CYAN}?{C.RESET} 请输入 Gitee 私人令牌：").strip()
        if not token:
            error("未提供令牌")
            return False
        cfg["token"] = token
        save_config(cfg)

    api_url = (f"https://gitee.com/api/v5/repos/{cfg['gitee_owner']}/{cfg['gitee_repo']}"
               f"/zipball?ref={cfg['gitee_branch']}")
    info(f"API 下载：{api_url}")

    tmp_dir = tempfile.mkdtemp(prefix="gitee_installer_")
    zip_path = os.path.join(tmp_dir, "repo.zip")

    try:
        req = urllib.request.Request(
            api_url,
            headers={"User-Agent": "Mozilla/5.0",
                     "Authorization": f"token {token}"}
        )
        with urllib.request.urlopen(req, timeout=120) as resp, \
             open(zip_path, "wb") as f:
            shutil.copyfileobj(resp, f)
        size_mb = os.path.getsize(zip_path) / 1024 / 1024
        ok(f"下载完成（{size_mb:.2f} MB）")
    except urllib.error.HTTPError as e:
        error(f"HTTP {e.code}：{e.reason}")
        if e.code == 401:
            warn("令牌无效或已过期")
        elif e.code == 403:
            warn("权限不足，请确认令牌勾选 projects 权限")
        elif e.code == 404:
            warn("仓库或分支不存在")
        shutil.rmtree(tmp_dir, ignore_errors=True)
        return False
    except Exception as e:
        error(f"下载失败：{e}")
        shutil.rmtree(tmp_dir, ignore_errors=True)
        return False

    info("解压中…")
    try:
        with zipfile.ZipFile(zip_path, "r") as zf:
            zf.extractall(tmp_dir)
        extracted = None
        for name in os.listdir(tmp_dir):
            full = os.path.join(tmp_dir, name)
            if os.path.isdir(full) and name != "__MACOSX":
                extracted = full
                break
        if not extracted:
            error("未找到解压后的项目目录")
            shutil.rmtree(tmp_dir, ignore_errors=True)
            return False

        os.makedirs(target_dir, exist_ok=True)
        for item in os.listdir(extracted):
            src = os.path.join(extracted, item)
            dst = os.path.join(target_dir, item)
            if os.path.isdir(src):
                if os.path.exists(dst):
                    shutil.rmtree(dst, ignore_errors=True)
                shutil.copytree(src, dst)
            else:
                shutil.copy2(src, dst)
        ok(f"已解压到：{target_dir}")
    except Exception as e:
        error(f"解压失败：{e}")
        shutil.rmtree(tmp_dir, ignore_errors=True)
        return False
    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)

    return True


# ========== 环境检测（只检测不执行） ==========
def find_python():
    """检测可用的 Python，返回列表"""
    found = []
    if sys.version_info >= (3, 8):
        found.append(sys.executable)
    for cmd in ("python", "python3"):
        try:
            r = subprocess.run(f'{cmd} -c "import sys; print(sys.executable)"',
                               shell=True, capture_output=True, text=True, timeout=5)
            if r.returncode == 0:
                path = r.stdout.strip()
                if path and os.path.isfile(path):
                    found.append(path)
        except Exception:
            pass
    # 去重
    seen = set()
    result = []
    for p in found:
        rp = os.path.realpath(p)
        if rp not in seen:
            seen.add(rp)
            result.append(p)
    return result


def has_venv(project_dir):
    """检查项目里是否已有虚拟环境"""
    for name in (".venv", "venv", "env"):
        activate = os.path.join(project_dir, name, "Scripts", "activate.bat")
        if os.path.isfile(activate):
            return name
    return None


def has_requirements(project_dir):
    return os.path.isfile(os.path.join(project_dir, "requirements.txt"))


# ========== 主流程 ==========
def main():
    os.system("cls" if os.name == "nt" else "clear")

    title("🎬 Gitee 项目安装器")

    cfg = load_config()

    # ---------- 1. 仓库信息 ----------
    print(f"\n{C.BOLD}【1/3】仓库信息{C.RESET}")
    cfg["gitee_owner"] = ask("Gitee 用户名", cfg["gitee_owner"])
    cfg["gitee_repo"] = ask("仓库名称", cfg["gitee_repo"])
    cfg["gitee_branch"] = ask("分支", cfg["gitee_branch"])
    save_config(cfg)

    # ---------- 2. 安装目录 ----------
    print(f"\n{C.BOLD}【2/3】安装目录{C.RESET}")
    default_dir = os.path.join(os.getcwd(), cfg["gitee_repo"])
    target_dir = os.path.abspath(ask("安装到哪个目录", cfg["install_dir"] or default_dir))
    cfg["install_dir"] = target_dir
    save_config(cfg)

    # ---------- 3. 下载方式 ----------
    print(f"\n{C.BOLD}【3/3】下载方式{C.RESET}")
    if has_git():
        info("检测到 Git 已安装")
        use_git = ask_yes_no("使用 Git clone 下载？（推荐）", default=True)
    else:
        warn("未检测到 Git，将使用 Gitee API 下载 ZIP")
        use_git = False
    cfg["use_git"] = use_git
    save_config(cfg)

    # ---------- 下载项目 ----------
    title("📥 下载项目")
    if use_git:
        success = download_via_git(cfg, target_dir)
    else:
        success = download_via_api(cfg, target_dir)

    if not success:
        error("项目下载失败")
        input("\n按回车退出…")
        return

    # ---------- 后续询问（默认不执行） ----------
    title("✅ 项目下载完成")

    print(f"  项目目录：{C.BOLD}{target_dir}{C.RESET}\n")

    # 检测环境
    venv_name = has_venv(target_dir)
    has_req = has_requirements(target_dir)
    pythons = find_python()

    print(f"  {C.CYAN}环境检测：{C.RESET}")
    if venv_name:
        print(f"    ✅ 已发现虚拟环境：{venv_name}")
    else:
        print(f"    ⚠️  未发现虚拟环境")
    if has_req:
        print(f"    ✅ 已发现 requirements.txt")
    else:
        print(f"    ⚠️  未发现 requirements.txt")
    if pythons:
        print(f"    ✅ 系统 Python：{pythons[0]}")
    else:
        print(f"    ⚠️  未检测到 Python")
    print()

    # ---------- 可选：创建虚拟环境 ----------
    if not venv_name and pythons:
        if ask_yes_no("是否创建虚拟环境？", default=False):
            venv_path = os.path.join(target_dir, ".venv")
            info(f"创建虚拟环境：{venv_path}")
            r = subprocess.run(f'"{pythons[0]}" -m venv "{venv_path}"',
                               shell=True, capture_output=True, text=True)
            if r.returncode == 0:
                ok("虚拟环境创建成功")
                venv_name = ".venv"
            else:
                error(f"创建失败：{r.stderr.strip()}")

    # ---------- 可选：安装依赖 ----------
    if venv_name and has_req:
        if ask_yes_no("是否安装依赖（pip install -r requirements.txt）？", default=False):
            py = os.path.join(target_dir, venv_name, "Scripts", "python.exe")
            req = os.path.join(target_dir, "requirements.txt")
            info("安装依赖中…")
            r = subprocess.run(f'"{py}" -m pip install -r "{req}"',
                               shell=True)
            if r.returncode == 0:
                ok("依赖安装完成")
            else:
                error("依赖安装失败")
    elif not venv_name:
        warn("未创建虚拟环境，跳过依赖安装")
    elif not has_req:
        warn("未找到 requirements.txt，跳过依赖安装")

    # ---------- 可选：数据库迁移 ----------
    if venv_name:
        if ask_yes_no("是否执行数据库迁移（migrate）？", default=False):
            py = os.path.join(target_dir, venv_name, "Scripts", "python.exe")
            info("执行迁移中…")
            for cmd in ("makemigrations", "migrate"):
                full = f'cd /d "{target_dir}" && "{py}" manage.py {cmd}'
                subprocess.run(full, shell=True)
            ok("数据库迁移完成")

    # ---------- 可选：启动服务 ----------
    if venv_name:
        if ask_yes_no("是否立即启动 Django 服务（端口 8002）？", default=False):
            py = os.path.join(target_dir, venv_name, "Scripts", "python.exe")
            print()
            info("启动服务：http://127.0.0.1:8002")
            info("按 Ctrl+C 停止\n")
            cmd = f'cd /d "{target_dir}" && "{py}" manage.py runserver 0.0.0.0:8002'
            try:
                subprocess.run(cmd, shell=True)
            except KeyboardInterrupt:
                pass

    title("🎉 全部完成")
    print(f"  项目位置：{C.BOLD}{target_dir}{C.RESET}")
    print(f"\n  {C.CYAN}下次启动服务：{C.RESET}")
    if venv_name:
        print(f'    cd /d "{target_dir}"')
        print(f'    {venv_name}\\Scripts\\activate.bat')
        print(f'    python manage.py runserver 0.0.0.0:8002')
    print()
    input("按回车退出…")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{C.YELLOW}已取消{C.RESET}")
        sys.exit(0)
    except Exception as e:
        error(f"发生错误：{e}")
        import traceback
        traceback.print_exc()
        input("\n按回车退出…")
