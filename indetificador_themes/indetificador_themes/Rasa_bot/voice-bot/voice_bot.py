import speech_recognition as sr
from IPython.display import Audio
import os
import ffmpeg
import whisper
from pydub import AudioSegment
from scipy.io.wavfile import write
import requests
import subprocess
from gtts import gTTS



bot_message = ""
message= ""

b = requests.post('http://localhost:5002/webhooks/rest/webhook', json={"message": "hola"})
print("Bot dice, ",end=' ')
for i in b.json():
    bot_message = i['text']
    print(f"{bot_message}")
myobj = gTTS(text=bot_message, lang='es')
myobj.save("welcome.mp3")
print('saved')
# Playing the converted file
subprocess.call(['mpg321', "welcome.mp3", '--play-and-exit'])
while bot_message != "Chau" or bot_message!='Gracias':
    r = sr.Recognizer()
    model = whisper.load_model("base")
    #forced_decoder_ids = processor.get_decoder_prompt_ids(language="french", task="transcribe")
    with sr.Microphone() as source:
        print('Respondeme por favor...')
        audio = r.listen(source)
        with open('record.wav', 'wb') as f:
            f.write(audio.get_wav_data())
        try:
            result = model.transcribe('record.wav', language='es', verbose=False)
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
    myobj = gTTS(text=bot_message, lang='es',tld='com.mx')
    myobj.save("welcome.mp3")
    print('saved')
    # Playing the converted file
    subprocess.call(['mpg321', "welcome.mp3", '--play-and-exit'])
