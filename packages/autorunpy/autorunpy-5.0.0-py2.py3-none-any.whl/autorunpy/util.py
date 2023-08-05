"""

    """

import json
from dataclasses import dataclass
from pathlib import Path


class Conf :
    def_fn = Path.cwd().parent / 'conf.json'
    repo_url = 'repo_url'
    python_version = 'python_version'
    module_2_run = "module_2_run"
    rm_venv = 'rm_venv'

@dataclass
class UserRepo :
    user_name: str
    repo_name: str
    user_slash_repo: str
    user_und_repo: str

def get_user_repo_from_url(repo_url) :
    gu = repo_url.split('github.com/')[1]
    user_name = gu.split('/')[0]
    repo_name = gu.split('/')[1]
    user_slash_repo = f'{user_name}/{repo_name}'
    user_und_repo = f'{user_name}_{repo_name}'
    return UserRepo(user_name , repo_name , user_slash_repo , user_und_repo)

def read_json(fp) :
    with open(fp , 'r') as f :
        return json.load(f)
