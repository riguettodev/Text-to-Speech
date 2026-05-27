# Text-to-Speech

Conversor de texto em áudio (MP3) usando [edge-tts](https://github.com/rany2/edge-tts)
— o serviço Text-to-Speech do Microsoft Edge. Tem interface gráfica (Tkinter) e
de terminal. Funciona em Windows, Linux e macOS.

## Instalação

Requer Python 3.9+. No Linux, a interface gráfica precisa do Tk do sistema:

```bash
sudo apt install python3-tk        # Debian/Ubuntu (no Windows já vem com o Python)
```

Instale o projeto em modo editável:

```bash
pip install -e .
```

## Uso

```bash
tts-gui      # interface gráfica
tts-cli      # interface de terminal
```

Sem instalar, a partir da pasta `src/`:

```bash
python -m tts.gui
python -m tts.cli
```

## Estrutura

```
src/tts/
├── core.py      # vozes, formatação de parâmetros e síntese (edge-tts)
├── system.py    # helpers de plataforma (abrir arquivo, limpar terminal)
├── gui.py       # interface Tkinter
└── cli.py       # interface de terminal
```

`gui` e `cli` são cascas finas sobre `core`; nenhuma lógica de síntese é duplicada.

## Créditos

Eduardo Riguetto (Kralot).
