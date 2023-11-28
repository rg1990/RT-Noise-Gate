import numpy as np
import matplotlib.pyplot as plt
import sounddevice as sd
from enum import Enum
from noise_gate import AudioConfig, Context
from gate_states import ClosedState
from queue import Queue


class PlaybackState(Enum):
    PLAYING = 1
    STOPPED = 2


class Player:
    def __init__(self, audio_config, audio_array):
        self.audio_config = audio_config
        self.audio_array = audio_array
        self.q = Queue()    # rename this
        self.stream = self.create_output_stream()
        self.gen = self.audio_generator_function()
        
        self.start_idx = 0
        self.playing = False
        
        self.pause_behaviour = False

        self.noise_gate = Context(self.audio_config, state=ClosedState())
        self.noise_gate.lookahead_pad_samples = 0

        self.stream.start()
        
        
    def create_output_stream(self):
        return sd.OutputStream(samplerate=self.audio_config.fs,
                                channels=1,
                                callback=self.output_callback,
                                blocksize=self.audio_config.blocksize)
    
    
    def set_audio_array(self, audio_array):
        self.audio_array = audio_array
        
    
    def set_start_idx(self, new_start_idx):
        # TODO Input validation
        self.start_idx = new_start_idx
        print(f"In Player class. New start_idx set to {self.start_idx}")
        
        # Create a new generator object with the new start_idx
        self.gen = self.audio_generator_function(start_idx=new_start_idx)
        
        
    def play_stop_command(self):
        # Play -> stop/pause
        if self.playing:
            #self.stream.stop()
            self.playing = False
            if not self.pause_behaviour:
                # This line means stop->start resumes from the previously selected playhead position
                # Otherwise the space bar acts as a pause function
                self.set_start_idx(new_start_idx=self.start_idx)
                # Redraw the playhead
                #self.display.set_playhead_position(self.start_idx)
        
        # Stop/pause -> play
        else:
            #print("Starting stream")
            #print(self.start_idx)
            #self.stream.start()
            self.playing = True
            
        print(self.stream.active)
            
        print(f"In Player.play_stop_command(). playing: {self.playing}")
        
        
    def output_callback(self, outdata, frames, time, status):
        try:
            if self.playing:
                data = next(self.gen).reshape(-1, 1)
                self.noise_gate.process_audio_block(data[:,0])
                gated_data = self.noise_gate.processed_array.reshape(-1, 1)
            else:
                data = np.zeros((self.audio_config.blocksize, 1))
                gated_data = np.zeros((self.audio_config.blocksize, 1))

            self.q.put_nowait([data, gated_data])
        
        except StopIteration:
            # Redraw the playhead
            #self.display.set_playhead_position(self.start_idx)
            # Create a new generator object with the new start_idx
            print(self.start_idx)
            self.gen = self.audio_generator_function(start_idx=self.start_idx)
            self.playing = False
            print(self.playing)
            
            self.stream.stop()
            raise sd.CallbackStop
        
        #outdata[:] = data
        outdata[:] = gated_data
        
        
    def audio_generator_function(self, start_idx=0):
        # Take a slice of the main audio_array if start_idx != 0
        arr = self.audio_array[start_idx:]
        
        # Find the number of sub-arrays we will create
        num_arrays = (len(arr) // self.audio_config.blocksize) + 1
        for i in range(num_arrays):
            
            # Try updating the GUI
            #self.display.set_playhead_position(start_idx + (i * self.audio_config.blocksize))
            
            # Slice a blocksize sub-array from the main array
            sub_arr = arr[i*self.audio_config.blocksize : (i+1)*self.audio_config.blocksize]
            
            # Check if we need to pad sub_arr to have the required shape
            if len(sub_arr) < self.audio_config.blocksize:
                sub_arr = np.pad(sub_arr, [0, self.audio_config.blocksize-len(sub_arr)])
            yield sub_arr
        
