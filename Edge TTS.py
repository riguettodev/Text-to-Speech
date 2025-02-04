import asyncio, edge_tts, random
from edge_tts import VoicesManager

# - - - - - - - - - - - - - - - - - - -

async def generate(text, voice, rate="+0%", volume="+0%", pitch="+0Hz") -> None:
    communicate = edge_tts.Communicate(f"{text}",
                                       f"{voice}", 
                                       rate=f"{rate}", 
                                       volume=f"{volume}",
                                       pitch=f"{pitch}"
                                       )
    await communicate.save(OUTPUT_FILE)

async def generate_select_voice(gender, language) -> None:
    voices = await VoicesManager.create()
    voice = voices.find(Gender=f"{gender}", Language=f"{language}")
    # Also supports Locales
    # voice = voices.find(Gender="Female", Locale="es-AR")

    communicate = edge_tts.Communicate(TEXTO, random.choice(voice)["Name"])
    await communicate.save(OUTPUT_FILE)

async def stream(text, voice) -> None:
    communicate = edge_tts.Communicate(f"{text}", f"{voice}")
    with open(OUTPUT_FILE, "wb") as file:
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                file.write(chunk["data"])
            elif chunk["type"] == "WordBoundary":
                print(f"WordBoundary: {chunk}")

# - - - - - - - - - - - - - - - - - - -

VOICE_MALE_PTBR = "pt-BR-AntonioNeural"
VOICE_FEMALE_PTBR = "pt-BR-FranciscaNeural"
OUTPUT_FILE = "output.mp3"

TEXTO = "Olá, seja bem vindo!"

# - - - - - - - - - - - - - - - - - - -

#asyncio.run(generate(TEXTO, VOICE_MALE_PTBR))