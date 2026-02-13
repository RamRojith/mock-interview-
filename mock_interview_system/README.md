# Mock Interview AI System

This is a Django-based mock interview application that uses:
- **Whisper** for Speech-to-Text.
- **Ollama (Llama-3)** for Interview Logic.
- **Cocoqui TTS** (placeholder) for Voice Output.

## Prerequisites

1.  **Python 3.10+** (Installed)
2.  **FFmpeg**: Required for audio processing.
    *   **Windows**: Download from [gyan.dev](https://www.gyan.dev/ffmpeg/builds/), extract, and add `bin` folder to System PATH.
    *   *Note: The app will fail to transcribe audio without this.*
3.  **Ollama**: Required for AI logic.
    *   Download from [ollama.com](https://ollama.com).
    *   Run: `ollama pull llama3` (or `mistral`).

## Setup

1.  **Activate Virtual Environment** (if applicable).
2.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
    *(Note: Dependencies are already installed in this environment)*

3.  **Database Migration** (Already done):
    ```bash
    python manage.py migrate
    ```

## Running the Application

1.  Start the server:
    ```bash
    cd mock_interview_system
    python manage.py runserver
    ```
2.  Open your browser to: `http://127.0.0.1:8000/`
3.  Enter a topic (e.g., "Java Developer") and click **Start Session**.
4.  Allow microphone access when prompted.

## Troubleshooting

-   **"Error transcribing"**: Ensure FFmpeg is installed and in your PATH. Restart terminal after installing.
-   **"Unable to generate feedback"**: Ensure Ollama is running (`ollama serve`) and you have pulled the model (`ollama pull llama3`).
