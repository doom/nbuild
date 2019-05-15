import os
import stat
from stdlib.log import elog, ilog
import stdlib.checks.base as base
import stdlib.checks.check as check
import stdlib.checks.edit as edit


def get_shlib_files(build):
    # dirs = check.find_dirs_ending_in('lib', build.install_cache)
    dirs = map(lambda x: os.path.join(build.install_cache, x), ['usr/lib64'])
    files = []
    for dirent in dirs:
        files += [os.path.join(dirent, x) for x in os.listdir(dirent)
                  if '.so' in x]
    return files


def get_bin_files(build):
    dirs = check.find_dirs_ending_in('bin', build.install_cache)
    files = []
    for dirent in dirs:
        files += [os.path.join(dirent, x) for x in os.listdir(dirent)]
    return files


class FilesExecCheck(base.Check):
    def __init__(self, build, files):
        super().__init__(files)
        self.build = build

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

    def diff(self, item):
        ilog("X permissions would be added")

    def edit(self, item):
        edit.open_shell(os.path.dirname(item))

    def _remove_prefix(self, item):
        return item[len(self.build.install_cache):]


class ExecCheck():
    def __init__(self, build):
        self.build = build

    def run(self):
        ilog(f"Checking files execute permission")
        FilesExecCheck(self.build, get_bin_files(self.build)).run()
        FilesExecCheck(self.build, get_shlib_files(self.build)).run()
