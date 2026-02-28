import pathlib

BASE_DIR: pathlib.Path = pathlib.Path(__file__).parent.parent
DATA_DIR: pathlib.Path = BASE_DIR / 'data'


FETCH_DATA: bool = True