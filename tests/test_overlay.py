#!/usr/bin/env python3
"""Test de integridade da superposición de marca 100% externa (omni.ja intacto)."""
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONFIG_DIR = ROOT / "config"
BRAND_DIR = CONFIG_DIR / "branding"


class TestOverlayIntegrity(unittest.TestCase):
    def test_chrome_manifest_integrity(self):
        """O ficheiro chrome.manifest debe existir en base/firefox/noutrora-overlay/."""
        manifest = ROOT / "base" / "firefox" / "noutrora-overlay" / "chrome.manifest"
        self.assertTrue(manifest.exists(), "Falta base/firefox/noutrora-overlay/chrome.manifest")
        text = manifest.read_text(encoding="utf-8")
        self.assertIn(
            "content noutrora-branding content/ contentaccessible=yes",
            text,
            "chrome.manifest debe declarar noutrora-branding con contentaccessible=yes",
        )
        self.assertIn("override chrome://branding/content/about-logo.svg", text)
        self.assertIn("override chrome://browser/skin/preferences/mozilla-logo.svg", text)

    def test_essential_brand_assets_exist(self):
        """Deben existir os ficheiros esenciais de identidade: SVG, ICO e ICNS."""
        self.assertTrue((BRAND_DIR / "noutrora.svg").exists(), "Falta noutrora.svg")
        self.assertTrue((BRAND_DIR / "noutrora.ico").exists(), "Falta noutrora.ico")
        self.assertTrue((BRAND_DIR / "firefox.icns").exists(), "Falta firefox.icns para macOS")

    def test_ui_icons_set(self):
        """Os iconos vectoriais da interface de usuario deben estar presentes."""
        icons_dir = BRAND_DIR / "icons"
        self.assertTrue(icons_dir.exists(), "Falta o directorio config/branding/icons")
        expected_icons = [
            "noutrora-anchor.svg",
            "noutrora-bookmark.svg",
            "noutrora-containers.svg",
            "noutrora-home.svg",
            "noutrora-mosaic94.svg",
            "noutrora-reload.svg",
            "noutrora-shield.svg",
            "noutrora-zen.svg",
        ]
        for icon in expected_icons:
            icon_file = icons_dir / icon
            self.assertTrue(icon_file.exists(), f"Falta o icono UI: {icon}")


if __name__ == "__main__":
    unittest.main()
