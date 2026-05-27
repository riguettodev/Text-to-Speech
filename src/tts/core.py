"""Núcleo de síntese de voz.

Sem dependências de interface: só edge-tts, formatação de parâmetros e a lista
de vozes. GUI e CLI consomem este módulo.
"""

import edge_tts

# Vozes pt-BR
VOZ_FEMININA = "pt-BR-FranciscaNeural"
VOZ_MASCULINA = "pt-BR-AntonioNeural"

# Rótulo exibido na UI -> nome interno do edge-tts
VOZES = {
    "Feminina (Português Brasileiro)": VOZ_FEMININA,
    "Masculina (Português Brasileiro)": VOZ_MASCULINA,
}


def fmt_porcentagem(valor):
    """Converte um valor -10..10 para o formato de rate/volume do edge-tts (ex.: +50%)."""
    n = int(valor) * 10
    return f"+{n}%" if n >= 0 else f"{n}%"


def fmt_hertz(valor):
    """Converte um valor -10..10 para o formato de pitch do edge-tts (ex.: -30Hz)."""
    n = int(valor) * 10
    return f"+{n}Hz" if n >= 0 else f"{n}Hz"


async def gerar_audio(texto, voz, rate="+0%", volume="+0%", pitch="+0Hz", saida="output.mp3"):
    """Sintetiza `texto` na `voz` informada e salva o MP3 em `saida`.

    Os parâmetros rate/volume/pitch já devem vir formatados (use fmt_porcentagem
    e fmt_hertz). edge-tts é assíncrono, daí a corrotina.
    """
    communicate = edge_tts.Communicate(texto, voz, rate=rate, volume=volume, pitch=pitch)
    await communicate.save(saida)
