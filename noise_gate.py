import numpy as np
import ramp_functions as rf

'''
The original template code is found here:
    https://refactoring.guru/design-patterns/state/python/example
'''

class AudioConfig:
    '''
    Values that configure audio playback, so they can be set independently
    of, and shared between, different objects that need them.
    '''
    def __init__(self, fs, blocksize=1024):
        self.fs = fs
        self.blocksize = blocksize


class Context:
    """
    This class represents the noise gate.
    
    The Context defines the interface of interest to clients. It also maintains
    a reference to an instance of a State subclass, which represents the current
    state of the Context.
    """

    def __init__(self, audio_config, state) -> None:
        self.audio_config = audio_config
        self.transition_to(state)
        
        # An on/off switch
        self.enabled = True

        # Specify an initial threshold value in dBFS
        self.thresh = -20
                
        # Specify attack, hold, release, and lookahead periods in seconds
        self.attack_time = 0 # seconds
        self.hold_time = 0.05  # seconds
        self.release_time = 0.05  # seconds
        self.lookahead_time = 0 # seconds
        
        # Calculate attack, hold, and release periods in samples
        self.attack_period_in_samples = self.seconds_to_samples(self.audio_config.fs, self.attack_time)        
        self.hold_period_in_samples = self.seconds_to_samples(self.audio_config.fs, self.hold_time)
        self.release_period_in_samples = self.seconds_to_samples(self.audio_config.fs, self.release_time)
        self.lookahead_period_in_samples = self.seconds_to_samples(self.audio_config.fs, self.lookahead_time)
        
        # Get zero padding for lookahead. Number of zeros determined by max lookahead time
        max_lookahead_time = 0.01 # seconds
        self.lookahead_pad_samples = 0 #self.seconds_to_samples(self.audio_config.fs, max_lookahead_time)
        
        # Define the attack and release multiplier ramps
        self.attack_ramp = rf.ramp_poly_increase(num_points=self.attack_period_in_samples)
        self.release_ramp = rf.ramp_poly_decrease(num_points=self.release_period_in_samples)
        
        # Initialise attributes for arrays
        self.processed_array = None
        self.coef_array = None
        self.mag_array = None
        
        # Attributes for debugging
        self.text_output = []


    def transition_to(self, state):
        """
        The Context allows changing the State object at runtime.
        """
        self._state = state
        self._state.context = self


    # Setters for gate parameters
    def set_attack_time(self, new_attack_time: float) -> None:
        self.attack_time = new_attack_time
        self.attack_period_in_samples = self.seconds_to_samples(self.audio_config.fs, self.attack_time)
        
        # Reset the sample counter to avoid index errors caused by shortening the attack time to a value
        # below the current sample_counter value
        self._state.sample_counter = 0
        # If we have attack time of zero, we immediately apply a coefficient of 1
        if self.attack_period_in_samples == 0:
            self.attack_ramp = np.array([1])
        else:
            self.attack_ramp = rf.ramp_poly_increase(num_points=self.attack_period_in_samples)
        #print(f"Samples in state: {self._state.sample_counter}. Len attack_ramp = {len(self.attack_ramp)}")
    
    
    def set_hold_time(self, new_hold_time: float) -> None:
        self.hold_time = new_hold_time
        self.hold_period_in_samples = self.seconds_to_samples(self.audio_config.fs, self.hold_time)
        
        
    def set_release_time(self, new_release_time: float) -> None:
        self.release_time = new_release_time
        self.release_period_in_samples = self.seconds_to_samples(self.audio_config.fs, self.release_time)

        # Reset the sample counter to avoid index errors caused by shortening the release time to a value
        # below the current sample_counter value
        self._state.sample_counter = 0
        # If we have release time of zero, we immediately apply a coefficient of 0
        if self.release_period_in_samples == 0:
            self.release_ramp = np.array([0])
        else:
            self.release_ramp = rf.ramp_poly_decrease(num_points=self.release_period_in_samples)
        #print(f"Samples in state: {self._state.sample_counter}. Len release = {len(self.release_ramp)}")



    @property
    def thresh(self) -> int:
        return self._thresh
    
    
    @thresh.setter
    def thresh(self, new_thresh: int) -> None:
        self._thresh = new_thresh


    @property
    def lin_thresh(self) -> float:
        return self.dBFS_to_lin(self.thresh)
    
    
    # These staticmethods could equally be defined outside the class
    @staticmethod
    def dBFS_to_lin(dBFS_val):
        ''' Helper method to convert a dBFS value to a linear value [0, 1] '''
        return 10 ** (dBFS_val / 20)
        

    @staticmethod
    def seconds_to_samples(fs, seconds_val):
        ''' Helper method to convert a time (seconds) value to a number of samples '''
        if seconds_val == 0:
            return 1
        else:
            return int(fs * seconds_val)

    
    # def process_audio_block(self, audio_array=None):
    #     '''
    #     Process an array of audio samples according to the gate's parameters,
    #     current state, and the sample values in the audio array.
    #     This implementation includes lookahead logic.
        
    #     '''
        
    #     # Initialise an array of coefficient values of the same length as audio_array
    #     # Set initial coefficient values outside valid range [0, 1] for easier debugging
    #     self.coef_array = np.ones(len(audio_array))[:-self.lookahead_pad_samples] * 2
    #     # Get the magnitude values of the audio array
    #     self.mag_array = np.abs(audio_array)

    #     # Iterate through the samples of the mag_arr, updating coef_array values
    #     for i, sample_mag in enumerate(self.mag_array[:-self.lookahead_pad_samples]):    
    #         # Get the coefficient value for the current sample, considering a lookahead period
    #         self.coef_array[i] = self._state.get_sample_coefficient(self.mag_array[i + self.lookahead_period_in_samples])
    #         # Increment the counter for tracking the samples elapsed in the current state
    #         self._state.sample_counter += 1
    #         # Create a log of the state and samples elapsed, for debugging
    #         self.text_output.append(f"{type(self._state).__name__}. {self._state.sample_counter}. {self.coef_array[i]:.3f}")
    #         # After processing the current sample, check if a transition is due
    #         self._state.handle_state_transition()
            
    #     self.processed_array = self.coef_array * audio_array[:-self.lookahead_pad_samples]


    def process_audio_block(self, audio_array=None):
        '''
        Process an array of audio samples according to the gate's parameters,
        current state, and the sample values in the audio array.
        This implementation includes lookahead logic.
        
        '''
        if not self.enabled:
            self.processed_array = audio_array
        else:
            # Initialise an array of coefficient values of the same length as audio_array
            # Set initial coefficient values outside valid range [0, 1] for easier debugging
            self.coef_array = np.ones(len(audio_array)) * 2
            # Get the magnitude values of the audio array
            self.mag_array = np.abs(audio_array)

            # Iterate through the samples of the mag_arr, updating coef_array values
            for i, sample_mag in enumerate(self.mag_array):    
                # Get the coefficient value for the current sample, considering a lookahead period
                self.coef_array[i] = self._state.get_sample_coefficient(self.mag_array[i])
                # Increment the counter for tracking the samples elapsed in the current state
                self._state.sample_counter += 1
                # Create a log of the state and samples elapsed, for debugging
                self.text_output.append(f"{type(self._state).__name__}. {self._state.sample_counter}. {self.coef_array[i]:.3f}")
                # After processing the current sample, check if a transition is due
                self._state.handle_state_transition()
                
            self.processed_array = self.coef_array * audio_array