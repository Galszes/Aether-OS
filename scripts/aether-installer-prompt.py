#!/usr/bin/python3
"""Aether OS Live Environment Prompt (replaces kubuntu-installer-prompt)."""

import os
import subprocess
import sys
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

LOGO_PATH = "/etc/calamares/branding/kubuntu/icon.png"


class AetherPrompt(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.proc: subprocess.Popen | None = None
        self.setWindowTitle("Try or Install Aether OS")
        self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint)
        self.setStyleSheet(
            """
            QWidget#root {
                background-color: #0b1120;
                color: #f8fafc;
            }
            QPushButton {
                background-color: #1e293b;
                color: #f8fafc;
                border: 1px solid #334155;
                border-radius: 12px;
                padding: 18px 34px;
                font-size: 18px;
                font-weight: 600;
                min-width: 220px;
            }
            QPushButton:hover {
                background-color: #334155;
                border-color: #38bdf8;
            }
            QPushButton#installBtn {
                background-color: #0284c7;
                border-color: #38bdf8;
            }
            QPushButton#installBtn:hover {
                background-color: #0369a1;
            }
            """
        )
        self.setObjectName("root")

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(20)

        logo_label = QLabel()
        logo_label.setAlignment(Qt.AlignCenter)
        if os.path.exists(LOGO_PATH):
            pm = QPixmap(LOGO_PATH).scaled(
                140, 140, Qt.KeepAspectRatio, Qt.SmoothTransformation
            )
            logo_label.setPixmap(pm)
        layout.addWidget(logo_label)

        title = QLabel("Try or Install Aether OS")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 32px; font-weight: 700; color: #f8fafc;")
        layout.addWidget(title)

        subtitle = QLabel("Aether OS 24.04 LTS — Agentic AI Operating System")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet("font-size: 16px; color: #94a3b8; margin-bottom: 16px;")
        layout.addWidget(subtitle)

        self.btn_row = QWidget()
        btn_layout = QHBoxLayout(self.btn_row)
        btn_layout.setSpacing(24)

        try_btn = QPushButton("Try Aether OS")
        try_btn.clicked.connect(self.on_try)
        btn_layout.addWidget(try_btn)

        install_btn = QPushButton("Install Aether OS")
        install_btn.setObjectName("installBtn")
        install_btn.clicked.connect(self.on_install)
        btn_layout.addWidget(install_btn)

        layout.addWidget(self.btn_row)

        self.timer = QTimer(self)
        self.timer.setInterval(500)
        self.timer.timeout.connect(self.check_calamares)

    def on_try(self) -> None:
        QApplication.quit()

    def on_install(self) -> None:
        self.btn_row.hide()
        self.proc = subprocess.Popen(["sudo", "-E", "calamares", "-D8"])
        self.timer.start()

    def check_calamares(self) -> None:
        if self.proc is not None and self.proc.poll() is not None:
            self.timer.stop()
            QApplication.quit()


def main() -> int:
    app = QApplication(sys.argv)
    w = AetherPrompt()
    w.showFullScreen()
    return app.exec_()


if __name__ == "__main__":
    raise SystemExit(main())
