import os
ascii_art = r'''
    __       __                      _                __
    \ \     / /____  _________ ___  (_)________  ____/ /__  _____
     \ \   / __/ _ \/ ___/ __ `__ \/ / ___/ __ \/ __  / _ \/ ___/
     / /  / /_/  __/ /  / / / / / / / /__/ /_/ / /_/ /  __/ /
    /_/   \__/\___/_/  /_/ /_/ /_/_/\___/\____/\__,_/\___/_/
'''

try:
    default_judge = os.environ["TERMICODER_JUDGE"]
except KeyError:
    default_judge = None
