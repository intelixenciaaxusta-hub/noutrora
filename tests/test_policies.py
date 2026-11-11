#!/usr/bin/env python3
"""Test de conformidade de políticas e privacidade segundo a Constitución de Noutrora."""
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONFIG_DIR = ROOT / "config"


class TestPoliciesAndPrivacy(unittest.TestCase):
    def setUp(self):
        self.template_path = CONFIG_DIR / "policies.template.json"
        self.assertTrue(self.template_path.exists(), "Falta policies.template.json")
        self.data = json.loads(self.template_path.read_text(encoding="utf-8"))
        self.policies = self.data.get("policies", {})
        self.cfg_text = (CONFIG_DIR / "noutrora.cfg").read_text(encoding="utf-8")

    def test_telemetry_and_privacy_disabled(self):
        """A telemetría, estudos e servizos de rastrexo deben estar totalmente desactivados."""
        self.assertTrue(self.policies.get("DisableTelemetry"), "A telemetría debe estar desactivada")
        self.assertTrue(self.policies.get("DisablePocket"), "Pocket debe estar desactivado")
        self.assertTrue(self.policies.get("DisableFirefoxStudies"), "Os estudos de Firefox deben estar desactivados")
        self.assertTrue(self.policies.get("DisableFirefoxAccounts"), "Firefox Accounts debe estar desactivado")
        self.assertFalse(self.policies.get("OfferToSaveLogins"), "Non debe pedir gardar contrasinais no navegador")

    def test_places_history_disabled_in_cfg(self):
        """A navegación non debe gardar historial (places.history.enabled = false)."""
        self.assertIn(
            'lockPref("places.history.enabled", false)',
            self.cfg_text,
            "places.history.enabled debe estar bloqueado a false en noutrora.cfg",
        )

    def test_homepage_policy_safety(self):
        """Homepage non debe forzar unha URL chrome:// que rompa o proceso de contido."""
        homepage = self.policies.get("Homepage", {})
        url = homepage.get("URL", "")
        self.assertFalse(
            url.startswith("chrome://"),
            "Homepage.URL non pode ser chrome:// porque Firefox bloquea a navegación en pestanas web",
        )
        self.assertEqual(
            homepage.get("StartPage"),
            "homepage-locked",
            "StartPage debe estar fixada a homepage-locked para garantir a páxina de inicio",
        )

    def test_first_run_skips_homepage_disabled(self):
        """O primeiro inicio non pode saltarse a páxina de inicio (firstrunSkipsHomepage = false)."""
        self.assertIn(
            'lockPref("browser.startup.firstrunSkipsHomepage", false)',
            self.cfg_text,
            "browser.startup.firstrunSkipsHomepage debe estar en false en noutrora.cfg",
        )

    def test_zero_infrastructure_ip_leak(self):
        """Os scripts de despregamento e modelos non deben conter IPs privadas nin nomes de host locais gravados en código."""
        package_web = (ROOT / "scripts" / "package_web.py").read_text(encoding="utf-8")
        self.assertNotIn("noutrora.local", package_web, "package_web.py non debe ter a IP do servidor gravada en código")
        self.assertNotIn("servidor", package_web, "package_web.py non debe ter servidor gravado en código")
        self.assertNotIn("smb://", package_web, "package_web.py non debe ter chamadas a smb://")
        self.assertNotIn("deploy_to_nas", package_web, "package_web.py non debe conter rutinas de despregamento no NAS privado")
        self.assertNotIn("noutrora.local", self.cfg_text, "noutrora.cfg non debe conter a IP do servidor")
        self.assertNotIn("noutrora.local", self.template_path.read_text(encoding="utf-8"), "policies.template.json non debe conter a IP do servidor")

    def test_package_web_tar_filter_privacy(self):
        """O filtro de empaquetado debe excluír estritamente ficheiros de contorna, instrucións privadas e normalizar UIDs."""
        import tarfile
        package_web = (ROOT / "scripts" / "package_web.py").read_text(encoding="utf-8")
        self.assertIn("tar_filter", package_web, "package_web.py debe implementar tar_filter")
        self.assertIn("AGENTS.md", package_web, "tar_filter debe excluír explicitamente AGENTS.md")
        self.assertIn("ti.uid = 0", package_web, "tar_filter debe normalizar UID a 0")



if __name__ == "__main__":
    unittest.main()

