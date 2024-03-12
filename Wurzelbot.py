import pyautogui
import sys

FIELD_HEIGHT = 12
FIELD_LEN = 17
FIELD_DIM = 40

DURATION = 0.02
pyautogui.PAUSE = DURATION

I = 204

startX, startY = pyautogui.position()

try:
    if(len(sys.argv) == 2):
        newI = int(sys.argv[1])
        if 0 <= newI <= 204:
            I = newI
except ValueError:
    pass

i = 0
broken = False


for y in range(FIELD_HEIGHT):

    if broken:
        break

    pyautogui.moveTo(startX, startY + FIELD_DIM*y, DURATION)

    for x in range(FIELD_LEN):

        broken = (i==I)

        if broken:
            break

        # pyautogui.click()
        i += 1

        pyautogui.move(FIELD_DIM, 0, DURATION)

