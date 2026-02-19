
// Generate all combinations of values of some set of arrays
function generateCombinations(...arrays) {
    if (arrays.length === 0) {
      return [[]];
    }
  
    function combine(currentIndex, partialCombination) {

        if (currentIndex === arrays.length) {
            combinations.push([...partialCombination]);
            return;
        }
  
        for (const value of arrays[currentIndex]) {
            partialCombination.push(value);
            combine(currentIndex + 1, partialCombination);
            partialCombination.pop();
        }

    }
  
    const combinations = [];
    combine(0, []);
  
    return combinations;
}

// For every feature combination, get possible instance conjunctions
function getConjunctions(combs, start_insts, terminal_insts) {

    let conjunctions = {};
    for (const comb of combs) {

        // Generate possible start and terminal instances for this combination
        let start_inst_options = [];
        for (let step = 0; step < start_insts.length; step++) {
            start_inst_options.push([]);
        }
        let terminal_inst_options = [];
        for (const feat of comb) {
            
            // Feature present
            if (feat == 1) {

                // Start instances for each step
                for (const [step, step_start_insts] of start_insts.entries()) {
                    start_inst_options[step].push(step_start_insts);
                }

                // Terminal instances
                terminal_inst_options.push(terminal_insts);

            // Feature absent
            } else {

                // Start instances for each step
                for (let step = 0; step < start_insts.length; step++) {
                    start_inst_options[step].push([0]);
                }

                // Terminal instances
                terminal_inst_options.push([0]);
            }
        }

        // Get instance combinations
        let start_combinations = [];
        for (let step = 0; step < start_inst_options.length; step++) {
            start_combinations.push(
                generateCombinations(...start_inst_options[step])
            );
        };
        let terminal_combinations = generateCombinations(...terminal_inst_options);

        // Get instance combinations
        conjunctions[comb] = {
            'start': start_combinations,
            'terminal': terminal_combinations
        }
    }
    return conjunctions
}

// Decompose 1d array into 2d array based on if an element is non-zero
function decomposeArray(array) {
    const decomposed = [];
    for (let i = 0; i < array.length; i++) {
        if (array[i] === 1) {
            decomposed.push(createOneHotArray(array.length, i));
        };
    };
    return decomposed;
};

// Create composition feature option set
function createOptionsSet(comb, start_features, randomize_order=false) {

    // Get array of each feature to be shown
    let comb_features = decomposeArray(comb);

    // Randomize order of feature categories on screen
    if (randomize_order) {
        comb_features = jsPsych.randomization.shuffleNoRepeats(comb_features);
    };

    // Get instances per feature category to build option set
    let option_set = []
    for (const comb_feature of comb_features) {
        let instances = start_features[comb_feature];

        // Randomize order of instances on screen within category
        if (randomize_order) {
            instances = jsPsych.randomization.shuffleNoRepeats(instances)
        };
        option_set = option_set.concat([instances])
    }

    return option_set
}


// Generate composition trial order
function generateTrials(
    conjunctions,
    combs,
    start_features,
    feature_tmat,
    instance_tmat,
    n_repeats = 1,
    match_comb_to_target = false,
    non_match_level_freq = 1,
    shuffle_all = false,
    n_steps_levels = [1]
) {
    
    // For each feature combination create option sets
    let correct_compositions = [];
    let targets = [];
    let options = [];
    let n_causal = [];
    let n_inference_steps = [];
    for (const comb of combs) {

        // For each option set create targets
        let comb_correct_compositions = [];
        let comb_targets = [];
        let comb_options = [];
        let comb_n_inference_steps = [];
        for (const target_comb of combs) {
            
            // If matching composition and target features
            // skip this target_comb if features don't match
            if (
                (match_comb_to_target) &&
                (comb != target_comb)
            ) {
                continue
            }
            
            for (let step = 0; step < conjunctions[target_comb]['start'].length; step++) {

                for (const n_steps of n_steps_levels) {

                    // Skip if number of inference steps exceeds the
                    // maximum number of steps possible
                    if (step + n_steps > conjunctions[target_comb]['start'].length) {
                        continue
                    }

                    for (const start of conjunctions[target_comb]['start'][step]) {

                        // Get target
                        let target = Array.from(start);
                        for (let i = 0; i < n_steps; i++) {
                            target = getSuccessor(
                                target,
                                instance_tmat,
                                feature_tmat
                            );
                        };
                        
                        // Get target
                        // const target = getSuccessor(start, instance_tmat, feature_tmat)

                        // Does the conjunction's features have different
                        // instance levels? (e.g. [3, 2, 0, 0] not [3, 3, 0, 0])
                        const inst_levels = getUniqueNonZeroValues(target);
                        const non_matched_levels = inst_levels.length > 1;
                        const added_rate = non_matched_levels*(non_match_level_freq - 1);
                        const conj_rate = n_repeats + n_repeats*added_rate;

                        // Add correct composition for this combination
                        comb_correct_compositions = comb_correct_compositions.concat(
                            createRepeatingArray(
                                start,
                                conj_rate
                            )
                        );
                        
                        // Add to target set for this combination
                        comb_targets = comb_targets.concat(
                            createRepeatingArray(
                                target,
                                conj_rate
                            )
                        );

                        // Add to options set for this combination
                        for (let i = 0; i < conj_rate; i++) {
                            comb_options = comb_options.concat([
                                createOptionsSet(
                                    comb,
                                    start_features[step],
                                    randomize_order = true
                                )
                            ])
                        };

                        // Track which step this trial is
                        comb_n_inference_steps = comb_n_inference_steps.concat(
                            createRepeatingArray(
                                n_steps,
                                conj_rate
                            )
                        )
    
                    };
                };
            };
        };

        // Count number of causal inferences that can
        // be made based on the target and options
        let comb_n_causal = [];
        for (
            const [trial, correct_composition]
            of comb_correct_compositions.entries()
        ) {
            comb_n_causal = comb_n_causal.concat([
                countFeaturesInOptions(
                    correct_composition,
                    comb_options[trial]
                )
            ]);
        };

        // Shuffle trial order
        const idx = jsPsych.randomization.shuffleNoRepeats(
            createIntArray(comb_targets.length)
        );
        comb_correct_compositions = sortByIndex(comb_correct_compositions, idx);
        comb_targets = sortByIndex(comb_targets, idx);
        comb_options = sortByIndex(comb_options, idx);
        comb_n_causal = sortByIndex(comb_n_causal, idx);
        comb_n_inference_steps = sortByIndex(comb_n_inference_steps, idx);
        
        // Add to full set
        correct_compositions = correct_compositions.concat(comb_correct_compositions);
        targets = targets.concat(comb_targets);
        options = options.concat(comb_options);
        n_causal = n_causal.concat(comb_n_causal);
        n_inference_steps = n_inference_steps.concat(comb_n_inference_steps);
    };

    // Permute trial order
    if (shuffle_all) {
        const idx = jsPsych.randomization.shuffleNoRepeats(
            createIntArray(targets.length)
        );
        correct_compositions = sortByIndex(correct_compositions, idx);
        targets = sortByIndex(targets, idx);
        options = sortByIndex(options, idx);
        n_causal = sortByIndex(n_causal, idx);
        n_inference_steps = sortByIndex(n_inference_steps, idx);
    }

    return {
        'correct_compositions': correct_compositions,
        'targets': targets,
        'options': options,
        'n_causal': n_causal,
        'n_inference_steps': n_inference_steps
    };
};

// Get a transition matrix of most likely transitions in each row
function getMostLikelyTransitionMatrix(tmat) {
    let tmat_likely = [];
    for (const feat of tmat) {
        tmat_likely.push(createOneHotArray(tmat.length, argmax(feat)));
    }
    return tmat_likely
}

// Get successor given a conjunction and transition matrix
function getSuccessor(conjunction, inst_tmat, feat_tmat) {
    let successor = createRepeatingArray(0, conjunction.length);
    conjunction.forEach((inst, feat) => {
        if (inst > 0) {

            // Sample successor feature
            const succ_feat = jsPsych.randomization.sampleWithReplacement(
                createIntArray(feat_tmat.length),
                1,
                feat_tmat[feat]
            )[0];

            // Sample successor instance
            const succ_inst = jsPsych.randomization.sampleWithReplacement(
                createIntArray(inst_tmat.length),
                1,
                inst_tmat[inst - 1]
            )[0] + 1;

            // Add feature to successor
            successor[succ_feat] = succ_inst;
        };
    });
    return successor
}

// Convert index in image map to conjunction vector
function convertIndexToConjunction(index, n_feats, n_insts) {
    const inst = index % n_insts;
    const feat = ((index - inst)/n_insts);
    const conj = createOneHotArray(n_feats, feat, filled_value=(inst + 1));
    return conj
}

// Get file names for an array of conjunctions
function getTrialFileNames(
    conjs,
    task_to_stim_feature_map,
    task_to_stim_instance_map,
    random_flip = true,
    all_flip = false
) {
    let conj_fnames = [];
    for (let conj_step of conjs) {
        
        // "nest" targets
        if (!Array.isArray(conj_step[0])) {
            conj_step = [conj_step];
        }

        for (const conj of conj_step) {

            // randomly flip position of features
            let flip = false;
            if (random_flip) {
                flip = randomBool();
            } else if (all_flip) {
                flip = true;
            }

            // Convert conjunction to stimulus file name
            const conj_fname = conjToImage(
                conj,
                task_to_stim_feature_map,
                task_to_stim_instance_map,
                flipped = flip
            );

            // Add to list of file names 
            conj_fnames = conj_fnames.concat([conj_fname]);
        
        };
        

    };
    return conj_fnames;
};

// Get options file names
function getOptionsFileNames(
    options,
    task_to_stim_feature_map,
    task_to_stim_instance_map
) {
    let options_fnames = []
    let i = 0;
    for (const feature of options) {
        options_fnames = options_fnames.concat([[]])
        for (const option of feature) {
            options_fnames[i] = options_fnames[i].concat([
                getTrialFileNames(
                    option,
                    task_to_stim_feature_map,
                    task_to_stim_instance_map,
                    random_flip = false
                )
            ]);
        };
        i += 1;
    }
    return options_fnames;
};

// Convert conjunction to stimulus image file name
function conjToImage(
    conj,
    task_to_stim_feature_map,
    task_to_stim_instance_map,
    flipped = false
) {

    let stim_feats = {};
    for (const [feat, inst] of conj.entries()) {
        const stim_feat = task_to_stim_feature_map[feat.toString()];
        const stim_inst = task_to_stim_instance_map[stim_feat][inst];
        stim_feats[stim_feat] = stim_inst;
    } ;

    let stim_conj = [];
    for (const stim_feat of STIM_FEATS) {
        stim_conj = stim_conj.concat([stim_feat + '-' + stim_feats[stim_feat]]);
    };

    if (flipped) {
        stim_conj = stim_conj.concat(['flipped']);
    };

    stim_fname = 'img/' + stim_conj.join('_') + '.png';

    return stim_fname;
}

// Get practice file names
function getPracticeFileNames(conjs) {
    let conj_fnames = [];
    for (const conj of conjs) {
        conj_fnames = conj_fnames.concat(['img/practice_' + conj[0] + '.png']);
    };
    return conj_fnames
};

// Add img/ label to file names
function addImgDir(fnames) {
    let new_fnames = [];
    for (const fname of fnames) {
        new_fnames = new_fnames.concat(['img/' + fname])
    };
    return new_fnames
};