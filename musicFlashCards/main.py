import time
import random
from PIL import Image
import cv2
import numpy as np

class randomLetter:

    def __init__(self):
         pass

    def _showImage(self, letter: str) -> None:
        path = f'{letter}.jpg'
        img = Image.open(path)
        img = np.array(img)
        # Display the image in a resizable window
        cv2.namedWindow("Image", cv2.WINDOW_NORMAL)
        cv2.imshow("Image", img)
        cv2.resizeWindow("Image", 1000, 1000)  # Set the window size
        cv2.waitKey(1500)  # how long letter shows
        cv2.destroyAllWindows()

    def printRandomLetters(self) -> None:
        while True:
            keys = {0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E', 5: 'F', 6: 'G'}
            randomNumba = random.randint(0, 6)
            letter = keys[randomNumba]
            print(letter)
            self._showImage(f'notes/{letter}')
            #time.sleep(1)   # time in between each letter

    def printTrebleClef(self) -> None:
            while True:
                notes = {0: 'middleC', 1: 'd', 2: 'e', 3: 'f', 4: 'g', 5: 'a', 6: 'b', 7: 'c2', 8: 'd2', 9: 'e2', 10: 'f2', 11: 'g2'}
                randomNumba = random.randint(0, 11)
                note = notes[randomNumba]
                print(note)
                self._showImage(f'trebleClef/{note}')
                time.sleep(2)   # time in between each letter

    def printBassClef(self) -> None:
            while True:
                notes = {0: 'a', 1: 'a2', 2: 'b', 3: 'b2', 4: 'c', 5: 'd', 6: 'e', 7: 'f', 8: 'g', 9: 'g2', 10: 'middleC'}
                randomNumba = random.randint(0, 10)
                note = notes[randomNumba]
                print(note)
                self._showImage(f'bassClef/{note}')
                time.sleep(2)   # time in between each letter


game = randomLetter()
game.printTrebleClef()