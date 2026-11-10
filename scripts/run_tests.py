#!/usr/bin/env python3
"""
Executor unificado de probas técnicas de Noutrora.
Garante que ningún cambio se suba nin se publique sen pasar a suite de probas.
"""
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TESTS_DIR = ROOT / "tests"


def run_all_tests() -> bool:
    print("🧭 ================================================================")
    print("   NOUTRORA — Batería de Probas de Integridade e Calma Atlántica")
    print("==================================================================")
    print("🔍 Descubrindo e executando probas en tests/...\n")

    loader = unittest.TestLoader()
    suite = loader.discover(start_dir=str(TESTS_DIR), pattern="test_*.py")

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    print("\n------------------------------------------------------------------")
    if result.wasSuccessful():
        print(f"✅ TODAS AS PROBAS PASARON ({result.testsRun} probas executadas con éxito).")
        print("🌊 Rumbo despexado e augas tranquilas para proceder.")
        print("------------------------------------------------------------------")
        return True
    else:
        print(f"❌ FALLARON {len(result.failures)} PROBAS e houbo {len(result.errors)} ERROS.")
        print("⚠️ ALERTA: Non se permite publicar nin realizar commits ata resolver os fallos.")
        print("------------------------------------------------------------------")
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
