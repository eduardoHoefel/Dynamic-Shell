import subprocess
from log import log

def execute(action, args = []):

    action = 'bin/' + action
    command = [action] + args
    #TODO: get stderr, stdout
    try:
        result = subprocess.check_output(command, stderr=subprocess.STDOUT)
        result = result.decode("utf-8")
        result = result.splitlines()
        returncode = 0
    except subprocess.CalledProcessError as e:
        returncode = e.returncode
        result = []

    return { "result": returncode, "return": result }
