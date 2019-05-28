import os
from elftools.elf.elffile import ELFFile
from elftools.common.exceptions import ELFError
from stdlib.log import ilog, elog, slog
import stdlib.package
import stdlib.checks.check as check
import stdlib.checks.base as base
import requests


def get_deps(filename):
    with open(filename, 'rb') as f:
        ret = elf_get_deps(f)
        if ret is None:
            return None
            # f.seek(0, 0)
            # ret = get_interpreter(f)
        return ret


def elf_get_deps(filehandle):
    try:
        elf = ELFFile(filehandle)
        section = next(x for x in elf.iter_sections()
                       if x.name.startswith('.dynamic'))
    except (StopIteration, ELFError):
        return None
    needed_tags = [tag.needed for tag in section.iter_tags()
                   if tag.entry['d_tag'] == 'DT_NEEDED']
    return needed_tags


def get_interpreter(filehandle):
    shebang = filehandle.readline()
    # if shebang.startswith('#!'):
    return shebang


def check_file(file, pkg):
    file_wo_prefix = file[len(pkg.install_dir):]
    found_deps = filter(lambda x: pkg.name not in x, get_deps(file))
    for dep in found_deps:
        found = False
        for key in pkg.run_dependencies.keys():
            _, _, name = stdlib.package.Package.split_id(key)
            if name in dep:
                found = True
                break
        if not found:
            elog(f"Possible missing dependency to '{dep}' in '{file_wo_prefix}'")
    return True


def check_files(files, pkg):
    return all(map(lambda x: check_file(x, pkg), files))


def check_bins(pkg):
    dirs = check.find_dirs_ending_in('bin', pkg.install_dir)
    for dirpath in dirs:
        path_wo_prefix = dirpath[len(pkg.install_dir):]
        ilog(f"Checking dependencies for files in '{path_wo_prefix}'")
        binpaths = map(lambda x: os.path.join(dirpath, x), os.listdir(dirpath))
        if not check_files(binpaths, pkg):
            return False
    return True


def check_libs(pkg):
    dirs = check.find_dirs_ending_in('lib', pkg.install_dir)
    for dirpath in dirs:
        path_wo_prefix = dirpath[len(pkg.install_dir):]
        ilog(f"Checking dependencies for shared libraries in '{path_wo_prefix}'")
        libpaths = map(lambda x: os.path.join(dirpath, x),
                       (f for f in os.listdir(dirpath) if '.so' in f))
        if not check_files(libpaths, pkg):
            return False
    return True


def check_deps(pkg):
    ilog("Checking dependencies")
    ret = all([
        check_bins(pkg),
        check_libs(pkg),
    ])
    if ret:
        slog("\tDependency checks OK")
    else:
        elog("\tSome dependency checks failed")
    return ret


###############################################################################
###############################################################################


class DepsExistCheck(base.Check):
    def __init__(self, build):
        super().__init__([
            'beta::sys-lib/libncurses6#6.1.0',
            'beta::sys-lib/zlib1#1.2.11',
            'prout::sys-lib/zlib1#1.2.11',
            'beta::prout/zlib1#1.2.11',
            'beta::sys-lib/zlib1#1.2.11',
            'beta::sys-lib/bonjour#1.0.0',
            'beta::sys-lib/libncurses6#6.1.0',
        ])
        self.build = build
        self.error = {}

    def validate(self, item):
        self.error['repository'] = None
        repository, category, name, version = self.split(item)
        url = f'https://{repository}.raven-os.org/api/p/{category}/{name}/{version}'
        if repository not in ['stable', 'beta', 'unstable']:
            self.error['repository'] = repository
            return False
        response = requests.get(url)
        return response.ok

    def show(self, item):
        if self.error['repository'] is not None:
            elog(f"The repository '{self.error['repository']}' doesn't exist")
        elog(f"The package '{item}' was not found")

    def fix(self, item):
        print('fix')

    def edit(self, item):
        print('edit')

    def diff(self, item):
        print('diff')

    @staticmethod
    def split(name):
        repo_end = name.find('::')
        repository = name[:repo_end]
        name = name[repo_end + 2:]

        category_end = name.find('/')
        category = name[:category_end]
        name = name[category_end + 1:]

        pkg_name_end = name.find('#')
        pkg_name = name[:pkg_name_end]
        name = name[pkg_name_end + 1:]

        version = name
        return repository, category, pkg_name, version

#     def get_elf_deps(elf_path):
#         with open(elf_path, 'rb') as file:
#             try:
#                 elf = ELFFile(file)
#                 dyn = elf.get_section_by_name(".dynamic")
#                 if dyn is not None:
#                     for tag in dyn.iter_tags():
#                         if tag.entry.d_tag == 'DT_NEEDED':
#                             yield tag.needed
#             except ELFError:
#                 yield None
