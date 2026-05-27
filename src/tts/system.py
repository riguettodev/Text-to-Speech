"""Helpers dependentes de plataforma (Windows, Linux, macOS)."""

import os
import subprocess
import sys


def abrir_arquivo(caminho):
    """Abre um arquivo no aplicativo padrão do sistema."""
    if sys.platform.startswith("win"):
        os.startfile(caminho)  # type: ignore[attr-defined]  # só existe no Windows
    elif sys.platform == "darwin":
        subprocess.run(["open", caminho], check=False)
    else:
        subprocess.run(["xdg-open", caminho], check=False)


def limpar_terminal():
    """Limpa a tela do terminal."""
    os.system("cls" if sys.platform.startswith("win") else "clear")
