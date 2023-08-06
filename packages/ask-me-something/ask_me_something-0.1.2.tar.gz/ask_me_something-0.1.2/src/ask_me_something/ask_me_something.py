import speech_recognition as sr
import argparse

r = sr.Recognizer()
m = sr.Microphone()
print("A moment of silence, please...")
with m as source: r.adjust_for_ambient_noise(source)

def ask(text = "Say something to mic", language = "en-en"):


    parser = argparse.ArgumentParser()
    parser.add_argument('-l', '--language', type=str, help='Language')


    args = parser.parse_args()

    if not args.language is None:
        language = args.language

    global r
    global m
    print(text)
    with m as source: audio = r.listen(source)
    try:
         data = r.recognize_google(audio, language=language)
         data = data.lower()
         print(data)
         return data

    except sr.UnknownValueError:
        print("I can't understand")
        return None
