# TODO: using .executor_interface instead of full path failed when bundle.
from contextlib import suppress
from typing import Optional

from vim_quest_cli.engine.engine_interface import (
    EngineInterface,
    EngineState,
    CursorPos,
)
from vim_quest_cli.interface.mapping import Keys


class NoCommandLeftException(Exception):
    pass


def clamp(n, minn, maxn):
    return max(min(maxn, n), minn)


NUMBERS = {0, 1, 2, 3, 4, 5, 6, 7, 9}
END_OF_LINE_MAX = 2147483647
LINE_BUFFER = 5


class PurePythonEngine(EngineInterface):
    def process(self, state: EngineState) -> EngineState:

        previous_state, next_state = state, state
        with suppress(NoCommandLeftException):
            while previous_state.command:
                next_state = self._execute_single_command(previous_state)
                previous_state = next_state

        return next_state

    def _execute_single_command(self, state: EngineState) -> EngineState:
        if not state.command:
            return state
        c = state.command[:]

        # First try to read numbers
        number = None
        if c[0] in [1, 2, 3, 4, 5, 6, 7, 8, 9]:
            number_str = c.pop(0)
            while c[0] in self.NUMBERS:
                number_str += c.pop(0)
            number = int(number_str)

        if c[0] == Keys.Down or c[0] == "j":
            return self._cursor_down(number, state.copy(command=c[1:]))

        if c[0] == Keys.Up or state.command[0] == "k":
            return self._cursor_up(number, state.copy(command=c[1:]))

        if c[0] == Keys.Left or state.command[0] == "h":
            return self._cursor_left(number, state.copy(command=c[1:]))

        if c[0] == Keys.Right or state.command[0] == "l":
            return self._cursor_right(number, state.copy(command=c[1:]))

        if c[0] == "$":
            return self._cursor_end_of_line(number, state.copy(command=c[1:]))

        if c[0] == "0":
            return self._cursor_beginning_of_line(number, state.copy(command=c[1:]))

        if c[0] == "G":
            return self._cursor_end_of_file(number, state.copy(command=c[1:]))

        if c[0:2] == ["g", "g"]:
            return self._cursor_beginning_of_file(number, state.copy(command=c[2:]))

        if c[0:2] == ["d", "d"]:
            return self._delete_line(number, state.copy(command=c[2:]))

        if c[-1] == Keys.Escape:  # TODO: it's not specifically like that
            return state.copy(command=[])

        raise NoCommandLeftException()

    @staticmethod
    def _cursor_down(number: Optional[int], state: EngineState) -> EngineState:
        number = number or 1
        new_lnum = min(state.cursor.line + number, len(state.buffer))
        col = min(
            state.cursor.col_want, PurePythonEngine._get_line_len(state, new_lnum)
        )
        return state.copy(cursor=state.cursor.copy(line=new_lnum, col=col))

    @staticmethod
    def _cursor_up(number: Optional[int], state: EngineState) -> EngineState:
        number = number or 1
        new_lnum = max(state.cursor.line - number, 1)
        col = min(
            state.cursor.col_want, PurePythonEngine._get_line_len(state, new_lnum)
        )
        return state.copy(cursor=state.cursor.copy(line=new_lnum, col=col))

    @staticmethod
    def _cursor_left(number: Optional[int], state: EngineState) -> EngineState:
        number = number or 1
        new_col = max(state.cursor.col - number, 1)
        return state.copy(cursor=state.cursor.copy(col=new_col, col_want=new_col))

    @staticmethod
    def _cursor_right(number: Optional[int], state: EngineState) -> EngineState:
        number = number or 1
        new_col = min(state.cursor.col + number, PurePythonEngine._get_line_len(state))
        return state.copy(cursor=state.cursor.copy(col=new_col, col_want=new_col))

    @staticmethod
    def _cursor_end_of_line(number: Optional[int], state: EngineState) -> EngineState:
        number = number or 1
        new_lnum = min(state.cursor.line + number - 1, len(state.buffer))
        if number == 1:  # Normal case
            return state.copy(
                cursor=state.cursor.copy(
                    line=new_lnum,
                    col=PurePythonEngine._get_line_len(state, new_lnum),
                    col_want=END_OF_LINE_MAX,
                )
            )

    @staticmethod
    def _cursor_beginning_of_line(
        number: Optional[int], state: EngineState
    ) -> EngineState:
        if number is not None:
            raise ValueError(
                "Cannot have beginning of line with number != 1 \n\n" + repr(state)
            )
        return state.copy(
            cursor=state.cursor.copy(
                col=1,
                col_want=1,
            )
        )

    @staticmethod
    def _cursor_end_of_file(number: Optional[int], state: EngineState) -> EngineState:
        if number is None:
            number = len(state.buffer)
        # TODO : It starts at the first non-space character.
        new_lnum = clamp(number, 0, len(state.buffer))
        new_col_num = PurePythonEngine._get_first_non_space_char(state, new_lnum)
        return state.copy(
            cursor=state.cursor.copy(
                line=new_lnum,
                col=new_col_num,
                col_want=new_col_num,
            )
        )

    @staticmethod
    def _cursor_beginning_of_file(
        number: Optional[int], state: EngineState
    ) -> EngineState:
        if number is None:
            number = 1
        new_lnum = clamp(number, 0, len(state.buffer))
        new_col_num = PurePythonEngine._get_first_non_space_char(state, new_lnum)
        return state.copy(
            cursor=state.cursor.copy(
                line=new_lnum,
                col=new_col_num,
                col_want=new_col_num,
            )
        )

    @staticmethod
    def _get_line_len(
        state: EngineState, line: Optional[int] = None, min_1: bool = True
    ) -> int:
        lnum = state.cursor.line if line is None else line
        line_len = len(state.buffer[lnum - 1])
        if min_1:
            line_len = max(line_len, 1)
        return line_len

    @staticmethod
    def _get_first_non_space_char(
        state: EngineState, lnum: Optional[int] = None, min_1: bool = True
    ) -> int:
        """Used for cursor positioning"""
        lnum = state.cursor.line if lnum is None else lnum
        line = state.buffer[lnum - 1]
        res = 0
        for res, char in enumerate(line):
            if char not in (" ", "\t"):
                break
        return max(res + 1, 1 if min_1 else 0)

    @staticmethod
    def _refresh_view(state):
        cursor_y = state.cursor_lnum

        # Find the max and min of the view, count the lines buffers and absolute min max
        max_view = min(
            cursor_y - 1 - LINE_BUFFER, len(state.buffer) - state.screen_rows - 1
        )
        min_view = max(cursor_y - state.screen_rows + LINE_BUFFER, 0)

        # If the view is inside
        if state.screen_ypos <= min_view:
            return state.copy(screen_ypos=min_view)

        if state.screen_ypos >= max_view:
            return state.copy(screen_ypos=max_view)

        return state

    def _delete_line(self, number: Optional[int], state: EngineState):
        new_buffer = (
            state.buffer[0 : state.cursor.line] + state.buffer[state.cursor.line + 1 :]
        )
        return state.copy(buffer=new_buffer)
