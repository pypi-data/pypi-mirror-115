'''
Execute Python command in Plover using strokes.
'''


from pathlib import Path
import typing
import plover  # type: ignore


def py_command(engine: 'plover.engine.StenoEngine', command: str)->None:
	locals_={"engine": engine, "plover": plover}
	exec(command, {}, locals_)


def py_command_file(engine: 'plover.engine.StenoEngine', path: str)->None:
	py_command(engine, Path(path).read_text())
