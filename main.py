import json, time
import pyttsx3, pyaudio, vosk
from lab_10.api import Api



class Speech:
    def __init__(self):
        self.speaker = 0
        self.tts = pyttsx3.init('sapi5')

    def set_voice(self, speaker):
        self.voices = self.tts.getProperty('voices')
        for count, voice in enumerate(self.voices):
            if count == 0:
                print('0')
                id = voice.id
            if speaker == count:
                id = voice.id
        return id

    def text2voice(self, speaker=0, text='Готов'):
        self.tts.setProperty('voice', self.set_voice(speaker))
        self.tts.say(text)
        self.tts.runAndWait()

class Recognize:
    def __init__(self):
        model = vosk.Model('vosk-model-small-ru-0.22')
        self.record = vosk.KaldiRecognizer(model, 16000)
        self.stream()

    def stream(self):
        pa = pyaudio.PyAudio()
        self.stream = pa.open(format=pyaudio.paInt16,
                         channels=1,
                         rate=16000,
                         input=True,
                         frames_per_buffer=8000)


    def listen(self):
        while True:
            data = self.stream.read(4000, exception_on_overflow=False)
            if self.record.AcceptWaveform(data) and len(data) > 0:
                answer = json.loads(self.record.Result())
                if answer['text']:
                    yield answer['text']


def speak(text):
    speech = Speech()
    speech.text2voice(speaker=1, text=text)

def getTemperture(data):
    return data['main']['temp'] - 273.15

def getWeather(data):
    return data['weather'][0]['main']

def getHumidity(data):
    return data['main']['humidity']

def getPressure(data):
    return data['main']['pressure']


rec = Recognize()
text_gen = rec.listen()
rec.stream.stop_stream()
speak('Starting')
time.sleep(0.5)
rec.stream.start_stream()
for text in text_gen:
    if text:
        cityName = text
        wet = Api(cityName)
        data = wet.getData()
        print(data)
        print(cityName)

        for texts in text_gen:
            if texts == 'погода':
                print(f"Погода в {cityName}: {getWeather(data)}")

            if texts == 'температура':
                print(f"Погода в {cityName}: {getTemperture(data)}")

            if texts == 'влажность':
                print(f"Погода в {cityName}: {getHumidity(data)}")

            if texts == 'давление':
                print(f"Погода в {cityName}: {getPressure(data)}")

            if texts == 'стоит ли гулять':
                if getTemperture(data) > 15 and getWeather(data) != 'Rain':
                    print('да стоит')
                else:
                    print('лучше остатся дома')