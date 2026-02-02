# Voice Assistant AI

A real-time voice assistant web application built with **FastAPI**, **OpenAI Whisper**, **ChatGPT**, and **gTTS**.

## 🚀 Quick Start

1. **Clone the repository:**

    ```bash
    git clone <repository-url>
    cd voice_assistant
    ```

2. **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

3. **Configure Environment:**
    Create a `.env` file in the root directory and add your OpenAI API Key:

    ```env
    OPENAI_API_KEY=your-secret-api-key-here
    ```

4. **Run the Server:**

    ```bash
    python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
    ```

5. **Use the Assistant:**
    Open [http://localhost:8000](http://localhost:8000) in your browser.

## ✨ Features

- **Real-time Audio Capture**: Uses browser `MediaRecorder` API.
- **WebSocket Streaming**: Streams audio chunks to the backend efficiently.
- **Speech-to-Text (STT)**: Transcribes audio using **OpenAI Whisper**.
- **Intelligence**: Generates responses using **ChatGPT (GPT-3.5/4)**.
- **Text-to-Speech (TTS)**: Converts responses to audio using **Google Text-to-Speech (gTTS)**.
- **Simple UI**: Clean, minimal interface for voice interaction.

## 🛠️ Configuration

| Variable | Description |
|----------|-------------|
| `OPENAI_API_KEY` | **Required.** Your OpenAI API Key for Whisper and ChatGPT. |

## 📦 Project Structure

```
voice_assistant/
├── main.py              # FastAPI application & WebSocket logic
├── requirements.txt     # Python dependencies
├── .env                 # Environment variables (API Keys)
├── services/            # Backend logic modules
│   ├── audio_manager.py # Temporary file management
│   ├── openai_client.py # Wrapper for OpenAI API
│   └── tts_engine.py    # Wrapper for gTTS
└── static/              # Frontend assets
    ├── index.html       # User Interface
    └── js/
        └── app.js       # Frontend logic (Recorder & WebSocket)
```

## 🔒 Security Note

This project uses your OpenAI API Key. **Never commit your `.env` file to a public repository.** A `.gitignore` file is included to prevent this.

## License

MIT
