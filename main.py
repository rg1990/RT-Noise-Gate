'''
Driver code for the noise gate using the state pattern.

'''

from noise_gate_state_pattern import AudioConfig, Context
from gate_states import ClosedState
import numpy as np
import audiofile
import matplotlib.pyplot as plt
import time


# Define some helper/test functions
def load_audio(fpath):
    data, fs = audiofile.read(fpath)
    data = data.T
    if len(data.shape) == 2:
        data = data[:,0]    # convert to mono
    return data


def test_gate_coef_values_are_valid(coef_arr):
    print("Testing gate coef_array values")
    assert(np.all([0<=val<=1 for val in coef_arr]))


if __name__ == "__main__":
    
    # Configure some audio properties
    audio_config = AudioConfig(fs=44100)
    
    # Create a context instance to represent the noise gate
    context = Context(audio_config, ClosedState())
    
    # Load audio from file
    sig = load_audio(fpath="./data/snare_test.wav")
    # Zero-pad the audio array to enable lookahead (experimental)
    sig = np.pad(sig, [0, context.lookahead_pad_samples])
    
    # Initially just process the whole array to check it behaves as expected
    # Later you can implement an audio stream and process individual blocks in real time
    start_time = time.perf_counter()
    context.process_audio_block(sig)
    elapsed_time = time.perf_counter() - start_time
    print(f"Time taken to process {len(sig)/audio_config.fs:.2f} seconds of audio: {elapsed_time:.2f} seconds")
    
    # Some testing on the result
    test_gate_coef_values_are_valid(context.coef_array)
    
    # Plot the result
    plt.plot(context.mag_array[:-context.lookahead_pad_samples], color='blue', linewidth=1, label='signal magnitude')
    plt.plot(context.coef_array, color='green', label='gate coefficient')
    plt.plot(np.abs(context.processed_array), color='orange', label='gate output')
    plt.axhline(context.lin_thresh, color='black', linewidth=1, label='gate threshold')
    plt.legend()
    plt.show()