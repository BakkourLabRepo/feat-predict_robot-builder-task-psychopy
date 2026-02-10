import pickle
import re
from os import listdir
from psychopy import visual, event, core
import numpy as np

########################################################################
### Task Loading Functions #########################################
########################################################################

def load_itis(run):
    """
    Load ITIs for a given run

    Arguments
    ---------
    run : int
        Run number
    
    Returns
    -------
    itis : list
        List of ITIs
    """
    set_id = np.random.permutation(len(listdir('iti'))) + 1
    set_id = set_id[run - 1]
    with open(f'iti/iti_{set_id}.pkl', 'rb') as f:
        itis = pickle.load(f)
    np.random.shuffle(itis) # Randomize ITI order
    return itis

def adjust_sizes(sizes, factor):
    """
    Adjust sizes of stimuli 
    
    Arguments
    ---------
    sizes : dict
        Dictionary containing sizes for each stimulus type
    factor : float
        Factor to scale sizes by

    Returns
    -------
    None
    """
    for key in sizes.keys():
        if sizes[key] is not None:
            if key == 'text':
                sizes[key] = sizes[key]*factor
            else:
                sizes[key] = (
                    sizes[key][0]*factor,
                    sizes[key][1]*factor
                )

def adjust_positions(positions, factor):
    """
    Adjust positions of stimuli

    Arguments
    ---------
    positions : dict
        Dictionary containing positions for each stimulus type
    factor : float
        Factor to scale positions by
    
    Returns
    -------
    None
    """
    for key in positions.keys():
        if positions[key] is not None:
            if key == 'feature_grid':
                positions[key] = [
                    (
                        int(positions[key][i][0]*factor),
                        int(positions[key][i][1]*factor)
                    )
                    for i in range(len(positions[key]))
                ]
            else:
                positions[key] = (
                    int(positions[key][0]*factor),
                    int(positions[key][1]*factor)
                )

def get_fnames_to_load(phase_fnames, feature_fnames, img_path):
    """
    Get file names to load based on phase

    Arguments
    ---------
    phase_fnames : list
        List of file names for the phase
    feature_fnames : list
        List of file names for the feature options
    img_path : str
        Path to image files
    
    Returns
    -------
    fnames_to_load : list
        List of file names to load
    """
    fnames_to_load = []
    for fname in phase_fnames:
        fnames_to_load.append(fname.replace('img', f'{img_path}/robots'))
    for fname in feature_fnames:
        fnames_to_load.append(fname.replace('img', f'{img_path}/robot_parts'))
    return fnames_to_load

def preload_stimuli(win, fnames_to_load, sizes, positions):
    """
    Preload choice phase stimuli

    Arguments
    ---------
    win : psychopy.visual.Window
        Window object to draw stimuli on
    fnames_to_load : list   
        List of file names to load
    sizes : dict
        Dictionary containing sizes for each stimulus type
    positions : dict
        Dictionary containing positions for each stimulus type
    
    Returns
    -------
    screen_objects : dict
        Dictionary containing all screen objects
    """

    # Dictionary to store screen objects
    screen_objects = {}

    # For each stimulus type load images
    for fname in fnames_to_load:
        if not '.png' in fname:
            continue

        # Size differs for robots parts versus robots
        if 'robot_parts' in fname:
            height = sizes['robot_parts'][0]
        elif 'instructions' in fname:
            height = sizes['instructions'][0]
        else:
            height = sizes['robots'][0]

        # Get key for stimulus
        key = fname.split('/')[-1]
        if 'instructions' in fname:
            key = key.replace('.png', '')
            key = int(key.split('_')[1])
        else: 
            key = 'img/' + key

        # Load image
        screen_objects[key] = visual.ImageStim(
            win,
            image = fname
        )
        aspect_ratio = screen_objects[key].size[0]/screen_objects[key].size[1]  
        width = height*aspect_ratio
        screen_objects[key].size = [width, height]


    # Border around composition during choice
    screen_objects['target_text'] = visual.TextStim(
        win,
        text = 'BLUEPRINT',
        pos = positions['target_text'],
        color = 'white',
        height = sizes['text']
    )

    # Border around composition during choice
    screen_objects['robots_border'] = visual.Rect(
        win = win,
        size = sizes['robots_border'],
        pos = positions['robots'],
        lineColor = 'white', 
        lineWidth = 10,  
        fillColor = None
    )

    # Fixation cross
    screen_objects['+'] = visual.TextStim(
        win,
        text = '+',
        height = sizes['text']
    )

    # Border around feature options
    grid_width = np.abs(
        positions['feature_grid'][2][0] - positions['feature_grid'][0][0]
        ) + 2*positions['feature_grid'][2][0]
    grid_height = np.abs(
        positions['feature_grid'][0][1] - positions['feature_grid'][1][1]
        ) + .75*positions['feature_grid'][0][1]
    grid_pos = np.mean(positions['feature_grid'], axis=0)
    screen_objects['options_pane'] = visual.Rect(
        win = win,
        width = grid_width,
        height = grid_height,
        pos = grid_pos,
        lineColor = 'white', 
        lineWidth = 10,  
        fillColor = None
    )

    # Border around selected feature
    screen_objects['selection_border'] = [
        visual.Rect(
            win = win,
            size = sizes['selection_border'],
            lineColor = 'white', 
            lineWidth = 10,  
            fillColor = None
        ) for _ in range(2) # 2 is max n that can be selected at once
    ]

    # Border around target during choice
    screen_objects['target_choice_border'] = visual.Rect(
            win = win,
            size = sizes['robots_choice_border'],
            pos = positions['target_choice'],
            lineColor = 'white', 
            lineWidth = 10,  
            fillColor = None
    )

    # Target choice text
    screen_objects['target_choice_text'] = visual.TextStim(
        win,
        text = 'BLUEPRINT',
        pos = positions['target_choice_text'],
        color = 'white',
        height = sizes['text']
    )

    # Composition text
    screen_objects['composition_text'] = visual.TextStim(
        win,
        text = 'Your builder:',
        pos = positions['composition_text'],
        color = 'white',
        height = sizes['text']
    )

    # Border around composition during choice
    screen_objects['composition_border'] = visual.Rect(
        win = win,
        size = sizes['robots_choice_border'],
        pos = positions['composition'],
        lineColor = 'white', 
        lineWidth = 10,  
        fillColor = None
    )
    
    # Border around composition pane
    screen_objects['composition_pane'] = visual.Rect(
        win = win,
        width = grid_width,
        height = 2*sizes['robots_choice_border'][1],
        pos = (0, positions['composition'][1] + positions['composition'][0]/10),
        lineColor = 'white', 
        lineWidth = 10,  
        fillColor = None
    )

    # Countdown during choice phase
    countdown_pos = grid_pos
    countdown_pos[1] += grid_height/2 + grid_height/10
    screen_objects['choice_countdown'] = visual.TextStim(
        win = win,
        text = '',
        pos = countdown_pos,
        color = 'white',
        height = sizes['text']
    )
    
    # Display total points 
    screen_objects['total_points'] = visual.TextStim(
        win = win,
        text = 'Total Points: 0',
        pos = (0, positions['composition'][1] - 1.5*positions['composition'][0]),
        color = 'white',
        height = sizes['text']
    )

    # Display total points 
    screen_objects['reward'] = visual.TextStim(
        win = win,
        text = 'NO RESPONSE\n???',
        pos = (0, 0),
        color = 'white',
        height = sizes['text']
    )

    return screen_objects

    

def preload_comprehension_instructions(win, fnames_to_load, sizes):
    """
    Preload comprehension instructions

    Arguments
    ---------
    win : psychopy.visual.Window
        Window object to draw stimuli on
    fnames_to_load : list   
        List of file names to load
    sizes : dict
        Dictionary containing sizes for each stimulus type
    
    Returns
    -------
    screen_objects : dict
        Dictionary containing all screen objects
    """

    # Dictionary to store screen objects
    screen_objects = {}

    # Count number of welcome slides to put in training set
    n_welcome_slides = np.sum(['welcome' in fname for fname in fnames_to_load])

    # For each stimulus type load images
    for fname in fnames_to_load:
        if not '.png' in fname:
            continue

        # Get key for stimulus
        key = fname.split('/')[-1]
        key = key.replace('.png', '')
        key = int(key.split('_')[1])
        if 'comprehension' in fname:
            key = f'comprehension_{key}'
        elif 'training' in fname: 
            key += n_welcome_slides
            
        # Load image
        screen_objects[key] = visual.ImageStim(
            win,
            image = fname
        )
        aspect_ratio = screen_objects[key].size[0]/screen_objects[key].size[1] 
        height = sizes['instructions'][0] 
        width = height*aspect_ratio
        screen_objects[key].size = [width, height]
    
    return screen_objects

def conj_to_img(
    conj,
    task_to_stim_feature_map,
    task_to_stim_instance_map
):
    """
    Convert array representation of item to its image file name

    Arguments
    ---------
    conj : list
        Array representation of item
    task_to_stim_feature_map : dict
        Mapping of task features to visual stimuli
    task_to_stim_instance_map : dict
        Mapping of task instances to visual stimuli
    
    Returns
    -------
    fname : str
        Image file name
    """
    
    stim_feats = {}
    for feat, inst in enumerate(conj):
        stim_feat = task_to_stim_feature_map[str(feat)]
        stim_inst = task_to_stim_instance_map[stim_feat][str(inst)]
        stim_feats[stim_feat] = stim_inst
    print(conj, stim_feats) # DEBUGGING
    stim_conj = []
    for stim_feat in ['bo', 'he', 'ar', 'an']:
        stim_conj.append(f'{stim_feat}-{stim_feats[stim_feat]}')

    # Randomly do or do not flip the image
    if np.random.choice(2):
        stim_conj.append('flipped')

    # Combine into image path
    fname = 'img/' + '_'.join(stim_conj) + '.png'

    return fname

def img_to_conj(
    fname,
    stim_to_task_feature_map,
    stim_to_task_instance_map
):
    """
    Convert stimulus file name to task conjunction

    Arguments
    ---------
    fname : str
        File name of stimulus
    stim_to_task_feature_map : dict
        Mapping of stimulus features to task features
    stim_to_task_instance_map : dict
        Mapping of stimulus instances to task instances
    
    Returns
    -------
    conj : np.ndarray
        Task conjunction
    """
    
    # Split fname into features
    fname = fname.replace('_flipped', '')
    fname = fname.replace('img/', '')
    fname = fname.replace('.png', '')
    features = fname.split('_')

    # Convert stim features to task features
    conj = np.zeros(len(features), dtype=int)
    for feature in features:
        stim_f, stim_i = feature.split('-')
        task_f = stim_to_task_feature_map[stim_f]
        task_i = stim_to_task_instance_map[stim_f][str(stim_i)]
        conj[task_f] = task_i
    
    return conj

def get_feature_label_from_fname(fname):
    """
    Get feature category label from file name

    Arguments
    ---------
    fname : str
        File name of stimulus
    
    Returns
    -------
    category_label : str
        Feature category label
    """
    
    # Regex pattern to extract fields and values
    pattern = r'(\w+)-(\d+)'
    matches = re.findall(pattern, fname.replace('_', ''))
    
    # Iterate through matches and find the key with a non-zero value
    category = None
    for key, value in matches:
        if int(value) != 0:
            category = key

    # Convert to feature label
    category_label = {
        'bo': 'Bodies',
        'he': 'Heads',
        'ar': 'Arms',
        'an': 'Antennas'
    }[category]
        
    return category_label

########################################################################
### Task Running Functions #############################################
########################################################################

def draw_instructions(
        win,
        pane,
        pane_key,
        screen_objects,
        forward_keys,
        backward_keys
        ):
    """
    Draws instructions. Keypress moves instructions pane forward or
    backwards.

    Arguments
    ---------
    win : psychopy.visual.Window
        Window object to draw stimuli on
    pane : int
        Current instructions pane
    pane_key : str or int
        Key for current instructions pane
    screen_objects : dict
        Dictionary of screen objects
    forward_keys : list
        List of keys to move instructions forward
    backward_keys : list
        List of keys to move instructions backwards
    
    Returns
    -------
    pane : int
        Updated instructions pane
    """

    screen_objects[pane_key].draw()
    win.flip()
    keypress = event.waitKeys()[0]

    # Move instructions forward or backwards
    if keypress in forward_keys:
        pane += 1
    elif keypress in backward_keys:
        pane -= 1
    elif keypress == 'escape':
        core.quit()

    return pane
    
def instructions(win, screen_objects, instructions_keys):
    """
    Displays instructions for the task.

    Arguments
    ---------
    win : psychopy.visual.Window
        Window object to draw stimuli on
    screen_objects : dict
        Dictionary of screen objects
    instructions_keys : dict
        Dictionary of keys to move instructions forward or backwards

    Returns
    -------
    None
    """
    
    pane = 1
    while pane in screen_objects.keys():
        pane = draw_instructions(
            win,
            pane,
            pane,
            screen_objects,
            instructions_keys['forward'],
            instructions_keys['backward']
            )
        if pane < 1:
            pane = 1

def comprehension(win, screen_objects, answers):
    """
    
    """
    
    pane = 1
    pane_key = f'comprehension_{pane}'
    while pane_key in screen_objects.keys():
        old_pane = pane
        pane = draw_instructions(
            win,
            pane,
            pane_key,
            screen_objects,
            answers[pane - 1],
            []
            )
        
        # Incorrect response was made
        if old_pane >= pane:
            return False
        pane_key = f'comprehension_{pane}'
    
    # Passed comprehension
    return True

def get_successor(conj, instance_tmat, feature_tmat):
    """
    Get the successor item given the current item
    
    Arguments
    ---------
    conj : list
        Array representation of current item
    instance_tmat : np.ndarray
        Transition matrix for instance values
    feature_tmat : np.ndarray
        Transition matrix for feature values
    
    Returns
    -------
    succ : list
        Array representation of successor item
    """
  
    n_feats = len(feature_tmat)
    n_insts = len(instance_tmat)
    succ = np.zeros(n_feats, dtype=int)
    for feat, inst in enumerate(conj):

        # Get successor feature
        succ_feat = np.random.choice(
                np.arange(n_feats),
                p = feature_tmat[feat]
            )

        # Get successor instance value
        if inst == 0:
            succ_inst = 0
        else:
            succ_inst = np.random.choice(
                np.arange(1, n_insts + 1),
                p = instance_tmat[inst - 1]
            )
        succ[succ_feat] = succ_inst

    return succ

def get_reward(successor, target):
    """
    Get the reward for the current item

    Arguments
    ---------
    successor : list
        Array representation of successor item
    target : list
        Array representation of target item
    
    Returns
    -------
    reward : int
        Number of overlapping features between successor and target
    """
    if len(successor) == 0:
        reward = -5
    else:
        overlap = (
            (successor != 0) &
            (successor == target)
        )
        reward = np.sum(overlap)
    return reward

def text_display(win, msg):
    """
    Display loading screen while task is loading

    Arguments
    ---------
    win : psychopy.visual.Window
        Window object to draw stimuli on
    msg : str
        Message to display
    
    Returns
    -------
    None
    """
    message = visual.TextStim(win, text=msg)
    message.draw()
    win.flip()

def draw_features(screen_objects, key_to_img, feature_grid, selected=[]):
    """
    Draw feature options on screen

    Arguments
    ---------
    screen_objects : dict
        Dictionary containing all screen objects
    key_to_img : dict
        Mapping of keypresses to images
    feature_grid : list
        List of positions for each feature option
    selected : list
        List of selected feature options
    
    Returns
    -------
    None
    """
    i_selected = 0
    for i, key in enumerate(key_to_img.keys()):
        img = key_to_img[key]
        img.pos = feature_grid[i]
        if key in selected:
            screen_objects['selection_border'][i_selected].pos = img.pos
            screen_objects['selection_border'][i_selected].draw()
            i_selected += 1
        img.draw()

def update_onset_times(onset_times, last_onset, onset):
    """
    Update onset times

    Arguments
    ---------
    onset_times : pandas.DataFrame
        Data frame to store onset times for each trial phase
    last_onset : list
        Length = 2 list where the first position is the last trial
        phase name and the second position is the onset time
    onset : float
        Current onset time
    
    Returns
    -------
    onset_times : pandas.DataFrame
        Updated onset times
    last_onset : list
        Updated last onset time
    """
    if last_onset[0] != None:
        onset_times = onset_times.append({
            'onset': last_onset[1],
            'duration': onset - last_onset[1],
            'trial_type': last_onset[0]
        }, ignore_index=True)
    return onset_times

def run_trial(
    clock = None,
    running_time = None,
    onset_times = None,
    last_onset = [None, 0],
    win = None,
    times = None,
    screen_objects = None,
    positions = None,
    sizes = None,
    task_to_stim_feature_map = None,
    task_to_stim_instance_map = None,
    feature_tmat = None,
    instance_tmat = None,
    show_transition = True,
    total_points = '???',
    keys = None,
    data = None,
    run_info = None,
    t = None,
    data_path = None,
    task_phase = None,
    options = None,
    options_fnames = None,
    target = None,
    target_fname = None,
    correct_composition = None,
    practice = False,
    debug = False
):
    """
    Run choice phase trial

    Arguments
    ---------
    clock : psychopy.core.Clock
        Clock object to track time
    running_time : float
        Running upper time limit for the run
    onset_times : pandas.DataFrame
        Data frame to store onset times for each trial phase
    last_onset : list
        Length = 2 list where the first position is the last trial
        phase name and the second position is the onset time
    win : psychopy.visual.Window
        Window object to draw stimuli on
    times : dict
        Dictionary containing durations for each trial phase
    screen_objects : dict
        Dictionary containing all screen objects
    positions : dict
        Dictionary containing positions for each stimulus type
    sizes : dict
        Dictionary containing sizes for each stimulus type
    task_to_stim_feature_map : dict
        Mapping of task features to visual stimuli
    task_to_stim_instance_map : dict
        Mapping of task feature instances to visual stimuli
    feature_tmat : np.ndarray
        Transition matrix for feature values
    instance_tmat : np.ndarray
        Transition matrix for instance values
    total_points : int
        Total points accrued so far in the task
    keys : list
        List of possible key presses
    data : pd.DataFrame
        Run data
    run_info : dict
        Dictionary containing run information
    t : int
        Trial number
    data_path : str
        Path to save data
    task_phase : str
        Phase of the task
    options : list
        List of feature options
    options_fnames : list
        List of file names for feature options
    target : list
        Target item
    target_fname : str
        File name for target item
    correct_composition : list
        Composition that will produce the target
    practice : bool
        Whether the trial is a practice trial or not
    debug : bool
        Run task in debugging mode
    
    Returns
    -------
    data : pd.DataFrame
        Updated run data
    reward : int
        Reward for the trial
    running_time : float
        Running upper time limit for the run
    """

    # Inter-trial interval
    screen_objects['+'].draw()
    win.flip()
    onset = clock.getTime()
    setup_next = True
    running_time += times['iti']
    while clock.getTime() < running_time:
        if setup_next:

            # Draw for next trial
            screen_objects[target_fname].pos = positions['robots']
            screen_objects[target_fname].size = sizes['robots']
            screen_objects[target_fname].draw()
            screen_objects['robots_border'].draw()
            screen_objects['target_text'].draw()
            setup_next = False
            event.clearEvents() # clear events - they clog the buffer

            # Get stimulus information
            target = np.array(target)
            options = np.array(options)
            correct_composition = np.array(correct_composition)
            target_comb = target.astype(bool).astype(int)
            options_comb = options.reshape(-1, len(target))
            options_comb = np.sum(options_comb, axis=0)
            options_comb = options_comb.astype(bool).astype(int)

            # Initialize other trial variables
            valid_response = 0
            successor = []
            successor_fname = -1
            selected = [] # current selections
            rt = []
            selections = [] # all selections made
            composition = []
            composition_fname = False
            correct = -1
            reward = -5

            # Update onset times
            onset_times = update_onset_times(onset_times, last_onset, onset)
            last_onset = ['iti', onset]


    # Target phase
    win.flip()
    onset = clock.getTime()
    setup_next = True
    running_time += times['target']
    while clock.getTime() < running_time:
        if setup_next:
            flip_win = False
            setup_next = False

            # Map keypresses to images and states
            key_to_img = {}
            key_to_state = {}
            for feat, fnames in enumerate(options_fnames):
                for inst, fname in enumerate(fnames):
                    key_idx = feat*len(fnames) + inst
                    key_to_img[keys[key_idx]] = screen_objects[fname]
                    key_to_state[keys[key_idx]] = options[feat][inst]

            # Draw countdown
            start_time = int(np.ceil(times['choice']))
            count = list(range(1, start_time))
            screen_objects['choice_countdown'].text = str(start_time)
            screen_objects['choice_countdown'].draw()

            # Draw options pane
            screen_objects['options_pane'].draw()
            draw_features(
                screen_objects,
                key_to_img,
                positions['feature_grid']
            )

            # Draw target and composition pane
            screen_objects[target_fname].pos = positions['target_choice']
            screen_objects[target_fname].size = sizes['robots_choice']
            screen_objects[target_fname].draw()
            screen_objects['target_choice_border'].draw()
            screen_objects['target_choice_text'].draw()
            screen_objects['composition_border'].draw()
            screen_objects['composition_text'].draw()
            screen_objects['composition_pane'].draw()
            
            # Total earnings
            screen_objects['total_points'].text = f'Total points: {total_points}'
            screen_objects['total_points'].draw()

            # Update onset times
            onset_times = update_onset_times(onset_times, last_onset, onset)
            last_onset = ['target', onset]
                

    # Choice phase
    win.flip()
    onset = clock.getTime()
    timer_clock = core.CountdownTimer(1)
    event.clearEvents()
    setup_next = True
    running_time += times['choice']
    while clock.getTime() < running_time:
        
        # Update onset times
        if setup_next:
            setup_next = False
            onset_times = update_onset_times(onset_times, last_onset, onset)
            last_onset = ['choice', onset]

        # Update countdown
        if timer_clock.getTime() < 0:
            flip_win = True
            timer_clock.add(1)
            screen_objects['choice_countdown'].text = str(count.pop())

        # Get keypresses
        if debug and len(selected) < 2:
            keypresses = np.random.choice(keys, 2)
        else:
            keypresses = event.getKeys()

        # Check for keypresses
        for key in keypresses:

            # Quit
            if key == 'escape':
                win.close()
                core.quit()
            elif key not in keys:
                continue

            # Add to reaction time array
            rt.append(clock.getTime() - running_time + times['choice'])

            # Add selected features
            selections.append(key_to_state[key])

            # Show feature selection
            if (key not in selected) or (timer_clock.getTime() < 0):
                flip_win = True

                # Track selected
                selected.append(key)

                # Ensure only one instance is selected per category
                if (key == keys[0]) and (keys[1] in selected):
                    selected.remove(keys[1])
                elif (key == keys[1]) and (keys[0] in selected):
                    selected.remove(keys[0])
                elif (key == keys[2]) and (keys[3] in selected):
                    selected.remove(keys[3])
                elif (key == keys[3]) and (keys[2] in selected):
                    selected.remove(keys[2])

                # Get composition
                composition = np.array([key_to_state[key] for key in selected])
                composition = np.sum(composition, axis=0)
                composition_fname = conj_to_img(
                    composition,
                    task_to_stim_feature_map,
                    task_to_stim_instance_map
                )

                # Update information for a valid response
                if len(selected) > 1:
                    valid_response = 1

                    # Successor
                    successor = get_successor(
                        composition,
                        instance_tmat,
                        feature_tmat
                    )
                    successor_fname = conj_to_img(
                        successor,
                        task_to_stim_feature_map,
                        task_to_stim_instance_map
                    )

                    # Reward
                    reward = get_reward(successor, target)

                    # Successor is correct
                    correct = int(np.all(successor == target))
                
        # Update window
        if flip_win:

            # Draw countdown
            screen_objects['choice_countdown'].draw()

            # Draw options pane
            screen_objects['options_pane'].draw()
            draw_features(
                screen_objects,
                key_to_img,
                positions['feature_grid'],
                selected
            )

            # Draw target and composition pane
            screen_objects[target_fname].draw()
            screen_objects['target_choice_border'].draw()
            screen_objects['target_choice_text'].draw()
            if len(selected) > 1:
                screen_objects[composition_fname].pos = positions['composition']
                screen_objects[composition_fname].size = sizes['robots_choice']
                screen_objects[composition_fname].draw()
            screen_objects['composition_border'].draw()
            screen_objects['composition_text'].draw()
            screen_objects['composition_pane'].draw()

            # Total point earnings
            screen_objects['total_points'].draw()

            # Show
            win.flip()
            flip_win = False

    # Show composition
    if task_phase == 'training':
        if len(selected) > 1:
            screen_objects[composition_fname].pos = positions['robots']
            screen_objects[composition_fname].size = sizes['robots']
            screen_objects[composition_fname].draw()
        else:
            screen_objects['reward'].text = 'NO RESPONSE\n???'
            screen_objects['reward'].draw()
        win.flip()
        onset = clock.getTime()
        setup_next = True
        running_time += times['seq1']
        while clock.getTime() < running_time:
            
            if setup_next:
                setup_next = False

                # Draw successor 
                if len(selected) > 1:
                    print(composition, successor, composition_fname, successor_fname)
                    screen_objects[successor_fname].pos = positions['robots']
                    screen_objects[successor_fname].size = sizes['robots']
                    screen_objects[successor_fname].draw()    

                # No response message
                else:
                    screen_objects['reward'].draw()

                # Update onset times
                onset_times = update_onset_times(onset_times, last_onset, onset)
                last_onset = ['seq1', onset]

    # Show successor
    if task_phase == 'training':
        setup_next = True
        win.flip()
        onset = clock.getTime()
        running_time += times['seq2']
        while clock.getTime() < running_time:
            if setup_next:
                setup_next = False

                # Setup reward display
                screen_objects['reward'].text = reward
                screen_objects['reward'].draw()

                # Update total points accrued
                if task_phase == 'training':
                    total_points += reward

                # Update onset times
                onset_times = update_onset_times(onset_times, last_onset, onset)
                last_onset = ['seq2', onset]

    # Show reward
    if task_phase == 'training':
        win.flip()
        onset = clock.getTime()
        trial_saved = False
        running_time += times['reward']
        while clock.getTime() < running_time:
            
            if not trial_saved:
                trial_saved = True

                # Update onset times
                onset_times = update_onset_times(onset_times, last_onset, onset)
                last_onset = ['reward', onset]

                # Format trial data
                trial_data = {
                    **run_info,
                    't': t + 1,
                    'target_comb': target_comb,
                    'options_comb': options_comb,
                    'options_fnames': options_fnames,
                    'options': options,
                    'correct_composition': correct_composition,
                    'composition_fname': composition_fname,
                    'composition': composition,
                    'successor_fname': successor_fname,
                    'successor': successor,
                    'target_fname': target_fname,
                    'target': target,
                    'reward': reward,
                    'correct': correct,
                    'valid_response': valid_response,
                    'rt': rt,
                    'selections': np.array(selections)
                }
                
                # Add to main data frame
                data = data.append(trial_data, ignore_index=True)

                # Save data
                phase = run_info['phase']
                subj = run_info['id']
                run = run_info['run']
                fname = f'sub-{subj}_task-{phase}_run-{run:02}.csv'
                data.to_csv(f'{data_path}/{fname}', index=False)
                fname = f'sub-{subj}_task-{phase}_run-{run:02}_events.tsv'
                onset_times.to_csv(f'{data_path}/{fname}', sep='\t', index=False)
    
    # Save test data. Time slip is less important here (outside scanner)
    elif task_phase == 'test':
                
        # Format trial data
        trial_data = {
            **run_info,
            't': t + 1,
            'target_comb': target_comb,
            'options_comb': options_comb,
            'options_fnames': options_fnames,
            'options': options,
            'correct_composition': correct_composition,
            'composition_fname': composition_fname,
            'composition': composition,
            'successor_fname': successor_fname,
            'successor': successor,
            'target_fname': target_fname,
            'target': target,
            'reward': reward,
            'correct': correct,
            'valid_response': valid_response,
            'rt': rt,
            'selections': np.array(selections)
        }
        
        # Add to main data frame
        data = data.append(trial_data, ignore_index=True)

        # Save data
        phase = run_info['phase']
        subj = run_info['id']
        run = run_info['run']
        fname = f'sub-{subj}_task-{phase}_run-{run:02}.csv'
        data.to_csv(f'{data_path}/{fname}', index=False)
        fname = f'sub-{subj}_task-{phase}_run-{run:02}_events.tsv'
        onset_times.to_csv(f'{data_path}/{fname}', sep='\t', index=False)

    return data, total_points, running_time, onset_times, last_onset

def run_covertask_trial(
    clock = None,
    running_time = None,
    onset_times = None,
    last_onset = [None, 0],
    win = None,
    times = None,
    screen_objects = None,
    stim_to_task_feature_map = None,
    stim_to_task_instance_map = None,
    response_keys = None,
    data = None,
    run_info = None,
    t = None,
    data_path = None,
    item_fname = None,
    correct_response = None,
    debug = False
):
    """
    Run cover-task trial

    Arguments
    ---------
    clock : psychopy.core.Clock
        Clock object to track time
    running_time : float
        Running upper time limit for the run
    onset_times : pandas.DataFrame
        Data frame to store onset times for each trial phase
    last_onset : list
        Length = 2 list where the first position is the last trial
        phase name and the second position is the onset time
    win : psychopy.visual.Window
        Window object to draw stimuli on
    times : dict
        Dictionary containing times for each trial phase
    screen_objects : dict
        Dictionary containing all screen objects
    stim_to_task_feature_map : dict
        Mapping of stimulus features to task features
    stim_to_task_instance_map : dict
        Mapping of stimulus instances to task instances
    response_keys : list
        List of keys that can be pressed for one-back/oddball response
    data : pd.DataFrame
        Data frame to store trial data
    run_info : dict
        Dictionary containing run information
    t : int
        Trial number
    data_path : str
        Path to save data
    item_fname : str
        File name of stimulus
    correct_response : int
        Should a response be made on this trial (1) or not (0)?
    debug : bool
        Run task in debugging mode
    
    Returns
    -------
    data : pd.DataFrame
        Updated data frame
    running_time : float
        Updated upper time limit for the run
    """

    # Fixation
    screen_objects['+'].draw()
    win.flip()
    onset = clock.getTime()
    setup_next = True
    running_time += times['+']
    while clock.getTime() < running_time:
        if setup_next:
            setup_next = False
            event.clearEvents() # clear events - they clog the buffer
            screen_objects[item_fname].draw()

            # Save current run data
            phase = run_info['phase']
            subj = run_info['id']
            run = run_info['run']
            fname = f'sub-{subj}_task-{phase}_run-{run:02}.csv'
            data.to_csv(f'{data_path}/{fname}', index=False)
            fname = f'sub-{subj}_task-{phase}_run-{run:02}_events.tsv'
            onset_times.to_csv(f'{data_path}/{fname}', sep='\t', index=False)

            # Get task representation of item if not response trial
            if correct_response:
                item = []
            else:
                item = img_to_conj(
                    item_fname,
                    stim_to_task_feature_map,
                    stim_to_task_instance_map
                )
            
            # Init trial data
            trial_data = {
                **run_info,
                't': t,
                'item_fname': item_fname,
                'item': item,
                'response': 0,
                'correct_response': correct_response,
                'rt': -1
            }
            data = data.append(trial_data, ignore_index=True)

            # Update onset times
            onset_times = update_onset_times(onset_times, last_onset, onset)
            last_onset = ['iti', onset]

            # If debugging, sample response now
            if debug:
                keypresses = [np.random.choice([
                    *response_keys,
                    *[-1]*len(response_keys)
                ])]


    # Target phase
    win.flip()
    onset = clock.getTime()
    response = 0
    setup_next = True
    running_time += times['display']
    while clock.getTime() < running_time:

        if setup_next:
            setup_next = False
            onset_times = update_onset_times(onset_times, last_onset, onset)
            last_onset = ['display', onset]

        # Get keypresses
        if not debug:
            keypresses = event.getKeys()

        # Check for keypresses
        for key in keypresses:

            # Quit
            if key == 'escape':
                win.close()
                core.quit()

            # Record first one-back response
            if (key in response_keys) and not response:
                rt = clock.getTime() - running_time + times['display']
                response = 1
                data.iloc[-1, data.columns.get_loc('rt')] = rt
                data.iloc[-1, data.columns.get_loc('response')] = response
    
    return data, running_time, onset_times, last_onset


def run_encoding_trial(
    clock = None,
    running_time = None,
    win = None,
    times = None,
    screen_objects = None,
    item_fname = None,
    category_name = False
):
    """
    Run encoding trial

    Arguments
    ---------
    clock : psychopy.core.Clock
        Clock object to track time
    running_time : float
        Running upper time limit for the run
    win : psychopy.visual.Window
        Window object to draw stimuli on
    times : dict
        Dictionary containing times for each trial phase
    screen_objects : dict
        Dictionary containing all screen objects
    item_fname : str
        File name of stimulus
    category_name : str or False
        Category label to display, if False do not display label

    Returns
    -------
    running_time : float
        Updated upper time limit for the run
    """

    if category_name:
        screen_objects['category'].text = category_name
        screen_objects['category'].draw()
        win.flip()
        running_time += times['category']
        while clock.getTime() < running_time:
            pass

    # Fixation
    screen_objects['+'].draw()
    win.flip()
    running_time += times['+']
    while clock.getTime() < running_time:
        pass
            
    # Stimulus display
    event.clearEvents() # clear events - they clog the buffer
    screen_objects[item_fname].draw()
    win.flip()
    running_time += times['display']
    while clock.getTime() < running_time:

        # Check for quit keypress
        keypresses = event.getKeys()
        for key in keypresses:
            if key == 'escape':
                win.close()
                core.quit()

    return running_time