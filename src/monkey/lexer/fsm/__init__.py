from typing import Callable, Tuple

class DFA:
    """The class simulates DFA Finite Machine"""
    def __init__(self, states: set, start_state: str, final_states: set, transition: Callable[[str, str], str]):
        """Create a DFA

        Args:
            states: set of all states in the DFA.
            start_state: start state of the DFA.
            final_states: set of accepting states.
            transition: A transition function should take current state and
                symbol and return next state if any otherwise None. 
        """
        self.states = states
        self.start = start_state
        self.final_states = final_states
        self.transition = transition
        
    def run(self, input: str) -> Tuple[bool, str]:
        """simulates self DFA against given input. 

        Args:
            input: character string to simulate

        Returns:
            A tuple of (accepted, value) where the
            accepted is a boolean represents whether
            starting part of input is accepted by DFA
            and value is a str contains part of the
            input accepted.
        """

        current_state = self.start

        buffer = ""

        for symbol in input:
            next_state = self.transition(current_state, symbol)
            if next_state is None:
                break
            buffer += symbol
            current_state = next_state
        
        accepted = current_state in self.final_states
        value = buffer
        
        return accepted, value

