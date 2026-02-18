from os import listdir
from psychopy import visual, event
from task_funcs import (
    adjust_sizes,
    text_display,
    preload_comprehension_instructions,
    instructions,
    comprehension
)
from config import (
    IMG_PATH,
    SIZES,
    SIZE_SCALE_COMPREHENSION,
    INSTRUCTIONS_KEYS,
    COMPREHENSION_ANSWERS
)

# Run training or oneback comprehension test
PHASE = input('Enter phase "training" or "oddball" or "oneback": ')

# Load instructions images
fnames_to_load = []
for fname in listdir(f'{IMG_PATH}/instructions'):
    if (PHASE in fname) or (PHASE == 'training' and 'welcome' in fname):
        fpath = f'{IMG_PATH}/instructions/{fname}'
        fnames_to_load.append(fpath)

# Create window in fullscreen with cursor off
win = visual.Window(fullscr=True, color='black', units='pix')
win.mouseVisible = False

# Set sizes relative to window height
win_h = win.size[1]*SIZE_SCALE_COMPREHENSION
adjust_sizes(SIZES, win_h)

# Preload stimuli
text_display(win, 'Loading stimuli...')
screen_objects = preload_comprehension_instructions(win, fnames_to_load, SIZES)

# Run instructions and test loop
passed = False
while not passed:

    # Show instructions
    instructions(
        win,
        screen_objects, 
        INSTRUCTIONS_KEYS
    )

    text_display(
        win,
        'You will now be tested on your understanding of the instructions. Press any key to begin.')
    event.waitKeys()

    # Run comprehension test
    passed = comprehension(
        win,
        screen_objects,
        COMPREHENSION_ANSWERS[PHASE]
    )

    if not passed:
        text_display(
            win,
            'That was not correct. Please read the instructions carefully and try again. Press any key to continue.')
        event.waitKeys()

text_display(win, 'You passed the comprehension test! Please get the experimenter.')
event.waitKeys()
win.close()
