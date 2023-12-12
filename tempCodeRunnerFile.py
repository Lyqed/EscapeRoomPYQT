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

            self.highlightSelectedRectangleInYellow()

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