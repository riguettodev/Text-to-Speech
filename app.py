"""Ponto de entrada para o executável empacotado (PyInstaller): abre a GUI.

Não pode apontar o PyInstaller direto para src/tts/gui.py porque os imports
relativos (from .core import ...) quebram fora do contexto de pacote. Este
launcher importa o pacote corretamente.
"""

from tts.gui import main

if __name__ == "__main__":
    main()
