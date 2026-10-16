import json
import subprocess
import sys
import pyautogui
from pathlib import Path
from app.tts import speak

BASE_DIR = Path(__file__).resolve().parent.parent
COMMANDS_FILE = BASE_DIR / "commands" / "commands.json"


def load_commands():
    with open(
        COMMANDS_FILE,
        "r",
        encoding="utf-8"
    ) as file:
        return json.load(file)


def find_command(command):
    command = command.lower().strip()

    commands = load_commands()

    for name, value in commands.items():

        # New command format
        if isinstance(value, dict):
            script = value.get("script")
            aliases = value.get("aliases", [])

            if command == name.lower():
                return script

            if command in [
                alias.lower()
                for alias in aliases
            ]:
                return script

        # Old command format
        else:
            if command == name.lower():
                return value

    return None


def handle_command(command):
    command = command.lower().strip()

    # ---------------------------------------------
    # DYNAMIC TYPE COMMAND
    # ---------------------------------------------
    if command.startswith("type "):
        text = command[5:].strip()

        if text:
            pyautogui.write(text, interval=0.03)

            response = f"Typing: {text}"
            speak(response)

            return response

    # ---------------------------------------------
    # NORMAL SCRIPT COMMANDS
    # ---------------------------------------------
    script = find_command(command)

    if script:
        script_path = BASE_DIR / script

        subprocess.Popen(
            [
                sys.executable,
                "-m",
                script[:-3].replace("/", ".").replace("\\", ".")
            ],
            shell=False,
            cwd=BASE_DIR
        )

        response = f"Analyzing & Executing: {command}"

        speak(response)

        return response

    response = f"I don't know that command: {command}"

    speak(response)

    return response