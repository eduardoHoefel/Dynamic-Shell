import subprocess
from src.log import log

def execute(action, args = []):

    action = 'bin/' + action
    command = ['sudo'] + [action] + args

    if 'background' in action:
        execute_background(command, args)
        return

    try:
        result = subprocess.check_output(command, stderr=subprocess.STDOUT)
        result = result.decode("utf-8")
        result = result.splitlines()
        returncode = 0
    except subprocess.CalledProcessError as e:
        returncode = e.returncode
        result = []

    return { "result": returncode, "return": result }

def execute_with_log(action, args = []):
    execute('log', [action] + args)
    result = execute(action, args)
    return result    

def execute_background(action, args):
    command = action + ['&']

    subprocess.Popen(command)
    return True
