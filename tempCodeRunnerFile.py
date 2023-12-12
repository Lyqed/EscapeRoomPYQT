def checkSequence(self):
        current_sequence = self.sequences[self.selected_index]
        if current_sequence in self.correct_sequences:
            index = self.correct_sequences.index(current_sequence)
            if not self.solved_sequences[index]:
                # Correctly mark and highlight the sequence
                self.labels[index].setStyleSheet("border: 2px solid green;")
                self.buttons[index].setStyleSheet("color: green;")
                self.buttons[index].setText('✔️')
                self.buttons[index].setEnabled(False)
                self.solved_sequences[index] = True

                self.checkAllSequencesSolved()

                # We need to find and highlight the next unsolved sequence
                self.moveToNextUnsolvedSequence()
            else:
                # If the sequence is already solved, mark the current sequence as incorrect
                self.markAsIncorrect(self.selected_index)
        else:
            # If the sequence does not match any correct sequence, mark it as incorrect
            self.markAsIncorrect(self.selected_index)

    def markAsIncorrect(self, index):
        self.labels[index].setStyleSheet("border: 1px solid;")
        self.buttons[index].setStyleSheet("color: red;")
        self.buttons[index].setText('❌')

    def moveToNextUnsolvedSequence(self):
        next_index = (self.selected_index + 1) % len(self.solved_sequences)
        while self.solved_sequences[next_index] and next_index != self.selected_index:
            next_index = (next_index + 1) % len(self.solved_sequences)

        if not self.solved_sequences[next_index]:
            self.selected_index = next_index
        self.highlightSelectedRectangle()