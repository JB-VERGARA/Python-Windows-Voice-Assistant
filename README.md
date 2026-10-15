# Python Windows Voice Assistant

A lightweight Windows desktop voice assistant built with Python and PySide6.

The assistant listens for a wake word, recognizes an exact voice command, and executes the Python script mapped to that command. New capabilities can be added through the built-in Script Manager without modifying the assistant's core.

> Say **"Bryan, open Chrome"** and the assistant executes the command.

## ✨ Features

- 🎙️ Voice command recognition
- 🔊 Text-to-speech responses
- 🗣️ Wake word detection
- ⚡ Exact command matching
- 🧩 Independent Python scripts for commands
- 🖥️ Floating Windows desktop interface
- 📌 Windows system tray integration
- ⏯️ Start / Pause listening
- 📜 Recent command history
- 🛠️ Built-in Script Manager
- ➕ Add custom commands and aliases
- ✏️ Edit existing commands
- 🗑️ Delete commands
- 🔒 No AI command interpretation
- 🐍 Built entirely with Python

## 🧠 How It Works

The assistant follows a simple and predictable command pipeline:

```text
Microphone
    ↓
Speech Recognition
    ↓
Wake Word Detection
    ↓
Exact Command Matching
    ↓
Command → Python Script
    ↓
Script Execution
    ↓
Text-to-Speech Response

## 🖥️ Interface
<img width="1902" height="944" alt="image" src="https://github.com/user-attachments/assets/69f1911f-cf9a-4547-b60b-39d65671d79d" />

<img width="1912" height="987" alt="image" src="https://github.com/user-attachments/assets/c4ad4265-0571-4455-89ef-13e7e1f545db" />

<img width="1907" height="984" alt="image" src="https://github.com/user-attachments/assets/58b64f4a-07fb-41cc-bfe4-6dea00e10d0a" />


