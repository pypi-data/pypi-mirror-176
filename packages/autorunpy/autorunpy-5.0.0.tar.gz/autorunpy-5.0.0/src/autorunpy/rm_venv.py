"""

    """

import sys

from .auto import rm_venv


if __name__ == '__main__' :
    conf_fp = sys.argv[1]
    rm_venv(conf_fp)
