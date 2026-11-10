#!/usr/bin/env python3
"""Test de integridade editorial e modular da Landing Page (index.html, style.css, app.js)."""
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


class TestLandingPage(unittest.TestCase):
    def setUp(self):
        self.html_path = ROOT / "index.html"
        self.assertTrue(self.html_path.exists(), "Falta index.html na raíz")
        self.text = self.html_path.read_text(encoding="utf-8")
        self.style_path = ROOT / "style.css"
        self.app_path = ROOT / "app.js"

    def test_modular_assets_exist_and_linked(self):
        """index.html debe ligar a style.css e app.js como módulos externos limpos."""
        self.assertTrue(self.style_path.exists(), "Falta style.css")
        self.assertTrue(self.app_path.exists(), "Falta app.js")
        self.assertIn('href="style.css"', self.text, "Falta a ligazón a style.css en index.html")
        self.assertIn('src="app.js"', self.text, "Falta o script app.js en index.html")

    def test_filosofia_and_decalogo_sections_exist(self):
        """A páxina oficial debe conter a sección de filosofía e o decálogo."""
        self.assertIn('id="filosofia"', self.text, "Falta a sección #filosofia")
        self.assertIn('id="decalogo"', self.text, "Falta o ancoraxe #decalogo")
        self.assertIn("A Forma de Ser e Pensar", self.text)
        self.assertIn("O Decálogo de Noutrora", self.text)

    def test_extensiones_section_and_items(self):
        """A páxina oficial debe conter a sección de equipamento coas 4 extensións de serie."""
        self.assertIn('id="equipamento"', self.text, "Falta a sección #equipamento")
        self.assertIn("uBlock Origin", self.text, "Falta mención a uBlock Origin")
        self.assertIn("I Still Don't Care About Cookies", self.text, "Falta mención a I Still Don't Care About Cookies")
        self.assertIn("SponsorBlock", self.text, "Falta mención a SponsorBlock")
        self.assertIn("Translate Web Pages", self.text, "Falta mención a Translate Web Pages")
        # Verificar vantaxes clave
        self.assertIn("publicidade", self.text.lower())
        self.assertIn("patrocinio", self.text.lower())
        self.assertIn("galego", self.text.lower())

    def test_decalogo_ten_points(self):
        """O decálogo debe conter os 10 principios fundacionais de Noutrora."""
        principios = [
            "Compartir porque si",
            "A túa intimidade é túa e punto",
            "Mover o cu para instalalo",
            "A IA é para ti, non para eles",
            "Menos parvada do momento e máis substancia",
            "Menos falar e máis ler",
            "A resistencia (Fahrenheit 451)",
            "Rebeldes coma Cameron Howe",
            "Aire de aldea contra o fume da cidade",
            "A nosa palabra",
        ]
        for p in principios:
            self.assertIn(p, self.text, f"Falta o principio '{p}' no decálogo")

    def test_ensaio_content_present(self):
        """O ensaio debe incluír os conceptos clave de economía do don e hipertexto."""
        self.assertIn("economía do don", self.text)
        self.assertIn("cultura do hipertexto", self.text)
        self.assertIn("Cory Doctorow", self.text)
        self.assertIn("aldeas irredutibles", self.text)

    def test_descargas_json_structure(self):
        """O ficheiro config/descargas.json debe ter a estrutura de plataformas e idiomas."""
        import json
        descargas_path = ROOT / "config" / "descargas.json"
        self.assertTrue(descargas_path.exists(), "Falta config/descargas.json")
        data = json.loads(descargas_path.read_text(encoding="utf-8"))
        self.assertIn("descargas", data)
        self.assertIn("plataformas", data["descargas"])
        for plat in ("linux", "windows", "mac"):
            self.assertIn(plat, data["descargas"]["plataformas"])
            self.assertIn("idiomas", data["descargas"]["plataformas"][plat])
            for lang in ("gl", "es", "eu", "ca"):
                self.assertIn(lang, data["descargas"]["plataformas"][plat]["idiomas"])

    def test_language_selector_and_counters_in_landing(self):
        """A páxina oficial debe conter o selector de 4 idiomas e a lóxica en app.js."""
        app_text = self.app_path.read_text(encoding="utf-8")
        self.assertIn("descargas.json", app_text, "Falta a carga de descargas.json en app.js")
        self.assertIn("selectInstallLanguage", app_text, "Falta a función selectInstallLanguage en app.js")
        self.assertIn("Galego", self.text)
        self.assertIn("Castelán", self.text)
        self.assertIn("Euskera", self.text)
        self.assertIn("Català", self.text)
        # Símbolos vectoriais circulares das bandeiras
        self.assertIn("flag-estreleira", self.text)
        self.assertIn("flag-ikurrina", self.text)
        self.assertIn("flag-estelada", self.text)
        self.assertIn("flag-castelan", self.text)

    def test_privacy_and_zero_external_trackers(self):
        """A páxina non debe chamar a CDNs externas nin Google Fonts, e debe incluír aviso legal."""
        self.assertNotIn("fonts.googleapis.com", self.text, "index.html non debe chamar a Google Fonts")
        self.assertNotIn("fonts.gstatic.com", self.text, "index.html non debe pre-conectar a gstatic")
        self.assertNotIn("cdn.tailwindcss.com", self.text, "index.html non debe depender da CDN externa de Tailwind")
        self.assertTrue((ROOT / "tailwind.js").exists(), "Falta o ficheiro tailwind.js local")
        self.assertIn('src="tailwind.js"', self.text, "Falta a ligazón local a tailwind.js")
        # Conformidade RGPD e LSSI-CE
        self.assertIn("intelixenciaaxusta@gmail.com", self.text, "Falta o correo de contacto de titularidade (Art. 10 LSSI)")
        self.assertIn('id="privacy-modal"', self.text, "Falta o modal de privacidade e aviso legal")
        self.assertIn("openPrivacyModal", self.app_path.read_text(encoding="utf-8"), "Falta a función openPrivacyModal en app.js")
        # Seguridade de contido e referente
        self.assertIn("Content-Security-Policy", self.text, "Falta a metaetiqueta Content-Security-Policy en index.html")
        self.assertIn('name="referrer" content="no-referrer"', self.text, "Falta a metaetiqueta Referrer-Policy en index.html")


if __name__ == "__main__":
    unittest.main()

