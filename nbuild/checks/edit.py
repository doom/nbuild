import os
from nbuild.log import ilog, wlog, qlog

def ask(question, default=True):
    while True:
        answer = qlog(question + '[Y/n/e] ').lower()
        if answer == '':
            return default
        elif answer in ['y', 'yes', 'ye']:
            return True
        elif answer in ['n', 'no']:
            return False
        elif answer in ['e', 'edit']:
            return 'edit'
        else:
            wlog("Unrecognized answer")
            continue

def open_shell(path):
    shell = os.environ.get('SHELL')
    if shell is None:
        wlog("No $SHELL environment variable found")
        shell = qlog("Please provide a valid shell: ")
    ilog(f"Opening {shell} in {path}, press CTRL-D to exit and resume checks")
    os.system(f'cd {path} && {shell}')


def open_editor(filepath):
    editor = os.environ.get('VISUAL') or os.environ.get('EDITOR')
    if editor is None:
        wlog("No $VISUAL nor $EDITOR environment variable found")
    rcode = 1
    while rcode != 0:
        editor = qlog("Please provide a valid editor: ")
        ilog(f"Opening {filepath} with {editor}")
        rcode = os.system(f'{editor} {filepath}')
