"""Conversor de texto em áudio (Text-to-Speech) usando edge-tts.

Camadas:
    core    -> síntese de voz, vozes e formatação de parâmetros
    system  -> helpers dependentes de plataforma (Windows/Linux/macOS)
    gui     -> interface gráfica (Tkinter)
    cli     -> interface de terminal
"""

__version__ = "0.9.0"
