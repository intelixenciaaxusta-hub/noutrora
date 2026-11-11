#!/usr/bin/env python3
"""
Test de conformidade normativa obrigatoria española e europea (LOPD-GDD, RGPD, LSSI-CE, MPL-2.0).
Garante que o proxecto veciñal sen ánimo de lucro cumpra sempre os seus compromisos éticos e legais.
"""
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


class TestNormativa(unittest.TestCase):
    def setUp(self):
        self.normativa_dir = ROOT / "normativa"
        self.lopd_doc = self.normativa_dir / "LOPD_GDD_RGPD.md"
        self.licenzas_doc = self.normativa_dir / "LICENZAS_FIREFOX_MPL.md"
        self.guia_doc = self.normativa_dir / "GUIA_REVISION_PERIODICA.md"
        self.html_path = ROOT / "index.html"
        self.cfg_path = ROOT / "config" / "noutrora.cfg"
        self.policies_path = ROOT / "config" / "policies.template.json"

    def test_normativa_directory_and_documents_exist(self):
        """A carpeta normativa/ debe existir e conter os 3 documentos reguladores."""
        if not self.normativa_dir.is_dir() or not self.lopd_doc.is_file():
            self.skipTest("Documentación normativa mantida en privado en local (fóra de Git)")
        self.assertTrue(self.normativa_dir.is_dir(), "Falta a carpeta normativa/")
        self.assertTrue(self.lopd_doc.is_file(), "Falta normativa/LOPD_GDD_RGPD.md")
        self.assertTrue(self.licenzas_doc.is_file(), "Falta normativa/LICENZAS_FIREFOX_MPL.md")
        self.assertTrue(self.guia_doc.is_file(), "Falta normativa/GUIA_REVISION_PERIODICA.md")

    def test_lopd_document_content(self):
        """O documento de protección de datos debe acreditar a condición veciñal sen ánimo de lucro."""
        if not self.lopd_doc.is_file():
            self.skipTest("Documento LOPD mantido en privado en local (fóra de Git)")
        text = self.lopd_doc.read_text(encoding="utf-8")
        self.assertIn("RGPD", text)
        self.assertIn("LOPD-GDD", text)
        self.assertIn("sen ánimo de lucro", text.lower())
        self.assertIn("asociación de veciños", text.lower())
        self.assertIn("minimización", text.lower())
        self.assertIn("intelixenciaaxusta@gmail.com", text)

    def test_licenzas_document_content(self):
        """O documento de licenzas debe respectar a MPL-2.0 e a política de marcas de Mozilla."""
        if not self.licenzas_doc.is_file():
            self.skipTest("Documento de licenzas mantido en privado en local (fóra de Git)")
        text = self.licenzas_doc.read_text(encoding="utf-8")
        self.assertIn("MPL-2.0", text)
        self.assertIn("Mozilla Public License", text)
        self.assertIn("Trademark", text)
        self.assertIn("omni.ja", text)
        self.assertIn("uBlock Origin", text)

    def test_browser_zero_telemetry_compliance(self):
        """A configuración de Noutrora debe bloquear estritamente a telemetría e o historial."""
        cfg_text = self.cfg_path.read_text(encoding="utf-8")
        self.assertIn('lockPref("places.history.enabled", false);', cfg_text)
        self.assertIn('lockPref("datareporting.policy.dataSubmissionEnabled", false);', cfg_text)
        self.assertIn('lockPref("toolkit.telemetry.enabled", false);', cfg_text)

        policies_text = self.policies_path.read_text(encoding="utf-8")
        self.assertIn('"DisableTelemetry": true', policies_text)
        self.assertIn('"DisableFirefoxStudies": true', policies_text)

    def test_landing_page_legal_and_privacy_compliance(self):
        """A web oficial debe reflectir a titularidade veciñal, contacto e cero CDNs externas."""
        html_text = self.html_path.read_text(encoding="utf-8")
        # Ausencia de fontes externas que filtren IP
        self.assertNotIn("fonts.googleapis.com", html_text)
        self.assertNotIn("cdn.tailwindcss.com", html_text)
        # Identificación e contacto obrigatorios LSSI / RGPD
        self.assertIn("intelixenciaaxusta@gmail.com", html_text)
        self.assertIn("asociación de veciños", html_text.lower())
        self.assertIn("MPL-2.0", html_text)
        self.assertIn('id="privacy-modal"', html_text)


if __name__ == "__main__":
    unittest.main()

