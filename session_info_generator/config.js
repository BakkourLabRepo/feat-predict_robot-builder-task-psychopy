
// CONDITION -> subject-level variables map
const CONDITION_MAP = {
    1: {'subject_id': '104', 'seed': 2, 'between_cond': 1},
    2: {'subject_id': '200', 'seed': 50, 'between_cond': 1}
}

// seed and conditions to generate trials for
const SEEDS = [
    0,  1,  2,  3,  4,  5,  6,  7,  8,  9, 10, 11, 12, 13, 14, 15, 16,
   17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33,
   34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50
];
// Conditions: 0 - 1I, 1 - 1II, 2 - 2I, 3 - 2II, 4 - 3I, 5 - 3II
const CONDITIONS = [0, 1, 2, 3, 4, 5]; 
const DOWNLOAD_DELAY_TIME = 1000 // delay time between downloads in ms
const SESSION_INFO_EXTENSION = 'json' // session info to 'json' or 'js'

// run on sona instead of mturk
const SONA = false;

// General info
const BREAK_TIME = 60;
const COUNTDOWN_TIME = 3;
const FONT_SIZE = window.innerHeight/30;
const FIX_SIZE = window.innerHeight/15;
const REWARD_FONT_SIZE = window.innerHeight/15;
const TARGET_FONT_SIZE = window.innerHeight/20;

//  environment features
const STIM_FEATS = ['bo', 'he', 'ar', 'an'];
const ENCODING_FEAT_LABELS = {
    'bo': 'Bodies',
    'he': 'Heads',
    'ar': 'Arms',
    'an': 'Antennas'
}
const STIM_INSTS = [1, 2, 3, 4, 5, 6];
const N_FEATS = 4;
const N_INSTS = 6;
const N_PER = 2;
const TRAINING_COMBS = [
    [1,1,0,0],
    [0,0,1,1]
];
const TEST_COMBS = [
    [1,1,0,0],
    [1,0,1,0],
    [1,0,0,1],
    [0,1,1,0],
    [0,1,0,1],
    [0,0,1,1]
];
const TARGET_COMBS = {

    // within-feature transitions only
    'within': [[1,1,0,0],
               [0,0,1,1]],

    // between-feature transitions only
    'between': [[0,0,1,1],
                [1,1,0,0]],

};
const START_INSTS = [
    [3,4],
    [2,5]
];
const TERMINAL_INSTS = [1,6];
const N_FRACTALS = N_FEATS*N_INSTS;
const NO_RESPONSE_REWARD = -5;

// Transition matrix between instance levels
const INSTANCE_TMAT = [[1,0,0,0,0,0],
                       [1,0,0,0,0,0],
                       [0,1,0,0,0,0],
                       [0,0,0,0,1,0],
                       [0,0,0,0,0,1],
                       [0,0,0,0,0,1]];

// Stimulus to task mappings by condition (after assignent of perceptual
// features to stimuli based on SEED; e.g., head -> 0, body -> 1, etc.)
const STIM_TO_TASK_MAPPINGS = [

    // Condition 1 (1I)
    {0: 0, 1: 1, 2: 2, 3: 3},

    // Condition 2 (1II)
    {0: 0, 1: 2, 2: 1, 3: 3},

    // Condition 3 (2I)
    {0: 2, 1: 3, 2: 0, 3: 1},

    // Condition 4 (3II)
    {0: 2, 1: 0, 2: 3, 3: 1},

    // Condition 5 (2II)
    {0: 2, 1: 0, 2: 1, 3: 3},

    // Condition 6 (3II)
    {0: 0, 1: 2, 2: 3, 3: 1}
]

// Transition matrix between feature levels. Differs by condition
const FEATURE_TMAT = [

    // Condition 1 (1I)
    [[1,0,0,0],
     [0,1,0,0],
     [0,0,1,0],
     [0,0,0,1]],

    // Condition 2 (1II)
    [[0,0,0,1],
     [0,0,1,0],
     [0,1,0,0],
     [1,0,0,0]],

    // Condition 3 (2I)
    [[0,0,1,0],
     [0,0,0,1],
     [1,0,0,0],
     [0,1,0,0]],

    // Condition 4 (3II)
    [[1,0,0,0],
     [0,1,0,0],
     [0,0,1,0],
     [0,0,0,1]],

    // Condition 5 (2II)
    [[1,0,0,0],
     [0,1,0,0],
     [0,0,1,0],
     [0,0,0,1]],

    // Condition 6 (3II)
    [[0,0,1,0],
     [0,0,0,1],
     [1,0,0,0],
     [0,1,0,0]]
];

const TRAIN_NON_MATCH_LEVEL_FREQ = 2;

// choice phases
const N_TRAINING_BLOCKS = 4;
const N_TEST_BLOCKS = 2;
const N_TRAIN_CONJ_REPEATS = 6;
const N_TEST_CONJ_REPEATS = 1;
