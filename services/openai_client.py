import os
import openai
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

class OpenAIService:
    @staticmethod
    async def transcribe_audio(file_path: str) -> str:
        """Transcribes audio using OpenAI Whisper model."""
        try:
            with open(file_path, "rb") as audio_file:
                transcript = await openai.Audio.atranscribe(
                    model="whisper-1",
                    file=audio_file
                )
            return transcript["text"]
        except Exception as e:
            print(f"Error in transcription: {e}")
            return ""

    @staticmethod
    async def get_chat_response(text: str) -> str:
        """Sends text to ChatGPT and returns the response."""
        try:
            response = await openai.ChatCompletion.acreate(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful voice assistant. Keep your answers concise and conversational."},
                    {"role": "user", "content": text}
                ]
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error in ChatGPT response: {e}")
            return "Thinking failed, sorry."
