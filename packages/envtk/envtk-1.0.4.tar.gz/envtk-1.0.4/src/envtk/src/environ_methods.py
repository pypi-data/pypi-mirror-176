
__mkenv = lambda __name:f"python3 -m venv {__name}"
__activate = lambda __name:f"source {__name}/bin/activate;"
__create = lambda __name:f"{__mkenv(__name)};{__activate(__name)}"

def create(__name:str):
    return __create(__name)
