import asyncio, edge_tts, os

# - - - - - - - - - - - - - - - - - - -
# Lista de Vozes em pt-BR

VOICE_FEMALE_PTBR = "pt-BR-FranciscaNeural"
VOICE_MALE_PTBR = "pt-BR-AntonioNeural"

# - - - - - - - - - - - - - - - - - - -
# Variáveis globais

TEXTO = ""
VOICE = ""
MODIFY_RATE = "+0%"
MODIFY_VOLUME = "+0%"
MODIFY_PITCH = "+0Hz"
OUTPUT_FILE = ""

# - - - - - - - - - - - - - - - - - - -
# Funções do Script

async def generate(text, voice, rate=MODIFY_RATE, volume=MODIFY_VOLUME, pitch=MODIFY_PITCH) -> None: # Fução Edge TTS    
    communicate = edge_tts.Communicate(f"{text}",
                                    f"{voice}", 
                                    rate=f"{rate}", 
                                    volume=f"{volume}",
                                    pitch=f"{pitch}"
                                    )
    await communicate.save(OUTPUT_FILE)

def credits_header(): # Cabeçalho de Créditos ao Autor
    print("Olá, seja Bem Vindo!")
    print("Este é um Script Text-to-Speech. Com ele você pode converter qualquer texto em áudio de forma simples e rápida!")
    print("- - - - - - - - - - - - - - - - - - - -")
    print("Script criado em Python utilizando Edge-TTS + async.")
    print("Créditos: Eduardo Riguetto (Kralot)")
    print("- - - - - - - - - - - - - - - - - - - -")
    print("")

def clean_terminal(): # Limpa o Terminal e adiciona o cabeçalho de Créditos ao Autor
    os.system('cls') # Limpa o Terminal
    credits_header() # Adiciona o cabeçalho de créditos ao autor

def input_texto(): # Inserir texto a ser convertido em áudio
    global TEXTO
    print("Digite o Texto a ser convertido em audio e pressione Enter:")
    TEXTO = input()

def select_voice(): # Selecionar Voz (Feminina ou Masculina)
    global VOICE
    while True:
        print("Digite F para selecionar a voz Feminina ou M para selecionar a voz Masculina:")
        VOICE_SELECT = input().upper()
        if VOICE_SELECT == "F":
            VOICE = "pt-BR-FranciscaNeural"
            break
        elif VOICE_SELECT == "M":
            VOICE = "pt-BR-AntonioNeural"
            break
        else:
            clean_terminal() # Limpa o Terminal
            print("Escolha invalida, por favor tente novamente.")

def select_rate(): # Alterar Velocidade da Voz
    global MODIFY_RATE
    while True:
        while True:
            try:
                print("Digite um número de 1 a 10 com um operador (+ ou -) para definir a intensidade da alteração.")
                MODIFY_RATE = input()
                OPERATOR = MODIFY_RATE[0]
                NUMBER = int(MODIFY_RATE[1:])
                if 0 <= NUMBER <= 10:
                    MODIFY_RATE = f"{OPERATOR}{NUMBER * 10}%"
                    break
                else:
                    clean_terminal() # Limpa o Terminal
                    print("Escolha invalida, por favor tente novamente.")
                    print("Digite um número de 1 a 10 com um operador (+ ou -) para definir a intensidade da alteração.")
            except ValueError:
                clean_terminal() # Limpa o Terminal
                print("Por favor, digite um número válido.")
        break

def select_volume(): # Alterar Volume da Voz
    global MODIFY_VOLUME
    while True:
        while True:
            try:
                print("Digite um número de 1 a 10 com um operador (+ ou -) para definir a intensidade da alteração:")
                MODIFY_VOLUME = input()
                OPERATOR = MODIFY_VOLUME[0]
                NUMBER = int(MODIFY_VOLUME[1:])
                if 0 <= NUMBER <= 10:
                    MODIFY_VOLUME = f"{OPERATOR}{NUMBER * 10}%"
                    break
                else:
                    clean_terminal() # Limpa o Terminal
                    print("Escolha invalida, por favor tente novamente.")
                    print("Digite um número de 1 a 10 com um operador (+ ou -) para definir a intensidade da alteração:")
            except ValueError:
                clean_terminal() # Limpa o Terminal
                print("Por favor, digite um número válido.")
        break

def select_pitch(): # Alterar Tom de Voz (Pitch)
    global MODIFY_PITCH
    while True:
        while True:
            try:
                print("Digite um número de 1 a 10 com um operador (+ ou -) para definir a intensidade da alteração:")
                MODIFY_PITCH = input()
                OPERATOR = MODIFY_PITCH[0]
                NUMBER = int(MODIFY_PITCH[1:])
                if 0 <= NUMBER <= 10:
                    MODIFY_PITCH = f"{OPERATOR}{NUMBER * 10}Hz"
                    break
                else:
                    clean_terminal() # Limpa o Terminal
                    print("Escolha invalida, por favor tente novamente.")
                    print("Digite um número de 1 a 10 com um operador (+ ou -) para definir a intensidade da alteração:")
            except ValueError:
                clean_terminal() # Limpa o Terminal
                print("Por favor, digite um número válido.")
        break

def select_name(): # Definir nome do Arquivo Final
    global OUTPUT_FILE
    print("Digite um nome para o arquivo MP3:")
    OUTPUT_FILE = input().strip() + ".mp3"
    OUTPUT_FILE = os.path.abspath(OUTPUT_FILE)

def modifications_menu(): # Menu de Modificações
    clean_terminal() # Limpa o Terminal
    while True:
        clean_terminal() # Limpa o Terminal
        print("Menu de Seleção: ")
        print("")
        print("1. Modificar Texto")
        print("2. Selecionar Voz")
        print("3. Alterar Velocidade")
        print("4. Alterar Volume")
        print("5. Alterar Tom de Voz")
        print("0. Finalizar e gerar novo áudio")
        print("")

        SELECTED = input("Escolha uma opção: ")
        match SELECTED:
            case "1": 
                clean_terminal() # Limpa o Terminal
                input_texto()
            case "2": 
                clean_terminal() # Limpa o Terminal
                select_voice()
            case "3": 
                clean_terminal() # Limpa o Terminal
                select_rate()
            case "4": 
                clean_terminal() # Limpa o Terminal
                select_volume()
            case "5": 
                clean_terminal() # Limpa o Terminal
                select_pitch()
            case "0":
                clean_terminal() # Limpa o Terminal
                select_name()
                print("- - - - - - - - - - - - - - - - - - - -")
                generate_audio()
            case _:
                clean_terminal() # Limpa o Terminal
                print("Escolha de Menu invalida, por favor tente novamente.")

def generate_new_audio(): # Questiona se deseja gerar um novo áudio e encaminha
    print("Você deseja modificar os parâmetros e gerar um novo áudio? (S/N)")
    MODIFY = input().upper()
    while True:
        if MODIFY == "S":
            clean_terminal() # Limpa o Terminal
            modifications_menu()
            break
        elif MODIFY == "N":
            clean_terminal() # Limpa o Terminal
            input("Pressione enter para sair.")
            exit()
        else:
            clean_terminal() # Limpa o Terminal
            print("Escolha invalida, por favor tente novamente.")
            print("Você deseja modificar os parâmetros e gerar um novo áudio? (S/N)")

def generate_audio(): # Gerar o Audio diante parâmetros informados:
    try:
        asyncio.run(generate(TEXTO, VOICE, MODIFY_RATE, MODIFY_VOLUME, MODIFY_PITCH))
        print("Arquivo gerado com sucesso!")
        print("Você deseja abrir o arquivo? (S/N)")
        
        while True:
            ABRIR_OU_SAIR = input().strip().upper()
            if ABRIR_OU_SAIR == "S":
                print("Abrindo arquivo...")
                os.system(f'start {OUTPUT_FILE}')
                print("- - - - - - - - - - - - - - - - - - - -")
                generate_new_audio()
                break
            elif ABRIR_OU_SAIR == "N":
                clean_terminal() # Limpa o Terminal
                generate_new_audio()      
                break 
            else:
                clean_terminal() # Limpa o Terminal
                print("Escolha invalida, por favor tente novamente.")
                print("Você deseja abrir o arquivo? (S/N)")

    except ValueError as error:
        print(f"Ocorreu um erro ao gerar o arquivo: {error}")
        MODIFY = print("Deseja alterar os parâmetros e tentar novamente? (S/N)")
        MODIFY = input().upper()
        if MODIFY == "S":
            clean_terminal() # Limpa o Terminal
            modifications_menu()
        elif MODIFY == "N":
            clean_terminal() # Limpa o Terminal
            input("Pressione enter para sair.")

def main(): # Função Principal
    credits_header() # Mostra o cabeçalho de Créditos ao Autor
    input_texto()
    clean_terminal() # Limpa o Terminal
    print("Seleção de Voz:")
    select_voice()
    clean_terminal() # Limpa o Terminal
    print("Você deseja alterar os parâmetros do gerador? (Velocidade, Volume, Pitch)")
    while True:
        print("Digite S para modificar parâmetros ou N para manter os parâmetros padrão:")
        MODIFY_PARAMETERS_QUESTION = input().strip().upper()
        if MODIFY_PARAMETERS_QUESTION == "S":
            while True:
                clean_terminal() # Limpa o Terminal
                print("Menu de Seleção: ")
                print("")
                print("1. Modificar Velocidade")
                print("2. Modificar Volume")
                print("3. Modificar Tom de Voz")
                print("0. Finalizar e gerar áudio")
                print("")

                SELECTED = input("Escolha uma opção: ")
                match SELECTED:
                    case "1": 
                        clean_terminal() # Limpa o Terminal
                        select_rate()
                    case "2": 
                        clean_terminal() # Limpa o Terminal
                        select_volume()
                    case "3": 
                        clean_terminal() # Limpa o Terminal
                        select_pitch()
                    case "0":
                        clean_terminal() # Limpa o Terminal
                        select_name()
                        print("- - - - - - - - - - - - - - - - - - - -")
                        generate_audio()
                        break
                    case _:
                        clean_terminal() # Limpa o Terminal
                        print("Escolha de Menu invalida, por favor tente novamente.")
        elif MODIFY_PARAMETERS_QUESTION == "N":
            clean_terminal() # Limpa o Terminal
            select_name()
            print("- - - - - - - - - - - - - - - - - - - -")
            generate_audio()
            break
        else:
            clean_terminal() # Limpa o Terminal
            print("Escolha invalida, por favor tente novamente.")

# - - - - - - - - - - - - - - - - - - -
# Execução do Script

if __name__ == "__main__":
    main()
