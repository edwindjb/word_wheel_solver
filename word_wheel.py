# Solve the Word Wheel Puzzle
import sys


def IsWord(word):
    # Check if the word is in the list
    return word in ALL_WORDS


def GenerateStrings(ring, max_length, num_wheel_letters, last_word):
    while True:
        word = ""
        for i in range(max_length):
            # Get the first letter of each ring       
            word += ring[i][0]

        # Print word[0].upper() if all letters in word are the same
        print (' ' * max_length * 5, word[0].upper()) if word[0] * max_length == word else None

        if word == last_word:
            break

        if IsWord(word):
            # Since we found this word, remove it from the list so we don't find it again
            ALL_WORDS.remove(word)
            
            words_at_this_position = word
            # Look for other words at this position
            for i in range(1, num_wheel_letters):
                next_word = ring[0][i]
                for j in range(1, max_length):
                    next_word += ring[j][i]
                if IsWord(next_word):
                    # Since we found this word, remove it from the list so we don't find it again
                    ALL_WORDS.remove(next_word)
            
                    words_at_this_position += " " + next_word
            print(words_at_this_position) if len(words_at_this_position) > max_length else None

        # Rotate the rings
        ring[max_length-1] = ring[max_length-1][1:] + ring[max_length-1][:1]
        wrapped_previous_ring = ring[max_length-1][0] == "a"

        for i in range(max_length-2, -1, -1):
            ring[i] = ring[i][1:] + ring[i][:1] if wrapped_previous_ring else ring[i]
            wrapped_previous_ring = wrapped_previous_ring and ring[i][0] == "a"


def main():
    # Create a list of a list letters A to Z in alphabetical order
    ring = [None] * NUM_RINGS
    ring[0] = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ".lower())
    for i in range(1, NUM_RINGS):
        ring[i] = ring[0].copy()    
        
    NUM_WHEEL_LETTERS = len(ring[0])

    last_word = ""
    try:
        for i in range(NUM_RINGS):
            # Get the last letter of each ring to make ending word
            last_word += ring[i][len(ring[i])-1]

    except IndexError:
        print(f"IndexError: {i=} is too long")
        return

    GenerateStrings(ring, NUM_RINGS, NUM_WHEEL_LETTERS, last_word)


if __name__ == "__main__":
    # Handle word length command line argument
    if len(sys.argv) > 1:
        NUM_RINGS = int(sys.argv[1])
    else:
        NUM_RINGS = 4
        
    ALL_WORDS = []
    DICTIONARY_FILE_NAME = "./word_list.txt"

    # Create a list of words from the dictionary file
    with open(DICTIONARY_FILE_NAME, "r") as f:
        words = f.read().splitlines()
    # Remove words that start with a capital letter and are not NUM_RINGS long
    ALL_WORDS = [word for word in words if word[0].islower() and len(word) == NUM_RINGS]

    exit(main())