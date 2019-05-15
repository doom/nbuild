import os
from stdlib.log import ilog, wlog, qlog
from core.args import get_args


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
    args = get_args()
    if args.visual:
        ret = os.system(f'xdg-open {path}')
        if ret == 0:
            return
        else:
            wlog("A problem occured while using xdg-open, falling back on opening a shell")
    shell = os.environ.get('SHELL')
    if shell is None:
        wlog("No $SHELL environment variable found")
        shell = qlog("Please provide a valid shell: ")
    ilog(f"Opening {shell} in {path}, press CTRL-D to exit and resume checks")
    os.system(f'cd {path} && {shell}')


def open_editor(filepath):
    args = get_args()
    if args.visual:
        editor = os.environ.get('VISUAL')
        if editor is None:
            wlog("No $VISUAL environment variable found, trying $EDITOR")
            editor = os.environ.get('EDITOR')
            if editor is None:
                wlog("No $EDITOR environment variable found")
                editor = qlog("Please provide a valid editor: ")
    else:
        editor = os.environ.get('EDITOR')
        if editor is None:
            wlog("No $EDITOR environment variable found")
            editor = qlog("Please provide a valid editor: ")
    ilog(f"Opening {filepath} with {editor}")
    os.system(f'{editor} {filepath}')
