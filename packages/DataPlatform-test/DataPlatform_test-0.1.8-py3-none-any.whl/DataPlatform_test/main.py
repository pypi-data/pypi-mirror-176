import sys
import fire
from version import version


sys.path.append('..')


def call_funcs():
    fire.Fire(
        {
            "-v": version
        }
    )

if __name__ == "__main__":
    call_funcs()