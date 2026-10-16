from PySide6.QtCore import QThread, Signal

from app.voice import listen
from app.command_handler import handle_command
from app.tts import speak
import pyautogui


class VoiceWorker(QThread):
    command_received = Signal(str)
    status_changed = Signal(str)
    speech_received = Signal(str)

    def run(self):
        wake_words = ["bryan", "brian", "system"]
        typing_mode = False

        while not self.isInterruptionRequested():

            self.status_changed.emit("● LISTENING")

            command = listen()

            if not command:
                continue

            # Keep original capitalization
            command = command.strip()

            if not command:
                continue

            # Tell the GUI what was heard
            self.speech_received.emit(command)

            # ==================================================
            # TYPING MODE
            # ==================================================

            if typing_mode:

                lower_command = command.lower().strip()

                # Check if user wants to end typing mode
                detected_wake_word = None

                for word in wake_words:
                    if lower_command.startswith(word):
                        detected_wake_word = word
                        break

                if detected_wake_word:

                    remaining = lower_command[
                        len(detected_wake_word):
                    ].strip()

                    if remaining == "stop type":
                        typing_mode = False

                        speak("Typing mode ended.")

                        self.command_received.emit(
                            "Typing mode ended."
                        )

                        continue

                # If not "Bryan, end type",
                # type whatever was spoken
                pyautogui.write(
                    command,
                    interval=0.03
                )

                self.command_received.emit(
                    f"Typing: {command}"
                )

                continue

            # ==================================================
            # NORMAL MODE
            # ==================================================

            lower_command = command.lower().strip()

            detected_wake_word = None

            for word in wake_words:
                if lower_command.startswith(word):
                    detected_wake_word = word
                    break

            # Ignore speech without wake word
            if detected_wake_word is None:
                continue

            # Remove wake word while preserving
            # the original capitalization
            command = command[
                len(detected_wake_word):
            ].strip()

            if not command:
                speak("Yes?")
                continue

            # ==================================================
            # START TYPING MODE
            # ==================================================

            if command.lower() == "type":
                typing_mode = True

                speak("Typing mode activated.")

                self.command_received.emit(
                    "Typing mode activated."
                )

                continue

            # ==================================================
            # NORMAL COMMAND
            # ==================================================

            self.status_changed.emit("● PROCESSING")

            result = handle_command(command)

            self.command_received.emit(result)

        self.status_changed.emit("● PAUSED")