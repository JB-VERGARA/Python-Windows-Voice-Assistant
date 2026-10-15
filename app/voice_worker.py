from PySide6.QtCore import QThread, Signal

from app.voice import listen
from app.command_handler import handle_command
from app.tts import speak


class VoiceWorker(QThread):
    command_received = Signal(str)
    status_changed = Signal(str)
    speech_received = Signal(str)

    def run(self):
        wake_words = ["bryan", "brian", "system"]

        while not self.isInterruptionRequested():

            self.status_changed.emit("● LISTENING")

            command = listen()

            if not command:
                continue

            command = command.lower().strip()

            if not command:
                continue

            # Tell the GUI what was heard
            self.speech_received.emit(command)

            detected_wake_word = None

            for word in wake_words:
                if command.startswith(word):
                    detected_wake_word = word
                    break

            # Ignore speech without wake word
            if detected_wake_word is None:
                continue

            # Remove wake word
            command = command[len(detected_wake_word):].strip()

            if not command:
                speak("Yes?")
                continue

            self.status_changed.emit("● PROCESSING")

            result = handle_command(command)

            self.command_received.emit(result)

        self.status_changed.emit("● PAUSED")