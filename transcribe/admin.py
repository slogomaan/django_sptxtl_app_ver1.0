from django.contrib import admin
from .models import Transcription

class TranscriptionAdmin(admin.ModelAdmin):
    list_display = ('id', 'audio_file', 'transcribed_text', 'email_sent')
    list_filter = ('email_sent',)

admin.site.register(Transcription, TranscriptionAdmin)
