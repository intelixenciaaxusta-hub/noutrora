#!/usr/bin/env python3
"""
Prepara la carpeta dist/noutrora.es/ lista para su despliegue hacia el servidor central servidor (noutrora.es):
- index.html (Landing page oficial noutrora.es)
- exploracion.json (Catálogo Cultural y Marinero Vivo)
- downloads/noutrora_2.0_all.deb (Instalador nativo de doble clic para Linux Ubuntu/Mint/Debian)
- downloads/Noutrora-Setup-Windows.cmd (Instalador de doble clic para Windows 10/11)
- downloads/Noutrora-Mac.command (Instalador de doble clic para macOS)
- downloads/noutrora-installer.tar.gz (Paquete universal)
"""
import hashlib
import os
import shutil
import subprocess
import sys
import tarfile
import tempfile
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DIST_DIR = ROOT / "dist"
WEB_DIST = DIST_DIR / "noutrora.es"
DOWNLOADS_DIR = WEB_DIST / "downloads"

INCLUDED_PATHS = [
    "CONSTITUCION.md",
    "SPEC.md",
    "CATALOGO.md",
    "README.md",
    "AGENTS.md",
    "decalogo.txt",
    "formadeserepensar.txt",
    "run.sh",
    "install-linux.sh",
    "config",
    "scripts",
]

INSTALL_SH = """#!/usr/bin/env bash
set -e

INSTALL_DIR="${NOUTRORA_DIR:-$HOME/Noutrora}"
ARCHIVE_URL="https://noutrora.es/downloads/noutrora-installer.tar.gz"

echo "🧭 Instalando Noutrora Browser en $INSTALL_DIR..."
mkdir -p "$INSTALL_DIR"

TMP_TAR="$(mktemp -t noutrora-XXXXXX.tar.gz)"
trap 'rm -f "$TMP_TAR"' EXIT

curl -fsSL "$ARCHIVE_URL" -o "$TMP_TAR"
tar -xzf "$TMP_TAR" -C "$INSTALL_DIR" --strip-components=1

cd "$INSTALL_DIR"
python3 scripts/bootstrap.py

if [[ "$(uname -s)" == "Linux" ]]; then
  ./install-linux.sh
fi

echo "✅ Noutrora instalado correctamente. Puedes abrirlo desde tu menú de aplicaciones o con: $INSTALL_DIR/run.sh"
"""

WINDOWS_INSTALLER_CMD = r"""@echo off
chcp 65001 >nul
title Instalador de Noutrora Browser v2.0 (Windows)
echo ================================================================
echo   🧭 NOUTRORA BROWSER v2.0 - Instalacion automatica en 1 paso
echo ================================================================
echo.
set "NOUTRORA_DIR=%LOCALAPPDATA%\Noutrora"
set "FF_DIR=%NOUTRORA_DIR%\firefox"
set "PROFILE_DIR=%NOUTRORA_DIR%\profile"
set "OVERLAY_ZIP=%TEMP%\noutrora-overlay-ready.zip"
set "FF_SETUP=%TEMP%\FirefoxSetup.exe"

if not exist "%NOUTRORA_DIR%" mkdir "%NOUTRORA_DIR%"
if not exist "%PROFILE_DIR%" mkdir "%PROFILE_DIR%"

if not exist "%FF_DIR%\firefox.exe" (
    if exist "%ProgramFiles%\Mozilla Firefox\firefox.exe" (
        echo [1/3] Copiando motor base Gecko local...
        xcopy "%ProgramFiles%\Mozilla Firefox\*" "%FF_DIR%\" /E /I /H /Y >nul
    ) else (
        echo [1/3] Descargando motor Gecko oficial para Windows en Galego (64-bit)...
        curl -fL "https://download.mozilla.org/?product=firefox-latest-ssl&os=win64&lang=gl" -o "%FF_SETUP%"
        echo Instalando motor base silencioso en %FF_DIR%...
        start /wait "" "%FF_SETUP%" /S /InstallDirectoryPath="%FF_DIR%"
    )
)

echo [2/3] Aplicando identidad Atlantica, Bitacora y escudo de privacidad...
curl -fsSL "https://noutrora.es/downloads/noutrora-overlay-ready.zip" -o "%OVERLAY_ZIP%"
powershell -NoProfile -ExecutionPolicy Bypass -Command "Expand-Archive -Path '%OVERLAY_ZIP%' -DestinationPath '%FF_DIR%' -Force"

echo [3/3] Creando acceso directo de Noutrora en tu Escritorio...
powershell -NoProfile -ExecutionPolicy Bypass -Command "$ws = New-Object -ComObject WScript.Shell; $s = $ws.CreateShortcut([Environment]::GetFolderPath('Desktop') + '\Noutrora.lnk'); $s.TargetPath = '%FF_DIR%\firefox.exe'; $s.Arguments = '-profile ' + [char]34 + '%PROFILE_DIR%' + [char]34 + ' -no-remote'; $s.WorkingDirectory = '%FF_DIR%'; $s.IconLocation = '%FF_DIR%\noutrora.ico'; $s.Description = 'Noutrora Browser'; $s.Save()"

echo.
echo ✅ ¡Noutrora instalado! Abriendo navegador con perfil aislado...
start "" "%FF_DIR%\firefox.exe" -profile "%PROFILE_DIR%" -no-remote
"""

MAC_INSTALLER_COMMAND = """#!/usr/bin/env bash
set -e
echo "================================================================"
echo "  🧭 NOUTRORA BROWSER v2.0 — Instalación automática para macOS"
echo "================================================================"

APP_DEST="/Applications/Noutrora.app"
if [ ! -w "/Applications" ]; then
  APP_DEST="$HOME/Applications/Noutrora.app"
  mkdir -p "$HOME/Applications"
fi

TMP_DMG="$(mktemp -t noutrora-ff-XXXXXX.dmg)"
TMP_ZIP="$(mktemp -t noutrora-ov-XXXXXX.zip)"
MOUNT_DIR="$(mktemp -d -t noutrora-mnt-XXXXXX)"
trap 'hdiutil detach "$MOUNT_DIR" -quiet 2>/dev/null || true; rm -f "$TMP_DMG" "$TMP_ZIP"; rmdir "$MOUNT_DIR" 2>/dev/null || true' EXIT

if [ ! -d "$APP_DEST" ]; then
  if [ -d "/Applications/Firefox.app" ]; then
    echo "[1/3] Preparando motor base desde tu equipo..."
    cp -R "/Applications/Firefox.app" "$APP_DEST"
  else
    echo "[1/3] Descargando motor Gecko oficial para macOS en Galego..."
    curl -fL "https://download.mozilla.org/?product=firefox-latest-ssl&os=osx&lang=gl" -o "$TMP_DMG"
    hdiutil attach "$TMP_DMG" -mountpoint "$MOUNT_DIR" -nobrowse -quiet
    cp -R "$MOUNT_DIR/Firefox.app" "$APP_DEST"
    hdiutil detach "$MOUNT_DIR" -quiet
  fi
fi

echo "[2/3] Inyectando configuración de Noutrora, Bitácora y Puerto Base..."
curl -fsSL "https://noutrora.es/downloads/noutrora-overlay-ready.zip" -o "$TMP_ZIP"
unzip -oq "$TMP_ZIP" -d "$APP_DEST/Contents/Resources"

# Re-firmar la aplicación con ad-hoc codesign para que macOS / Apple Silicon respete la integridad
if command -v codesign >/dev/null 2>&1; then
  echo "Aplicando firma de integridad local (codesign)..."
  codesign --force --deep --sign - "$APP_DEST" 2>/dev/null || true
fi

echo "[3/3] Listo en $APP_DEST. Abriendo Noutrora..."
xattr -cr "$APP_DEST" 2>/dev/null || true
open "$APP_DEST"
"""

USR_BIN_NOUTRORA = """#!/usr/bin/env bash
set -e
USER_NOUTRORA="$HOME/.local/share/noutrora"
mkdir -p "$USER_NOUTRORA"

# Copiar/actualizar la capa de configuración desde /opt/noutrora al perfil del usuario
cp -rf /opt/noutrora/config /opt/noutrora/scripts /opt/noutrora/run.sh "$USER_NOUTRORA/"
chmod +x "$USER_NOUTRORA/run.sh"

if [ ! -x "$USER_NOUTRORA/base/firefox/firefox" ]; then
  if command -v zenity >/dev/null 2>&1; then
    (
      echo "20"
      echo "# Preparando el motor Gecko oficial para Noutrora (solo la primera vez)..."
      cd "$USER_NOUTRORA" && python3 scripts/bootstrap.py
      echo "100"
    ) | zenity --progress --title="Noutrora Browser" --text="Preparando travesía..." --pulsate --auto-close --no-cancel || true
  else
    cd "$USER_NOUTRORA" && python3 scripts/bootstrap.py
  fi
fi

exec "$USER_NOUTRORA/run.sh" "$@"
"""

DEB_CONTROL = """Package: noutrora
Version: 2.0-1
Section: web
Priority: optional
Architecture: all
Depends: python3, curl, tar, xz-utils
Maintainer: Proyecto Noutrora <intelixenciaaxusta@gmail.com>
Homepage: https://noutrora.es
Description: Noutrora Browser - Navegacion Atlantica Silenciosa
 Navegador humanista y privado basado en el motor Gecko de Firefox.
 Cero robo de datos, sin historial de navegacion, sesiones persistentes,
 uBlock Origin de serie y Puerto Base cultural.
"""

DEB_DESKTOP = """[Desktop Entry]
Version=1.0
Name=Noutrora
GenericName=Navegador Web Atlántico
Comment=Navega en calma por el océano digital sin rastreo ni ruido
Exec=/usr/bin/noutrora %u
Icon=noutrora
Terminal=false
Type=Application
Categories=Network;WebBrowser;
MimeType=text/html;text/xml;application/xhtml+xml;x-scheme-handler/http;x-scheme-handler/https;
StartupWMClass=Noutrora
StartupNotify=true
"""


def build_deb_package(dest_deb: Path) -> None:
    with tempfile.TemporaryDirectory() as tmpdir:
        pkg_root = Path(tmpdir) / "noutrora_2.0_all"
        debian_dir = pkg_root / "DEBIAN"
        opt_dir = pkg_root / "opt" / "noutrora"
        bin_dir = pkg_root / "usr" / "bin"
        apps_dir = pkg_root / "usr" / "share" / "applications"
        icons_svg_dir = pkg_root / "usr" / "share" / "icons" / "hicolor" / "scalable" / "apps"
        icons_png_dir = pkg_root / "usr" / "share" / "icons" / "hicolor" / "128x128" / "apps"

        for d in (pkg_root, debian_dir, opt_dir, bin_dir, apps_dir, icons_svg_dir, icons_png_dir):
            d.mkdir(parents=True, exist_ok=True)
            d.chmod(0o755)

        (debian_dir / "control").write_text(DEB_CONTROL, encoding="utf-8")
        (debian_dir / "control").chmod(0o644)

        for rel in INCLUDED_PATHS:
            src = ROOT / rel
            dst = opt_dir / rel
            if src.is_dir():
                shutil.copytree(src, dst, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
            elif src.is_file():
                shutil.copy2(src, dst)

        launcher = bin_dir / "noutrora"
        launcher.write_text(USR_BIN_NOUTRORA, encoding="utf-8")
        launcher.chmod(0o755)

        (apps_dir / "noutrora.desktop").write_text(DEB_DESKTOP, encoding="utf-8")
        shutil.copy2(ROOT / "config" / "branding" / "noutrora.svg", icons_svg_dir / "noutrora.svg")
        shutil.copy2(ROOT / "config" / "branding" / "default128.png", icons_png_dir / "noutrora.png")

        subprocess.run(
            ["dpkg-deb", "--root-owner-group", "--build", str(pkg_root), str(dest_deb)],
            check=True,
            stdout=subprocess.DEVNULL,
        )


def build_web_package() -> None:
    # 0. Asegurar compilación previa del overlay
    subprocess.run([sys.executable, str(ROOT / "scripts" / "build.py")], check=True)

    if WEB_DIST.exists():
        shutil.rmtree(WEB_DIST)
    DOWNLOADS_DIR.mkdir(parents=True, exist_ok=True)

    # 1. Copiar la Landing Page como index.html, el Catálogo Vivo (exploracion.json) y los iconos de favicon
    landing_src = ROOT / "noutrora_landing_page_oficial.html"
    shutil.copy2(landing_src, WEB_DIST / "index.html")
    shutil.copy2(ROOT / "config" / "exploracion.json", WEB_DIST / "exploracion.json")
    shutil.copy2(ROOT / "config" / "branding" / "noutrora.svg", WEB_DIST / "favicon.svg")
    shutil.copy2(ROOT / "config" / "branding" / "noutrora-512.png", WEB_DIST / "apple-touch-icon.png")

    pasos = ROOT / "config" / "pasos"
    if pasos.exists():
        shutil.copytree(pasos, WEB_DIST / "pasos")

    # 2. Crear el paquete universal noutrora-installer.tar.gz
    tar_path = DOWNLOADS_DIR / "noutrora-installer.tar.gz"
    with tarfile.open(tar_path, "w:gz") as tf:
        for rel in INCLUDED_PATHS:
            p = ROOT / rel
            if p.exists():
                tf.add(
                    p,
                    arcname=f"Noutrora/{rel}",
                    filter=lambda ti: None if "__pycache__" in ti.name or ti.name.endswith(".pyc") else ti,
                )

    # 3. Generar instalador nativo .deb de doble clic para Linux (Ubuntu / Mint / Debian)
    deb_path = DOWNLOADS_DIR / "noutrora_2.0_all.deb"
    build_deb_package(deb_path)

    # 4. Generar instaladores de doble clic para Windows y macOS + overlay precompilado (sin necesidad de Python)
    from package_native import build_precompiled_overlay_zip

    build_precompiled_overlay_zip(DOWNLOADS_DIR / "noutrora-overlay-ready.zip")
    win_path = DOWNLOADS_DIR / "Noutrora-Setup-Windows.cmd"
    win_path.write_text(WINDOWS_INSTALLER_CMD, encoding="utf-8")
    mac_path = DOWNLOADS_DIR / "Noutrora-Mac.command"
    mac_path.write_text(MAC_INSTALLER_COMMAND, encoding="utf-8")
    mac_path.chmod(0o755)

    # Sincronizar el deb con motor amd64 de package_native si existe
    native_deb_src = ROOT / "dist" / "nas" / "noutrora_2.0_amd64.deb"
    if native_deb_src.exists():
        shutil.copy2(native_deb_src, DOWNLOADS_DIR / "noutrora_2.0_amd64.deb")

    # 5. Calcular SHA-256
    sha256_hash = hashlib.sha256(deb_path.read_bytes()).hexdigest()
    (DOWNLOADS_DIR / "noutrora_2.0_all.deb.sha256").write_text(
        f"{sha256_hash}  noutrora_2.0_all.deb\n", encoding="utf-8"
    )

    # 6. Escribir install.sh de respaldo
    install_sh_path = WEB_DIST / "install.sh"
    install_sh_path.write_text(INSTALL_SH, encoding="utf-8")
    install_sh_path.chmod(0o755)

    # 7. Archivos de configuración para Cloudflare Pages (_headers) y GitHub Pages (CNAME / .nojekyll)
    (WEB_DIST / "CNAME").write_text("noutrora.es\n", encoding="utf-8")
    (WEB_DIST / ".nojekyll").write_text("", encoding="utf-8")
    (WEB_DIST / "_headers").write_text(
        "/exploracion.json\n  Content-Type: application/json; charset=utf-8\n  Access-Control-Allow-Origin: *\n"
        "/install.sh\n  Content-Type: text/plain; charset=utf-8\n"
        "/downloads/*.deb\n  Content-Type: application/vnd.debian.binary-package\n"
        "/downloads/*.tar.gz\n  Content-Type: application/gzip\n",
        encoding="utf-8",
    )

    # 8. Generar archivo ZIP único
    zip_path = DIST_DIR / "noutrora-web-v2.0.zip"
    if zip_path.exists():
        zip_path.unlink()
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for dirpath, dirnames, filenames in os.walk(WEB_DIST):
            dirnames.sort()
            filenames.sort()
            for fname in filenames:
                full = Path(dirpath) / fname
                rel = full.relative_to(WEB_DIST).as_posix()
                zf.write(full, arcname=rel)

    deb_kb = deb_path.stat().st_size / 1024
    print("✅ Paquete Web Noutrora v2.0 listo para despliegue en servidor central servidor (noutrora.es):")
    print(f"   - Carpeta local generada: dist/noutrora.es/")
    print(f"   - Destino buzón SMB: /srv/servidor/publicaciones/ibm/noutrora.es/")
    print(f"   - Instalador nativo Linux (.deb doble clic): downloads/noutrora_2.0_all.deb ({deb_kb:.1f} KB)")
    print(f"   - Catálogo Cultural Vivo incluido: exploracion.json")


if __name__ == "__main__":
    build_web_package()
