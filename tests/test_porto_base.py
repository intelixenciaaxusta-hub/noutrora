#!/usr/bin/env python3
"""Test de conformidade do Catálogo Cultural e Marinero Vivo e Porto Base (3x2)."""
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONFIG_DIR = ROOT / "config"


class TestPortoBaseAndCatalog(unittest.TestCase):
    def setUp(self):
        self.catalog_path = CONFIG_DIR / "exploracion.json"
        self.assertTrue(self.catalog_path.exists(), "Falta config/exploracion.json")
        self.data = json.loads(self.catalog_path.read_text(encoding="utf-8"))
        self.home_text = (CONFIG_DIR / "home.html").read_text(encoding="utf-8")

    def test_catalog_structure_and_keys(self):
        """O catálogo exploracion.json debe conter as seccións esenciais."""
        for section in ("perder_el_rumbo", "mundo_nuevo", "zambullirse", "libros", "puertos"):
            self.assertIn(section, self.data, f"Falta a sección '{section}' en exploracion.json")
            self.assertIsInstance(self.data[section], list, f"A sección '{section}' debe ser unha lista")
            self.assertGreater(len(self.data[section]), 0, f"A sección '{section}' non pode estar baleira")

    def test_items_have_title_and_url(self):
        """Todos os elementos culturais deben ter polo menos título e URL válidos."""
        for section in ("perder_el_rumbo", "mundo_nuevo", "zambullirse", "libros"):
            for item in self.data[section]:
                title = item.get("titulo") or item.get("title") or item.get("name")
                url = item.get("url") or item.get("article_url") or item.get("more_url")
                self.assertTrue(title, f"Elemento sen título en {section}: {item}")
                self.assertTrue(url, f"Elemento sen URL en {section}: {item}")

    def test_home_html_integrity(self):
        """home.html non debe conter restos rotos nin variables sen interpolar do build."""
        self.assertIn("Porto Base", self.home_text, "home.html debe facer referencia ao Porto Base")
        self.assertIn("Perder o norte", self.home_text, "Falta a carta 01 · Perder o norte")
        self.assertIn("Terra á vista", self.home_text, "Falta a carta 02 · Terra á vista")
        self.assertIn("Mergullar", self.home_text, "Falta a carta 03 · Mergullar")
        self.assertIn("Atracar", self.home_text, "Falta a carta 05 · Atracar")
        self.assertIn("Fondear", self.home_text, "Falta a carta 06 · Fondear")


    def test_search_form_native_navigation(self):
        """O formulario de busca debe permitir navegación nativa en contornas chrome:// e file://."""
        self.assertIn(
            'action="https://duckduckgo.com/"',
            self.home_text,
            "O formulario de busca debe ter action predeterminado cara ao buscador",
        )
        self.assertIn(
            'method="GET"',
            self.home_text,
            "O formulario de busca debe usar method=GET para navegación web estándar",
        )
        self.assertIn(
            'name="q"',
            self.home_text,
            "O input de busca debe ter name=q para envío estándar do termo de busca",
        )
        self.assertIn(
            "navigateSafely",
            self.home_text,
            "home.html debe dispor de navigateSafely para evitar bloqueos de seguridade dende chrome://",
        )


if __name__ == "__main__":
    unittest.main()
