import os
import requests
import urllib
from elftools.elf.elffile import ELFFile
from elftools.common.exceptions import ELFError
from stdlib.log import ilog, elog, slog, wlog
import stdlib.package
import stdlib.checks.check as check
import stdlib.checks.base as base
import core.config
import stdlib.deplinker.elf


class DepsMissingCheck(base.CheckOnManifest):
    def __init__(self, pkg):
        elfs = stdlib.deplinker.elf._find_elfs(
                pkg,
                [
                    '{,usr/}bin/*',
                    '{,usr/}lib{,32,64}/*',
                ],
        )
        super().__init__(pkg, filter(lambda x: not os.path.islink(os.path.join(pkg.wrap_cache, x)), elfs))
        self.missing_deps = []
        slog("Looking for missing dependencies")

    def validate(self, item):
        ilog(f"Checking {item}")

        self.missing_deps = []
        deps = stdlib.deplinker.elf._fetch_elf_dependencies(self.pkg, item)
        for d in deps:
            res = self._solve_remotely(d)
            if res not in self.manifest['dependencies']:
                self.missing_deps.append((d, res))
        return len(self.missing_deps) == 0

    def show(self, item):
        for dep, package in self.missing_deps:
            elog(f"Missing dependency to {dep}")

    def diff(self, item):
        can_fix = False
        for dep, package in self.missing_deps:
            if package is not None:
                ilog(f"{package}#* would be added as a dependency, as it contains {dep}")
                can_fix = True
            else:
                wlog(f"No package has been found for {dep}, please try manual search")
        return can_fix

    def fix(self, item):
        msgs = []
        for dep, package in self.missing_deps:
            if package is not None:
                self.manifest['dependencies'][package] = '*'
                msgs.append(f"{package}#* has been added as a dependency")
            else:
                wlog(f"Nothing could be done automatically for {dep}")
        self.update_manifest()
        for m in msgs:
            ilog(m)

    @staticmethod
    def _solve_remotely(dep):
        config = core.config.get_config()

        if config.get('repositories') is None:
            return None

        # Try all repositories from top to bottom
        for repository in config['repositories']:
            try:
                url = core.config.get_config()['repositories'][repository]['url']
                r = requests.get(
                    url=f'{url}/api/search?q={urllib.parse.quote(dep)}&search_by=content&exact_match=true',
                )

                if r.status_code == 200:
                    results = r.json()

                    if len(results) == 1:
                        result = results[0]
                        if result['all_versions']:
                            return result['name']
                elif r.status_code == 404:
                    stdlib.log.elog(f"\"{repository}\" doesn't contain a package with file \"{dep}\"")
                else:
                    raise RuntimeError("Repository returned an unknown status code")
            except RuntimeError:
                stdlib.log.elog(f"An unknown error occurred when fetching \"{repository}\" (is the link dead?), skipping...")

        return None


class DepsExistCheck(base.CheckOnManifest):
    def __init__(self, pkg):
        super().__init__(pkg, None)
        self.items = self.manifest['dependencies'].copy().items()
        self.error = {}
        slog("Verifying that current dependencies really exist")

    def validate(self, item):
        config = core.config.get_config()
        full_name, semver = item
        ilog(f"Checking {full_name}#{semver}")
        self.error['repository'] = None
        repository, category, name = self.split(full_name)
        repo = config['repositories'].get(repository)
        if repo is None:
            self.error['repository'] = repository
            return False
        url = f'{repo["url"]}/api/p/{category}/{name}'
        if semver != '*':
            url += f'/{semver}'
        response = requests.get(url)
        return response.ok

    def show(self, item):
        name, semver = item
        if self.error['repository'] is not None:
            elog(f"The repository '{self.error['repository']}' wasn't found")
        elog(f"The package '{name}#{semver}' was not found")

    def fix(self, item):
        name, semver = item
        del self.manifest['dependencies'][name]
        self.update_manifest()
        ilog(f"{name} has been removed from dependencies")

    def diff(self, item):
        name, semver = item
        ilog(f"The dependency to {name} would be removed from the manifest.toml")

    @staticmethod
    def split(name):
        repo_end = name.find('::')
        repository = name[:repo_end]
        name = name[repo_end + 2:]

        category_end = name.find('/')
        category = name[:category_end]
        name = name[category_end + 1:]

        return repository, category, name

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
