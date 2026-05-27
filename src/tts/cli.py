"""Interface de terminal interativa para o conversor Text-to-Speech."""

import asyncio
import os

from .core import VOZ_FEMININA, VOZ_MASCULINA, fmt_hertz, fmt_porcentagem, gerar_audio
from .system import abrir_arquivo, limpar_terminal

SEP = "- " * 20


def cabecalho():
    print("Olá, seja Bem Vindo!")
    print("Conversor Text-to-Speech: transforma texto em áudio de forma simples e rápida.")
    print(SEP)
    print("Feito em Python com edge-tts. Créditos: Eduardo Riguetto (Kralot)")
    print(SEP)
    print()


def perguntar_sim_nao(pergunta):
    while True:
        resposta = input(f"{pergunta} [S/N] ").strip().upper()
        if resposta == "S":
            return True
        if resposta == "N":
            return False
        print("Responda com S ou N.")


def ler_texto():
    print("Digite o texto a ser convertido em áudio e pressione Enter:")
    return input().strip()


def ler_voz():
    while True:
        escolha = input("Voz — [F]eminina ou [M]asculina? ").strip().upper()
        if escolha == "F":
            return VOZ_FEMININA
        if escolha == "M":
            return VOZ_MASCULINA
        print("Escolha inválida, tente novamente.")


def ler_parametro(rotulo):
    """Lê um inteiro de -10 a 10 (ex.: +5, -3, 0)."""
    while True:
        bruto = input(f"{rotulo} — número de -10 a 10 (ex.: +5, -3, 0): ").strip()
        try:
            valor = int(bruto)
        except ValueError:
            print("Digite um número válido (ex.: +5).")
            continue
        if -10 <= valor <= 10:
            return valor
        print("O número deve estar entre -10 e 10.")


def menu_parametros(rate, volume, pitch):
    while True:
        print()
        print(f"1. Velocidade ({rate:+d})")
        print(f"2. Volume ({volume:+d})")
        print(f"3. Pitch ({pitch:+d})")
        print("0. Concluir")
        opcao = input("Escolha: ").strip()
        if opcao == "1":
            rate = ler_parametro("Velocidade")
        elif opcao == "2":
            volume = ler_parametro("Volume")
        elif opcao == "3":
            pitch = ler_parametro("Pitch")
        elif opcao == "0":
            return rate, volume, pitch
        else:
            print("Opção inválida.")


def gerar(texto, voz, rate, volume, pitch, saida):
    try:
        asyncio.run(
            gerar_audio(
                texto,
                voz,
                rate=fmt_porcentagem(rate),
                volume=fmt_porcentagem(volume),
                pitch=fmt_hertz(pitch),
                saida=saida,
            )
        )
        print(f"Arquivo gerado com sucesso: {saida}")
        return True
    except Exception as error:
        print(f"Erro ao gerar o arquivo: {error}")
        return False


def main():
    limpar_terminal()
    cabecalho()

    texto = ler_texto()
    voz = ler_voz()
    rate = volume = pitch = 0
    if perguntar_sim_nao("Deseja ajustar velocidade/volume/pitch?"):
        rate, volume, pitch = menu_parametros(rate, volume, pitch)

    while True:
        nome = input("Nome do arquivo MP3 (sem extensão): ").strip() or "output"
        saida = os.path.abspath(nome + ".mp3")
        print(SEP)
        if gerar(texto, voz, rate, volume, pitch, saida) and perguntar_sim_nao("Abrir o arquivo agora?"):
            abrir_arquivo(saida)

        if not perguntar_sim_nao("Gerar outro áudio?"):
            break

        if perguntar_sim_nao("Alterar o texto?"):
            texto = ler_texto()
        if perguntar_sim_nao("Alterar a voz?"):
            voz = ler_voz()
        if perguntar_sim_nao("Ajustar velocidade/volume/pitch?"):
            rate, volume, pitch = menu_parametros(rate, volume, pitch)

    print("Até logo!")


if __name__ == "__main__":
    main()
