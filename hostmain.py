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
            button.clicked.connect(self.make_button_handler(i))
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
            self.selected_index = (self.selected_index + 1) % 5 if key == Qt.Key_Right else (self.selected_index - 1) % 5
            self.highlightSelectedRectangle()

        elif key in (Qt.Key_0, Qt.Key_1, Qt.Key_2, Qt.Key_3, Qt.Key_4, Qt.Key_5, Qt.Key_6, Qt.Key_7, Qt.Key_8, Qt.Key_9, Qt.Key_A, Qt.Key_B, Qt.Key_C, Qt.Key_D, Qt.Key_E, Qt.Key_F, Qt.Key_G, Qt.Key_H, Qt.Key_I, Qt.Key_J, Qt.Key_K, Qt.Key_L, Qt.Key_M, Qt.Key_N, Qt.Key_O, Qt.Key_P, Qt.Key_Q, Qt.Key_R, Qt.Key_S, Qt.Key_T, Qt.Key_U, Qt.Key_V, Qt.Key_W, Qt.Key_X, Qt.Key_Y, Qt.Key_Z):
            current_sequence = self.sequences[self.selected_index]
            if len(current_sequence) < 4:
                self.sequences[self.selected_index] += event.text().upper()
                self.labels[self.selected_index].setText(self.sequences[self.selected_index])

        elif key == Qt.Key_Backspace and self.sequences[self.selected_index]:
            self.sequences[self.selected_index] = self.sequences[self.selected_index][:-1]
            self.labels[self.selected_index].setText(self.sequences[self.selected_index])

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    ex = EscapeRoomApp()
    sys.exit(app.exec_())
