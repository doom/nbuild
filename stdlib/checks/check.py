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


def check_package(pkg):
    # name = pkg.manifest.metadata.name

    # suffix = pkg.name.split('-')[-1] if '-' in pkg.name else None

    # check_syntax(pkg)
    # if suffix is None or suffix == 'bin':
    #     check_deps(pkg)
    #     check_exec(pkg)
    # suffix_checks(pkg)
    # ilog("All checks done")
    # ExeCheck.ExecCheck(pkg).run()
    # stx_chk.IdCheck(pkg).run()
    # stx_chk.DescriptionCheck(pkg).run()
    ExeCheck.ExecCheck(pkg).run()

    # base.Check.commit(pkg)
