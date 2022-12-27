# Solve the Word Wheel Puzzle
import sys


class Dictionary:
    DICTIONARY_FILE_NAME = "./word_list.txt"

    def __init__(self, word_len_filter: int = 4) -> None:
        self.filename: str = Dictionary.DICTIONARY_FILE_NAME
        self.all_words: list[str] = []
        self.load(word_len_filter)

    def load(self, word_len_filter: int) -> None:
        # Create a list of words from the dictionary file
        with open(self.filename, "r") as f:
            words: list = f.read().splitlines()
        # Remove words that start with a capital letter and are not word_len_filter long
        self.all_words = [word for word in words if word[0].islower() and len(word) == word_len_filter]

    def is_word(self, word: str) -> bool:
        return word in self.all_words

    def remove_word(self, word: str) -> None:
        self.all_words.remove(word)


class WordWheelSolver:
    def __init__(self, num_rings: int) -> None:
        self.num_rings: int = num_rings
        self.ring: list[list] = [None] * self.num_rings
        self.num_wheel_letters: int = 26
        self.last_word: str = ""
        self.dictionary: Dictionary = Dictionary(self.num_rings)

        # Create a list of a list letters A to Z in alphabetical order
        self.ring[0] = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ".lower())
        for i in range(1, self.num_rings):
            self.ring[i] = self.ring[0].copy()    
            
        self.num_wheel_letters: int = len(self.ring[0])
        self.last_word = self.get_last_word()

    def get_last_word(self) -> str:
        last_word: str = ""
        for i in range(self.num_rings):
            # Get the last letter of each ring to make ending word
            last_word += self.ring[i][len(self.ring[i])-1]
        return last_word

    def find_additional_words_at_this_position(self, first_word) -> str:
        words_at_this_position: str = first_word
        # Look for other words at this position
        for i in range(1, self.num_wheel_letters):
            next_word = self.ring[0][i]
            for j in range(1, self.num_rings):
                next_word += self.ring[j][i]
            if self.dictionary.is_word(next_word):
                # Since we found this word, remove it from the list so we don't find it again
                self.dictionary.remove_word(next_word)
                words_at_this_position += " " + next_word
        return words_at_this_position

    def rotate_rings(self) -> None:
        # Rotate the rings
        self.ring[self.num_rings-1] = self.ring[self.num_rings-1][1:] + self.ring[self.num_rings-1][:1]
        wrapped_previous_ring: bool = self.ring[self.num_rings-1][0] == "a"

        for i in range(self.num_rings-2, -1, -1):
            self.ring[i] = self.ring[i][1:] + self.ring[i][:1] if wrapped_previous_ring else self.ring[i]
            wrapped_previous_ring = wrapped_previous_ring and self.ring[i][0] == "a"

    def make_word_from_rings(self) -> str:
        word: str = ""
        for i in range(self.num_rings):
            # Get the first letter of each ring
            word += self.ring[i][0]
        return word

    def solve(self) -> None:
        while True:
            word: str = self.make_word_from_rings()

            # Print word[0].upper() if all letters in word are the same
            print (' ' * self.num_rings * 5, word[0].upper()) if word[0] * self.num_rings == word else None

            if word == self.last_word:
                break

            if self.dictionary.is_word(word):
                # Since we found this word, remove it from the list so we don't find it again
                self.dictionary.remove_word(word)
                words_at_this_position: str = self.find_additional_words_at_this_position(word)
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