import subprocess
from gtts import gTTS

myobj = gTTS(text='hola como estas?', lang='es')
myobj.save("welcome.mp3")
print('saved')
# Playing the converted file
subprocess.call(['mpg321', "welcome.mp3", '--play-and-exit'])
