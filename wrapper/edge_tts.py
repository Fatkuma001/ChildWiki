import asyncio
import uuid
from typing import Optional

from edge_tts import Communicate


class TextToSpeechConverter:
    # Get all available voices from https://github.com/rany2/edge-tts
    DEFAULT_VOICE = "zh-CN-XiaoxiaoNeural"
    OUTPUT_FILE_FORMAT = "/tmp/{}.mp3"

    def __init__(self, voice: Optional[str] = None):
        self.voice = voice or self.DEFAULT_VOICE

    async def synthesize(self, text: str, output_file: str) -> None:
        """Synthesize text to speech and save to an output file."""
        communicate = Communicate(text, self.voice)
        await communicate.save(output_file)

    def convert(self, text: str) -> str:
        """Convert text to speech and return the output file path."""
        audio_file = self.OUTPUT_FILE_FORMAT.format(uuid.uuid4())
        asyncio.run(self.synthesize(text, audio_file))
        return audio_file
