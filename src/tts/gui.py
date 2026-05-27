"""Interface gráfica (Tkinter) para o conversor Text-to-Speech."""

import asyncio
import os
import threading

import tkinter as tk
from tkinter import messagebox, scrolledtext, ttk

from .core import VOZES, fmt_hertz, fmt_porcentagem, gerar_audio
from .system import abrir_arquivo

NOME_APP = "Text-to-Speech GUI"


class TTSApp:
    def __init__(self, root):
        self.root = root
        self.ultimo_arquivo = None

        root.title(f"{NOME_APP} | by: Kralot")
        root.minsize(500, 560)

        self._montar_widgets()

    def _montar_widgets(self):
        pad = {"padx": 8, "pady": 4}
        frm = ttk.Frame(self.root, padding=12)
        frm.pack(fill="both", expand=True)
        frm.columnconfigure(1, weight=1)

        row = 0

        # Texto
        ttk.Label(frm, text="Texto:").grid(row=row, column=0, sticky="nw", **pad)
        self.txt_texto = tk.Text(frm, height=8, wrap="word")
        self.txt_texto.grid(row=row, column=1, sticky="nsew", **pad)
        frm.rowconfigure(row, weight=1)
        row += 1

        # Voz
        ttk.Label(frm, text="Voz:").grid(row=row, column=0, sticky="w", **pad)
        self.cbo_voz = ttk.Combobox(frm, values=list(VOZES.keys()), state="readonly")
        self.cbo_voz.current(0)
        self.cbo_voz.grid(row=row, column=1, sticky="ew", **pad)
        row += 1

        ttk.Separator(frm).grid(row=row, column=0, columnspan=2, sticky="ew", pady=8)
        row += 1

        # Sliders de modificação da voz
        self.var_rate = tk.IntVar(value=0)
        self.var_volume = tk.IntVar(value=0)
        self.var_pitch = tk.IntVar(value=0)
        row = self._adicionar_slider(frm, row, "Velocidade", self.var_rate)
        row = self._adicionar_slider(frm, row, "Volume", self.var_volume)
        row = self._adicionar_slider(frm, row, "Pitch", self.var_pitch)

        ttk.Separator(frm).grid(row=row, column=0, columnspan=2, sticky="ew", pady=8)
        row += 1

        # Nome do arquivo
        ttk.Label(frm, text="Nome do arquivo:").grid(row=row, column=0, sticky="w", **pad)
        self.ent_arquivo = ttk.Entry(frm)
        self.ent_arquivo.insert(0, "output")
        self.ent_arquivo.grid(row=row, column=1, sticky="ew", **pad)
        row += 1

        # Checkbox abrir após gerar
        self.var_abrir = tk.BooleanVar(value=False)
        ttk.Checkbutton(
            frm, text="Abrir arquivo após gerar", variable=self.var_abrir
        ).grid(row=row, column=1, sticky="w", **pad)
        row += 1

        # Botões
        btns = ttk.Frame(frm)
        btns.grid(row=row, column=0, columnspan=2, sticky="ew", **pad)
        self.btn_gerar = ttk.Button(btns, text="Gerar Áudio", command=self.on_gerar)
        self.btn_gerar.pack(side="left")
        self.btn_abrir = ttk.Button(
            btns, text="Abrir Arquivo", command=self.on_abrir, state="disabled"
        )
        self.btn_abrir.pack(side="left", padx=6)
        ttk.Button(btns, text="Limpar Logs", command=self.on_limpar_logs).pack(side="left")
        row += 1

        # Área de logs
        self.log = scrolledtext.ScrolledText(frm, height=6, state="disabled", wrap="word")
        self.log.grid(row=row, column=0, columnspan=2, sticky="nsew", **pad)
        frm.rowconfigure(row, weight=1)

    def _adicionar_slider(self, frm, row, rotulo, var):
        ttk.Label(frm, text=f"{rotulo}:").grid(row=row, column=0, sticky="w", padx=8, pady=4)
        sub = ttk.Frame(frm)
        sub.grid(row=row, column=1, sticky="ew", padx=8, pady=4)
        sub.columnconfigure(0, weight=1)

        # ttk.Scale é contínuo; arredondamos para travar em inteiros (-10..10)
        ttk.Scale(
            sub,
            from_=-10,
            to=10,
            variable=var,
            command=lambda v, var=var: var.set(round(float(v))),
        ).grid(row=0, column=0, sticky="ew")

        valor_lbl = ttk.Label(sub, width=4)
        valor_lbl.grid(row=0, column=1, padx=(6, 0))
        var.trace_add("write", lambda *_, var=var, lbl=valor_lbl: lbl.config(text=str(var.get())))
        valor_lbl.config(text=str(var.get()))
        return row + 1

    # - - - Logs (thread-safe via root.after) - - -

    def log_msg(self, msg):
        def _append():
            self.log.config(state="normal")
            self.log.insert("end", msg + "\n")
            self.log.see("end")
            self.log.config(state="disabled")

        self.root.after(0, _append)

    def on_limpar_logs(self):
        self.log.config(state="normal")
        self.log.delete("1.0", "end")
        self.log.config(state="disabled")

    # - - - Ações - - -

    def on_abrir(self):
        if not self.ultimo_arquivo or not os.path.exists(self.ultimo_arquivo):
            messagebox.showwarning(NOME_APP, "Nenhum arquivo gerado ainda.")
            return
        try:
            abrir_arquivo(self.ultimo_arquivo)
        except Exception as error:
            self.log_msg(f"Não foi possível abrir o arquivo: {error}")

    def on_gerar(self):
        texto = self.txt_texto.get("1.0", "end").strip()
        if not texto:
            messagebox.showwarning(NOME_APP, "Digite um texto para converter.")
            return

        nome = self.ent_arquivo.get().strip() or "output"
        saida = os.path.abspath(nome + ".mp3")
        voz = VOZES[self.cbo_voz.get()]
        rate = fmt_porcentagem(self.var_rate.get())
        volume = fmt_porcentagem(self.var_volume.get())
        pitch = fmt_hertz(self.var_pitch.get())

        # Gera em thread separada para não congelar a janela durante a síntese.
        self.btn_gerar.config(state="disabled")
        self.log_msg(f"Gerando áudio... (rate={rate}, volume={volume}, pitch={pitch})")
        threading.Thread(
            target=self._worker,
            args=(texto, voz, rate, volume, pitch, saida),
            daemon=True,
        ).start()

    def _worker(self, texto, voz, rate, volume, pitch, saida):
        try:
            asyncio.run(gerar_audio(texto, voz, rate=rate, volume=volume, pitch=pitch, saida=saida))
            self.root.after(0, self._on_sucesso, saida)
        except Exception as error:
            self.root.after(0, self._on_erro, error)

    def _on_sucesso(self, saida):
        self.ultimo_arquivo = saida
        self.btn_gerar.config(state="normal")
        self.btn_abrir.config(state="normal")
        self.log_msg(f"Arquivo gerado com sucesso: {saida}")
        if self.var_abrir.get():
            try:
                abrir_arquivo(saida)
                self.log_msg("Abrindo arquivo...")
            except Exception as error:
                self.log_msg(f"Não foi possível abrir o arquivo: {error}")

    def _on_erro(self, error):
        self.btn_gerar.config(state="normal")
        self.log_msg(f"Erro ao gerar o arquivo: {error}")
        messagebox.showerror(NOME_APP, f"Erro ao gerar o arquivo:\n{error}")


def main():
    root = tk.Tk()
    try:
        ttk.Style().theme_use("clam")  # aparência consistente entre os SOs
    except tk.TclError:
        pass
    TTSApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
