import sys

from PySide6.QtCore import Qt, QPoint
from PySide6.QtGui import QAction, QColor, QIcon, QPainter, QPixmap
from PySide6.QtWidgets import (
    QApplication,
    QFrame,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QMenu,
    QPushButton,
    QStyle,
    QSystemTrayIcon,
    QVBoxLayout,
    QWidget,
)

from app.voice_worker import VoiceWorker
from app.script_manager import ScriptManager


class BryanAssistant(QWidget):
    def __init__(self):
        super().__init__()

        self.voice_worker = None

        self.setup_window()
        self.setup_ui()
        self.setup_tray()

    # --------------------------------------------------
    # WINDOW
    # --------------------------------------------------

    def setup_window(self):
        self.setWindowTitle("Bryan Assistant")

        self.setFixedSize(380, 520)

        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.Tool
            | Qt.WindowType.WindowStaysOnTopHint
        )

        self.setAttribute(
            Qt.WidgetAttribute.WA_TranslucentBackground
        )

    # --------------------------------------------------
    # UI
    # --------------------------------------------------

    def setup_ui(self):

        self.container = QFrame()

        self.container.setObjectName("container")

        self.container.setStyleSheet("""
            #container {
                background-color: #111827;
                border: 1px solid #263244;
                border-radius: 20px;
            }

            QLabel {
                color: #f3f4f6;
            }

            #title {
                font-size: 22px;
                font-weight: 700;
            }

            #subtitle {
                color: #9ca3af;
                font-size: 12px;
            }

            #status {
                font-size: 16px;
                font-weight: 600;
                color: #60a5fa;
            }

            #heard {
                color: #d1d5db;
                font-size: 13px;
            }

            #historyTitle {
                font-size: 13px;
                font-weight: 600;
                color: #9ca3af;
            }

            QListWidget {
                background-color: #0b1220;
                border: 1px solid #1f2937;
                border-radius: 12px;
                padding: 6px;
                color: #d1d5db;
                font-size: 12px;
            }

            QListWidget::item {
                padding: 7px;
                border-radius: 7px;
            }

            QListWidget::item:selected {
                background-color: #1e293b;
            }

            QPushButton {
                background-color: #1f2937;
                color: #f3f4f6;
                border: none;
                border-radius: 10px;
                padding: 10px 14px;
                font-size: 12px;
                font-weight: 600;
            }

            QPushButton:hover {
                background-color: #2d3a4f;
            }

            QPushButton:pressed {
                background-color: #374151;
            }

            #startButton {
                background-color: #2563eb;
            }

            #startButton:hover {
                background-color: #3b82f6;
            }

            #scriptButton {
                background-color: #172033;
            }

            #closeButton {
                background-color: transparent;
                color: #9ca3af;
                font-size: 16px;
                padding: 4px 8px;
            }

            #closeButton:hover {
                color: #ffffff;
                background-color: #1f2937;
            }
        """)

        # --------------------------------------------------
        # HEADER
        # --------------------------------------------------

        title = QLabel("Bryan Assistant")
        title.setObjectName("title")

        subtitle = QLabel("Your desktop command assistant")
        subtitle.setObjectName("subtitle")

        close_button = QPushButton("×")
        close_button.setObjectName("closeButton")
        close_button.setFixedSize(32, 32)
        close_button.clicked.connect(self.hide)

        header_left = QVBoxLayout()
        header_left.setSpacing(2)
        header_left.addWidget(title)
        header_left.addWidget(subtitle)

        header = QHBoxLayout()
        header.addLayout(header_left)
        header.addStretch()
        header.addWidget(close_button)

        # --------------------------------------------------
        # STATUS
        # --------------------------------------------------

        self.status_label = QLabel("● NOT LISTENING")
        self.status_label.setObjectName("status")

        self.info_label = QLabel(
            'Press "Start Listening" to activate Bryan.'
        )

        self.info_label.setWordWrap(True)
        self.info_label.setObjectName("heard")

        # --------------------------------------------------
        # HISTORY
        # --------------------------------------------------

        history_title = QLabel("RECENT COMMANDS")
        history_title.setObjectName("historyTitle")

        self.history_list = QListWidget()

        # --------------------------------------------------
        # BUTTONS
        # --------------------------------------------------

        self.start_button = QPushButton(
            "🎙  Start Listening"
        )

        self.pause_button = QPushButton(
            "⏸  Pause"
        )

        self.script_button = QPushButton(
            "＋  Scripts"
        )

        self.start_button.setObjectName("startButton")
        self.script_button.setObjectName("scriptButton")

        self.start_button.clicked.connect(
            self.start_listening
        )

        self.pause_button.clicked.connect(
            self.pause_listening
        )

        self.script_button.clicked.connect(
            self.open_script_manager
        )

        buttons_top = QHBoxLayout()

        buttons_top.addWidget(self.start_button)
        buttons_top.addWidget(self.pause_button)

        # --------------------------------------------------
        # MAIN LAYOUT
        # --------------------------------------------------

        layout = QVBoxLayout(self.container)

        layout.setContentsMargins(
            18,
            18,
            18,
            18
        )

        layout.setSpacing(12)

        layout.addLayout(header)

        layout.addSpacing(4)

        layout.addWidget(self.status_label)
        layout.addWidget(self.info_label)

        layout.addSpacing(5)

        layout.addWidget(history_title)
        layout.addWidget(self.history_list)

        layout.addLayout(buttons_top)

        layout.addWidget(self.script_button)

        outer_layout = QVBoxLayout(self)

        outer_layout.setContentsMargins(
            4,
            4,
            4,
            4
        )

        outer_layout.addWidget(self.container)

    # --------------------------------------------------
    # SYSTEM TRAY
    # --------------------------------------------------

    def setup_tray(self):

        self.tray = QSystemTrayIcon(self)

        icon = QApplication.style().standardIcon(
            QStyle.StandardPixmap.SP_ComputerIcon
        )

        self.tray.setIcon(icon)

        self.tray.setToolTip(
            "Bryan Assistant"
        )

        tray_menu = QMenu()

        show_action = QAction(
            "Show Bryan Assistant",
            self
        )

        start_action = QAction(
            "Start Listening",
            self
        )

        pause_action = QAction(
            "Pause",
            self
        )

        scripts_action = QAction(
            "Scripts",
            self
        )

        quit_action = QAction(
            "Exit",
            self
        )

        show_action.triggered.connect(
            self.show_popup
        )

        start_action.triggered.connect(
            self.start_listening
        )

        pause_action.triggered.connect(
            self.pause_listening
        )

        scripts_action.triggered.connect(
            self.open_script_manager
        )

        quit_action.triggered.connect(
            QApplication.quit
        )

        tray_menu.addAction(show_action)
        tray_menu.addSeparator()
        tray_menu.addAction(start_action)
        tray_menu.addAction(pause_action)
        tray_menu.addSeparator()
        tray_menu.addAction(scripts_action)
        tray_menu.addSeparator()
        tray_menu.addAction(quit_action)

        self.tray.setContextMenu(tray_menu)

        self.tray.activated.connect(
            self.tray_clicked
        )

        self.tray.show()

    # --------------------------------------------------
    # POPUP POSITION
    # --------------------------------------------------

    def show_popup(self):

        self.adjustSize()

        screen = QApplication.primaryScreen()

        if not screen:
            self.show()
            return

        available = screen.availableGeometry()

        x = (
            available.right()
            - self.width()
            - 12
        )

        y = (
            available.bottom()
            - self.height()
            - 12
        )

        self.move(QPoint(x, y))

        self.show()
        self.raise_()
        self.activateWindow()

    # --------------------------------------------------
    # TRAY CLICK
    # --------------------------------------------------

    def tray_clicked(self, reason):

        if (
            reason
            == QSystemTrayIcon.ActivationReason.Trigger
        ):

            if self.isVisible():
                self.hide()
            else:
                self.show_popup()

    # --------------------------------------------------
    # START LISTENING
    # --------------------------------------------------

    def start_listening(self):

        if (
            self.voice_worker
            and self.voice_worker.isRunning()
        ):
            return

        self.info_label.setText(
            "Bryan is listening for your commands..."
        )

        self.voice_worker = VoiceWorker()

        self.voice_worker.status_changed.connect(
            self.update_status
        )

        self.voice_worker.command_received.connect(
            self.command_received
        )

        self.voice_worker.speech_received.connect(
            self.speech_received
        )

        self.voice_worker.start()

    # --------------------------------------------------
    # PAUSE
    # --------------------------------------------------

    def pause_listening(self):

        if (
            self.voice_worker
            and self.voice_worker.isRunning()
        ):

            self.voice_worker.requestInterruption()

        self.status_label.setText(
            "● PAUSED"
        )

        self.info_label.setText(
            "Voice commands are currently paused."
        )

    # --------------------------------------------------
    # STATUS
    # --------------------------------------------------

    def update_status(self, status):

        self.status_label.setText(status)

    # --------------------------------------------------
    # SPEECH
    # --------------------------------------------------

    def speech_received(self, speech):

        self.info_label.setText(
            f'Heard: "{speech}"'
        )

    # --------------------------------------------------
    # COMMAND RESULT
    # --------------------------------------------------

    def command_received(self, result):

        self.info_label.setText(result)

        if result.startswith("Executing:"):

            history_text = f"✓  {result}"

        else:

            history_text = f"✗  {result}"

        self.history_list.insertItem(
            0,
            history_text
        )

    # --------------------------------------------------
    # SCRIPT MANAGER
    # --------------------------------------------------

    def open_script_manager(self):

        dialog = ScriptManager(self)

        dialog.exec()

    # --------------------------------------------------
    # HIDE ON CLOSE
    # --------------------------------------------------

    def closeEvent(self, event):

        event.ignore()

        self.hide()


# ======================================================
# APPLICATION
# ======================================================

if __name__ == "__main__":

    app = QApplication(sys.argv)

    app.setQuitOnLastWindowClosed(False)

    window = BryanAssistant()

    window.show_popup()

    sys.exit(app.exec())