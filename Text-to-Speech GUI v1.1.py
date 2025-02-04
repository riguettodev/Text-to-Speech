from PySimpleGUI import PySimpleGUI as sg
import asyncio, edge_tts, os, requests

# - - - - - - - - - - - - - - - - - - -

sg.theme('DarkGrey1') # Tema do PySimpleGUI

nome_app = "Text-to-Speech GUI v1.1"

menu_bar = [ # Menu da Janela Principal
    ['Arquivo',[
        '!Abrir',
        '!Salvar',
        '---',
        '!Propriedades',
        'Sair'
    ]],
    ['Ajuda',[
        'Verificar Serviço',
        '---',
        'Sobre'
        ]
    ]
]

NAME_SIZE = 10
def name(name):
    dots = NAME_SIZE-len(name)-2
    return sg.Text(name + ':' + ' '*dots, size=(NAME_SIZE,1), justification='left',pad=(0,0))

layout = [ # Layout da Janela Principal
    [sg.Menu(menu_bar)],
    [name('Texto'), sg.Multiline(key='TEXTO', size=(35,10), expand_x=True, border_width=(1))],
    [name('Voz'), sg.Combo(['Feminina (Português Brasileiro)', 'Masculina (Português Brasileiro)'], default_value='Feminina (Português Brasileiro)', readonly=True, expand_x=True, key='VOICE')],
    [sg.Sizer(0,10)],
    [sg.HorizontalSeparator()],
    [sg.Sizer(0,10)],
    [name('Velocidade'), sg.Slider((-10, 10), orientation='horizontal', default_value='0', size=(16,15), expand_x=True, key='RATE')],
    [name('Volume'), sg.Slider((-10, 10), orientation='horizontal', default_value='0', size=(16,15), expand_x=True, key='VOLUME')],
    [name('Pitch'), sg.Slider((-10, 10), orientation='horizontal', default_value='0', size=(16,15), expand_x=True, key='PITCH')],
    [sg.Sizer(0,10)],
    [sg.HorizontalSeparator()],
    [sg.Sizer(0,10)],
    [sg.Text('Nome do Arquivo:'), sg.Input(key='OUTPUT_FILE', size=(20,1), expand_x=True)],
    [sg.Sizer(0,5)],
    [sg.Checkbox("Abrir arquivo após conclusão", key='OPEN_FILE')],
    [sg.Sizer(0,10)],
    [sg.Button('Gerar Áudio'), sg.Button('Abrir Arquivo'), sg.Button('Limpar Logs')],
    [sg.Sizer(0,10)],
    [sg.HorizontalSeparator()],  
    [sg.Output(size=(0,8), expand_x=True, key='output_window')]
]

window_main = sg.Window(f'{nome_app} | by: Kralot', # Definições da Janela Principal
                        layout,
                        resizable=True,
                        auto_save_location=True,)

# Janela: Ajuda → Verificar Serviço
def create_window_verificar_servico():
    
    verificar_servico = [ # Layout da Janela
        [sg.Text("Verificando disponibilidade do Microsoft Edge Text-to-Speech")],
        [sg.Text("Aguarde, o programa não está travado!")],
        [sg.HorizontalSeparator()],
        [sg.Output(size=(50,10), expand_x=True)]
        ]
    
    window_verificar_servico_location = (window_main.CurrentLocation()[0] + -10, # Localização Horizontal
                                            window_main.CurrentLocation()[1] + 57) # Localização Vertical
    
    # Configuração da Janela
    window_verificar_servico = sg.Window('Verificar Serviço',
                                            verificar_servico,
                                            location=window_verificar_servico_location,
                                            resizable=True)
    
    
    # Ler os Eventos da Janela e criar uma lista
    eventos_verificar_servico, valores_verificar_servico = window_verificar_servico.read(timeout=0) # Gerar a Janela

    # Configuração dos Eventos da Janela
    if eventos_verificar_servico == sg.TIMEOUT_EVENT:
        verificar_tts = requests.get('https://speech.platform.bing.com/')
        print(verificar_tts.text)
    if eventos_verificar_servico == sg.WINDOW_CLOSED: # Verificar fechamento da Janela
        window_verificar_servico.close() # Fechar a Janela

# Janela: Ajuda → Sobre
def create_window_sobre():
    sobre = [ # Layout da Janela
        [sg.Text('Este programa foi criado utilizando a biblioteca EdgeTTS para Python, que utiliza o serviço Text-To-Speech da Microsoft para gerar áudios a partir de textos.',
                        size=(51,4))],
        [sg.Text('Interface criada utilizando PySimpleGUI')],
        [sg.Text('Criado por: Eduardo Riguetto (Kralot)')]
        ]
    
    window_sobre_location = (window_main.CurrentLocation()[0] + -25, # Localização Horizontal
                                    window_main.CurrentLocation()[1] + 57) # Localização Vertical
        
    window_sobre = sg.Window('Sobre',
                                sobre,
                                location=window_sobre_location)
    
    # Ler os Eventos da Janela e criar uma lista
    eventos_sobre, valores_sobre = window_sobre.read() # Gerar a Janela
    
    # Configuração dos Eventos da Janela
    if eventos_sobre == sg.WINDOW_CLOSED: # Verificar fechamento da Janela
        window_sobre.close() # Fechar a Janela

# - - - - - - - - - - - - - - - - - - -

def button_generate_audio(valores): # Tratar os eventos ao clicar no botão "Gerar Áudio"

    global OUTPUT_FILE

    TEXTO = valores['TEXTO']
    
    if valores['VOICE'] == 'Feminina (Português Brasileiro)':
        VOICE = 'pt-BR-FranciscaNeural'
    if valores['VOICE'] == 'Masculina (Português Brasileiro)':
        VOICE = 'pt-BR-AntonioNeural'
    
    RATE = int(valores['RATE'])*10
    MODIFY_RATE = f'+{RATE}%' if RATE >= 0 else f'{RATE}%'
    
    VOLUME = int(valores['VOLUME'])*10
    MODIFY_VOLUME = f'+{VOLUME}%' if VOLUME >= 0 else f'{VOLUME}%'
    
    PITCH = int(valores['PITCH'])*10
    MODIFY_PITCH = f'+{PITCH}Hz' if PITCH >= 0 else f'{PITCH}Hz'
    
    FILE_NAME = valores['OUTPUT_FILE']
    OUTPUT_FILE = f'{FILE_NAME}.mp3'

    asyncio.run(generate(TEXTO, VOICE, MODIFY_RATE, MODIFY_VOLUME, MODIFY_PITCH, OUTPUT_FILE))

async def generate(text, voice, rate, volume, pitch, output) -> None:  # Função para execução do EdgeTTS
    communicate = edge_tts.Communicate(text, voice, rate=rate, volume=volume, pitch=pitch)
    await communicate.save(output)

# - - - - - - - - - - - - - - - - - - -

program_running = True

while program_running: # Loop de Execução do Programa
    
    eventos, valores = window_main.read() # Listas de Eventos da Janela Principal
    
    if eventos == sg.WINDOW_CLOSED: # Verificar fechamento da Janela Principal
        program_running = False # Fechar o Programa
        break # Quebra o Loop de Execução do Programa
    
    # Menu: Arquivo → Sair
    if eventos == 'Sair':
        program_running = False # Fechar o Programa
        window_main.close()
        break
   
    # Menu: Ajuda → Verificar Serviço
    if eventos == 'Verificar Serviço':
        create_window_verificar_servico()

    # Menu: Ajuda → Sobre
    if eventos == 'Sobre':
        create_window_sobre()

    # Botões da Janela Principal
    if eventos == 'Gerar Áudio':
        try:
            button_generate_audio(valores)
            print("Arquivo gerado com sucesso!")
            if valores['OPEN_FILE'] == True:
                try:
                    print("Abrindo arquivo...")
                    print("- - - - - - - - - - - - - - -")
                    os.system(f'start {OUTPUT_FILE}')
                except Exception as error:
                    print(f'Não foi possível abrir o arquivo:')
                    print("")
                    print(f'{error}')
        except Exception as error:
            print(f"Ocorreu um erro ao gerar o arquivo:")
            print("")
            print(f'{error}')
    if eventos == 'Abrir Arquivo':
        try:
            print("Abrindo o ultimo arquivo gerado...")
            print("- - - - - - - - - - - - - - -")
            os.system(f'start {OUTPUT_FILE}')
        except Exception as error:
            print(f'Não foi possível abrir o arquivo:')
            print("")
            print(f'{error}')
    if eventos == 'Limpar Logs':
        window_main['output_window'].update('')

