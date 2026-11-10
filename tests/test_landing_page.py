#!/usr/bin/env python3
"""Test de integridade editorial da Landing Page (noutrora_landing_page_oficial.html)."""
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


class TestLandingPage(unittest.TestCase):
    def setUp(self):
        self.html_path = ROOT / "noutrora_landing_page_oficial.html"
        self.assertTrue(self.html_path.exists(), "Falta noutrora_landing_page_oficial.html")
        self.text = self.html_path.read_text(encoding="utf-8")

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


if __name__ == "__main__":
    unittest.main()

