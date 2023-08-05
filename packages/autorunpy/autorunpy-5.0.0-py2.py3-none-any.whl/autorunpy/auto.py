"""

    """

import subprocess

from .github_release import download_latest_release
from .util import Conf
from .util import get_user_repo_from_url
from .util import read_json


cnf = Conf()

def make_venv(fp = cnf.def_fn) :
    js = read_json(fp)

    rp_url = js[cnf.repo_url]
    usrp = get_user_repo_from_url(rp_url)

    pyv = js[cnf.python_version]

    subprocess.run(['pyenv' , 'install' , '--skip-existing' , pyv])
    subprocess.run(['pyenv' , 'virtualenv-delete' , '-f' , usrp.user_und_repo])
    subprocess.run(['pyenv' , 'virtualenv' , pyv , usrp.user_und_repo])

    print(usrp.user_und_repo)

def dl_and_ret_dirpath(fp = cnf.def_fn) :
    js = read_json(fp)
    rp_url = js[cnf.repo_url]
    dirp = download_latest_release(rp_url)
    print(dirp)

def ret_module_2_run_name(fp = cnf.def_fn) :
    js = read_json(fp)
    print(js[cnf.module_2_run])

def rm_venv(fp = cnf.def_fn) :
    js = read_json(fp)

    rp_url = js[cnf.repo_url]
    usrp = get_user_repo_from_url(rp_url)

    rmv = js[cnf.rm_venv]
    if rmv :
        cmd = ['pyenv' , 'virtualenv-delete' , '-f' , usrp.user_und_repo]
        subprocess.run(cmd)
        print(f'\n LOG: {usrp.user_und_repo} venv has been deleted')
    else :
        print(f'\n LOG: {usrp.user_und_repo} venv has NOT been deleted')
