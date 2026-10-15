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

## 🖥️ Interface

<img width="1898" height="970" alt="image" src="https://github.com/user-attachments/assets/2a443146-2fe9-47fa-b746-28ec9a87b04b" />

<img width="1918" height="885" alt="image" src="https://github.com/user-attachments/assets/7ac5798b-c07e-4e67-bd30-e60ccd8b2e57" />

<img width="1917" height="918" alt="image" src="https://github.com/user-attachments/assets/86388b65-f1e9-4e68-a3d2-4b232c964262" />




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







