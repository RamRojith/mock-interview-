import whisper
import ollama
import json
import os
import uuid
import asyncio
import edge_tts
from django.conf import settings
from asgiref.sync import async_to_sync
from datetime import datetime

class AIService:
    def __init__(self):
        self._whisper_model = None  # Lazy load
        self._ollama_available = None  # Cache Ollama availability

    @property
    def whisper_model(self):
        if self._whisper_model is None:
            print("Loading Whisper model...")
            try:
                self._whisper_model = whisper.load_model("base")
                print("Whisper model loaded successfully")
            except Exception as e:
                print(f"Error loading Whisper: {e}")
                self._whisper_model = None
        return self._whisper_model
    
    def check_ollama_availability(self):
        """Check if Ollama service is running"""
        if self._ollama_available is not None:
            return self._ollama_available
        
        try:
            # Try a simple list command to check if Ollama is running
            ollama.list()
            self._ollama_available = True
            print("Ollama service is available")
            return True
        except Exception as e:
            print(f"Ollama service not available: {e}")
            self._ollama_available = False
            return False

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
        # Check if Ollama is available
        if not self.check_ollama_availability():
            print("Ollama not available, using fallback response")
            return self._generate_fallback_response(transcript, history, topic)
        
        system_prompt = (
            f"You are a professional AI Mock Interviewer for a fresher applying to a top MNC. "
            f"The interview topic is: {topic}. "
            "Your role is to:\n"
            "1. Analyze the candidate's answer professionally\n"
            "2. Provide constructive, encouraging feedback\n"
            "3. Give a score from 1-10 based on relevance, clarity, and confidence\n"
            "4. Ask the next relevant interview question\n\n"
            "Be supportive but honest. Focus on helping the candidate improve.\n"
            "Return ONLY valid JSON in this exact format:\n"
            '{"feedback": "Your detailed feedback here", "score": 8, "next_question": "Your next question here"}'
        )
        
        messages = [{'role': 'system', 'content': system_prompt}]
        for turn in history[-5:]:
            messages.append({'role': 'assistant', 'content': f"Question: {turn['question']}"})
            messages.append({'role': 'user', 'content': f"Answer: {turn['answer']}"})
        
        # Current turn
        messages.append({'role': 'user', 'content': f"Candidate Answer: {transcript}"})

        try:
            response = ollama.chat(model='llama3', messages=messages, format='json')
            content = response['message']['content']
            return json.loads(content)
        except Exception as e:
            print(f"Ollama error: {e}")
            # Reset availability flag to recheck next time
            self._ollama_available = None
            return self._generate_fallback_response(transcript, history, topic)
    
    def _generate_fallback_response(self, transcript, history, topic):
        """Generate a basic response when Ollama is not available"""
        question_count = len(history) + 1
        
        # Basic question templates based on topic
        common_questions = [
            f"Can you explain your experience with {topic}?",
            f"What are the key skills required for {topic}?",
            f"Tell me about a challenging project related to {topic}.",
            "What are your strengths and weaknesses?",
            "Where do you see yourself in 5 years?",
            "Why should we hire you?",
            "Do you have any questions for us?"
        ]
        
        next_question = common_questions[min(question_count, len(common_questions) - 1)]
        
        return {
            "feedback": "Thank you for your response. Your answer shows good understanding. Keep practicing to improve your confidence and clarity.",
            "score": 7,
            "next_question": next_question
        }

    def generate_comprehensive_report(self, session_data):
        """
        Generate a comprehensive interview evaluation report.
        
        Args:
            session_data: {
                'student_name': str,
                'topic': str,
                'interview_type': str (HR/Technical/General),
                'responses': [
                    {
                        'question': str,
                        'answer': str,
                        'score': int,
                        'feedback': str,
                        'time_taken': int (seconds)
                    }
                ]
            }
        
        Returns:
            dict with comprehensive evaluation
        """
        
        # Check if Ollama is available
        if not self.check_ollama_availability():
            print("Ollama not available, using fallback report")
            return self._generate_fallback_report(session_data)
        
        system_prompt = """You are a professional AI Interview Evaluator and Communication Coach.

Your task is to analyze a complete mock interview and generate a detailed evaluation report.

You must provide THREE independent analyses:

1. INTERVIEW PERFORMANCE ANALYSIS
   - Evaluate relevance, clarity, confidence, structure, and professionalism
   - Identify strengths and weaknesses
   - Provide actionable improvement tips

2. GRAMMAR & LANGUAGE SKILLS ANALYSIS
   - Analyze grammar accuracy, sentence structure, vocabulary quality
   - Identify repeated words, filler words, common mistakes
   - Provide grammar score (0-10) and vocabulary level
   - Give specific improvement suggestions

3. OVERALL EVALUATION
   - Calculate interview skills score (0-10)
   - Calculate grammar skills score (0-10)
   - Calculate confidence score (0-10)
   - Provide overall score (average)
   - Give final verdict and interview readiness level
   - Provide improvement roadmap

Return ONLY valid JSON in this exact format:
{
    "interview_performance": {
        "strengths": ["strength 1", "strength 2", "strength 3"],
        "weaknesses": ["weakness 1", "weakness 2"],
        "improvement_tips": ["tip 1", "tip 2", "tip 3"]
    },
    "grammar_analysis": {
        "grammar_score": 8,
        "vocabulary_level": "Intermediate",
        "common_issues": ["issue 1", "issue 2"],
        "improvement_suggestions": ["suggestion 1", "suggestion 2"]
    },
    "overall_evaluation": {
        "interview_skills_score": 7,
        "grammar_skills_score": 8,
        "confidence_score": 7,
        "overall_score": 7.3,
        "final_verdict": "Your detailed verdict here",
        "readiness_level": "Interview Ready / Needs Practice / Needs Significant Improvement",
        "improvement_roadmap": ["step 1", "step 2", "step 3"]
    }
}

Be professional, supportive, and provide actionable feedback. Never discourage the student."""

        # Prepare interview data for analysis
        interview_summary = f"Interview Topic: {session_data.get('topic', 'General')}\n"
        interview_summary += f"Interview Type: {session_data.get('interview_type', 'General')}\n\n"
        interview_summary += "Questions and Answers:\n\n"
        
        for idx, response in enumerate(session_data.get('responses', []), 1):
            interview_summary += f"Q{idx}: {response.get('question', '')}\n"
            interview_summary += f"A{idx}: {response.get('answer', '')}\n"
            interview_summary += f"Score: {response.get('score', 0)}/10\n"
            interview_summary += f"Feedback: {response.get('feedback', '')}\n\n"

        messages = [
            {'role': 'system', 'content': system_prompt},
            {'role': 'user', 'content': f"Please analyze this interview and provide a comprehensive evaluation:\n\n{interview_summary}"}
        ]

        try:
            response = ollama.chat(model='llama3', messages=messages, format='json')
            content = response['message']['content']
            evaluation = json.loads(content)
            
            # Add metadata
            evaluation['metadata'] = {
                'student_name': session_data.get('student_name', 'Student'),
                'topic': session_data.get('topic', 'General'),
                'interview_type': session_data.get('interview_type', 'General'),
                'date': datetime.now().strftime('%B %d, %Y'),
                'total_questions': len(session_data.get('responses', [])),
                'average_score': sum(r.get('score', 0) for r in session_data.get('responses', [])) / max(len(session_data.get('responses', [])), 1)
            }
            
            return evaluation
            
        except Exception as e:
            print(f"Report generation error: {e}")
            # Reset availability flag to recheck next time
            self._ollama_available = None
            # Return fallback report
            return self._generate_fallback_report(session_data)

    def _generate_fallback_report(self, session_data):
        """Generate a basic report if AI fails"""
        responses = session_data.get('responses', [])
        avg_score = sum(r.get('score', 0) for r in responses) / max(len(responses), 1)
        
        return {
            "interview_performance": {
                "strengths": ["Completed the interview", "Provided answers to all questions"],
                "weaknesses": ["Could improve answer clarity", "Could provide more detailed responses"],
                "improvement_tips": ["Practice common interview questions", "Structure your answers using STAR method", "Speak clearly and confidently"]
            },
            "grammar_analysis": {
                "grammar_score": 7,
                "vocabulary_level": "Intermediate",
                "common_issues": ["Minor grammatical errors", "Could use more professional vocabulary"],
                "improvement_suggestions": ["Read professional articles", "Practice speaking in English daily"]
            },
            "overall_evaluation": {
                "interview_skills_score": round(avg_score),
                "grammar_skills_score": 7,
                "confidence_score": 6,
                "overall_score": round((avg_score + 7 + 6) / 3, 1),
                "final_verdict": "You have completed the mock interview. Continue practicing to improve your confidence and communication skills.",
                "readiness_level": "Needs Practice",
                "improvement_roadmap": ["Practice more mock interviews", "Work on communication skills", "Research common interview questions"]
            },
            "metadata": {
                'student_name': session_data.get('student_name', 'Student'),
                'topic': session_data.get('topic', 'General'),
                'interview_type': session_data.get('interview_type', 'General'),
                'date': datetime.now().strftime('%B %d, %Y'),
                'total_questions': len(responses),
                'average_score': round(avg_score, 1)
            }
        }

    async def _generate_tts_async(self, text, output_path):
        """Async helper for Edge-TTS"""
        communicate = edge_tts.Communicate(text, "en-US-AriaNeural")
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
