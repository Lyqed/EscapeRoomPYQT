from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QWidget
from PyQt5.QtCore import Qt, QRect, QTimer, pyqtSlot
from PyQt5.QtGui import QPixmap
import os


class NoHoverButton(QPushButton):
    def __init__(self, *args, **kwargs):
        super(NoHoverButton, self).__init__(*args, **kwargs)
        self.setStyleSheets()

    def setStyleSheets(self):
        self.setStyleSheet("""
            QPushButton {
                /* Define your normal button styles here */
                background-color: transparent; /* Example style */
                border: none; /* Example style */
            }
            QPushButton:hover {
                /* Repeat the same styles for the hover state */
                background-color: transparent;
                border: none;
            }
            QPushButton:pressed {
                /* Optionally, define styles for when the button is pressed */
                /* Example: slightly different background color */
                background-color: lightgray;
            }
        """)


class EscapeRoomApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.correct_sequences = ['1234', 'DADW', 'KOBE', 'YOS1', 'D837']
        self.selected_index = 0
        self.sequences = ['' for _ in range(5)]
        self.labels = []
        self.buttons = []
        self.initUI()
        self.solved_sequences = [False for _ in range(5)]  # Track solved sequences


    def initUI(self):
        self.setWindowTitle('Escape Room App')
        self.setGeometry(100, 100, 800, 600)  # Temporary smaller size for debugging
        # self.showFullScreen()  # Comment out for debugging

        # Create labels and buttons
        for i in range(5):
            label = QLabel('', self)
            label.setAlignment(Qt.AlignCenter)
            label.setFrameShape(QLabel.Box)
            label.setLineWidth(1)
            self.labels.append(label)
        
            button = NoHoverButton('O', self)
            button.setFocusPolicy(Qt.NoFocus)  # Set the focus policy to NoFocus
            self.buttons.append(button)

        self.updateUI()
        self.show()

    def make_button_handler(self, index):
        @pyqtSlot()
        def button_handler():
            # Debug print
            print(f"Button {index} clicked, sequence: {self.sequences[index]}")
            
            if self.sequences[index] == self.correct_sequences[index]:
                self.buttons[index].setText('✔️')
            else:
                self.buttons[index].setText('❌')
        return button_handler

    def updateUI(self):
        rect_width = 100
        total_width = 5 * rect_width + 4 * 50
        start_x = (self.width() - total_width) // 2

        for i in range(5):
            x_pos = start_x + i * (rect_width + 50)
            self.labels[i].setGeometry(x_pos, 200, rect_width, 50)
            self.buttons[i].setGeometry(x_pos, 260, rect_width, 30)

        self.highlightSelectedRectangle()

    def highlightSelectedRectangle(self):
        for i, label in enumerate(self.labels):
            if self.sequences[i] == self.correct_sequences[i]:  # Maintain green border for solved sequences
                label.setStyleSheet("border: 2px solid green;")
            elif i == self.selected_index:
                label.setStyleSheet("background-color: yellow; border: 1px solid;")  # Highlight selected
            else:
                label.setStyleSheet("background-color: none; border: 1px solid;")  # Default style


    def resizeEvent(self, event):
        self.updateUI()
        super().resizeEvent(event)

    def keyPressEvent(self, event):
        key = event.key()
        if key in (Qt.Key_Right, Qt.Key_Left):
            new_index = self.selected_index

            # Attempt to find the next unsolved sequence index
            while True:
                if key == Qt.Key_Right:
                    new_index += 1
                else:  # Qt.Key_Left
                    new_index -= 1

                # If we go out of bounds, just break and do not update the index
                if new_index < 0 or new_index >= len(self.labels):
                    break

                # If we find an unsolved sequence, update the index and break
                if self.sequences[new_index] != self.correct_sequences[new_index]:
                    self.selected_index = new_index
                    break

            self.highlightSelectedRectangle()

        # Rest of the keyPressEvent code remains the same


        elif key in range(Qt.Key_0, Qt.Key_9 + 1) or key in range(Qt.Key_A, Qt.Key_Z + 1):
            if not self.solved_sequences[self.selected_index]:
                current_sequence = self.sequences[self.selected_index]
                if len(current_sequence) < 4:  # Allow up to four characters
                    self.sequences[self.selected_index] += event.text().upper()
                    self.labels[self.selected_index].setText(self.sequences[self.selected_index])

                    if len(self.sequences[self.selected_index]) == 4:
                        self.checkSequence()

        elif key == Qt.Key_Backspace:
            if self.sequences[self.selected_index] != self.correct_sequences[self.selected_index]:  # Check if the current sequence is not yet solved
                if self.sequences[self.selected_index]:
                    self.sequences[self.selected_index] = self.sequences[self.selected_index][:-1]
                    self.labels[self.selected_index].setText(self.sequences[self.selected_index])

        elif key == Qt.Key_F11:
            if self.isFullScreen():
                self.showNormal()
            else:
                self.showFullScreen()

        super().keyPressEvent(event)

    def checkSequence(self):
        current_sequence = self.sequences[self.selected_index]
        if current_sequence == self.correct_sequences[self.selected_index]:
            # Marking the current sequence as correct and highlighting it
            self.labels[self.selected_index].setStyleSheet("border: 2px solid green;")
            self.buttons[self.selected_index].setStyleSheet("color: green;")
            self.buttons[self.selected_index].setText('✔️')
            self.solved_sequences[self.selected_index] = True

            self.moveToNextUnsolvedSequence()  # Move to the next unsolved sequence
        else:
            # Mark the current sequence as incorrect
            self.markAsIncorrect(self.selected_index)

        # Check if all sequences are solved
        self.checkAllSequencesSolved()

    def markAsIncorrect(self, index):
        self.labels[index].setStyleSheet("border: 1px solid;")
        self.buttons[index].setStyleSheet("color: red;")
        self.buttons[index].setText('❌')

    def moveToNextUnsolvedSequence(self):
        # Find the next sequence that is not yet solved
        for i in range(1, len(self.solved_sequences)):
            next_index = (self.selected_index + i) % len(self.solved_sequences)
            if not self.solved_sequences[next_index]:
                self.selected_index = next_index
                break
        self.highlightSelectedRectangle()


    def checkAllSequencesSolved(self):
        if all(seq == correct for seq, correct in zip(self.sequences, self.correct_sequences)):
            self.startAnimation()
            
    def startAnimation(self):
        self.anim_index = 0
        self.anim_speed = 200  # Initial speed in milliseconds
        self.anim_timer = QTimer(self)
        self.anim_timer.timeout.connect(self.animateHighlight)
        self.anim_timer.start(self.anim_speed)
        
    
    def animateHighlight(self):
        # Reset all to default style
        for label in self.labels:
            label.setStyleSheet("background-color: none; border: 1px solid;")

        # Highlight current index
        self.labels[self.anim_index].setStyleSheet("background-color: yellow; border: 1px solid;")

        # Increase animation speed
        self.anim_speed = max(50, self.anim_speed - 10)  # Decrease time for faster cycling
        self.anim_timer.setInterval(self.anim_speed)

        # Move to next index or end animation
        self.anim_index = (self.anim_index + 1) % len(self.labels)
        if self.anim_speed == 50:  # When speed is at its maximum
            self.anim_timer.stop()
            QTimer.singleShot(3000, self.showImage)  # Show image after 3 seconds
        
 

    def showImage(self):
        image_label = QLabel(self)
        pixmap = QPixmap('library.png')
        if pixmap.isNull():
            print("Failed to load the image.")
            return

        image_label.setPixmap(pixmap.scaled(self.size(), Qt.KeepAspectRatioByExpanding))
        image_label.setGeometry(0, 0, self.width(), self.height())  # Cover the entire window
        image_label.show()


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    ex = EscapeRoomApp()
    sys.exit(app.exec_())
