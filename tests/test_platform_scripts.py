#!/usr/bin/env python3
"""Test de scripts de arranque e instalación multiplataforma (Windows, macOS, Linux)."""
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


class TestPlatformScripts(unittest.TestCase):
    def test_windows_script_crlf_terminators(self):
        """O instalador de Windows Noutrora-Setup-Windows.cmd debe usar estritamente CRLF."""
        win_cmd = ROOT / "Noutrora-Setup-Windows.cmd"
        self.assertTrue(win_cmd.exists(), "Falta Noutrora-Setup-Windows.cmd na raíz")
        raw_bytes = win_cmd.read_bytes()
        self.assertIn(b"\r\n", raw_bytes, "O script de Windows debe conter terminadores CRLF (\\r\\n)")
        # Comprobar que non teña terminadores LF soltos
        cleaned = raw_bytes.replace(b"\r\n", b"")
        self.assertNotIn(b"\n", cleaned, "Non pode haber terminadores Unix LF soltos no script de Windows")

    def test_windows_script_syntax_and_profile(self):
        """O script de Windows non debe usar parénteses conflitivos en if e debe illar o perfil."""
        text = (ROOT / "Noutrora-Setup-Windows.cmd").read_text(encoding="utf-8")
        # Asegurar que use -profile e non o dobre guión --profile
        self.assertIn("-profile", text, "Debe empregar -profile con guión sinxelo")
        self.assertNotIn("--profile", text, "Non pode empregar --profile con dobre guión")
        self.assertIn("-no-remote", text, "Debe usar -no-remote para evitar colisións de instancias")
        self.assertIn("goto :have_engine", text, "Debe empregar fluxo goto limpo para evitar erros de sintaxe CMD")

    def test_mac_script_profile_isolation(self):
        """O script de macOS debe illar o perfil en ~/Library/Application Support/Noutrora/profile."""
        from scripts.package_web import MAC_INSTALLER_COMMAND
        self.assertIn(
            "Library/Application Support/Noutrora/profile",
            MAC_INSTALLER_COMMAND,
            "macOS debe definir o perfil illado en ~/Library/Application Support/Noutrora/profile",
        )
        self.assertIn(
            "-no-remote",
            MAC_INSTALLER_COMMAND,
            "macOS debe arrincar con -no-remote para non colidir co Firefox do sistema",
        )

    def test_linux_scripts_syntax(self):
        """Os scripts bash de Linux deben ter sintaxe válida (bash -n)."""
        for script in (ROOT / "run.sh", ROOT / "install-linux.sh"):
            if script.exists():
                res = subprocess.run(["bash", "-n", str(script)], capture_output=True, text=True)
                self.assertEqual(res.returncode, 0, f"Erro de sintaxe bash en {script.name}: {res.stderr}")


if __name__ == "__main__":
    unittest.main()
