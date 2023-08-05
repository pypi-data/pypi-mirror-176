import subprocess
import os

def clone(repo, local):
    p = subprocess.Popen(['git', 'clone', repo, local], stdout=subprocess.PIPE)
    return p.communicate()

def get_repo_name(remote_url):
    return os.path.splitext(os.path.basename(remote_url))[0]