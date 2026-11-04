#!/usr/bin/env python3
import base64
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONFIG_DIR = ROOT / "config"
BRAND_DIR = CONFIG_DIR / "branding"
BASE_FIREFOX = ROOT / "base" / "firefox"


def build():
    if not BASE_FIREFOX.exists():
        raise SystemExit(f"No se encontró el motor base en {BASE_FIREFOX}")

    # 1. Asegurar que los iconos del timón existen
    if not (BRAND_DIR / "noutrora.svg").exists():
        import subprocess
        subprocess.run(["python3", str(ROOT / "scripts" / "generate_logo.py")], check=True)

    # 2. Leer plantilla de políticas y marcadores personales
    policies_data = json.loads((CONFIG_DIR / "policies.template.json").read_text(encoding="utf-8"))
    bookmarks_data = json.loads((CONFIG_DIR / "bookmarks.json").read_text(encoding="utf-8"))
    policies_data["policies"]["Bookmarks"] = bookmarks_data

    # 3. Escribir distribution/policies.json en el motor base
    dist_dir = BASE_FIREFOX / "distribution"
    dist_dir.mkdir(parents=True, exist_ok=True)
    (dist_dir / "policies.json").write_text(
        json.dumps(policies_data, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    # 4. Inyectar iconos de ventana y sistema (timón de barco)
    icons_dir = BASE_FIREFOX / "browser" / "chrome" / "icons" / "default"
    icons_dir.mkdir(parents=True, exist_ok=True)
    for size in (16, 32, 48, 64, 128):
        src_icon = BRAND_DIR / f"default{size}.png"
        if src_icon.exists():
            shutil.copy2(src_icon, icons_dir / f"default{size}.png")

    # 5. Copiar autoconfig.js y noutrora.cfg (con el logo SVG incrustado para Nueva Pestaña)
    pref_dir = BASE_FIREFOX / "defaults" / "pref"
    pref_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy2(CONFIG_DIR / "defaults" / "pref" / "autoconfig.js", pref_dir / "autoconfig.js")

    svg_b64 = base64.b64encode((BRAND_DIR / "noutrora.svg").read_bytes()).decode("ascii")
    cfg_text = (CONFIG_DIR / "noutrora.cfg").read_text(encoding="utf-8")
    cfg_text = cfg_text.replace("__NOUTRORA_SVG_BASE64__", svg_b64)
    (BASE_FIREFOX / "noutrora.cfg").write_text(cfg_text, encoding="utf-8")

    print("✅ Noutrora compilado/aplicado correctamente sobre base/firefox/")
    print("   - Logo: Timón de barco (ventana + página de inicio Noutrora)")
    print(f"   - Marcadores inyectados: {len(bookmarks_data)}")
    print("   - Extensiones preinstaladas: Bitwarden + uBlock Origin")
    print("   - Telemetría, Pocket, IA y gestor interno de claves: DESACTIVADOS")


if __name__ == "__main__":
    build()
