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
    instructions,
    run_trial
)
from config import (
    DEBUG,
    SHOW_INSTRUCTIONS,
    DATA_PATH,
    IMG_PATH,
    TIMES,
    POST_RUN_DELAY,
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
PHASE = input('Enter phase "training" or "test": ')
while True:
    if PHASE in ['training', 'test']:
        break
    PHASE = input('Invalid phase. Enter phase "training" or "test": ')

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

# Get stimuli to load based on phase
if PHASE == 'training':
    fnames_to_load = get_fnames_to_load(train_fnames, feature_fnames, IMG_PATH)
    phase_trial_info = train_trial_info
elif PHASE == 'test':
    fnames_to_load = get_fnames_to_load(test_fnames, feature_fnames, IMG_PATH)
    phase_trial_info = test_trial_info

# Load instructions images
if SHOW_INSTRUCTIONS:
    for fname in listdir(f'{IMG_PATH}/instructions'):
        if (PHASE in fname) and ('comprehension' not in fname):
            fpath = f'{IMG_PATH}/instructions/{fname}'
            fnames_to_load.append(fpath)

# Create window in fullscreen with cursor off
win = visual.Window(fullscr=True, color='black', units='pix')
win.mouseVisible = False

# Set sizes relative to window height
win_h = win.size[1]*SIZE_SCALE
adjust_sizes(SIZES, win_h)
adjust_positions(POSITIONS, win_h)

# Preload stimuli
text_display(win, 'Loading stimuli...')
screen_objects = preload_stimuli(win, fnames_to_load, SIZES, POSITIONS)


########################################################################
### Run task ##########################################################
########################################################################

# Instructions
if SHOW_INSTRUCTIONS:
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
if PHASE == 'training':
    total_points = 0
elif PHASE == 'test':
    total_points = '???'

for run in range(1, len(phase_trial_info) + 1):

    run_info = {
        'id': SUBJ,
        'seed': SEED,
        'condition': CONDITION,
        'between_cond': int(CONDITION in [1, 2, 5]),
        'phase': PHASE,
        'run': run
    }

    # Take break instructions
    #if SHOW_INSTRUCTIONS:
    #    instructions(win, screen_objects, INSTRUCTIONS_KEYS)

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

print(f'Total points for {PHASE}: {total_points}')

# Close the window
win.close()
core.quit()