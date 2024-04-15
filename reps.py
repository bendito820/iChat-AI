import speech_recognition as sr
import pyttsx3
from groq import Groq


client = Groq(
    api_key=''
)

r = sr.Recognizer()


def change_voice(engine, language, gender="None"):
    for voice in engine.getProperty('voices'):
        engine.setProperty('voice')
        return True

    raise RuntimeError(
        "LAnguage '{}' for gender '{}' not found".format(language, gender)
    )


def SpeakText(command):
    engine = pyttsx3.init()
    change_voice(engine, 'portuguese')
    engine.say(command)
    engine.runAndWait()


SpeakText('E la vamos mais uma vez')


while True:
    try:
        print('you can start speaking...')
        with sr.Microphone() as source2:
            r.adjust_for_ambient_noise(source2, duration=0.2)
            audio2 = r.listen(source2)

            MyText = r.recognize_google_cloud(audio2, language='en')
            MyText = MyText.lower()

            if MyText == 'exit':
                break

            print(f'Prompt: {MyText}')
            chat_completion = client.chat.completions.create(messages=[{
                'role': 'user',
                'content': MyText
            }], model='mixtral')
            print('Answer: ', chat_completion.choices[0].message.content)
            SpeakText(chat_completion.choices[0].message.content)
    except sr.RequestError as e:
        print('Could not request results; {0}'.format(e))

    except sr.UnknownValueError:
        print('unknown error occurred')

engine = pyttsx3.init()
for voice in engine.getProperty('voices'):
    print(voice)
