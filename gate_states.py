from abc import ABC, abstractmethod


class State(ABC):
    """
    The base State class declares methods that all concrete States should
    implement and also provides a backreference to the Context object,
    associated with the State. This backreference can be used by States to
    transition the Context to another State.
    """

    @property
    def context(self):
        return self._context


    @context.setter
    def context(self, context) -> None:
        self._context = context


    @abstractmethod
    def get_sample_coefficient(self, sample_mag: float) -> float:
        pass
    
    
    @abstractmethod
    def check_if_state_transition_is_due(self, sample_mag: float=None) -> None:
        pass
    
    
    @abstractmethod
    def on_entry(self):
        # This method may not be needed
        pass
    
    
    @abstractmethod
    def on_exit(self):
        pass


"""
Concrete States implement various behaviors, associated with a state of the
Context.
"""

class ClosedState(State):
    
    def __init__(self):
        self.sample_counter = 0
        self.transition_pending = False
    
    
    def get_sample_coefficient(self, sample_mag: float=0) -> float:
        ''' 
        Get the appropriate coefficient value to multiply with the current
        audio sample value.
        
        In the closed state, the coefficient is always 0.0.
        '''
        
        self.transition_pending = self.check_if_state_transition_is_due(sample_mag)
        return 0.0
        
    
    def check_if_state_transition_is_due(self, sample_mag: float=0) -> None:
        '''
        Check if a condition is met that initiates a transition.
        For ClosedState, we want to check if the sample magnitude exceeds the threshold.
        '''
        return sample_mag > self.context.lin_thresh
    
    
    def on_entry(self):
        pass
    
    
    def on_exit(self):
        pass
        
        
    def handle_state_transition(self):
        if self.transition_pending:
            self.context.transition_to(OpeningState())


class OpeningState(State):
    '''
    - In OpeningState, the coefficient is determined by the shape of the
        specified attack ramp.
    
    - The only state we can transition to from OpeningState is OpenState.
    '''
    
    def __init__(self):
        self.sample_counter = 0
        self.transition_pending = False
    
    
    def get_sample_coefficient(self, sample_mag: float=0) -> float:        
        self.transition_pending = self.check_if_state_transition_is_due()
        if self.transition_pending:
            return 1.0
        else:
            # Get a value from the gate's attack ramp
            return self.context.attack_ramp[self.sample_counter]
        
        
    def check_if_state_transition_is_due(self, sample_mag: float=0) -> None:
        # Transition to OpenState occurs once attack period has elapsed
        return self.sample_counter >= self.context.attack_period_in_samples
    
    
    def handle_state_transition(self):
        if self.transition_pending:
            self.context.transition_to(OpenState())
            self.on_exit()
    
    
    def on_entry(self):
        pass
    
    
    def on_exit(self):
        # This may not be needed, since we construct a new instance when
        # transitioning, but it may make it more robust
        self.sample_counter = 0
    

class OpenState(State):
    '''
    In OpenState, the coefficient is always 1.0.
    The only state we can transition to from OpenState is ClosingState.
    '''
    
    def __init__(self):
        self.sample_counter = 0
        self.transition_pending = False
    
    
    def get_sample_coefficient(self, sample_mag: float=0) -> float:
        self.transition_pending = self.check_if_state_transition_is_due(sample_mag)
        return 1.0
    
    
    def check_if_state_transition_is_due(self, sample_mag: float=0) -> None:
        # The gate can't transition before its hold period has elapsed
        if self.sample_counter < self.context.hold_period_in_samples:
            return False
        else:
            # If the signal magnitude falls below the threshold, we want to
            # transition to ClosingState.
            return sample_mag < self.context.lin_thresh
    
    
    def on_entry(self):
        pass
    
    
    def on_exit(self):
        # This may not be needed, since we construct a new instance when
        # transitioning, but it may make it more robust
        self.sample_counter = 0
        
        
    def handle_state_transition(self):
        if self.transition_pending:
            self.context.transition_to(ClosingState())
            self.on_exit()
    

class ClosingState(State):
    '''
    In ClosingState:
    - The coefficient is determined by the shape of the specified release ramp.
    - The state can transition to either ClosedState or OpenState.
    '''
    
    def __init__(self):
        self.sample_counter = 0
        self.transition_pending = False
        self.new_state = None
    
    
    def get_sample_coefficient(self, sample_mag: float=0) -> float:
        self.transition_pending = self.check_if_state_transition_is_due(sample_mag)
        return self.context.release_ramp[self.sample_counter]
        
        
    def check_if_state_transition_is_due(self, sample_mag: float=0) -> None:        
        ''' There are two possible states that we can transition to from ClosingState. '''
        if sample_mag > self.context.lin_thresh:
            self.transition_pending = True
            self.new_state = OpenState()
            return True
        
        # TODO - find out why we need a -1 here to avoid an IndexError
        if self.sample_counter >= self.context.release_period_in_samples-1:
            self.transition_pending = True
            self.new_state = ClosedState()
            return True
        
        
    def handle_state_transition(self):
        if self.transition_pending:
            self.context.transition_to(self.new_state)
            self.on_exit()
        
        
    def on_entry(self):
        pass
    
    
    def on_exit(self):
        # This may not be needed, since we construct a new instance when
        # transitioning, but it may make it more robust
        self.sample_counter = 0