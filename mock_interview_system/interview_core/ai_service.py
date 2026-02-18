import whisper
import ollama
import json
import os
import uuid
import asyncio
import edge_tts
from django.conf import settings
from asgiref.sync import async_to_sync

class AIService:
    def __init__(self):
        self._whisper_model = None  # Lazy load

    @property
    def whisper_model(self):
        if self._whisper_model is None:
            print("Loading Whisper model...")
            try:
                self._whisper_model = whisper.load_model("base")
            except Exception as e:
                print(f"Error loading Whisper: {e}")
                self._whisper_model = None
        return self._whisper_model

    def transcribe_audio(self, file_path):
        if not self.whisper_model:
            return "Error: Whisper model not loaded."
        try:
            result = self.whisper_model.transcribe(file_path)
            return result["text"]
        except Exception as e:
            return f"Error transcribing: {str(e)}"

    def generate_response(self, transcript, history, topic):
        """
        Sends transcript and history to Ollama to get feedback and next question.
        Returns JSON: { "feedback": str, "score": int, "next_question": str }
        """
        system_prompt = (
            f"You are a mock interviewer for a fresher applying to a top MNC. "
            f"The topic is: {topic}. "
            "Analyze the candidate's answer based on the previous question. "
            "Provide constructive, professional feedback, a score (1-10), and the next relevant interview question. "
            "Keep the next question concise. "
            "Return ONLY JSON in this format: "
            '{"feedback": "...", "score": 8, "next_question": "..."}'
        )
        
        messages = [{'role': 'system', 'content': system_prompt}]
        for turn in history[-5:]:
            messages.append({'role': 'assistant', 'content': f"Question: {turn['question']}"}) # Fix: AI asks question
            messages.append({'role': 'user', 'content': f"Answer: {turn['answer']}"}) # Fix: User answers
        
        # Current turn
        messages.append({'role': 'user', 'content': f"Candidate Answer: {transcript}"})

        try:
            response = ollama.chat(model='llama3', messages=messages, format='json')
            content = response['message']['content']
            return json.loads(content)
        except Exception as e:
            print(f"Ollama error: {e}")
            return {
                "feedback": "I couldn't process that response correctly. Let's continue.",
                "score": 5,
                "next_question": "Could you tell me more about your technical skills?"
            }

    async def _generate_tts_async(self, text, output_path):
        """Async helper for Edge-TTS"""
        communicate = edge_tts.Communicate(text, "en-US-AriaNeural") # High quality voice
        await communicate.save(output_path)

    def text_to_speech(self, text, output_filename=None):
        """
        Converts text to speech using Edge-TTS (online, free, high quality).
        """
        if not text or not str(text).strip():
            return None

        # Sanitize and prepare path
        safe_name = f"tts_{uuid.uuid4().hex}"
        if output_filename:
            safe_name = os.path.basename(output_filename).replace(" ", "_")
        
        output_dir = os.path.join(settings.MEDIA_ROOT, "tts")
        os.makedirs(output_dir, exist_ok=True)
        
        filename = f"{safe_name}.mp3"
        file_path = os.path.join(output_dir, filename)

        try:
            # Run async function in sync context
            async_to_sync(self._generate_tts_async)(text, file_path)
            
            # Return URL
            media_url = f"{settings.MEDIA_URL.rstrip('/')}/tts/{filename}"
            return media_url
        except Exception as e:
            print(f"Edge-TTS error: {e}")
            return None


# Singleton instance shared across the app to avoid reloading heavy models.
ai_service = AIService()
