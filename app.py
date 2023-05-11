import sys
import random
import time
import threading
import pyautogui
import keyboard
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QSlider, QTextEdit, QProgressBar
from PyQt5.QtCore import Qt


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Auto Typer")
        self.setGeometry(100, 100, 400, 250)

        vbox = QVBoxLayout()
        hbox1 = QHBoxLayout()
        self.text_label = QLabel("Enter Text to Type:")
        self.text_edit = QTextEdit()
        hbox1.addWidget(self.text_label)
        hbox1.addWidget(self.text_edit)
        vbox.addLayout(hbox1)

        hbox2 = QHBoxLayout()
        self.countdown_label = QLabel("")
        self.start_button = QPushButton("Start Typing")
        self.start_button.clicked.connect(self.start_typing)
        self.stop_button = QPushButton("Stop Typing")
        self.stop_button.clicked.connect(self.stop_typing)
        hbox2.addWidget(self.countdown_label)
        hbox2.addWidget(self.start_button)
        hbox2.addWidget(self.stop_button)
        keyboard.on_press_key("F9", self.start_typing)
        vbox.addLayout(hbox2)

        hbox3 = QHBoxLayout()
        self.speed_label = QLabel("Typing Speed:")
        self.speed_slider = QSlider(Qt.Horizontal)
        self.speed_slider.setMinimum(100)
        self.speed_slider.setMaximum(500)  # Change maximum value to 500
        self.speed_slider.setValue(0)  # Set initial value to 0
        self.speed_slider.setTickPosition(QSlider.TicksBelow)
        self.speed_slider.setTickInterval(100)
        hbox3.addWidget(self.speed_label)
        hbox3.addWidget(self.speed_slider)
        vbox.addLayout(hbox3)

        self.countdown_bar = QProgressBar()
        self.countdown_bar.setMinimum(0)
        self.countdown_bar.setMaximum(5000)
        self.countdown_bar.setValue(0)
        vbox.addWidget(self.countdown_bar)


        self.setLayout(vbox)
        self.show()

    def start_typing(self):
        self.start_button.setEnabled(False)
        self.stop_button.setEnabled(True)
        text_to_type = self.text_edit.toPlainText()

        speed_factor = self.speed_slider.value() / 100  # Convert slider value to speed factor between 1 and 5

        def countdown():
            for i in range(5000, -1000, -1000):
                self.countdown_bar.setValue(i)
                time.sleep(1)
            self.countdown_label.setText("Typing...")


        countdown_thread = threading.Thread(target=countdown)
        countdown_thread.start()

        time.sleep(5)  # Delay for 5 seconds before starting to type
        self.countdown_label.setText("Typing...")

        for char in text_to_type:
            if char == " ":
                pyautogui.press("space")
                wait_time = random.uniform(0.15, 0.2)  # Random wait time between words
            else:
                pyautogui.typewrite(char)
                wait_time = random.uniform(0.02, 0.04)  # Random wait time between keystrokes
            wait_time /= speed_factor  # Adjust wait time based on speed factor
            time.sleep(wait_time)

            if keyboard.is_pressed("F9"):  # Check for hotkey (F9) to stop typing
                break

        self.countdown_label.setText("Done.")
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)

    def stop_typing(self):
        keyboard.press_and_release("F9")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())
