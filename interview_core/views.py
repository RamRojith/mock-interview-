from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http import JsonResponse
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
        'initial_question_id': latest_question.id if latest_question else None,
        'initial_audio_url': None
    }
    
    # If there is a question, try to ensure audio exists
    if latest_question:
        # Generate audio for the question
        audio_url = ai_service.text_to_speech(latest_question.text, output_filename=f"question_{latest_question.id}.mp3")
        context['initial_audio_url'] = audio_url

    return render(request, 'interview_core/interview.html', context)


def health_check_view(request):
    """Check the health status of all required services"""
    health_status = {
        'ollama': False,
        'whisper': False,
        'edge_tts': True,  # Assume available (online service)
        'overall': False
    }
    
    # Check Ollama
    health_status['ollama'] = ai_service.check_ollama_availability()
    
    # Check Whisper
    try:
        model = ai_service.whisper_model
        health_status['whisper'] = model is not None
    except:
        health_status['whisper'] = False
    
    # Overall status
    health_status['overall'] = health_status['ollama'] and health_status['whisper']
    
    return JsonResponse({
        'status': 'healthy' if health_status['overall'] else 'degraded',
        'services': health_status,
        'message': 'All services operational' if health_status['overall'] else 'Some services unavailable - using fallback mode'
    })


@method_decorator(csrf_exempt, name='dispatch')
class StartSessionView(APIView):
    def post(self, request):
        serializer = InterviewSessionSerializer(data=request.data)
        if serializer.is_valid():
            session = serializer.save()
            
            # Generate highly specific opening question based on role
            topic = session.topic
            topic_lower = topic.lower()
            
            # Comprehensive role-based opening questions
            if "python" in topic_lower:
                initial_question_text = f"Good morning! Thank you for joining us today for the {session.topic} position. Let's start with - tell me about yourself, your background in Python programming, and what specifically interests you about this role?"
            
            elif "java" in topic_lower:
                initial_question_text = f"Hello! Welcome to the interview for the {session.topic} position. To begin, could you tell me about yourself, your experience with Java development, and why you're interested in this opportunity?"
            
            elif "javascript" in topic_lower or "js developer" in topic_lower:
                initial_question_text = f"Good morning! Thanks for being here for the {session.topic} interview. Let's start - tell me about yourself, your JavaScript experience, and what excites you about this role?"
            
            elif any(kw in topic_lower for kw in ['data scientist', 'data analyst', 'machine learning', 'ml engineer']):
                initial_question_text = f"Hello! Welcome to the {session.topic} interview. Let's begin with you telling me about your background, your experience with data analysis or machine learning, and what draws you to this field?"
            
            elif any(kw in topic_lower for kw in ['web developer', 'frontend', 'backend', 'fullstack', 'full stack']):
                initial_question_text = f"Good morning! Thank you for coming in for the {session.topic} position. Tell me about yourself, your web development experience, and what aspects of web development you're most passionate about?"
            
            elif any(kw in topic_lower for kw in ['devops', 'cloud engineer', 'aws', 'azure', 'kubernetes']):
                initial_question_text = f"Hello! Welcome to the {session.topic} interview. Let's start with you introducing yourself, your experience with DevOps or cloud technologies, and why you're interested in this role?"
            
            elif any(kw in topic_lower for kw in ['qa', 'quality assurance', 'test engineer', 'sdet']):
                initial_question_text = f"Good morning! Thanks for joining us for the {session.topic} position. Tell me about yourself, your testing experience, and what interests you about quality assurance?"
            
            elif any(kw in topic_lower for kw in ['mobile developer', 'android', 'ios', 'flutter', 'react native']):
                initial_question_text = f"Hello! Welcome to the {session.topic} interview. Let's begin - tell me about yourself, your mobile development experience, and what excites you about building mobile applications?"
            
            elif any(kw in topic_lower for kw in ['database', 'dba', 'sql', 'mongodb', 'postgresql']):
                initial_question_text = f"Good morning! Thank you for coming in for the {session.topic} position. Tell me about yourself, your database experience, and what interests you about database administration or engineering?"
            
            elif any(kw in topic_lower for kw in ['security', 'cybersecurity', 'infosec', 'penetration tester']):
                initial_question_text = f"Hello! Welcome to the {session.topic} interview. Let's start with you telling me about your background, your interest in cybersecurity, and what specific areas of security you're most passionate about?"
            
            elif any(kw in topic_lower for kw in ['ui', 'ux', 'designer', 'product designer']):
                initial_question_text = f"Good morning! Thanks for being here for the {session.topic} position. Tell me about yourself, your design background, and what aspects of UI/UX design you find most interesting?"
            
            elif any(kw in topic_lower for kw in ['project manager', 'scrum master', 'product manager', 'program manager']):
                initial_question_text = f"Hello! Welcome to the {session.topic} interview. Let's begin with you introducing yourself, your project management experience, and what draws you to this leadership role?"
            
            elif any(kw in topic_lower for kw in ['business analyst', 'ba', 'systems analyst']):
                initial_question_text = f"Good morning! Thank you for joining us for the {session.topic} position. Tell me about yourself, your experience in business analysis, and what interests you about this role?"
            
            elif any(kw in topic_lower for kw in ['network engineer', 'network admin', 'cisco', 'ccna']):
                initial_question_text = f"Hello! Welcome to the {session.topic} interview. Let's start - tell me about yourself, your networking experience, and what aspects of network engineering you're most interested in?"
            
            elif any(kw in topic_lower for kw in ['software engineer', 'software developer', 'programmer', 'developer']):
                initial_question_text = f"Good morning! Thank you for coming in for the {session.topic} position. Tell me about yourself, your software development experience, and what specifically interests you about this opportunity?"
            
            else:
                # Generic but professional opening
                initial_question_text = f"Good morning! Thank you for joining us today for the {session.topic} position. Let's start with - tell me about yourself, your relevant background and experience, and why you're interested in this role?"
            
            # Create first question
            question = Question.objects.create(
                text=initial_question_text, 
                topic=session.topic, 
                difficulty='easy'
            )
            
            # Generate audio for first question
            audio_url = ai_service.text_to_speech(initial_question_text, output_filename=f"question_{question.id}.mp3") 
            
            return APIResponse({
                "session_id": session.id,
                "message": "Interview started",
                "first_question": initial_question_text,
                "question_id": question.id,
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
        
        # Get the current question being answered
        question_id = request.data.get('question_id')
        question = get_object_or_404(Question, id=question_id) if question_id else None

        # If no question_id provided, get the latest question for this topic
        if not question:
            question = Question.objects.filter(topic=session.topic).last()
            if not question:
                return APIResponse({"error": "No question found"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Save Audio
        audio_file = request.FILES.get('audio_file')
        if not audio_file:
             return APIResponse({"error": "Audio file required"}, status=status.HTTP_400_BAD_REQUEST)

        response_obj = Response.objects.create(
            session=session,
            question=question,
            audio_file=audio_file
        )

        # 1. Transcribe the audio
        transcript = ai_service.transcribe_audio(response_obj.audio_file.path)
        response_obj.transcription = transcript
        response_obj.save()

        # 2. Build conversation history for context
        history = []
        previous_responses = Response.objects.filter(session=session).order_by('created_at')
        for resp in previous_responses:
            history.append({
                "question": resp.question.text,
                "answer": resp.transcription,
                "score": resp.score,
                "feedback": resp.ai_feedback
            })

        # 3. Get AI evaluation and next question
        ai_result = ai_service.generate_response(transcript, history, session.topic)
        
        # Update current response with feedback
        response_obj.ai_feedback = ai_result.get('feedback', 'Thank you for your response.')
        response_obj.score = ai_result.get('score', 7)
        response_obj.save()

        # 4. Create next question
        next_q_text = ai_result.get('next_question', "Thank you for your time. That concludes our interview.")
        
        # Check if interview should end (after 10-12 questions for comprehensive interview)
        total_questions = Question.objects.filter(topic=session.topic).count()
        
        if total_questions >= 12 or "concludes" in next_q_text.lower() or "thank you for your time" in next_q_text.lower():
            # Interview is complete
            return APIResponse({
                "feedback": response_obj.ai_feedback,
                "score": response_obj.score,
                "next_question": None,
                "audio_url": None,
                "interview_complete": True
            }, status=status.HTTP_200_OK)
        
        # Create next question
        next_question = Question.objects.create(
            text=next_q_text, 
            topic=session.topic, 
            difficulty='medium'
        )

        # 5. Generate TTS for next question
        audio_url = ai_service.text_to_speech(next_q_text, output_filename=f"question_{next_question.id}.mp3")
        
        return APIResponse({
            "feedback": response_obj.ai_feedback,
            "score": response_obj.score,
            "next_question": {
                "id": next_question.id,
                "text": next_question.text
            },
            "audio_url": audio_url,
            "interview_complete": False
        }, status=status.HTTP_200_OK)
