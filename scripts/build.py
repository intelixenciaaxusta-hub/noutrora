#!/usr/bin/env python3
import base64
import json
import re
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONFIG_DIR = ROOT / "config"
BRAND_DIR = CONFIG_DIR / "branding"
BASE_FIREFOX = ROOT / "base" / "firefox"


def b64_file(path: Path) -> str:
    return base64.b64encode(path.read_bytes()).decode("ascii")


def restore_original_omni_if_needed() -> None:
    """
    Asegura que base/firefox/omni.ja y base/firefox/browser/omni.ja sean 100% los originales
    de fábrica sin modificar (arquitectura de Superposición 100% externa).
    """
    for omni in (BASE_FIREFOX / "omni.ja", BASE_FIREFOX / "browser" / "omni.ja"):
        orig = omni.with_suffix(".ja.orig")
        if orig.exists():
            orig.replace(omni)
    stamp = BASE_FIREFOX / ".noutrora-omni-stamp"
    if stamp.exists():
        stamp.unlink()


def setup_external_branding_overlay() -> None:
    """
    Crea la carpeta externa base/firefox/noutrora-overlay/ con su propio chrome.manifest.
    Desde noutrora.cfg se registra en memoria al arrancar (nsIComponentRegistrar.autoRegister),
    redirigiendo todos los iconos de chrome://branding/ hacia nuestros activos sin tocar omni.ja.
    """
    overlay_dir = BASE_FIREFOX / "noutrora-overlay"
    content_dir = overlay_dir / "content"
    content_dir.mkdir(parents=True, exist_ok=True)

    for asset in (
        "noutrora.svg",
        "noutrora-wordmark.svg",
        "noutrora-wordmark-dark.svg",
        "noutrora-512.png",
        "default16.png",
        "default32.png",
        "default48.png",
        "default64.png",
        "default128.png",
        "noutrora-cofre.svg",
        "noutrora-historial.svg",
        "noutrora-dispositivos.svg",
    ):
        src = BRAND_DIR / asset
        if src.exists():
            shutil.copy2(src, content_dir / asset)

    home_src = CONFIG_DIR / "home.html"
    if home_src.exists():
        exploracion_path = CONFIG_DIR / "exploracion.json"
        exploracion_json = (
            exploracion_path.read_text(encoding="utf-8").strip()
            if exploracion_path.exists()
            else '{"perder_o_norte":[],"terra_a_vista":[],"mergullar":[],"libros":[],"portos":[]}'
        )
        home_text = home_src.read_text(encoding="utf-8")
        home_text = home_text.replace("__NOUTRORA_SVG_BASE64__", b64_file(BRAND_DIR / "noutrora.svg"))
        home_text = home_text.replace("__NOUTRORA_WORDMARK_BASE64__", b64_file(BRAND_DIR / "noutrora-wordmark.svg"))
        home_text = home_text.replace("__NOUTRORA_WORDMARK_DARK_BASE64__", b64_file(BRAND_DIR / "noutrora-wordmark-dark.svg"))
        # Blindaxe fronte a Script Tag Breakout ao inxectar contido JSON
        exploracion_safe = re.sub(r"<\s*/\s*script", r"<\\/script", exploracion_json, flags=re.IGNORECASE)
        home_text = home_text.replace("__NOUTRORA_EXPLORACION_JSON__", exploracion_safe)
        (content_dir / "home.html").write_text(home_text, encoding="utf-8")

    (content_dir / "brand.properties").write_text(
        "brandShorterName = Noutrora\n"
        "brandShortName = Noutrora\n"
        "brandFullName = Noutrora Browser\n",
        encoding="utf-8",
    )

    (content_dir / "places.properties").write_text(
        "BookmarksMenuFolderTitle = Menú da Bitácora\n"
        "BookmarksToolbarFolderTitle = Barra da Bitácora\n"
        "OtherBookmarksFolderTitle = Outra Bitácora\n"
        "MobileBookmarksFolderTitle = Bitácora móbil\n"
        "OrganizerQueryAllBookmarks = Toda a Bitácora\n",
        encoding="utf-8",
    )

    manifest_lines = [
        "content noutrora-branding content/ contentaccessible=yes",
        "override chrome://branding/content/icon16.png chrome://noutrora-branding/content/default16.png",
        "override chrome://branding/content/icon32.png chrome://noutrora-branding/content/default32.png",
        "override chrome://branding/content/icon48.png chrome://noutrora-branding/content/default48.png",
        "override chrome://branding/content/icon64.png chrome://noutrora-branding/content/default64.png",
        "override chrome://branding/content/icon128.png chrome://noutrora-branding/content/default128.png",
        "override chrome://branding/content/about-logo.png chrome://noutrora-branding/content/default128.png",
        "override chrome://branding/content/about-logo@2x.png chrome://noutrora-branding/content/noutrora-512.png",
        "override chrome://branding/content/about-logo-private.png chrome://noutrora-branding/content/default128.png",
        "override chrome://branding/content/about-logo-private@2x.png chrome://noutrora-branding/content/noutrora-512.png",
        "override chrome://branding/content/about.png chrome://noutrora-branding/content/noutrora-512.png",
        "override chrome://branding/content/about-logo.svg chrome://noutrora-branding/content/noutrora.svg",
        "override chrome://branding/content/about-wordmark.svg chrome://noutrora-branding/content/noutrora-wordmark.svg",
        "override chrome://branding/content/firefox-wordmark.svg chrome://noutrora-branding/content/noutrora-wordmark.svg",
        "override chrome://global/skin/icons/defaultFavicon.svg chrome://noutrora-branding/content/noutrora.svg",
        "override chrome://global/skin/illustrations/kit-happy.svg chrome://noutrora-branding/content/noutrora.svg",
        "override chrome://global/skin/illustrations/kit-concerned.svg chrome://noutrora-branding/content/noutrora.svg",
        "override chrome://browser/skin/preferences/mozilla-logo.svg chrome://noutrora-branding/content/noutrora.svg",
        "override chrome://browser/skin/window-firefox.svg chrome://noutrora-branding/content/noutrora.svg",
        "override chrome://browser/skin/sidebar/firefox.svg chrome://noutrora-branding/content/noutrora.svg",
        "override chrome://browser/skin/sidebar/foxy.svg chrome://noutrora-branding/content/noutrora.svg",
        "override chrome://browser/skin/firefox-view.svg chrome://noutrora-branding/content/noutrora.svg",
        "override chrome://browser/content/browser/logos/share-firefox.svg chrome://noutrora-branding/content/noutrora.svg",
        "override chrome://browser/content/activity-stream/data/content/assets/splash-logo.svg chrome://noutrora-branding/content/noutrora.svg",
        "override chrome://browser/content/firefoxview/history-empty.svg chrome://noutrora-branding/content/noutrora-historial.svg",
        "override chrome://browser/skin/sidebar/kit-page-history.svg chrome://noutrora-branding/content/noutrora-historial.svg",
        "override chrome://browser/content/firefoxview/synced-tabs-empty.svg chrome://noutrora-branding/content/noutrora-dispositivos.svg",
        "override chrome://browser/content/firefoxview/synced-tabs-error.svg chrome://noutrora-branding/content/noutrora-dispositivos.svg",
        "override chrome://browser/skin/sidebar/kit-tabs-devices.svg chrome://noutrora-branding/content/noutrora-dispositivos.svg",
        "override chrome://browser/skin/sidebar/kit-tabs-devices-error.svg chrome://noutrora-branding/content/noutrora-dispositivos.svg",
        "override chrome://global/content/megalist/icons/cpm-fox-illustration.svg chrome://noutrora-branding/content/noutrora-cofre.svg",
        "override chrome://browser/skin/privatebrowsing/favicon.svg chrome://noutrora-branding/content/noutrora.svg",
        "override chrome://browser/skin/privatebrowsing/pbm-logo.svg chrome://noutrora-branding/content/noutrora.svg",
        "override chrome://branding/locale/brand.properties chrome://noutrora-branding/content/brand.properties",
        "override chrome://places/locale/places.properties chrome://noutrora-branding/content/places.properties",
    ]
    (overlay_dir / "chrome.manifest").write_text("\n".join(manifest_lines) + "\n", encoding="utf-8")


def setup_xdg_icon_override() -> None:
    """
    Prepara un directorio XDG de iconos local en base/xdg-data/icons/ (para Mint-Y y hicolor)
    de modo que el escritorio Linux (MATE/GTK3) muestre siempre la brújula de Noutrora
    en la lista de ventanas de la barra de tareas sin tocar los iconos del sistema.
    """
    xdg_icons = ROOT / "base" / "xdg-data" / "icons"
    png_512 = (BRAND_DIR / "noutrora-512.png").read_bytes()

    size_map = {
        16: (BRAND_DIR / "default16.png").read_bytes(),
        32: (BRAND_DIR / "default32.png").read_bytes(),
        48: (BRAND_DIR / "default48.png").read_bytes(),
        64: (BRAND_DIR / "default64.png").read_bytes(),
        128: (BRAND_DIR / "default128.png").read_bytes(),
        256: png_512,
        512: png_512,
    }
    for sz, data in size_map.items():
        hicolor_apps = xdg_icons / "hicolor" / f"{sz}x{sz}" / "apps"
        hicolor_apps.mkdir(parents=True, exist_ok=True)
        for name in ("noutrora.png", "firefox.png", "firefox-default.png"):
            (hicolor_apps / name).write_bytes(data)

    mint_theme_src = Path("/usr/share/icons/Mint-Y/index.theme")
    mint_dir = xdg_icons / "Mint-Y"
    mint_dir.mkdir(parents=True, exist_ok=True)
    if mint_theme_src.exists():
        shutil.copy2(mint_theme_src, mint_dir / "index.theme")

    for folder, sz in (
        ("16", 16), ("16@2x", 32),
        ("22", 32), ("22@2x", 48),
        ("24", 32), ("24@2x", 48),
        ("32", 32), ("32@2x", 64),
        ("48", 48), ("48@2x", 128),
        ("64", 64), ("64@2x", 128),
        ("96", 128), ("96@2x", 256),
        ("256", 256), ("256@2x", 512),
    ):
        app_dir = mint_dir / "apps" / folder
        app_dir.mkdir(parents=True, exist_ok=True)
        data = size_map[sz]
        for icon_name in (
            "noutrora.png",
            "firefox.png",
            "firefox-default.png",
            "firefox-icon.png",
            "firefox-gtk3.png",
            "firefox-original.png",
            "firefox-esr.png",
        ):
            (app_dir / icon_name).write_bytes(data)


def build():
    if not BASE_FIREFOX.exists():
        bootstrap_script = ROOT / "scripts" / "bootstrap.py"
        if bootstrap_script.exists():
            print("ℹ️  Motor base non atopado en base/firefox/. Descargando motor Gecko oficial en galego...")
            subprocess.run(["python3", str(bootstrap_script)], check=True)
        else:
            raise SystemExit(f"Non se atopou o motor base en {BASE_FIREFOX}")

    # 0. Garantizar que omni.ja esté 100% original (Superposición pura)
    restore_original_omni_if_needed()

    # 1. Asegurar que los activos de identidad visual v2.0 existen
    icons_src_dir = BRAND_DIR / "icons"
    if not (BRAND_DIR / "noutrora-wordmark.svg").exists() or not icons_src_dir.exists():
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

    # 4. Inyectar iconos de ventana y superposición externa (sin tocar omni.ja)
    icons_dir = BASE_FIREFOX / "browser" / "chrome" / "icons" / "default"
    icons_dir.mkdir(parents=True, exist_ok=True)
    for size in (16, 32, 48, 64, 128):
        src_icon = BRAND_DIR / f"default{size}.png"
        if src_icon.exists():
            for prefix in ("default", "noutrora", "firefox"):
                shutil.copy2(src_icon, icons_dir / f"{prefix}{size}.png")

    setup_external_branding_overlay()
    setup_xdg_icon_override()

    # 5. Copiar autoconfig.js y noutrora.cfg (con el logotipo e iconos vectoriales incrustados)
    pref_dir = BASE_FIREFOX / "defaults" / "pref"
    pref_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy2(CONFIG_DIR / "defaults" / "pref" / "autoconfig.js", pref_dir / "autoconfig.js")

    cfg_text = (CONFIG_DIR / "noutrora.cfg").read_text(encoding="utf-8")
    replacements = {
        "__NOUTRORA_WORDMARK_BASE64__": b64_file(BRAND_DIR / "noutrora-wordmark.svg"),
        "__NOUTRORA_WORDMARK_DARK_BASE64__": b64_file(BRAND_DIR / "noutrora-wordmark-dark.svg"),
        "__ICON_HOME_B64__": b64_file(icons_src_dir / "noutrora-home.svg"),
        "__ICON_RELOAD_B64__": b64_file(icons_src_dir / "noutrora-reload.svg"),
        "__ICON_BOOKMARK_B64__": b64_file(icons_src_dir / "noutrora-bookmark.svg"),
        "__ICON_ANCHOR_B64__": b64_file(icons_src_dir / "noutrora-anchor.svg"),
        "__ICON_ZEN_B64__": b64_file(icons_src_dir / "noutrora-zen.svg"),
        "__ICON_SHIELD_B64__": b64_file(icons_src_dir / "noutrora-shield.svg"),
        "__ICON_MOSAIC94_B64__": b64_file(icons_src_dir / "noutrora-mosaic94.svg"),
    }
    for placeholder, b64_val in replacements.items():
        cfg_text = cfg_text.replace(placeholder, b64_val)

    (BASE_FIREFOX / "noutrora.cfg").write_text(cfg_text, encoding="utf-8")

    print("✅ Noutrora compilado en modo Superposición 100% Externa (omni.ja intacto)")
    print("   - Identidad v2.0: Brújula en la 2.ª «o» (Modo Calma) + Paleta Océano Atlántico")
    print("   - Overlay de marca registrado vía noutrora-overlay/chrome.manifest")
    print("   - Set de 7 iconos vectoriales UI (24x24 SVG) inyectados")
    print(f"   - Marcadores inyectados: {len(bookmarks_data)}")


if __name__ == "__main__":
    build()
