from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel
from PyQt5.QtCore import Qt, QRect, pyqtSlot

class EscapeRoomApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.correct_sequences = ['1234', '5678', 'ABCD', 'EFGH', 'IJKL']
        self.selected_index = 0
        self.sequences = ['' for _ in range(5)]
        self.labels = []
        self.buttons = []

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

            button = QPushButton('O', self)
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
            if i == self.selected_index:
                label.setStyleSheet("background-color: yellow")
            else:
                label.setStyleSheet("background-color: none")

    def resizeEvent(self, event):
        self.updateUI()
        super().resizeEvent(event)

    def keyPressEvent(self, event):
        key = event.key()
        if key in (Qt.Key_Right, Qt.Key_Left):
            # Update selected_index and ensure it stays within bounds
            if key == Qt.Key_Right:
                self.selected_index = (self.selected_index + 1) % len(self.labels)
            else:
                self.selected_index = (self.selected_index - 1) % len(self.labels)

            self.highlightSelectedRectangle()

        elif key in range(Qt.Key_0, Qt.Key_9 + 1) or key in range(Qt.Key_A, Qt.Key_Z + 1):
            current_sequence = self.sequences[self.selected_index]
            if len(current_sequence) < 4:
                self.sequences[self.selected_index] += event.text().upper()
                self.labels[self.selected_index].setText(self.sequences[self.selected_index])
                self.checkSequence(self.selected_index)  # Check the sequence after adding a character

        elif key == Qt.Key_Backspace and self.sequences[self.selected_index]:
            self.sequences[self.selected_index] = self.sequences[self.selected_index][:-1]
            self.labels[self.selected_index].setText(self.sequences[self.selected_index])
            self.checkSequence(self.selected_index)  # Check the sequence after removing a character

        elif key == Qt.Key_F11:
            if self.isFullScreen():
                self.showNormal()
            else:
                self.showFullScreen()

        super().keyPressEvent(event)

        
    def checkSequence(self, index):
        if self.sequences[index] == self.correct_sequences[index]:
            self.buttons[index].setText('✔️')
        else:
            self.buttons[index].setText('❌')



if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    ex = EscapeRoomApp()
    sys.exit(app.exec_())
