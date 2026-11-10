#!/usr/bin/env python3
"""Genera Noutrora.dmg para macOS (solo se ejecuta en un Mac: usa hdiutil y codesign).

Descarga el Firefox oficial (universal, vale para Intel y M1), le inyecta el overlay
precompilado (dist/nas/noutrora-overlay-ready.zip) en Contents/Resources, lo firma
ad-hoc (sin cuenta Apple Developer) y crea un .dmg de arrastrar a Aplicaciones.
"""
import shutil
import subprocess
import tempfile
import urllib.request
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OVERLAY_ZIP = ROOT / "dist" / "nas" / "noutrora-overlay-ready.zip"
OUT_DMG = ROOT / "dist" / "nas" / "Noutrora.dmg"
URL = "https://download.mozilla.org/?product=firefox-latest-ssl&os=osx&lang=gl"


def run(*cmd):
    subprocess.run([str(c) for c in cmd], check=True)


def main() -> None:
    if not OVERLAY_ZIP.exists():
        raise SystemExit("Falta el overlay: ejecuta antes scripts/package_native.py")
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        src_dmg, mnt, stage = tmp / "firefox.dmg", tmp / "mnt", tmp / "stage"
        mnt.mkdir(); stage.mkdir()
        print("Descargando Firefox oficial...")
        urllib.request.urlretrieve(URL, src_dmg)
        run("hdiutil", "attach", src_dmg, "-mountpoint", mnt, "-nobrowse", "-quiet")
        try:
            run("cp", "-R", mnt / "Firefox.app", stage / "Noutrora.app")
        finally:
            run("hdiutil", "detach", mnt, "-quiet")
        app = stage / "Noutrora.app"
        res = app / "Contents" / "Resources"
        with zipfile.ZipFile(OVERLAY_ZIP) as zf:
            zf.extractall(res)
        for extra in ("noutrora.ico",):
            (res / extra).unlink(missing_ok=True)
        macos_dir = app / "Contents" / "MacOS"
        ff_bin = macos_dir / "firefox"
        if ff_bin.exists() and not (macos_dir / "firefox-bin").exists():
            ff_bin.rename(macos_dir / "firefox-bin")
            launcher = (
                "#!/bin/bash\n"
                'DIR="$(cd "$(dirname "$0")" && pwd)"\n'
                'PROFILE_DIR="$HOME/Library/Application Support/Noutrora/profile"\n'
                'mkdir -p "$PROFILE_DIR"\n'
                'HOME_PAGE="$DIR/../Resources/noutrora-overlay/content/home.html"\n'
                'exec "$DIR/firefox-bin" -profile "$PROFILE_DIR" -no-remote "$HOME_PAGE" "$@"\n'
            )
            ff_bin.write_text(launcher, encoding="utf-8")
            ff_bin.chmod(0o755)

        run("xattr", "-cr", app)
        run("codesign", "--force", "--deep", "--sign", "-", app)
        (stage / "Applications").symlink_to("/Applications")
        OUT_DMG.parent.mkdir(parents=True, exist_ok=True)
        OUT_DMG.unlink(missing_ok=True)
        run("hdiutil", "create", "-volname", "Noutrora", "-srcfolder", stage,
            "-ov", "-format", "UDZO", OUT_DMG)
    print(f"Listo: {OUT_DMG}")


if __name__ == "__main__":
    main()
