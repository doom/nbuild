#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-

import stdlib
from core.log import ilog
from core.args import get_args


def all_in_one_binary() -> stdlib.Aggregate:
    build = stdlib.current_build()

    ilog("Splitting using the \"All in one (binary)\" method", indent=False)

    # Create the binary package
    bin = stdlib.Package(
        stdlib.PackageId(
            build.manifest.name,
        ),
        build.manifest.description,
    )

    bin.move('usr/local/bin/*', 'usr/bin/')

    bin.drain(
        '{,usr/}{,s}bin/',
        'usr/libexec/',
        'usr/share/{locale,man,bash-completion/completions,icons,applications}/',
        f'usr/share/{build.manifest.name}/',
        'etc/',
    )

    # Create doc package
    doc = stdlib.Package(
        stdlib.PackageId(
            f'{build.manifest.name}-doc',
        ),
        f'Documentation for {build.manifest.name}.',
    )

    doc.drain(
        'usr/share/doc/',
        'usr/share/info/',
    )

    return stdlib.Aggregate(bin, doc)
