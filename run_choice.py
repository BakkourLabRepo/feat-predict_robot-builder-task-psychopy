import json
import pickle
from os import listdir, makedirs
import numpy as np
import pandas as pd
from psychopy import visual, core, event
from task_funcs import (
    get_fnames_to_load,
    adjust_sizes,
    adjust_positions,
    text_display,
    preload_stimuli,
    preload_covertask_stimuli,
    preload_comprehension_instructions,
    get_feature_label_from_fname,
    comprehension,
    instructions,
    fingers_to_keys,
    countdown,
    run_trial,
    run_encoding_trial
)
from config import (
    DEBUG,
    SHOW_INSTRUCTIONS,
    DATA_PATH,
    IMG_PATH,
    TIMES,
    ENCODING_TIMES,
    CATEGORY_REPEATS,
    POST_RUN_DELAY,
    COMPREHENSION_ANSWERS,
    SIZES,
    SIZE_SCALE,
    POSITIONS,
    KEYS,
    INSTANCE_TMAT,
    FEATURE_TMAT,
    INSTRUCTIONS_KEYS
)


########################################################################
### Setup session ######################################################
########################################################################

# Input session parameters
SUBJ = input('Enter subject ID: ')
CONDITION = int(input('Enter condition: '))
SEED = int(input('Enter seed: '))

# Create data directory
DATA_PATH = f'{DATA_PATH}/feat-predict-mri_{SUBJ}'
makedirs(DATA_PATH, exist_ok=True)

# Random seed for reproducibility
np.random.seed(SEED)

# Select feature transition matrix based on condition
feature_tmat = FEATURE_TMAT[CONDITION]

# Load session information
f = open(f'session_info/session-info_{SEED}-{CONDITION}.json')
session_info = json.load(f)
train_trial_info = session_info['train_trial_info']
test_trial_info = session_info['test_trial_info']
train_fnames = session_info['train_fnames']
test_fnames = session_info['test_fnames']
feature_fnames = session_info['feature_fnames']
task_to_stim_feature_map = session_info['task_to_stim_feature_map']
task_to_stim_instance_map = session_info['task_to_stim_instance_map']

# Create window in fullscreen with cursor off
win = visual.Window(fullscr=True, color='black', units='pix')
win.mouseVisible = False

# Set sizes relative to window height
win_h = win.size[1]*SIZE_SCALE
adjust_sizes(SIZES, win_h)
adjust_positions(POSITIONS, win_h)


#######################################################################
### Show Welcome Instructions #########################################
#######################################################################


# Load instructions images
fnames_to_load = []
for fname in listdir(f'{IMG_PATH}/instructions'):
    if 'welcome' in fname:
        fpath = f'{IMG_PATH}/instructions/{fname}'
        fnames_to_load.append(fpath)

# Preload stimuli
text_display(win, 'Loading stimuli...')
screen_objects = preload_covertask_stimuli(
    win,
    fnames_to_load,
    SIZES
)

# Show instructions
if SHOW_INSTRUCTIONS:
    instructions(win, screen_objects, INSTRUCTIONS_KEYS)


#######################################################################
### Run Encoding ######################################################
#######################################################################

# Order feature fnames into categories
feature_fname_categories = {}
for fname in feature_fnames:
    category = get_feature_label_from_fname(fname)
    if category not in feature_fname_categories.keys():
        feature_fname_categories[category] = []
    feature_fname_categories[category].append(fname)

# Load stimulus fnames
fnames_to_load = []
for fname in np.unique(feature_fnames):
    fnames_to_load.append(fname.replace('img', f'{IMG_PATH}/robot_parts'))

# Load instructions images
for fname in listdir(f'{IMG_PATH}/instructions'):
    if 'encoding' in fname:
        fpath = f'{IMG_PATH}/instructions/{fname}'
        fnames_to_load.append(fpath)

# Preload stimuli
text_display(win, 'Loading stimuli...')
screen_objects = preload_covertask_stimuli(
    win,
    fnames_to_load,
    SIZES
)

# Show instructions
if SHOW_INSTRUCTIONS:
    instructions(win, screen_objects, INSTRUCTIONS_KEYS)

# Task clock
running_time = 0
clock = core.Clock()

# Run phase
category_labels = np.array(list(feature_fname_categories.keys()))
for _ in range(CATEGORY_REPEATS):
    category_labels = np.random.permutation(category_labels)
    for category in category_labels:
        instance_labels = np.random.permutation(
            feature_fname_categories[category]
        )
        category_name = category
        for feature_fname in instance_labels:

            # Run trial
            running_time = run_encoding_trial(
                clock = clock,
                running_time = running_time,
                win = win,
                times = ENCODING_TIMES,
                screen_objects = screen_objects,
                item_fname = feature_fname,
                category_name = category_name
            )
            category_name = False


#######################################################################
### Run Comprehension #################################################
#######################################################################

# Load instructions images
fnames_to_load = []
for fname in listdir(f'{IMG_PATH}/instructions'):
    if 'training' in fname:
        fpath = f'{IMG_PATH}/instructions/{fname}'
        fnames_to_load.append(fpath)

# Preload stimuli
text_display(win, 'Loading stimuli...')
screen_objects = preload_comprehension_instructions(
    win,
    fnames_to_load,
    SIZES
    )

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
    passed = comprehension(win, screen_objects, COMPREHENSION_ANSWERS)

    if not passed:
        text_display(
            win,
            'That was not correct. Please read the instructions carefully and try again. Press any key to continue.')
        event.waitKeys()

text_display(win, 'You passed the comprehension test!\n\nYou\'ll now start the real task.\n\nPress any key to continue.')
event.waitKeys()


#######################################################################
### Run Choice Task ###################################################
#######################################################################

for phase in ['training', 'test']:

    # Get stimuli to load based on phase
    if phase == 'training':
        fnames_to_load = get_fnames_to_load(train_fnames, feature_fnames, IMG_PATH)
        phase_trial_info = train_trial_info
    elif phase == 'test':
        fnames_to_load = get_fnames_to_load(test_fnames, feature_fnames, IMG_PATH)
        phase_trial_info = test_trial_info

    # Load instructions images
    if SHOW_INSTRUCTIONS:
        for fname in listdir(f'{IMG_PATH}/instructions'):
            if ('test' in fname) or ('fingers' in fname):
                fpath = f'{IMG_PATH}/instructions/{fname}'
                fnames_to_load.append(fpath)
            

    # Preload stimuli
    text_display(win, 'Loading stimuli...')
    screen_objects = preload_stimuli(win, fnames_to_load, SIZES, POSITIONS)

    # Instructions
    if SHOW_INSTRUCTIONS and (phase == 'test'):
        instructions(win, screen_objects, INSTRUCTIONS_KEYS)

    # Initialize data frame
    data = pd.DataFrame(columns=[
        'id',
        'seed',
        'condition',
        'between_cond',
        'phase',
        'run',
        't',
        'n_steps',
        'target_comb',
        'options_comb',
        'options_fnames',
        'options',
        'correct_composition',
        'composition_fname',
        'composition',
        'successor_fname',
        'successor',
        'target_fname',
        'target',
        'reward',
        'correct',
        'valid_response',
        'rt',
        'selections'
    ])

    # Initialize total points 
    if phase == 'training':
        total_points = 0
    elif phase == 'test':
        total_points = '???'

    for run in range(1, len(phase_trial_info) + 1):

        run_info = {
            'id': SUBJ,
            'seed': SEED,
            'condition': CONDITION,
            'between_cond': int(CONDITION in [1, 2, 5]),
            'phase': phase,
            'run': run
        }

        # Show fingers to keyboard instructions and countdown
        if SHOW_INSTRUCTIONS:
            fingers_to_keys(win, screen_objects, KEYS)
            countdown(win, screen_objects)


        # Global task clock
        running_time = 0
        clock = core.Clock()

        # Run phase
        for t, trial_info in enumerate(phase_trial_info[run - 1]):

            # Run trial
            trial_info = {
                'clock': clock,
                'running_time': running_time,
                'win': win,
                'times': TIMES,
                'screen_objects': screen_objects,
                'positions': POSITIONS,
                'sizes': SIZES,
                'task_to_stim_feature_map': task_to_stim_feature_map,
                'task_to_stim_instance_map': task_to_stim_instance_map,
                'feature_tmat': feature_tmat,
                'instance_tmat': INSTANCE_TMAT,
                'total_points': total_points,
                'keys': KEYS,
                'data': data,
                'run_info': run_info,
                't': t,
                'data_path': DATA_PATH,
                'debug': DEBUG,
                **trial_info
            }
            data, total_points, running_time = run_trial(**trial_info)

        # Post run delay
        screen_objects['+'].draw()
        win.flip()
        running_time += POST_RUN_DELAY
        while clock.getTime() < running_time:
            pass

        # Take break instructions
        if SHOW_INSTRUCTIONS and run != len(phase_trial_info):
            screen_objects['break'].text = f'Take a break!\n\nRound {run} of {len(phase_trial_info)} completed.\n\nPress any key to continue.'
            screen_objects['break'].draw()
            win.flip()
            event.waitKeys()

    print(f'Total points for {phase}: {total_points}')

if SHOW_INSTRUCTIONS:
    text_display(win, 'You\'ve finished the game!\n\nPlease get the experimenter.')
    event.waitKeys()

# Close the window
win.close()
core.quit()