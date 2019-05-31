import os
import stat
from stdlib.log import elog, ilog, slog
import stdlib.checks.base as base
import stdlib.checks.check as check
import stdlib.checks.edit as edit
import core.cache as cache


def get_shlib_files(pkg):
    # dirs = check.find_dirs_ending_in('lib', pkg.install_cache)
    dirs = map(lambda x: os.path.join(cache.get_wrap_cache(pkg), x), ['usr/lib64'])
    files = []
    for dirent in dirs:
        if os.path.isdir(dirent):
            files += [os.path.join(dirent, x) for x in os.listdir(dirent)
                      if '.so' in x]
    files = filter(lambda x: not os.path.islink(x), files)
    return files


def get_bin_files(pkg):
    dirs = check.find_dirs_ending_in('bin', cache.get_wrap_cache(pkg))
    files = []
    for dirent in dirs:
        if os.path.isdir(dirent):
            files += [os.path.join(dirent, x) for x in os.listdir(dirent)]
    files = filter(lambda x: not os.path.islink(x), files)
    return files


class FilesExecCheck(base.Check):
    def __init__(self, pkg, files):
        super().__init__(files)
        self.pkg = pkg

    def validate(self, item):
        ilog(f"Checking {self._remove_prefix(item)}")
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
        return item[len(cache.get_wrap_cache(self.pkg)) + 1:]


class ExecCheck():
    def __init__(self, pkg):
        self.pkg = pkg

    def run(self):
        slog(f"Checking files execute permission")
        FilesExecCheck(self.pkg, get_bin_files(self.pkg)).run()
        FilesExecCheck(self.pkg, get_shlib_files(self.pkg)).run()
