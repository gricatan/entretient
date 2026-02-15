from mistralai import Mistral
from mistralai.extra.realtime import UnknownRealtimeEvent
from mistralai.models import (
    AudioFormat,
    RealtimeTranscriptionError,
    RealtimeTranscriptionSessionCreated,
    TranscriptionStreamDone,
    TranscriptionStreamTextDelta,
)
from dotenv import load_dotenv

import asyncio
import os, sys
from typing import AsyncIterator

load_dotenv()

API_KEY = os.getenv("MISTRAL_API_KEY")
client = Mistral(api_key=API_KEY)
messages = [
    {
        "role": "system",
        "content": "Tu est un assistant d'entretien tu recoit le contenu de l'entretient et tu doit prompt pour conseiller la marche a suivre",
    },
]
message_len = ""
message_max = 500
output = ""


# microphone is always pcm_s16le here
audio_format = AudioFormat(encoding="pcm_s16le", sample_rate=16000)


async def iter_microphone(
    *,
    sample_rate: int,
    chunk_duration_ms: int,
) -> AsyncIterator[bytes]:
    """
    Yield microphone PCM chunks using PyAudio (16-bit mono).
    Encoding is always pcm_s16le.
    """
    import pyaudio

    p = pyaudio.PyAudio()
    chunk_samples = int(sample_rate * chunk_duration_ms / 1000)

    stream = p.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=sample_rate,
        input=True,
        frames_per_buffer=chunk_samples,
    )

    loop = asyncio.get_running_loop()
    try:
        while True:
            # stream.read is blocking; run it off-thread
            data = await loop.run_in_executor(None, stream.read, chunk_samples, False)
            yield data
    finally:
        stream.stop_stream()
        stream.close()
        p.terminate()


audio_stream = iter_microphone(
    sample_rate=audio_format.sample_rate, chunk_duration_ms=480
)


async def main():
    global output
    global messages
    global message_len

    try:
        async for event in client.audio.realtime.transcribe_stream(
            audio_stream=audio_stream,
            model="voxtral-mini-transcribe-realtime-2602",
            audio_format=audio_format,
        ):
            if isinstance(event, RealtimeTranscriptionSessionCreated):
                print("Session created... : \033[1m'Dis Bonjoul ô miclo 😉 !'\033[0m")

            elif isinstance(event, TranscriptionStreamTextDelta):
                print(event.text, end="", flush=True)
                message_len = message_len + event.text

                if len(message_len) > message_max:
                    messages.append(
                        {
                            "role": "user",
                            "content": message_len,
                        }
                    )

                    message_len = ""  # reset

                    model_chat = "mistral-large-latest"
                    response = await client.chat.stream_async(
                        model=model_chat, messages=messages
                    )

                    async for chunk in response:
                        if chunk.data.choices[0].delta.content is not None:
                            print(chunk.data.choices[0].delta.content, end="")
                            output += chunk.data.choices[0].delta.content

            elif isinstance(event, TranscriptionStreamDone):
                print("Transcription done.")

            elif isinstance(event, RealtimeTranscriptionError):
                print(f"Error: {event}")

            elif isinstance(event, UnknownRealtimeEvent):
                print(f"Unknown event: {event}")
                continue

    except KeyboardInterrupt:
        print("Stopping...")


sys.exit(asyncio.run(main()))
