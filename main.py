import speech_recognition as sr
import pyttsx3
from groq import Groq

client = Groq(
    api_key="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",
)


# Initialize the recognizer
r = sr.Recognizer()


# language  : en_US, de_DE, ...
# gender    : VoiceGenderFemale, VoiceGenderMale
def change_voice(engine, language, gender='None'):
    for voice in engine.getProperty('voices'):
        if language.lower() in voice.name.lower():
            engine.setProperty('voice', voice.id)
            return True

    raise RuntimeError(
        "Language '{}' for gender '{}' not found".format(language, gender))

# Function to convert text to
# speech


def SpeakText(command):
    # Initialize the engine
    engine = pyttsx3.init()
    change_voice(engine, 'portuguese')
    engine.say(command)
    engine.runAndWait()


# SpeakText("E la vamos mais uma vez")

# Loop infinitely for user to
# speak
while True:

    # Exception handling to handle
    # exceptions at the runtime
    try:
        print('you can start speaking... ')
        # use the microphone as source for input.
        with sr.Microphone() as source2:

            # wait for a second to let the recognizer
            # adjust the energy threshold based on
            # the surrounding noise level
            r.adjust_for_ambient_noise(source2, duration=0.2)

            # listens for the user's input
            audio2 = r.listen(source2)

            # Using google to recognize audio
            MyText = r.recognize_google(audio2, language='pt-BR')
            MyText = MyText.lower()

            # say Exit to Exit the program
            if MyText == 'exit':
                break

            print(f"Prompt: {MyText}")
            chat_completion = client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": f' {MyText}, responde em portugues',
                    }
                ],
                model="mixtral-8x7b-32768",
            )

            print("Answer: ", chat_completion.choices[0].message.content)
            SpeakText(chat_completion.choices[0].message.content)

    except sr.RequestError as e:
        print("Could not request results; {0}".format(e))

    except sr.UnknownValueError:
        print("unknown error occurred")


###############################
#    LIST INSTALLED VOICES    #
###############################

# engine = pyttsx3.init()

# for voice in engine.getProperty('voices'):
#     print(voice)
# #
