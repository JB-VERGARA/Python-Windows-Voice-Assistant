import speech_recognition as sr


def listen():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Listening...")

        recognizer.adjust_for_ambient_noise(
            source,
            duration=0.5
        )

        try:
            audio = recognizer.listen(
                source,
                timeout=2,
                phrase_time_limit=5
            )

        except sr.WaitTimeoutError:
            return ""

    try:
        command = recognizer.recognize_google(audio)

        print(f"You said: {command}")

        return command.lower()

    except sr.UnknownValueError:
        print("I couldn't understand that.")
        return ""

    except sr.RequestError as error:
        print(f"Speech recognition error: {error}")
        return ""