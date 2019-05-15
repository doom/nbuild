import os
import stdlib.checks.executable as ExeCheck
from stdlib.checks.dependencies import check_deps
from stdlib.log import ilog
from stdlib.checks.suffix_check import suffix_checks
import stdlib.checks.base as base
import stdlib.checks.syntax_check as stx_chk

_is_check = False


def set_check():
    global _is_check
    _is_check = True


def is_check():
    global _is_check
    return _is_check


def find_dirs_ending_in(end, path):
    dirs = []
    for (dirname, dirnames, filenames) in os.walk(path):
        dirs += [os.path.join(dirname, subdirname) for subdirname in dirnames
                 if subdirname.endswith(end)]
    return dirs


def check_package(build):
    # name = build.manifest.metadata.name

    # suffix = build.name.split('-')[-1] if '-' in build.name else None

    # check_syntax(build)
    # if suffix is None or suffix == 'bin':
    #     check_deps(build)
    #     check_exec(build)
    # suffix_checks(build)
    # ilog("All checks done")
    # ExeCheck.ExecCheck(build).run()
    # stx_chk.IdCheck(build).run()
    # stx_chk.DescriptionCheck(build).run()
    ExeCheck.ExecCheck(build).run()

    # base.Check.commit(build)
