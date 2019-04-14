import os
import stat
from nbuild.log import elog, ilog
import nbuild.checks.base as base
import nbuild.checks.check as check


def get_shlib_files(pkg):
    dirs = check.find_dirs_ending_in('lib', pkg.install_dir)
    files = []
    for dirent in dirs:
        files += [os.path.join(dirent, x) for x in os.listdir(dirent)
                  if '.so' in x]
    return files


def get_bin_files(pkg):
    dirs = check.find_dirs_ending_in('bin', pkg.install_dir)
    files = []
    for dirent in dirs:
        files += [os.path.join(dirent, x) for x in os.listdir(dirent)]
    return files


class FilesExecCheck(base.Check):
    def __init__(self, pkg, files, local_state=base.Check.global_state):
        super().__init__(files, local_state=local_state)
        self.pkg = pkg

    def validate(self, item):
        return os.access(item, os.X_OK)

    def show(self, item):
        path_wo_prefix = self._remove_prefix(item)
        elog(f"'{path_wo_prefix}' is not executable, but should be")

    def fix(self, item):
        perms = os.stat(item).st_mode
        path_wo_prefix = self._remove_prefix(item)
        ilog(f"'{path_wo_prefix}' has been given execute permissions")
        os.chmod(item, perms | stat.S_IXOTH | stat.S_IXGRP | stat.S_IXUSR)

    def _remove_prefix(self, item):
        return item[len(self.pkg.install_dir):]


class ExecCheck():
    def __init__(self, pkg, local_state=base.Check.global_state):
        self.pkg = pkg
        self.state = local_state

    def run(self):
        ilog(f"Checking files execute permission")
        FilesExecCheck(self.pkg, get_bin_files(self.pkg), local_state=self.state).run()
        FilesExecCheck(self.pkg, get_shlib_files(self.pkg), local_state=self.state).run()
