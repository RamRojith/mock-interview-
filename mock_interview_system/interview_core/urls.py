from django.urls import path
from .views import StartSessionView, ProcessResponseView, index_view, interview_view

urlpatterns = [
    path('', index_view, name='index'),
    path('interview/<int:session_id>/', interview_view, name='interview'),
    path('api/start-session/', StartSessionView.as_view(), name='start_session'),
    path('api/process-response/', ProcessResponseView.as_view(), name='process_response'),
]
