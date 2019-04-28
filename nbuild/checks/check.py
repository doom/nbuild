import os
import nbuild.checks.executable as ExeCheck
from nbuild.checks.dependencies import check_deps
from nbuild.log import ilog
from nbuild.checks.suffix_check import suffix_checks
import nbuild.checks.base as base
import nbuild.checks.syntax_check as stx_chk


def find_dirs_ending_in(end, path):
    dirs = []
    for (dirname, dirnames, filenames) in os.walk(path):
        dirs += [os.path.join(dirname, subdirname) for subdirname in dirnames
                 if subdirname.endswith(end)]
    return dirs


def check_package(pkg):
    suffix = pkg.name.split('-')[-1] if '-' in pkg.name else None
    ilog(f"Checking package installed at {pkg.install_dir}", indent=False)

    # check_syntax(pkg)
    # if suffix is None or suffix == 'bin':
    #     check_deps(pkg)
    #     check_exec(pkg)
    # suffix_checks(pkg)
    # ilog("All checks done")
    # ExeCheck.ExecCheck(pkg).run()
    stx_chk.IdCheck(pkg).run()
    stx_chk.DescriptionCheck(pkg).run()
    base.CheckOnManifest.commit(pkg)
    ExeCheck.ExecCheck(pkg).run()
    base.Check.commit(pkg)
