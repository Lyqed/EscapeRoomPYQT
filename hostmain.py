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
        self.correct_sequences = ['1111', '2222', '3333', '4444', '5555']
        self.selected_index = 0
        self.sequences = ['' for _ in range(5)]
        self.labels = []
        self.buttons = []
        self.solved_sequences = []  # Initialize before calling initUI
        self.initUI()



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
            current_sequence = self.sequences[i]
            if current_sequence in self.solved_sequences:  # Check if sequence is solved
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

            while True:
                if key == Qt.Key_Right:
                    new_index += 1
                else:  # Qt.Key_Left
                    new_index -= 1

                print(f"New Index: {new_index}, Labels Length: {len(self.labels)}")  # Debug statement

                if new_index < 0 or new_index >= len(self.labels):
                    break

                if self.sequences[new_index] not in self.solved_sequences:
                    self.selected_index = new_index
                    break

            self.highlightSelectedRectangle()


        elif key in range(Qt.Key_0, Qt.Key_9 + 1) or key in range(Qt.Key_A, Qt.Key_Z + 1):
            current_sequence = self.sequences[self.selected_index]
            if current_sequence not in self.solved_sequences:
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
        if current_sequence in self.correct_sequences and current_sequence not in self.solved_sequences:
            # Correct sequence is entered
            self.the_index_to_mark_as_green = self.selected_index
            self.buttons[self.selected_index].setStyleSheet("color: green;")
            self.buttons[self.selected_index].setText('✔️')
            self.solved_sequences.append(current_sequence)  # Add solved sequence
            self.moveToNextUnsolvedSequence()
        else:
            # Incorrect sequence is entered
            self.markAsIncorrect(self.selected_index)

        # Check if all sequences are solved
        self.checkAllSequencesSolved()

    def markAsIncorrect(self, index):
        self.labels[index].setStyleSheet("border: 1px solid;")
        self.buttons[index].setStyleSheet("color: red;")
        self.buttons[index].setText('❌')

    def moveToNextUnsolvedSequence(self):
        for i in range(1, len(self.correct_sequences)):
            next_index = (self.selected_index + i) % len(self.correct_sequences)
            if self.sequences[next_index] not in self.solved_sequences:
                self.selected_index = next_index
                break
        self.highlightSelectedRectangle()


    def checkAllSequencesSolved(self):
        if all(seq in self.solved_sequences for seq in self.correct_sequences):
            self.startAnimation()
            
    def startAnimation(self):
        self.anim_index = 0
        self.anim_speed = 50  # Start with slower speed
        self.is_accelerating = True  # Flag to check if accelerating or decelerating
        self.anim_timer = QTimer(self)
        self.anim_timer.timeout.connect(self.animateHighlight)
        self.anim_timer.start(self.anim_speed)

    def animateHighlight(self):
        # Update label positions
        for i, label in enumerate(self.labels):
            new_y = label.y() + 10  # Move down
            if new_y > self.height():
                new_y = -label.height()  # Reset to top
            label.move(label.x(), new_y)

        # Adjust animation speed
        if self.is_accelerating:
            self.anim_speed = min(200, self.anim_speed + 5)  # Accelerate
            if self.anim_speed == 200:
                self.is_accelerating = False
        else:
            self.anim_speed = max(50, self.anim_speed - 5)  # Decelerate

        self.anim_timer.setInterval(self.anim_speed)

        # Stop animation condition
        if not self.is_accelerating and self.anim_speed == 50:
            self.anim_timer.stop()
            QTimer.singleShot(20, self.showImage)  # Delay to show image

        
 

    def showImage(self):
        image_label = QLabel(self)
        pixmap = QPixmap('C:\Stoarge\Filen\Escape room project\libary.png')
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
