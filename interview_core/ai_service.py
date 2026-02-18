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
        
        question_number = len(history) + 1
        
        # Determine role category for specialized evaluation
        role_category = self._determine_role_category(topic)
        
        system_prompt = f"""You are a SENIOR TECHNICAL INTERVIEWER with 15+ years of experience conducting interviews for FRESHER/STUDENT positions at top tech companies.

ROLE CONTEXT: {topic}
ROLE CATEGORY: {role_category}
QUESTION NUMBER: {question_number}
CANDIDATE LEVEL: FRESHER/STUDENT (0-2 years experience)

YOUR MISSION: Conduct a REALISTIC, COMPREHENSIVE interview that evaluates if this FRESHER candidate has potential for growth and learning.

═══════════════════════════════════════════════════════════════

CRITICAL: YOU ARE INTERVIEWING A FRESHER/STUDENT!

- They may not have deep experience - that's OKAY
- Look for POTENTIAL, LEARNING ABILITY, and PASSION
- Ask questions appropriate for their level
- Be encouraging but honest
- Focus on fundamentals, not advanced topics
- Value academic projects and personal learning
- Look for problem-solving ability over perfect answers

═══════════════════════════════════════════════════════════════

PART 1: ANSWER ANALYSIS (Be THOROUGH but FAIR for freshers)

Analyze the candidate's answer on these dimensions:

1. RELEVANCE (Did they answer the question?)
   - Directly addressed the question: Yes/No
   - Stayed on topic: Yes/No
   - Understood what was asked: Yes/No

2. TECHNICAL UNDERSTANDING (For their level)
   - Shows basic understanding: Yes/No/Partial
   - Can explain concepts: Yes/No
   - Admits when they don't know: Yes/No (GOOD!)
   - Willing to learn: Yes/No

3. COMMUNICATION QUALITY
   - Clarity: Clear/Somewhat Clear/Unclear
   - Structure: Organized/Disorganized
   - Confidence: Confident/Hesitant/Unsure
   - Honesty: Honest about limitations (IMPORTANT!)

4. EXAMPLES & EVIDENCE (Academic/Personal projects count!)
   - Provided examples: Yes/No
   - Examples from: Class/Personal/Internship
   - Shows hands-on experience: Yes/No
   - Demonstrates learning: Yes/No

5. LEARNING MINDSET (CRUCIAL for freshers)
   - Shows curiosity: Yes/No
   - Mentions self-learning: Yes/No
   - Acknowledges gaps: Yes/No
   - Wants to improve: Yes/No

═══════════════════════════════════════════════════════════════

PART 2: SCORING (Be REALISTIC but FAIR for freshers)

Score 1-10 based on FRESHER expectations:

**9-10/10 - EXCEPTIONAL FRESHER (Rare)**
- Strong fundamentals for their level
- Multiple relevant examples (class/personal projects)
- Clear communication and confidence
- Shows genuine passion and self-learning
- Would be a top fresher hire

**7-8/10 - STRONG FRESHER**
- Good understanding of basics
- At least one good example/project
- Clear communication
- Shows learning ability
- Would be a good hire

**5-6/10 - AVERAGE FRESHER**
- Basic understanding present
- Some relevant points made
- Could use more examples
- Shows potential with guidance
- Needs mentoring but hireable

**3-4/10 - BELOW AVERAGE**
- Limited understanding
- Vague or incomplete answers
- Few/no examples
- Needs significant development
- May need more preparation

**1-2/10 - NOT READY**
- Very limited knowledge
- Off-topic or confused
- No examples or evidence
- Not ready for this role yet
- Needs more learning time

IMPORTANT FOR FRESHERS:
- Don't expect expert knowledge
- Value learning ability over experience
- Academic projects are valid experience
- Honesty about gaps is GOOD
- Passion and curiosity matter a lot

═══════════════════════════════════════════════════════════════

PART 3: FEEDBACK (Be ENCOURAGING but HONEST)

Structure your feedback for freshers:

1. START POSITIVE (always find something):
   "I appreciate that you [specific thing]..."
   "It's good that you mentioned [specific point]..."

2. IDENTIFY AREAS FOR GROWTH (not "issues"):
   - "To strengthen your answer, consider [specific advice]..."
   - "In future interviews, try to [specific technique]..."
   - "You could improve by [specific action]..."

3. GIVE ACTIONABLE ADVICE:
   - "Practice explaining [concept] in simpler terms"
   - "Work on [specific skill] through [specific resource]"
   - "Try building a project that involves [specific technology]"

4. BE ENCOURAGING:
   - "Keep learning and practicing"
   - "You're on the right track"
   - "With more experience, you'll improve"

═══════════════════════════════════════════════════════════════

PART 4: NEXT QUESTION (COMPREHENSIVE INTERVIEW - Ask 10-12 questions!)

Question Strategy for FRESHERS in {role_category}:

**Question {question_number} Guidelines:**
{self._get_question_guidelines(question_number, role_category, topic)}

INTERVIEW STRUCTURE (10-12 questions total):
1. Introduction & Background
2. Motivation & Interest
3. Technical Fundamentals (easy)
4. Technical Application (medium)
5. Problem-Solving Ability
6. Teamwork & Collaboration (behavioral)
7. Learning & Growth (behavioral)
8. Initiative & Passion (behavioral)
9. Career Goals
10. Strengths & Weaknesses
11. Candidate Questions
12. Closing

ADAPTIVE QUESTIONING FOR FRESHERS:
- If score 7+: Ask slightly deeper question (but still appropriate for freshers)
- If score 4-6: Continue with standard progression
- If score <4: Ask simpler question or different topic
- Always be encouraging and supportive

Make questions:
- Appropriate for FRESHERS/STUDENTS
- Conversational and friendly
- Progressive but not overwhelming
- Based on their level and previous answers
- Include behavioral questions (teamwork, learning, challenges)

═══════════════════════════════════════════════════════════════

RETURN FORMAT (ONLY VALID JSON):

{{
  "feedback": "Your encouraging, specific feedback here (3-5 sentences)",
  "score": X,
  "next_question": "Your natural, conversational question here"
}}

Remember: 
- You are interviewing a FRESHER/STUDENT
- Be thorough - ask 10-12 questions total
- Be encouraging but honest
- Look for POTENTIAL and LEARNING ABILITY
- Value passion and curiosity
- Academic projects count as experience
- Be a mentor, not just an evaluator"""

        messages = [{'role': 'system', 'content': system_prompt}]
        
        # Add conversation history with detailed context
        for idx, turn in enumerate(history[-4:], 1):
            messages.append({'role': 'assistant', 'content': f"Question {idx}: {turn['question']}"})
            messages.append({'role': 'user', 'content': f"Candidate's Answer: {turn['answer']}"})
            if 'feedback' in turn and 'score' in turn:
                messages.append({'role': 'assistant', 'content': f"My Evaluation: Score {turn['score']}/10. {turn['feedback']}"})
        
        # Current turn with emphasis
        current_question = history[-1]['question'] if history else "Tell me about yourself"
        messages.append({
            'role': 'user', 
            'content': f"""CURRENT QUESTION: "{current_question}"

CANDIDATE'S ANSWER: "{transcript}"

WORD COUNT: {len(transcript.split())} words

Now provide your thorough evaluation following ALL the guidelines above. Be specific, honest, and professional."""
        })

        try:
            response = ollama.chat(
                model='llama3', 
                messages=messages, 
                format='json',
                options={
                    'temperature': 0.7,  # Balanced creativity
                    'top_p': 0.9,
                    'num_predict': 500  # Allow longer responses
                }
            )
            content = response['message']['content']
            result = json.loads(content)
            
            # Validate and ensure quality
            if 'score' in result:
                result['score'] = max(1, min(10, int(result['score'])))
            
            if 'feedback' not in result or len(result['feedback']) < 20:
                result['feedback'] = "Your answer needs more detail and specific examples to demonstrate your knowledge."
            
            if 'next_question' not in result or len(result['next_question']) < 10:
                result['next_question'] = self._get_fallback_question(question_number, topic)
            
            return result
        except Exception as e:
            print(f"Ollama error: {e}")
            self._ollama_available = None
            return self._generate_fallback_response(transcript, history, topic)
    
    def _determine_role_category(self, topic):
        """Determine the category of the role for specialized handling"""
        topic_lower = topic.lower()
        
        if any(kw in topic_lower for kw in ['python', 'java', 'c++', 'javascript', 'developer', 'programmer', 'software engineer']):
            return "Software Development"
        elif any(kw in topic_lower for kw in ['data scientist', 'data analyst', 'machine learning', 'ai', 'ml']):
            return "Data Science & Analytics"
        elif any(kw in topic_lower for kw in ['web', 'frontend', 'backend', 'fullstack', 'react', 'angular', 'node']):
            return "Web Development"
        elif any(kw in topic_lower for kw in ['devops', 'cloud', 'aws', 'azure', 'kubernetes', 'docker']):
            return "DevOps & Cloud"
        elif any(kw in topic_lower for kw in ['qa', 'test', 'quality assurance', 'automation']):
            return "Quality Assurance"
        elif any(kw in topic_lower for kw in ['mobile', 'android', 'ios', 'flutter', 'react native']):
            return "Mobile Development"
        elif any(kw in topic_lower for kw in ['database', 'sql', 'dba', 'mongodb', 'postgresql']):
            return "Database Administration"
        elif any(kw in topic_lower for kw in ['security', 'cybersecurity', 'penetration', 'ethical hacking']):
            return "Cybersecurity"
        elif any(kw in topic_lower for kw in ['ui', 'ux', 'design', 'graphic']):
            return "UI/UX Design"
        elif any(kw in topic_lower for kw in ['project manager', 'scrum', 'agile', 'product manager']):
            return "Project Management"
        elif any(kw in topic_lower for kw in ['business analyst', 'ba', 'requirements']):
            return "Business Analysis"
        elif any(kw in topic_lower for kw in ['network', 'cisco', 'routing', 'switching']):
            return "Network Engineering"
        else:
            return "General Technical"
    
    def _get_question_guidelines(self, question_number, role_category, topic):
        """Get specific guidelines for question generation based on interview stage - REAL INTERVIEWER STYLE"""
        
        if question_number == 1:
            return f"""Opening question - Be warm and welcoming like a real interviewer.
Ask: "Tell me about yourself, your educational background, and what specifically interests you about {topic}?"
Make it conversational and friendly to put the candidate at ease."""
        
        elif question_number == 2:
            return f"""Follow-up question - Dig deeper into their motivation.
Ask one of:
- "Why did you choose {role_category} as your career path?"
- "What sparked your interest in {topic}?"
- "What do you hope to achieve in your first year as a {topic}?"
Be genuinely curious about their journey."""
        
        elif question_number == 3:
            # First technical question - Start with fundamentals
            guidelines = {
                "Software Development": f"""First technical question - Start with FUNDAMENTALS appropriate for freshers.
Ask one of:
- "Can you explain what [basic concept] means in {topic}?" (e.g., variables, functions, OOP)
- "What's the difference between [concept A] and [concept B]?" (e.g., list vs array, class vs object)
- "Walk me through how you would approach [simple problem]"
- "Tell me about a programming project you've worked on, even if it was for a class"
Make it accessible for students/freshers. Don't ask advanced questions yet.""",
                
                "Data Science & Analytics": """First technical question - Start with DATA BASICS.
Ask one of:
- "What's the difference between structured and unstructured data?"
- "How would you handle missing values in a dataset?"
- "Explain what data cleaning means and why it's important"
- "Tell me about a data analysis project you've done, even for coursework"
Keep it fundamental - they're students/freshers.""",
                
                "Web Development": """First technical question - Start with WEB FUNDAMENTALS.
Ask one of:
- "Can you explain the difference between HTML, CSS, and JavaScript?"
- "What does responsive design mean to you?"
- "How do you make a website work on both desktop and mobile?"
- "Tell me about a website you've built, even if it was a class project"
Focus on basics - appropriate for freshers.""",
                
                "DevOps & Cloud": """First technical question - Start with BASIC CONCEPTS.
Ask one of:
- "What does DevOps mean to you?"
- "Can you explain what version control is and why it's important?"
- "What's the difference between development and production environments?"
- "Have you used Git? Tell me about your experience"
Keep it simple - they're learning.""",
                
                "Quality Assurance": """First technical question - Start with TESTING BASICS.
Ask one of:
- "What's the difference between manual and automated testing?"
- "Why is testing important in software development?"
- "Can you describe the process of finding and reporting a bug?"
- "Have you done any testing? Tell me about it"
Make it accessible for beginners.""",
                
                "Mobile Development": """First technical question - Start with MOBILE BASICS.
Ask one of:
- "What's the difference between native and cross-platform mobile development?"
- "How do mobile apps differ from websites?"
- "What mobile apps have you built or worked on?"
- "What challenges do you think mobile developers face?"
Keep it fundamental.""",
                
                "Database Administration": """First technical question - Start with DATABASE BASICS.
Ask one of:
- "What is a database and why do we need them?"
- "Can you explain what SQL is?"
- "What's the difference between a table and a database?"
- "Have you worked with any databases? Tell me about it"
Focus on fundamentals.""",
                
                "Cybersecurity": """First technical question - Start with SECURITY BASICS.
Ask one of:
- "What does cybersecurity mean to you?"
- "Can you name some common security threats?"
- "Why is password security important?"
- "What security practices do you follow personally?"
Keep it accessible.""",
                
                "UI/UX Design": """First technical question - Start with DESIGN BASICS.
Ask one of:
- "What's the difference between UI and UX?"
- "What makes a good user interface?"
- "Can you describe your design process?"
- "Show me a design you've created and explain your choices"
Focus on fundamentals.""",
                
                "Project Management": """First technical question - Start with PM BASICS.
Ask one of:
- "What does a project manager do?"
- "Have you ever led a team project? Tell me about it"
- "How do you prioritize tasks when everything seems urgent?"
- "What project management tools have you used?"
Keep it simple.""",
                
                "General Technical": f"""First technical question - Start with FUNDAMENTALS.
Ask about:
- Basic concepts in {topic}
- Their learning journey
- Simple problem-solving
- Academic or personal projects
Make it appropriate for freshers."""
            }
            return guidelines.get(role_category, f"Ask fundamental questions about {topic} suitable for freshers")
        
        elif question_number == 4:
            # Second technical question - Slightly deeper
            guidelines = {
                "Software Development": f"""Second technical question - Go SLIGHTLY DEEPER but still appropriate for freshers.
Ask one of:
- "How do you debug your code when something goes wrong?"
- "Can you explain [intermediate concept] in {topic}?" (e.g., loops, functions, error handling)
- "Walk me through how you would solve [practical problem]"
- "What's the most challenging bug you've encountered and how did you fix it?"
Build on their previous answer. If they struggled, keep it simple. If they did well, go deeper.""",
                
                "Data Science & Analytics": """Second technical question - PRACTICAL APPLICATION.
Ask one of:
- "How would you visualize [type of data]?"
- "What Python libraries have you used for data analysis?"
- "Can you explain what a correlation means?"
- "How do you know if your analysis is correct?"
Adjust based on their previous answer.""",
                
                "Web Development": """Second technical question - PRACTICAL WEB SKILLS.
Ask one of:
- "How do you center a div?" (classic question!)
- "What's the box model in CSS?"
- "Can you explain how you would fetch data from an API?"
- "What frameworks or libraries have you learned?"
Keep it practical.""",
                
                "DevOps & Cloud": """Second technical question - PRACTICAL DEVOPS.
Ask one of:
- "Have you used any cloud platforms? Which ones?"
- "Can you explain what CI/CD means?"
- "How do you deploy a web application?"
- "What's your experience with Linux/command line?"
Focus on practical experience.""",
                
                "Quality Assurance": """Second technical question - TESTING PRACTICE.
Ask one of:
- "How would you test [specific feature]?"
- "What makes a good test case?"
- "Have you used any testing tools? Which ones?"
- "How do you decide what to test first?"
Make it practical.""",
                
                "Mobile Development": """Second technical question - MOBILE SPECIFICS.
Ask one of:
- "How do you handle different screen sizes?"
- "What's your experience with [platform/framework]?"
- "How do mobile apps store data?"
- "What's the most challenging part of mobile development for you?"
Keep it relevant.""",
                
                "Database Administration": """Second technical question - SQL BASICS.
Ask one of:
- "Can you write a simple SQL query to [do something basic]?"
- "What's a primary key?"
- "How do you join two tables?"
- "What databases have you worked with?"
Focus on SQL fundamentals.""",
                
                "Cybersecurity": """Second technical question - SECURITY CONCEPTS.
Ask one of:
- "What is encryption and why is it important?"
- "Can you explain what HTTPS does?"
- "What's the difference between authentication and authorization?"
- "How would you secure a web application?"
Keep it conceptual.""",
                
                "UI/UX Design": """Second technical question - DESIGN PROCESS.
Ask one of:
- "How do you gather user requirements?"
- "What design tools do you use?"
- "Can you explain your design workflow?"
- "How do you handle design feedback?"
Focus on process.""",
                
                "Project Management": """Second technical question - PM SKILLS.
Ask one of:
- "How do you handle conflicting priorities?"
- "What's your experience with Agile or Scrum?"
- "How do you track project progress?"
- "Tell me about a time you had to meet a tight deadline"
Make it practical.""",
                
                "General Technical": f"""Second technical question - PRACTICAL APPLICATION.
Ask about:
- How they apply {topic} knowledge
- Tools and technologies they've used
- Problem-solving approach
- Real-world scenarios
Adjust difficulty based on previous answer."""
            }
            return guidelines.get(role_category, f"Ask practical questions about {topic}")
        
        elif question_number == 5:
            # Third technical question - Problem-solving
            return f"""Third technical question - PROBLEM-SOLVING ABILITY.
Ask one of:
- "Tell me about a technical challenge you faced and how you overcame it"
- "How do you approach learning new technologies?"
- "Describe a project that didn't go as planned. What did you learn?"
- "If you encountered [specific problem], how would you solve it?"
- "What resources do you use when you're stuck on a problem?"

Focus on their THINKING PROCESS and LEARNING ABILITY, not just technical knowledge.
This reveals how they handle real-world challenges."""
        
        elif question_number == 6:
            # First behavioral question
            return f"""First BEHAVIORAL question - TEAMWORK & COLLABORATION.
Ask one of:
- "Tell me about a time you worked on a team project. What was your role?"
- "How do you handle disagreements with team members?"
- "Describe a situation where you had to help a teammate who was struggling"
- "What makes you a good team player?"
- "Have you ever had to work with someone difficult? How did you handle it?"

Use "Tell me about a time..." format. Look for SPECIFIC EXAMPLES, not generic answers.
This is crucial for freshers - teamwork is essential."""
        
        elif question_number == 7:
            # Second behavioral question
            return f"""Second BEHAVIORAL question - LEARNING & GROWTH.
Ask one of:
- "Tell me about a time you failed at something. What did you learn?"
- "How do you stay updated with the latest trends in {topic}?"
- "Describe a situation where you had to learn something completely new quickly"
- "What's the biggest mistake you've made and how did you handle it?"
- "How do you handle constructive criticism?"

Look for SELF-AWARENESS and GROWTH MINDSET.
Freshers should show they can learn from mistakes."""
        
        elif question_number == 8:
            # Third behavioral question
            return f"""Third BEHAVIORAL question - INITIATIVE & PASSION.
Ask one of:
- "Tell me about a project you started on your own (not for class)"
- "What side projects or personal learning are you working on?"
- "How do you practice and improve your {topic} skills outside of work/school?"
- "What's something you built just because you wanted to?"
- "What tech blogs, channels, or communities do you follow?"

Look for GENUINE INTEREST and SELF-MOTIVATION.
Passionate freshers stand out."""
        
        elif question_number == 9:
            # Career goals question
            return f"""CAREER GOALS question - FUTURE VISION.
Ask one of:
- "Where do you see yourself in 3-5 years?"
- "What kind of projects do you want to work on?"
- "What skills do you want to develop in your first year here?"
- "What type of work environment helps you thrive?"
- "What are you looking for in your first job?"

Look for REALISTIC GOALS and SELF-AWARENESS.
Freshers should have thought about their career path."""
        
        elif question_number == 10:
            # Strengths and weaknesses
            return f"""STRENGTHS & WEAKNESSES question - SELF-AWARENESS.
Ask one of:
- "What are your greatest strengths as a {topic}?"
- "What's one area you're actively working to improve?"
- "What do you think you'll find most challenging in this role?"
- "What feedback do you typically receive from professors/peers?"
- "What's something you're not good at yet, but want to be?"

Look for HONEST SELF-ASSESSMENT.
Good answer: Acknowledges weakness + shows they're working on it."""
        
        elif question_number >= 11:
            # Closing questions
            return f"""CLOSING questions - WRAP UP THE INTERVIEW.
Ask one of:
- "Do you have any questions for us about the role or company?"
- "Is there anything else you'd like me to know about you?"
- "What excites you most about this opportunity?"
- "When would you be available to start if selected?"
- "How do you feel the interview went?"

Be friendly and give them a chance to ask questions.
Thank them for their time. Make them feel valued."""
        
        else:
            return f"Continue with relevant questions for {topic}. Be conversational and natural."
    
    def _get_fallback_question(self, question_number, topic):
        """Get a fallback question if AI fails to generate one"""
        fallback_questions = [
            f"Tell me about your experience with {topic}.",
            f"What interests you most about {topic}?",
            f"Can you describe a project you've worked on related to {topic}?",
            "What are your greatest strengths?",
            "How do you handle challenging situations?",
            "Where do you see yourself in 5 years?",
            "Why should we hire you?",
            "Do you have any questions for us?"
        ]
        return fallback_questions[min(question_number - 1, len(fallback_questions) - 1)]
    
    def _generate_fallback_response(self, transcript, history, topic):
        """Generate a highly accurate response when Ollama is not available"""
        question_count = len(history) + 1
        role_category = self._determine_role_category(topic)
        
        # Comprehensive role-specific question banks
        role_questions = {
            "Software Development": {
                "python": [
                    "Tell me about yourself and your experience with Python programming.",
                    "What are the key differences between lists, tuples, and sets in Python?",
                    "Explain how Python handles memory management and garbage collection.",
                    "Describe a challenging Python project you've worked on and how you approached it.",
                    "What Python libraries and frameworks are you most comfortable with?",
                    "How do you debug and optimize Python code for better performance?",
                    "Tell me about a time when you had to learn a new Python concept quickly.",
                    "Where do you see yourself growing as a Python developer?"
                ],
                "java": [
                    "Tell me about yourself and your Java programming experience.",
                    "Explain the difference between abstract classes and interfaces in Java.",
                    "What are the four pillars of Object-Oriented Programming? Explain each.",
                    "Describe a complex Java application you've built. What challenges did you face?",
                    "How does Java handle memory management? Explain the garbage collector.",
                    "What Java frameworks have you worked with? Describe your experience.",
                    "How do you approach exception handling in Java applications?",
                    "What are your career goals as a Java developer?"
                ],
                "javascript": [
                    "Tell me about yourself and your JavaScript experience.",
                    "Explain the difference between var, let, and const in JavaScript.",
                    "What is the event loop in JavaScript and how does it work?",
                    "Describe a JavaScript project you're proud of. What made it challenging?",
                    "How do you handle asynchronous operations in JavaScript?",
                    "What JavaScript frameworks or libraries are you proficient in?",
                    "How do you debug JavaScript code in production?",
                    "Where do you see JavaScript development heading in the next few years?"
                ],
                "general": [
                    f"Tell me about yourself and your interest in {topic}.",
                    f"What programming languages are you most comfortable with for {topic}?",
                    f"Describe a technical challenge you faced and how you solved it.",
                    f"How do you stay updated with the latest trends in {topic}?",
                    "What's your approach to writing clean, maintainable code?",
                    "Tell me about a time you had to debug a difficult issue.",
                    "How do you handle code reviews and feedback?",
                    "What are your long-term career goals in software development?"
                ]
            },
            "Data Science & Analytics": [
                "Tell me about yourself and your interest in data science.",
                "What data analysis tools and programming languages do you know?",
                "Explain the difference between supervised and unsupervised learning.",
                "How would you approach cleaning and preparing a messy dataset?",
                "Describe a data analysis project you've completed. What insights did you find?",
                "What statistical concepts are you most comfortable with?",
                "How do you choose the right visualization for different types of data?",
                "What machine learning algorithms have you worked with?",
                "How do you validate the accuracy of your models?",
                "Where do you see yourself growing in the data science field?"
            ],
            "Web Development": [
                "Tell me about yourself and your web development experience.",
                "What's the difference between frontend and backend development?",
                "Which web technologies and frameworks are you most proficient in?",
                "Describe a website or web application you've built from scratch.",
                "How do you ensure your websites are responsive across different devices?",
                "Explain how you would optimize a slow-loading website.",
                "What's your approach to debugging web applications?",
                "How do you handle browser compatibility issues?",
                "What are the latest web development trends you're excited about?",
                "Where do you see your career in web development going?"
            ],
            "DevOps & Cloud": [
                "Tell me about yourself and your experience with DevOps practices.",
                "Explain the concept of CI/CD and why it's important.",
                "What's the difference between Docker and Kubernetes?",
                "Describe your experience with cloud platforms like AWS, Azure, or GCP.",
                "How do you approach infrastructure as code?",
                "Tell me about a time you automated a manual process. What was the impact?",
                "How do you monitor and troubleshoot production systems?",
                "What's your experience with version control and Git workflows?",
                "How do you ensure security in DevOps pipelines?",
                "What are your goals in the DevOps and cloud space?"
            ],
            "Quality Assurance": [
                "Tell me about yourself and your experience in quality assurance.",
                "What's the difference between manual and automated testing?",
                "Which testing tools and frameworks have you worked with?",
                "Describe your approach to creating comprehensive test cases.",
                "How do you prioritize which tests to automate first?",
                "Tell me about a critical bug you found. How did you discover it?",
                "What's your experience with different types of testing (unit, integration, E2E)?",
                "How do you ensure test coverage is adequate?",
                "How do you communicate testing results to developers and stakeholders?",
                "Where do you see the future of QA and testing?"
            ],
            "Mobile Development": [
                "Tell me about yourself and your mobile development experience.",
                "What mobile platforms have you developed for (iOS, Android, cross-platform)?",
                "Explain the mobile app lifecycle and its key stages.",
                "Describe a mobile app you've built. What challenges did you face?",
                "How do you handle different screen sizes and resolutions?",
                "What's your approach to mobile app performance optimization?",
                "How do you test mobile applications across different devices?",
                "What mobile development frameworks are you familiar with?",
                "How do you handle offline functionality in mobile apps?",
                "What are your career aspirations in mobile development?"
            ],
            "Database Administration": [
                "Tell me about yourself and your database experience.",
                "Explain database normalization and why it's important.",
                "What's the difference between SQL and NoSQL databases?",
                "Describe your experience with database design and schema creation.",
                "How do you optimize slow database queries?",
                "What's your approach to database backup and recovery?",
                "Tell me about a time you had to troubleshoot a database performance issue.",
                "How do you ensure database security and access control?",
                "What database management systems are you most comfortable with?",
                "Where do you see yourself growing as a database professional?"
            ],
            "Cybersecurity": [
                "Tell me about yourself and your interest in cybersecurity.",
                "Explain the CIA triad in information security.",
                "What are the most common web application vulnerabilities?",
                "Describe your experience with security tools and technologies.",
                "How would you approach securing a web application?",
                "Tell me about a security incident you've investigated or heard about.",
                "What's your understanding of encryption and cryptography?",
                "How do you stay updated with the latest security threats?",
                "What certifications or training do you have in cybersecurity?",
                "What are your career goals in the security field?"
            ],
            "UI/UX Design": [
                "Tell me about yourself and your design background.",
                "What's the difference between UI and UX design?",
                "Which design tools are you most proficient in?",
                "Describe your design process from concept to final product.",
                "How do you conduct user research and incorporate feedback?",
                "Show me a design project you're proud of. What made it successful?",
                "How do you ensure your designs are accessible to all users?",
                "What design principles do you follow?",
                "How do you handle design feedback and criticism?",
                "Where do you see design trends heading?"
            ],
            "Project Management": [
                "Tell me about yourself and your project management experience.",
                "Explain the difference between Agile and Waterfall methodologies.",
                "Describe a project you managed from start to finish.",
                "How do you handle project scope creep?",
                "What's your approach to stakeholder management?",
                "Tell me about a time a project went off track. How did you handle it?",
                "How do you prioritize tasks and manage resources?",
                "What project management tools do you use?",
                "How do you measure project success?",
                "What are your goals as a project manager?"
            ],
            "Business Analysis": [
                "Tell me about yourself and your experience as a business analyst.",
                "How do you gather and document business requirements?",
                "What techniques do you use for requirements elicitation?",
                "Describe a complex business problem you helped solve.",
                "How do you bridge the gap between business and technical teams?",
                "What tools do you use for business analysis?",
                "Tell me about a time stakeholders had conflicting requirements.",
                "How do you validate that requirements are complete and accurate?",
                "What's your experience with process modeling and improvement?",
                "Where do you see your career in business analysis going?"
            ],
            "Network Engineering": [
                "Tell me about yourself and your networking experience.",
                "Explain the OSI model and its seven layers.",
                "What's the difference between TCP and UDP?",
                "Describe your experience with network design and implementation.",
                "How do you troubleshoot network connectivity issues?",
                "What networking protocols are you most familiar with?",
                "Tell me about a complex network problem you solved.",
                "How do you ensure network security?",
                "What certifications do you have (CCNA, CCNP, etc.)?",
                "What are your career goals in network engineering?"
            ]
        }
        
        # Select appropriate question set
        topic_lower = topic.lower()
        questions = None
        
        # Try to match specific technology first
        if "python" in topic_lower:
            questions = role_questions["Software Development"]["python"]
        elif "java" in topic_lower:
            questions = role_questions["Software Development"]["java"]
        elif "javascript" in topic_lower or "js" in topic_lower:
            questions = role_questions["Software Development"]["javascript"]
        elif role_category in role_questions:
            if isinstance(role_questions[role_category], dict):
                questions = role_questions[role_category]["general"]
            else:
                questions = role_questions[role_category]
        else:
            questions = role_questions["Software Development"]["general"]
        
        # Get next question
        next_question = questions[min(question_count - 1, len(questions) - 1)]
        
        # Advanced scoring based on multiple factors
        answer_words = transcript.split()
        answer_length = len(answer_words)
        
        # Check for technical keywords based on role
        technical_keywords = self._get_technical_keywords(role_category, topic)
        keyword_count = sum(1 for word in answer_words if word.lower() in technical_keywords)
        
        # Check for example indicators
        example_indicators = ['example', 'instance', 'project', 'experience', 'worked on', 'built', 'created', 'developed']
        has_examples = any(indicator in transcript.lower() for indicator in example_indicators)
        
        # Calculate score
        score = 5  # Base score
        feedback_parts = []
        
        # Length evaluation
        if answer_length < 15:
            score = 3
            feedback_parts.append("Your answer is too brief and lacks detail.")
        elif answer_length < 40:
            score = 5
            feedback_parts.append("Your answer could be more detailed.")
        elif answer_length < 80:
            score = 6
            feedback_parts.append("Good answer length.")
        else:
            score = 7
            feedback_parts.append("Excellent detailed response.")
        
        # Technical content evaluation
        if keyword_count >= 3:
            score += 1
            feedback_parts.append("You demonstrated good technical knowledge.")
        elif keyword_count >= 1:
            feedback_parts.append("Try to include more technical details.")
        else:
            score -= 1
            feedback_parts.append("Your answer lacks technical depth.")
        
        # Example evaluation
        if has_examples:
            score += 1
            feedback_parts.append("Good use of specific examples.")
        else:
            feedback_parts.append("Consider providing specific examples from your experience.")
        
        # Ensure score is in valid range
        score = max(1, min(10, score))
        
        # Construct feedback
        feedback = " ".join(feedback_parts)
        if score >= 7:
            feedback += " Keep up this level of detail in your responses."
        elif score >= 5:
            feedback += " To improve, provide more specific examples and technical details."
        else:
            feedback += " Focus on answering the question directly with relevant details and examples."
        
        return {
            "feedback": feedback,
            "score": score,
            "next_question": next_question
        }
    
    def _get_technical_keywords(self, role_category, topic):
        """Get technical keywords for scoring based on role"""
        keywords = {
            "Software Development": ['code', 'function', 'class', 'algorithm', 'data structure', 'api', 'framework', 'library', 'debug', 'test', 'deploy', 'git', 'version control'],
            "Data Science & Analytics": ['data', 'analysis', 'model', 'algorithm', 'statistics', 'visualization', 'pandas', 'numpy', 'machine learning', 'dataset', 'feature', 'prediction'],
            "Web Development": ['html', 'css', 'javascript', 'frontend', 'backend', 'api', 'responsive', 'framework', 'react', 'angular', 'vue', 'node', 'database'],
            "DevOps & Cloud": ['docker', 'kubernetes', 'ci/cd', 'pipeline', 'deployment', 'cloud', 'aws', 'azure', 'infrastructure', 'automation', 'monitoring'],
            "Quality Assurance": ['test', 'testing', 'automation', 'bug', 'quality', 'selenium', 'junit', 'integration', 'regression', 'test case'],
            "Mobile Development": ['mobile', 'app', 'android', 'ios', 'react native', 'flutter', 'ui', 'responsive', 'performance', 'api'],
            "Database Administration": ['database', 'sql', 'query', 'table', 'index', 'normalization', 'backup', 'recovery', 'performance', 'optimization'],
            "Cybersecurity": ['security', 'vulnerability', 'encryption', 'authentication', 'authorization', 'firewall', 'penetration', 'threat', 'risk'],
            "UI/UX Design": ['design', 'user', 'interface', 'experience', 'wireframe', 'prototype', 'usability', 'accessibility', 'figma', 'sketch'],
            "Project Management": ['project', 'agile', 'scrum', 'stakeholder', 'timeline', 'budget', 'risk', 'resource', 'deliverable'],
            "Business Analysis": ['requirements', 'stakeholder', 'process', 'analysis', 'documentation', 'workflow', 'business', 'solution'],
            "Network Engineering": ['network', 'router', 'switch', 'protocol', 'tcp', 'ip', 'firewall', 'vpn', 'bandwidth', 'latency']
        }
        return keywords.get(role_category, [])

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
