#!/usr/bin/env python3
"""
Instalador Ligero de Noutrora (Opción 1 — < 1 MB, 100% compatible con MPL 2.0 y marcas de Mozilla).
Si no existe el motor base en base/firefox/, lo descarga automáticamente desde el servidor
oficial de Mozilla para la plataforma actual y aplica la superposición de Noutrora.
"""
import os
import platform
import shutil
import subprocess
import sys
import tarfile
import tempfile
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BASE_DIR = ROOT / "base"
BASE_FIREFOX = BASE_DIR / "firefox"


def detect_mozilla_os() -> str:
    sys_name = platform.system().lower()
    machine = platform.machine().lower()

    if sys_name == "linux":
        if machine in ("aarch64", "arm64"):
            return "linux64-aarch64"
        return "linux64"
    if sys_name == "darwin":
        return "osx"
    if sys_name == "windows":
        return "win64"
    raise SystemExit(f"Sistema operativo no soportado automáticamente: {sys_name} ({machine})")


def download_and_extract_linux(os_tag: str) -> None:
    url = f"https://download.mozilla.org/?product=firefox-latest-ssl&os={os_tag}&lang=gl"
    print(f"⬇️  Descargando motor oficial Gecko en Galego desde Mozilla ({os_tag})...")
    BASE_DIR.mkdir(parents=True, exist_ok=True)

    with tempfile.NamedTemporaryFile(prefix="noutrora_engine_", suffix=".tar.xz", delete=False) as tmp:
        tmp_path = Path(tmp.name)

    try:
        urllib.request.urlretrieve(url, tmp_path)
        print("📦 Extrayendo motor base en base/firefox/...")
        with tarfile.open(tmp_path, mode="r:*") as tf:
            try:
                tf.extractall(path=BASE_DIR, filter="data")
            except TypeError:
                tf.extractall(path=BASE_DIR)
    finally:
        if tmp_path.exists():
            tmp_path.unlink()


def is_engine_valid() -> bool:
    if not BASE_FIREFOX.is_dir():
        return False
    sys_name = platform.system().lower()
    if sys_name == "linux":
        binary = BASE_FIREFOX / "firefox"
        return binary.is_file() and os.access(binary, os.X_OK)
    if sys_name == "darwin":
        return (BASE_FIREFOX / "firefox").is_file() or (BASE_FIREFOX / "Firefox.app").exists()
    if sys_name == "windows":
        return (BASE_FIREFOX / "firefox.exe").is_file()
    try:
        return any(BASE_FIREFOX.iterdir())
    except OSError:
        return False


def ensure_engine() -> None:
    if is_engine_valid():
        return

    if BASE_FIREFOX.exists():
        print("⚠️  Motor base en base/firefox incompleto ou corrupto. Limpando para descarga limpa...")
        shutil.rmtree(BASE_FIREFOX, ignore_errors=True)

    os_tag = detect_mozilla_os()
    if os_tag.startswith("linux"):
        download_and_extract_linux(os_tag)
    else:
        print(
            f"ℹ️  Para {os_tag}, descarga el binario oficial desde https://www.mozilla.org/firefox/all/ "
            f"y extráelo en {BASE_FIREFOX}"
        )
        sys.exit(1)


def main() -> None:
    ensure_engine()
    subprocess.run(["python3", str(ROOT / "scripts" / "build.py")], check=True)


if __name__ == "__main__":
    main()

