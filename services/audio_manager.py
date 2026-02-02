import os
import uuid
import aiofiles

AUDIO_DIR = "temp_audio"

if not os.path.exists(AUDIO_DIR):
    os.makedirs(AUDIO_DIR)

class AudioManager:
    @staticmethod
    def get_temp_file_path(extension=".wav") -> str:
        filename = f"{uuid.uuid4()}{extension}"
        return os.path.join(AUDIO_DIR, filename)

    @staticmethod
    async def save_chunk(file_path: str, chunk: bytes):
        """Appends a byte chunk to a file."""
        async with aiofiles.open(file_path, "ab") as f:
            await f.write(chunk)
            
    @staticmethod
    def delete_file(file_path: str):
        if os.path.exists(file_path):
            os.remove(file_path)
