from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.views import APIView
from rest_framework.response import Response as APIResponse
from rest_framework import status, parsers
from .models import InterviewSession, Response, Question
from .serializers import InterviewSessionSerializer, ResponseSerializer
from .ai_service import ai_service
import os
from django.conf import settings

def landing_view(request):
    return render(request, 'interview_core/landing.html')

def mic_test_view(request):
    return render(request, 'interview_core/mic_test.html')

def index_view(request):
    return render(request, 'interview_core/index.html')

def interview_report_view(request, session_id):
    """Generate and display comprehensive interview report"""
    session = get_object_or_404(InterviewSession, id=session_id)
    
    # Gather all responses for this session
    responses = Response.objects.filter(session=session).order_by('created_at')
    
    # Prepare data for report generation
    session_data = {
        'student_name': 'Student',  # Can be extended with user model
        'topic': session.topic,
        'interview_type': 'General',  # Can be extended
        'responses': [
            {
                'question': resp.question.text,
                'answer': resp.transcription,
                'score': resp.score,
                'feedback': resp.ai_feedback,
                'time_taken': 0  # Can be tracked if needed
            }
            for resp in responses
        ]
    }
    
    # Generate comprehensive report using AI
    report = ai_service.generate_comprehensive_report(session_data)
    
    context = {
        'session': session,
        'report': report,
        'responses': responses
    }
    
    return render(request, 'interview_core/report.html', context)

def interview_view(request, session_id):
    session = get_object_or_404(InterviewSession, id=session_id)
    
    # Get the latest question for this session to display initially
    latest_question = Question.objects.filter(topic=session.topic).last()
    
    context = {
        'session_id': session.id, 
        'topic': session.topic,
        'initial_question': latest_question.text if latest_question else "Waiting for first question...",
        'initial_audio_url': None
    }
    
    # If there is a question, try to ensure audio exists
    if latest_question:
        # We can try to generate/get the audio URL here. 
        # For simplicity, we'll generate it if it doesn't exist, or just return the path if we had a standard naming convention.
        # Let's generate it to be safe and simple for now.
        audio_url = ai_service.text_to_speech(latest_question.text, output_filename=f"question_{latest_question.id}.mp3")
        context['initial_audio_url'] = audio_url

    return render(request, 'interview_core/interview.html', context)


@method_decorator(csrf_exempt, name='dispatch')
class StartSessionView(APIView):
    def post(self, request):
        serializer = InterviewSessionSerializer(data=request.data)
        if serializer.is_valid():
            session = serializer.save()
            # Generate first question
            initial_question_text = "Tell me about yourself and your background."
            # Check if this question already exists for the topic to avoid duplicates or just create new
            question = Question.objects.create(text=initial_question_text, topic=session.topic, difficulty='easy')
            
            # Generate audio for first question
            audio_url = ai_service.text_to_speech(initial_question_text, output_filename=f"question_{question.id}.mp3") 
            
            return APIResponse({
                "session_id": session.id,
                "message": "Interview started",
                "first_question": initial_question_text,
                "audio_url": audio_url
            }, status=status.HTTP_201_CREATED)
        return APIResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@method_decorator(csrf_exempt, name='dispatch')
class ProcessResponseView(APIView):
    parser_classes = [parsers.MultiPartParser, parsers.FormParser]

    def post(self, request):
        session_id = request.data.get('session_id')
        if not session_id:
            return APIResponse({"error": "Session ID required"}, status=status.HTTP_400_BAD_REQUEST)
        
        session = get_object_or_404(InterviewSession, id=session_id)
        
        # Save Student Response
        # We need a question to link response to. For MVP, we presume the last question.
        # But here we just create a dummy question link or find the last asked question.
        # Ideally, frontend sends question_id too. Let's assume frontend sends question_id.
        question_id = request.data.get('question_id')
        question = get_object_or_404(Question, id=question_id) if question_id else None

        # If no question_id provided, create a placeholder or get latest
        if not question:
            question = Question.objects.filter(topic=session.topic).last()
        
        # Save Audio
        audio_file = request.FILES.get('audio_file')
        if not audio_file:
             return APIResponse({"error": "Audio file required"}, status=status.HTTP_400_BAD_REQUEST)

        response_obj = Response.objects.create(
            session=session,
            question=question,
            audio_file=audio_file
        )

        # 1. Transcribe
        transcript = ai_service.transcribe_audio(response_obj.audio_file.path)
        response_obj.transcription = transcript
        response_obj.save()

        # 2. Analyze & Generate Next Question
        # Build history
        history = []
        previous_responses = Response.objects.filter(session=session).order_by('created_at')
        for resp in previous_responses:
            history.append({
                "question": resp.question.text,
                "answer": resp.transcription
            })

        ai_result = ai_service.generate_response(transcript, history, session.topic)
        
        # Update current response with feedback
        response_obj.ai_feedback = ai_result.get('feedback', '')
        response_obj.score = ai_result.get('score', 0)
        response_obj.save()

        # Create Next Question
        next_q_text = ai_result.get('next_question', "Thank you. Let's move on.")
        next_question = Question.objects.create(text=next_q_text, topic=session.topic, difficulty='medium')

        # 3. TTS for Next Question
        audio_url = ai_service.text_to_speech(next_q_text, output_filename=f"question_{next_question.id}.mp3")
        
        return APIResponse({
            "feedback": response_obj.ai_feedback,
            "score": response_obj.score,
            "next_question": {
                "id": next_question.id,
                "text": next_question.text
            },
            "audio_url": audio_url
        }, status=status.HTTP_200_OK)
