/*
 * General utility functions
 */

// Create integer array of a given length
function createIntArray(length) {
    return Array.from({length}, (_, index) => index);
}

// Create an array of repeated values
function createRepeatingArray(value, count) {
    return Array(count).fill(value);
}

// Create an array of repeated 2D arrays
function repeat2DArray(array2D, count) {
    const array3D = [];
    for (let i = 0; i < count; i++) {
        const array2DCopy = array2D.map(row => row.slice());
        array3D.push(array2DCopy);
    }
    return array3D;
}

// Repeat values in an array some number of times
function repeatArray(array, repeats) {
    return array.flatMap(value => createRepeatingArray(value, repeats));
}

// Created a repeating tiled array
function tileArray(array, repeats) {
    const repeatedArray = [];
    for (let i = 0; i < repeats; i++) {
        repeatedArray.push(...array);
    }
    return repeatedArray;
}

// Add value to array 
function addValueToArray(array, value) {
    for (let i = 0; i < array.length; i++) {
        array[i] += value;
    }
    return array;
}

// Zip two arrays into key-value pairs
function zipArrays(keys, values) {
    const result = {};
    keys.forEach((key, index) => {
        result[key] = values[index];
    });
    return result;
}

// Sum of array values
function arraySum(array) {
    return array.reduce((partialSum, a) => partialSum + a, 0);
}

// Element-wise sum of two arrays
function elementWiseSum(array_1, array_2) {
    if ((array_1 == null) || (array_2 == null)) {
        return null
    }
    const result = [];
    for (let i = 0; i < array_1.length; i++) {
        result.push(array_1[i] + array_2[i]);
    }
    return result;
}

// Are arr1 and arr2 the same?
function arraysEqual(arr1, arr2) {
    const same_length = (arr1.length === arr2.length);
    const same_values = arr1.every((value, index) => value === arr2[index]);
    return (same_length && same_values)
}

// Sort array by some index array
function sortByIndex(array, idx) {
    return idx.map(index => array[index]);
}

// Get non-zero values
function getNonZeroValues(array) {
    let non_zero_values = array.filter(value => value !== 0);
    return non_zero_values
}

// Get unique non-zero values of array
function getUniqueNonZeroValues(array) {
    let non_zero_values = getNonZeroValues(array);
    non_zero_values = [...new Set(non_zero_values)];
    return non_zero_values;
}

// Convert non-zero values of 1d array to 1
function binarizeArray(array) {
    let array_binary = [];
    for (const value of array) {
        array_binary.push(Number(value != 0))
    }
    return array_binary
}

// Is 1d array subarray in 2d array array?
function isSubarrayIn2DArray(subarray, array) {
    for (let i = 0; i < array.length; i++) {
      if (arraysEqual(subarray, array[i])) {
            return true;
        }
    }
    return false;
}

// Does arr1 have at least one common element with arr2
function hasCommonElements(arr1, arr2) {
    return arr1.some(item => arr2.includes(item));
};

// Get argmax of an array
function argmax(array) {
    if (array.length === 0) {
        // Handle empty array case
        return -1; // Return -1 or another appropriate value
    }
  
    let maxIndex = 0;
    let maxValue = array[0];
  
    for (let i = 1; i < array.length; i++) {
        if (array[i] > maxValue) {
            maxValue = array[i];
            maxIndex = i;
        }
    }
    return maxIndex;
}

// Create onehot array
function createOneHotArray(size, index, filled_value=1) {
    if (index < 0 || index >= size) {
        // Handle invalid index
        console.error("Invalid index for one-hot array.");
        return null;
    }
  
    const oneHotArray = Array(size).fill(0);
    oneHotArray[index] = filled_value; // can specify val other than 1
  
    return oneHotArray;
}

// Randomly sample true or false
function randomBool() {
    outcome = jsPsych.randomization.sampleWithoutReplacement(
        [false, true],
        1
    )[0];
    return outcome;
}

// Generate a random integer between min (inclusive) and max (exclusive)
function getRandomInt(min, max) {
    return Math.floor(Math.random() * (max - min + 1)) + min;
  }

// Sample random index from array
function getRandomIndex(array) {
    return Math.floor(Math.random() * array.length);
}

// Randomly shuffle array
function shuffle(array) {
    for (let i = array.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [array[i], array[j]] = [array[j], array[i]];
    };
};


// Save dictionary as json or js var
// Delay time used for multiple downloads 
function saveDictionaryWithDelay(
    dict,
    file_type,
    fname,
    delay_time=0,
    var_name=null
) {
    setTimeout(() => {
        let jsonString = null;
        let blob = null;

        // Save as json
        if (file_type == 'json') {
            jsonString = JSON.stringify(dict, null, 2);
            blob = new Blob([jsonString], {type: 'application/json'});

        // Save as js
        } else if (file_type == 'js') {
            jsString = `var ${var_name} = ${JSON.stringify(dict, null, 2)};`;
            blob = new Blob([jsString], {type: 'application/javascript'});
        }

        // Download file
        const a = document.createElement('a');
        a.href = URL.createObjectURL(blob);
        fname = fname.replace(/\..*$/, '') + '.' + file_type;
        a.download = fname;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(a.href);

        console.log(`Saved: ${fname}`)
    }, delay_time); 
}
  
