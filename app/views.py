from django.shortcuts import render
from django.http import HttpResponse
import joblib
import os
from CyberBullying_Detection_WebApp import settings
from django.core.files.storage import FileSystemStorage
from CyberBullying_Detection_WebApp.settings import STATIC_ROOT, MEDIA_ROOT, ML_Modal as mdl
# video conversion imports
import wave, math, contextlib
import speech_recognition as sr
from moviepy.editor import AudioFileClip


# Create your views here.
def home(request):
    return render(request, template_name='index.html')


def predict_text(request):
    data = request.POST.get('text_data')
    res = mdl.predict([data])
    res = bully_type_beautify(res)
    return HttpResponse(res)


def detect_cb_audio(request):
    file = request.FILES.get('file')
    fs = FileSystemStorage()
    file2 = fs.save(file.name, file)
    fileurl = fs.url(file2)
    data = audio_to_text(MEDIA_ROOT + '/' + fileurl.split('/')[2])
    print("Dataaaaaa#########\n", data)
    res = mdl.predict([data])
    res = bully_type_beautify(res)
    return HttpResponse(res)


def detect_cb_video(request):
    file = request.FILES.get('file')
    fs = FileSystemStorage()
    file2 = fs.save(file.name, file)
    fileurl = fs.url(file2)
    data = video_to_text(MEDIA_ROOT + '/' + fileurl.split('/')[2])
    print("Dataaaaaa#########\n", data)
    res = mdl.predict([data])
    res = bully_type_beautify(res)
    return HttpResponse(res)


def video_to_text(file):
    audio_output = "speech.wav"
    # video_clip = "age.mp4"
    video_clip = file
    audioclip = AudioFileClip(video_clip)
    audioclip.write_audiofile(audio_output)
    with contextlib.closing(wave.open(audio_output, 'r')) as f:
        frames = f.getnframes()
        rate = f.getframerate()
        duration = frames / float(rate)
    total_duration = math.ceil(duration / 60)
    r = sr.Recognizer()
    textual_output = ''
    for i in range(0, total_duration):
        with sr.AudioFile(audio_output) as source:
            audio = r.record(source, offset=i * 60, duration=60)
        # f = open("transcription.txt", "a")
        # f.write(r.recognize_google(audio))
        # f.write(" ")
        textual_output += r.recognize_google(audio)
        # textual_output.append(r.recognize_google(audio))
    f.close()
    return textual_output


def audio_to_text(audio_file):
    with contextlib.closing(wave.open(audio_file, 'r')) as f:
        frames = f.getnframes()
        rate = f.getframerate()
        duration = frames / float(rate)
    total_duration = math.ceil(duration / 60)
    r = sr.Recognizer()
    textual_output = ''
    for i in range(0, total_duration):
        with sr.AudioFile(audio_file) as source:
            audio = r.record(source, offset=i * 60, duration=60)
        # f = open("transcription.txt", "a")
        # f.write(r.recognize_google(audio))
        # f.write(" ")
        textual_output += r.recognize_google(audio)
        # textual_output.append(r.recognize_google(audio))
    f.close()
    return textual_output


def bully_type_beautify(bully):
    resp = ''
    if bully == 'religion':
        resp = 'Religious Bullying'
    elif bully == 'age':
        resp = 'Age Bullying'
    elif bully == 'gender':
        resp = 'Gender Bullying'
    elif bully == 'ethnicity':
        resp = 'Ethnicity Bullying'
    elif bully == 'not_cyberbullying':
        resp = 'Not Cyberbullying'
    else:
        resp = bully
    return resp
