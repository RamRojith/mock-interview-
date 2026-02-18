from django.urls import path
from .views import StartSessionView, ProcessResponseView, landing_view, mic_test_view, index_view, interview_view, interview_report_view

urlpatterns = [
    path('', landing_view, name='landing'),
    path('mic-test/', mic_test_view, name='mic_test'),
    path('start/', index_view, name='interview_start'),
    path('interview/<int:session_id>/', interview_view, name='interview'),
    path('report/<int:session_id>/', interview_report_view, name='interview_report'),
    path('api/start-session/', StartSessionView.as_view(), name='start_session'),
    path('api/process-response/', ProcessResponseView.as_view(), name='process_response'),
]
