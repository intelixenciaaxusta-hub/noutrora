#!/usr/bin/env python3
"""
Genera los paquetes de instalación de una sola vez para Linux, Windows y macOS:
1. Pre-compila el overlay completo (noutrora-overlay-ready.zip) con noutrora.cfg,
   autoconfig.js, policies.json, noutrora-overlay/ y el icono nativo noutrora.ico,
   para que Windows y macOS NO necesiten tener Python instalado.
2. Genera el paquete .deb COMPLETO (con el motor Gecko ya incluido dentro, ~85 MB)
   en dist/nas/noutrora_2.0_amd64.deb para alojar en el NAS o en Raiola.
"""
import shutil
import struct
import subprocess
import tempfile
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BASE_FIREFOX = ROOT / "base" / "firefox"
DIST_NAS = ROOT / "dist" / "nas"
WEB_DOWNLOADS = ROOT / "dist" / "noutrora.es" / "downloads"


def create_windows_ico(png_path: Path, ico_path: Path) -> None:
    """Crea un archivo de icono nativo de Windows (.ico) a partir de default128.png."""
    png_bytes = png_path.read_bytes()
    # Cabecera ICONDIR (6 bytes) + 1 ICONDIRENTRY (16 bytes) para PNG 128x128
    header = struct.pack("<HHH", 0, 1, 1)
    entry = struct.pack(
        "<BBBBHHII",
        128,  # width
        128,  # height
        0,    # color count
        0,    # reserved
        1,    # color planes
        32,   # bits per pixel
        len(png_bytes),
        22,   # offset
    )
    ico_path.write_bytes(header + entry + png_bytes)


def build_precompiled_overlay_zip(dest_zip: Path) -> None:
    """Empaqueta los archivos ya compilados en base/firefox para inyección directa sin Python."""
    ico_path = ROOT / "config" / "branding" / "noutrora.ico"
    create_windows_ico(ROOT / "config" / "branding" / "default128.png", ico_path)

    dest_zip.parent.mkdir(parents=True, exist_ok=True)
    if dest_zip.exists():
        dest_zip.unlink()

    with zipfile.ZipFile(dest_zip, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        zf.write(BASE_FIREFOX / "noutrora.cfg", arcname="noutrora.cfg")
        zf.write(BASE_FIREFOX / "defaults" / "pref" / "autoconfig.js", arcname="defaults/pref/autoconfig.js")
        zf.write(BASE_FIREFOX / "distribution" / "policies.json", arcname="distribution/policies.json")
        zf.write(ico_path, arcname="noutrora.ico")
        zf.write(ROOT / "config" / "branding" / "noutrora-512.png", arcname="noutrora-512.png")

        overlay_dir = BASE_FIREFOX / "noutrora-overlay"
        for p in sorted(overlay_dir.rglob("*")):
            if p.is_file():
                rel = p.relative_to(BASE_FIREFOX).as_posix()
                zf.write(p, arcname=rel)


def build_full_linux_deb(dest_deb: Path) -> None:
    """Construye noutrora_2.0_amd64.deb con el motor completo base/firefox incluido (~85 MB)."""
    dest_deb.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as tmpdir:
        pkg_root = Path(tmpdir) / "noutrora_2.0_amd64"
        debian_dir = pkg_root / "DEBIAN"
        opt_dir = pkg_root / "opt" / "noutrora"
        bin_dir = pkg_root / "usr" / "bin"
        apps_dir = pkg_root / "usr" / "share" / "applications"
        icons_svg_dir = pkg_root / "usr" / "share" / "icons" / "hicolor" / "scalable" / "apps"
        icons_png_dir = pkg_root / "usr" / "share" / "icons" / "hicolor" / "128x128" / "apps"

        for d in (pkg_root, debian_dir, opt_dir, bin_dir, apps_dir, icons_svg_dir, icons_png_dir):
            d.mkdir(parents=True, exist_ok=True)
            d.chmod(0o755)

        control_text = """Package: noutrora
Version: 2.0-1
Section: web
Priority: optional
Architecture: amd64
Maintainer: Proyecto Noutrora <intelixenciaaxusta@gmail.com>
Homepage: https://noutrora.es
Description: Noutrora Browser - Navegacion Atlantica Silenciosa (Paquete Completo)
 Navegador completo listo para usar sin descargas adicionales.
 Cero robo de datos, sin historial de navegacion, sesiones persistentes,
 uBlock Origin y Puerto Base cultural incluidos.
"""
        (debian_dir / "control").write_text(control_text, encoding="utf-8")
        (debian_dir / "control").chmod(0o644)

        # Copiar el motor base/firefox ya compilado y xdg-data
        shutil.copytree(BASE_FIREFOX, opt_dir / "firefox", symlinks=True)
        xdg_src = ROOT / "base" / "xdg-data"
        if xdg_src.exists():
            shutil.copytree(xdg_src, opt_dir / "xdg-data", symlinks=True)

        launcher_script = """#!/usr/bin/env bash
export MOZ_APP_REMOTINGNAME="Noutrora"
export GDK_PROGRAM_CLASS="Noutrora"
export XDG_DATA_DIRS="/opt/noutrora/xdg-data:${XDG_DATA_DIRS:-/usr/local/share:/usr/share}"
exec "/opt/noutrora/firefox/firefox" --class "Noutrora" --name "noutrora" "$@"
"""
        launcher = bin_dir / "noutrora"
        launcher.write_text(launcher_script, encoding="utf-8")
        launcher.chmod(0o755)

        desktop_entry = """[Desktop Entry]
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
        (apps_dir / "noutrora.desktop").write_text(desktop_entry, encoding="utf-8")
        shutil.copy2(ROOT / "config" / "branding" / "noutrora.svg", icons_svg_dir / "noutrora.svg")
        shutil.copy2(ROOT / "config" / "branding" / "default128.png", icons_png_dir / "noutrora.png")

        subprocess.run(
            ["dpkg-deb", "-Zxz", "-z3", "--root-owner-group", "--build", str(pkg_root), str(dest_deb)],
            check=True,
            stdout=subprocess.DEVNULL,
        )


if __name__ == "__main__":
    # 1. Asegurar que base/firefox está recién compilado
    subprocess.run(["python3", str(ROOT / "scripts" / "build.py")], check=True)

    # 2. Crear noutrora-overlay-ready.zip precompilado (sin necesidad de Python en Mac/Windows)
    DIST_NAS.mkdir(parents=True, exist_ok=True)
    overlay_zip = DIST_NAS / "noutrora-overlay-ready.zip"
    build_precompiled_overlay_zip(overlay_zip)

    # 3. Construir el instalador .deb completo con motor incluido (~85 MB) para el NAS/Raiola
    full_deb = DIST_NAS / "noutrora_2.0_amd64.deb"
    print("📦 Construyendo instalador .deb completo con el motor incluido (puede tardar 15 s)...")
    build_full_linux_deb(full_deb)
    deb_mb = full_deb.stat().st_size / (1024 * 1024)
    print(f"✅ Paquete Linux completo creado: dist/nas/noutrora_2.0_amd64.deb ({deb_mb:.1f} MB)")

