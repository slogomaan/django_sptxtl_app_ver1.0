import os
import speech_recognition as sr
from deepmultilingualpunctuation import PunctuationModel
from pydub import AudioSegment
from pydub.silence import split_on_silence
import spacy
from googletrans import Translator
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from django.conf import settings

model = PunctuationModel()
nlp = spacy.load("en_core_web_sm")

def transcribe_audio(audio_file_path):
    # Initialize the recognizer
    recognizer = sr.Recognizer()
    # Loading the audio file
    audio = AudioSegment.from_wav(audio_file_path)
    # Checking the duration of the audio file
    audio_duration = len(audio) / 1000  # Duration in seconds
    # Transcribing the audio
    if audio_duration > 60:
        # Splitting the audio into chunks based on silence
        audio_chunks = split_on_silence(audio, min_silence_len=450, silence_thresh=-47)
        # Transcribing each chunk separately
        transcribed_chunks = ""
        for i, chunk in enumerate(audio_chunks):
            print(f"Transcribing Chunk {i+1}")
            try:
                chunk.export("temp.wav", format="wav")
                with sr.AudioFile("temp.wav") as source:
                    chunk_audio_data = recognizer.record(source)
                text = recognizer.recognize_google(chunk_audio_data, language='en-US')  # Assuming English audio
                transcribed_chunks += text + " "
                os.remove("temp.wav")
            except sr.UnknownValueError:
                print("Speech Recognition could not understand the audio.")
                print("Transcribed Chunks (English):", transcribed_chunks)
    else:
        # Transcribing the entire audio in one go
        try:
            with sr.AudioFile(audio_file_path) as source:
                audio_data = recognizer.record(source)
                text = recognizer.recognize_google(audio_data, language='en-US')  # Assuming English audio
            print("Transcribed Text (English):", text)
            transcribed_chunks = text  # Storing the transcribed text
        except sr.UnknownValueError:
            print("Speech Recognition could not understand the audio.")
            transcribed_chunks = ""  # Assigning empty string if transcription fails
    return transcribed_chunks

def index(request):
    languages = ['Hindi', 'Bengali', 'Telgu', 'Marathi', 'Tamil', 'Urdu', 'Gujarati', 'Kannada', 'Malayalam', 'Odia', 'Punjabi', 'Assamese', 'Maithili', 'Santali']
    return render(request, 'transcribe/index.html', {'languages': languages})

def transcribe_audio_view(request):
    if request.method == 'POST':
        try:
            audio_file = request.FILES.get('audio_file')
            if not audio_file:
                return render(request, 'transcribe/index.html', {'error_message': "No audio file provided."})
            language = request.POST.get('language')
            audio_file_path = os.path.join(settings.MEDIA_ROOT, audio_file.name)
            with open(audio_file_path, 'wb+') as f:
                for chunk in audio_file.chunks():
                    f.write(chunk)

            transcribed_text = transcribe_audio(audio_file_path)
            if not transcribed_text:
                return render(request, 'transcribe/index.html', {'error_message': "Error transcribing the audio file."})

            restored_text = model.restore_punctuation(transcribed_text)
            updated_text = '. '.join([sentence[0].upper() + sentence[1:] for sentence in restored_text.split('. ')])
            translator = Translator()
            translated_text = translator.translate(updated_text, dest=language)

            context = {
                'transcribed_text': updated_text,
                'translated_text': translated_text.text,
                'languages': ['Hindi', 'Bengali', 'Telgu', 'Marathi', 'Tamil', 'Urdu', 'Gujarati', 'Kannada', 'Malayalam', 'Odia', 'Punjabi', 'Assamese', 'Maithili', 'Santali']
            }
            return render(request, 'transcribe/index.html', context)
        except Exception as e:
            print(f"Error: {e}")
            return render(request, 'transcribe/index.html', {'error_message': "Error processing the audio file."})

@csrf_exempt
def send_email(request):
    if request.method == 'POST':
        transcribed_text = request.POST.get('transcribed_text')
        translated_text = request.POST.get('translated_text')
        language = request.POST.get('language')
        email_receivers = request.POST.get('email_receivers')

        subject = "Audio to Text Conversion"
        body = f"""Greetings,
        
This is a conversion of audio speech to text (in English),
then conversion to {language.upper()}.

The transcribed text: {transcribed_text}

The translation in {language.upper()}:
{translated_text}

Regards,
Shashwat Behera"""

        try:
            send_mail(
                subject,
                body,
                settings.EMAIL_HOST_USER,
                email_receivers.split(', '),
                fail_silently=False,
            )
            return HttpResponse("Email sent successfully!")
        except Exception as e:
            print(f"Error: {e}")
            return HttpResponse("Error sending the email.")
    return HttpResponse("Invalid request method.")
 