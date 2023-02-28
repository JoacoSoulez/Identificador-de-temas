import speech_recognition as sr
from IPython.display import Audio
import os
import ffmpeg
import whisper
from pydub import AudioSegment
from scipy.io.wavfile import write
import requests


bot_message = ""
message= ""

b = requests.post('http://localhost:5002/webhooks/rest/webhook', json={"message": "hola"})
print("Bot dice, ",end=' ')
for i in b.json():
    bot_message = i['text']
    print(f"{bot_message}")

while bot_message != "Chau" or bot_message!='Gracias':
    r = sr.Recognizer()
    model = whisper.load_model("base")
    with sr.Microphone() as source:
        print('Respondeme por favor...')
        audio = r.listen(source)
        with open('record.wav', 'wb') as f:
            f.write(audio.get_wav_data())
        try:
            result = model.transcribe('record.wav')
            print('Dijiste: {}'.format(result["text"]))
        except:
            print('no entendi, repita por favor')

    if len(result)==0:
        continue
    print("Enviando mensaje...")

    b = requests.post('http://localhost:5002/webhooks/rest/webhook', json={"message": str(result["text"])})

    print("Bot dice, ",end=' ')
    for i in b.json():
        bot_message = i['text']
        print(f"{bot_message}")
