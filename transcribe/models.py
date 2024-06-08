from django.db import models

class Transcription(models.Model):
    audio_file = models.FileField(upload_to='audio_files/')
    transcribed_text = models.TextField()
    translated_text = models.TextField()
    email_sent = models.BooleanField(default=False)

    def __str__(self):
        return f"Transcription ID: {self.id}"

