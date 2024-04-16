import speech_recognition as sr
import pyttsx3
from groq import Groq


client = Groq(
    api_key="my_key"
)

r = sr.Recognizer()


def change_voice(engine, language, gender="None"):
    for voice in engine.getProperty('voices'):
        if language.lower() in voice.name.lower():
            engine.setProperty('voice', voice.id)
            return True

    raise RuntimeError(
        ""
    )


def SpeakText():
    engine = pyttsx3.init()
    change_voice(engine, 'portuguese')
    engine.say(command)
    engine.runAndWait()


while True:
    try:
        print('You can start speaking...')
        with sr.Microphone() as source2:
            r.adjust_for_ambient_noise(source2, duration=0.2)

            audio2 = r.listen(source2)

            MyText = r.recognize_google_cloud(audio2, language='pt-BR')
            MyText = MyText.lower()

            if MyText == 'exit':
                break

            print(f'Prompt: {MyText}')
            chat_completion = client.chat.completions.create(
                messages=[
                    {
                        'role': 'user',
                        'content': f' {MyText}'
                    }
                ],
                model='mixtral-8x7b-32768'
            )

            print(f'Answer: {chat_completion.choices[0].message.content}')
            SpeakText(chat_completion.choices[0].message.content)
    except sr.RequestError as e:
        print(e)

    except sr.UnknownValueError:
        print('unknoen error occurred')
