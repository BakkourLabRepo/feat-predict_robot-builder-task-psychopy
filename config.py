import numpy as np

# Run in debug mode (fast ITIs and random responses)
DEBUG = False

# Whether to show instructions
SHOW_INSTRUCTIONS = True

# Path to save data to
DATA_PATH = 'data'

# Path to image files
IMG_PATH = 'img/png'

# Possible key presses during choice phase
KEYS = ['1', '2', '9', '0']

# Instructions keys
INSTRUCTIONS_KEYS = {
    'forward': ['right', 'g', 'r'],
    'backward': ['left', 'b', 'y'],
}

# Correct key presses for comprehension test
COMPREHENSION_ANSWERS = ['2', '1', '2', '2']

# Duration of each trial phase during choice
TIMES = {
    'iti': 0.5,
    'target': 2,
    'choice': 8,
    'seq1': 2,
    'seq2': 2,
    'reward': 1.5
}

# Delay before starting the first trial
PRE_RUN_DELAY = 1
POST_RUN_DELAY = 1

# Encoding times
ENCODING_TIMES = {
    'category': 1.5,
    '+': .5,
    'display': 3
}

# Number of times to repeat each category during encoding
CATEGORY_REPEATS = 2

# Fast times if debugging
if DEBUG:
    TIMES = {key: .05 for key in TIMES.keys()}
    ENCODING_TIMES = {key: .05 for key in ENCODING_TIMES.keys()}
    PRE_RUN_DELAY = .05
    POST_RUN_DELAY = .05

# Stimulus sizes. Will be re-scaled based on window height.
SIZE_SCALE = 1
SIZES = {
    'robot_parts': (.045, .045),
    'robots': (.13, 0.13),
    'robots_border': (.15, .15),
    'robots_choice': (.075, .075),
    'robots_choice_border': (.081, .081),
    'instructions': (.35, .35),
    'selection_border': (.051, .051),
    'text': .015
}

# Stimulus positions. Will be re-scaled based on window height.
POSITIONS = {
    'feature_grid': [
        (-.07,  .13),
        (-.07, .045),
        ( .07,  .13),
        ( .07, .045)
    ],
    'robots': (0, 0),
    'target_text': (0, .09),
    'target_choice': (-.075, -.11),
    'target_choice_text': (-.075, -.05),
    'composition': (.075, -.11),
    'composition_text': (.075, -.05)
}

# Transition matrix for instance values
INSTANCE_TMAT = np.array([
    [1,0,0,0,0,0],
    [1,0,0,0,0,0],
    [0,1,0,0,0,0],
    [0,0,0,0,1,0],
    [0,0,0,0,0,1],
    [0,0,0,0,0,1]
])

# Instance values at each step
INSTANCE_VALUES = [
    [3, 4],
    [2, 5],
    [1, 6]
]

# Transition matrix for feature values ([[step1], [step2]])
FEATURE_TMAT = np.array([

    # Condition 1 (1I) - semantic congruent
    [

        # Step 1
        [[1,0,0,0],
         [0,1,0,0],
         [0,0,1,0],
         [0,0,0,1]],

        # Step 2
        [[1,0,0,0],
         [0,1,0,0],
         [0,0,1,0],
         [0,0,0,1]],

    ],

    # Condition 2 (1II) - semantic incongruent

    [
        # Step 1
        [[0,0,0,1],
         [0,0,1,0],
         [0,1,0,0],
         [1,0,0,0]],

        # Step 2
        [[0,0,1,0],
         [0,0,0,1],
         [1,0,0,0],
         [0,1,0,0]],

    ],

    # Condition 3 (2I) - semantic incongruent
    [

        # Step 1
        [[0,0,1,0],
         [0,0,0,1],
         [1,0,0,0],
         [0,1,0,0]],

        # Step 2
        [[0,0,0,1],
         [0,0,1,0],
         [0,1,0,0],
         [1,0,0,0]],

    ],

    # Condition 4 (3II) - semantic congruent
    [

        # Step 1
        [[1,0,0,0],
         [0,1,0,0],
         [0,0,1,0],
         [0,0,0,1]],

        # Step 2
        [[1,0,0,0],
         [0,1,0,0],
         [0,0,1,0],
         [0,0,0,1]],

    ],

    # Condition 5 (2II) - semantic congruent
    [

        # Step 1
        [[1,0,0,0],
         [0,1,0,0],
         [0,0,1,0],
         [0,0,0,1]],

        # Step 2
        [[1,0,0,0],
         [0,1,0,0],
         [0,0,1,0],
         [0,0,0,1]],

    ],

    # Condition 6 (3II) - semantic incongruent
    [
        # Step 1
        [[0,0,1,0],
         [0,0,0,1],
         [1,0,0,0],
         [0,1,0,0]],

        # Step 2
        [[0,0,0,1],
         [0,0,1,0],
         [0,1,0,0],
         [1,0,0,0]]

    ]
    
])