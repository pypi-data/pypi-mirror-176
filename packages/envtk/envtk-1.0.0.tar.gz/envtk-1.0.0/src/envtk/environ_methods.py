__create = lambda __name:f"""
python3 -m venv {__name};
source __{__name}/bin/activate;
"""

def create(__name:str):
    return __create(__name)
