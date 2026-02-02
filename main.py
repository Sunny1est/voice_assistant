from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os
from services.audio_manager import AudioManager
from services.openai_client import OpenAIService
from services.tts_engine import TTSService

app = FastAPI()

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def get():
    return FileResponse("static/index.html")

@app.websocket("/ws/audio")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    
    # Create a unique temp file for this session
    audio_file_path = AudioManager.get_temp_file_path(".webm") # Browser sends webm/opus usually
    
    try:
        while True:
            # Receive data chunk
            data = await websocket.receive_bytes()
            
            # Application protocol: sending specific byte sequence to signal end of stream?
            # Or simplified: Client sends a text message "END" to finish recording.
            # But receive_bytes() waits for bytes. 
            # Let's handle mixed types or assume client sends special 0-byte or control frame if simple.
            # actually better: client sends "END" string, server handles it.
            # But we are in receive_bytes loop.
            
            # Strategy: We need to handle both binary (audio) and text (control) messages.
            # receive() returns a dict with type.
            
            # Let's simple check: if bytes are small and match a magic sequence? No, unreliable.
            # Use `receive` generic method.
            pass 
            
    except WebSocketDisconnect:
        print("Client disconnected")
    finally:
        # Cleanup if needed
        pass

# Redefining the endpoint with proper logic
@app.websocket("/ws/audio_stream")
async def audio_stream(websocket: WebSocket):
    await websocket.accept()
    audio_file_path = AudioManager.get_temp_file_path(".webm")
    
    try:
        while True:
            message = await websocket.receive()
            
            if "bytes" in message and message["bytes"]:
                # Append audio chunk
                await AudioManager.save_chunk(audio_file_path, message["bytes"])
                
            elif "text" in message and message["text"] == "END":
                # End of recording signal
                await websocket.send_text("Processing...")
                
                # 1. Transcribe
                print(f"Transcribing {audio_file_path}...")
                transcript = await OpenAIService.transcribe_audio(audio_file_path)
                await websocket.send_text(f"You said: {transcript}")
                
                if not transcript:
                    await websocket.send_text("Could not understand audio.")
                    continue
                
                # 2. Get ChatGPT Response
                print(f"Asking ChatGPT: {transcript}")
                gpt_response = await OpenAIService.get_chat_response(transcript)
                await websocket.send_text(f"GPT: {gpt_response}")
                
                # 3. Generate Audio Response
                print(f"Generating TTS...")
                audio_url = TTSService.text_to_speech(gpt_response)
                
                # Send back the URL to play
                await websocket.send_json({"type": "audio_response", "url": audio_url})
                
                # Allow new recording? Reset file path?
                # For this simple demo, we can just close or let loop continue.
                # Let's cleanup the old file and start fresh for next turn if needed.
                AudioManager.delete_file(audio_file_path)
                audio_file_path = AudioManager.get_temp_file_path(".webm")
                
    except WebSocketDisconnect:
        print("Client disconnected")
        AudioManager.delete_file(audio_file_path)
    except Exception as e:
        print(f"Error: {e}")
        await websocket.close()
        AudioManager.delete_file(audio_file_path)
