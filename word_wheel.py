# Solve the Word Wheel Puzzle
import sys


class WordWheelSolver:
    DICTIONARY_FILE_NAME = "./word_list.txt"

    def __init__(self, num_rings):
        self.num_rings: int = num_rings
        self.all_words: list = []
        self.ring: list[list] = [None] * self.num_rings
        self.num_wheel_letters = 26
        self.last_word = ""

        # Create a list of words from the dictionary file
        with open(WordWheelSolver.DICTIONARY_FILE_NAME, "r") as f:
            words = f.read().splitlines()
        # Remove words that start with a capital letter and are not self.num_rings long
        self.all_words = [word for word in words if word[0].islower() and len(word) == self.num_rings]

        # Create a list of a list letters A to Z in alphabetical order
        self.ring[0] = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ".lower())
        for i in range(1, self.num_rings):
            self.ring[i] = self.ring[0].copy()    
            
        self.num_wheel_letters = len(self.ring[0])
        self.last_word = self.get_last_word()

    def get_last_word(self):
        last_word = ""
        for i in range(self.num_rings):
            # Get the last letter of each ring to make ending word
            last_word += self.ring[i][len(self.ring[i])-1]
        return last_word

    def IsWord(self, word):
        # Check if the word is in the list
        return word in self.all_words

    def remove_word_from_list(self, word):
        # Since we found this word, remove it from the list so we don't find it again
        self.all_words.remove(word)

    def find_additional_words_at_this_position(self, first_word):
        words_at_this_position = first_word
        # Look for other words at this position
        for i in range(1, self.num_wheel_letters):
            next_word = self.ring[0][i]
            for j in range(1, self.num_rings):
                next_word += self.ring[j][i]
            if self.IsWord(next_word):
                # Since we found this word, remove it from the list so we don't find it again
                self.remove_word_from_list(next_word)
                words_at_this_position += " " + next_word
        return words_at_this_position

    def rotate_rings(self):
        # Rotate the rings
        self.ring[self.num_rings-1] = self.ring[self.num_rings-1][1:] + self.ring[self.num_rings-1][:1]
        wrapped_previous_ring = self.ring[self.num_rings-1][0] == "a"

        for i in range(self.num_rings-2, -1, -1):
            self.ring[i] = self.ring[i][1:] + self.ring[i][:1] if wrapped_previous_ring else self.ring[i]
            wrapped_previous_ring = wrapped_previous_ring and self.ring[i][0] == "a"

    def make_word_from_rings(self):
        word = ""
        for i in range(self.num_rings):
            # Get the first letter of each ring
            word += self.ring[i][0]
        return word

    def solve(self):
        while True:
            word = self.make_word_from_rings()

            # Print word[0].upper() if all letters in word are the same
            print (' ' * self.num_rings * 5, word[0].upper()) if word[0] * self.num_rings == word else None

            if word == self.last_word:
                break

            if self.IsWord(word):
                # Since we found this word, remove it from the list so we don't find it again
                self.remove_word_from_list(word)
                words_at_this_position = self.find_additional_words_at_this_position(word)
                print(words_at_this_position) if len(words_at_this_position) > self.num_rings else None

            self.rotate_rings()

if __name__ == "__main__":
    # Handle word length command line argument
    if len(sys.argv) > 1:
        try:
            NUM_RINGS = int(sys.argv[1])
        except ValueError:
            print("Invalid argument. Using default of 4.")
            NUM_RINGS = 4
    else:
        NUM_RINGS = 4

    wws = WordWheelSolver(NUM_RINGS)
    wws.solve()