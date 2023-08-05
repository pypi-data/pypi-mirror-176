#!/usr/bin/env python3.8
import argparse
import dataclasses
import enum

from vim_quest_cli.deps import create_modules_if_is_js  # Keep as the first module
from vim_quest_cli.corpus import labyrinth
from vim_quest_cli.engine.engine_interface import EngineState, EngineInterface
from vim_quest_cli.engine.pure_python.pure_python_engine import PurePythonEngine
from vim_quest_cli.engine.vim_exe.vim_exe_engine import VimExeEngine
from vim_quest_cli.interface.curses_window import Window
from vim_quest_cli.interface.terminal_ui import TerminalUI
from vim_quest_cli.mode.go_to_x import GoToXMode
from vim_quest_cli.mode.labyrinth import LabyrinthMode
from vim_quest_cli.mode.mode_interface import Mode
from vim_quest_cli.view.view import ViewFactory


class Engines(enum.Enum):
    PURE_PYTHON = PurePythonEngine
    VIM_EXE = VimExeEngine
    DEFAULT = PurePythonEngine


class Modes(enum.Enum):
    GOT_TO_X = GoToXMode
    LABYRINTH = LabyrinthMode


@dataclasses.dataclass(frozen=True)
class Options:
    engine_cls: EngineInterface
    terminal: str


def parse_args() -> Options:
    parser = argparse.ArgumentParser(description="Vim powaa.")
    parser.add_argument(
        "-e",
        "--engine",
        default=Engines.DEFAULT.value,
        type=lambda v: Engines[v].value,
        choices=[e.name for e in Engines],
        help="Select and engine to use",
    )
    parser.add_argument(
        "-t",
        "--terminal",
        default="ansi",
        choices=("ansi", "curses"),
        help="wich terminal to use",
    )
    # TODO add param for the mode
    # TODO add param for a file to load

    parsed_args = parser.parse_args()
    return Options(
        engine_cls=parsed_args.engine,
        terminal=parsed_args.terminal,
    )


def main():
    args = parse_args()

    state = EngineState(
        buffer="tu to\nto#to\nti#ti\ntu#tu\nti tu".split("\n"),
    )

    mode_cls = Modes.GOT_TO_X.value

    mode = mode_cls(
        engine=args.engine_cls(),
        view=ViewFactory(),
        state=state,
    )

    t = TerminalUI(mode=mode)

    if args.terminal == "ansi":
        t.start_ansi()
    elif args.terminal == "curses":
        t.start_curses()
    else:
        raise ValueError("Terminal parameters not in [ansi|curses]")


def as_single_method():
    t = TerminalUI(
        mode=Modes.GOT_TO_X.value(
            engine=PurePythonEngine(),
            view=ViewFactory(),
            state=EngineState(
                buffer="tu to\nto#to\nti#ti\ntu#tu\nti tu".split("\n"),
            ),
        ),
    )

    def res_method(user_input: str) -> str:
        res = []
        w = Window(stdout_write_fct=res.append)
        t.loop_one_step(user_input, w)

        return "".join(res)

    return res_method


if __name__ == "__main__":
    main()
