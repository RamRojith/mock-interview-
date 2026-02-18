from django.apps import AppConfig


class InterviewCoreConfig(AppConfig):
    name = 'interview_core'

    def ready(self):
        # Warm the Whisper model at startup so the first request doesn't block on loading.
        from .ai_service import ai_service
        try:
            _ = ai_service.whisper_model
        except Exception as exc:
            # Don't crash the server if the model fails to load; log and continue.
            print(f"[InterviewCore] Whisper warmup failed: {exc}")
