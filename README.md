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


/image.png




