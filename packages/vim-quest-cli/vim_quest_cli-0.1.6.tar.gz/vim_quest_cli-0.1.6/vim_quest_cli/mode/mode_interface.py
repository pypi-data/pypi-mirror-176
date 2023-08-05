# TODO: tests that take a mode (every mode with seed needs a seed in the init)
# and do unittest on them. Pushing a few key and expecting the output.
from typing import Iterable

from vim_quest_cli.engine.engine_interface import EngineInterface, EngineState
from vim_quest_cli.interface.mapping import Keys
from vim_quest_cli.view.view import ViewFactory, ViewData


class Mode:
    engine: EngineInterface
    state: EngineState
    view: ViewFactory

    def __init__(self, engine: EngineInterface, state: EngineState, view: ViewFactory):
        self._engine = engine
        self._state = state
        self._view = view
        self._init_after_params()

    def feedkeys(self, keys: Iterable[Keys] = ()) -> ViewData:

        state_previous = self._state.with_added_command(keys)
        state_next = self._engine.process(self._state.with_added_command(keys))

        self._state = self.state_change(state_previous, state_next)

        view = self._view.createView(self._state)
        return self.change_view(view)

    # To be overloaded by subclasses
    def _init_after_params(self):
        pass

    def change_view(self, view: ViewData) -> ViewData:
        return view

    def state_change(
        self, state_init: EngineState, state_end: EngineState
    ) -> EngineState:
        return state_end


"""

the screeze has to be passed around for mode to be able to use it.
Maybe in a GeneralConfig structure ?
- If the printing is unicode friendly or not.

    create_new_path
        - keep the curspor pos.
        - Generate a target to go
    When someting moves :
        - Check if the move ends up on the target,
        - If yes, then create new path.
    When printing happens :
        - change the target in red (first by just changing the target text by the red addition)

Improvements :
    - Cancel every non-movement.
    - Have the redness be part of the visual buffer.
    - Then add the target as metadata of the input, and use that to check what's happening.
"""

"""         
            k 
            ^ 
        h < x > l
            v
            j
             
"""


class PassthroughMode:

    pass
